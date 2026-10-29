import shutil
from pathlib import Path

from sklearn.model_selection import train_test_split

from mlebench.utils import read_csv

ID = "ID"
LABELS = ["efs", "efs_time"]


def prepare(raw: Path, public: Path, private: Path):
    """
    Kaggle's train.csv (28800 patients) is split 90/10 into a new train and a held-out test, as in the
    official MLE-bench entries (train_test_split, test_size=0.1, random_state=0). Kaggle's own test.csv
    (3 example rows, no labels) is used only for its column list. Original IDs are kept.

    public/  train.csv (all columns), test.csv (Kaggle test columns: no efs, no efs_time),
             sample_submission.csv (ID, prediction), data_dictionary.csv (copied unchanged)
    private/ answers.csv (ID, efs, efs_time, race_group) -- race_group is needed by the metric
    """
    old_train = read_csv(raw / "train.csv")
    test_columns = read_csv(raw / "test.csv").columns.tolist()

    new_train, held_out = train_test_split(old_train, test_size=0.1, random_state=0)
    # Keep the original row order inside each part (only membership is random).
    new_train = new_train.sort_index()
    held_out = held_out.sort_index()

    new_test = held_out[test_columns].copy()
    answers = held_out[[ID, *LABELS, "race_group"]].copy()

    # Kaggle's sample_submission uses prediction = 0.5
    sample_submission = new_test[[ID]].copy()
    sample_submission["prediction"] = 0.5

    # Checks
    assert test_columns == [c for c in old_train.columns if c not in LABELS], test_columns
    assert not set(LABELS) & set(new_test.columns), "labels leaked into public test"
    assert new_train.columns.tolist() == old_train.columns.tolist()
    assert len(new_train) + len(new_test) == len(old_train)
    assert old_train[ID].is_unique
    assert set(new_train[ID]).isdisjoint(new_test[ID]), "train and test IDs overlap"
    assert answers[ID].tolist() == new_test[ID].tolist() == sample_submission[ID].tolist()
    assert answers[[*LABELS, "race_group"]].notna().all().all()
    assert set(answers["efs"].unique()) <= {0, 1}

    new_train.to_csv(public / "train.csv", index=False)
    new_test.to_csv(public / "test.csv", index=False)
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    shutil.copy(raw / "data_dictionary.csv", public / "data_dictionary.csv")
    answers.to_csv(private / "answers.csv", index=False)
