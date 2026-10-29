from pathlib import Path

from sklearn.model_selection import train_test_split

from mlebench.utils import read_csv

ID, TARGET = "id", "target"


def prepare(raw: Path, public: Path, private: Path):
    """
    Kaggle's train.csv (2834 excerpts) is split 90/10 into a new train and a held-out test, as in the
    official MLE-bench entries (train_test_split, test_size=0.1, random_state=0). Kaggle's own test.csv
    (7 example rows, no labels) is used only for its column list.

    public/  train.csv (all original columns), test.csv (Kaggle test columns: id, url_legal, license,
             excerpt -- no target, no standard_error), sample_submission.csv (id, target)
    private/ answers.csv (id, target, standard_error)
    """
    old_train = read_csv(raw / "train.csv")
    test_columns = read_csv(raw / "test.csv").columns.tolist()

    new_train, held_out = train_test_split(old_train, test_size=0.1, random_state=0)
    # Keep the original row order inside each part (only membership is random).
    new_train = new_train.sort_index()
    held_out = held_out.sort_index()

    new_test = held_out[test_columns].copy()
    answers = held_out[[ID, TARGET, "standard_error"]].copy()

    # Kaggle's sample_submission uses target = 0.0
    sample_submission = new_test[[ID]].copy()
    sample_submission[TARGET] = 0.0

    # Checks
    assert test_columns == ["id", "url_legal", "license", "excerpt"], test_columns
    assert TARGET not in new_test.columns and "standard_error" not in new_test.columns
    assert new_train.columns.tolist() == old_train.columns.tolist()
    assert len(new_train) + len(new_test) == len(old_train)
    assert set(new_train[ID]).isdisjoint(new_test[ID]), "train and test ids overlap"
    assert old_train[ID].is_unique
    assert answers[ID].tolist() == new_test[ID].tolist() == sample_submission[ID].tolist()
    assert answers[TARGET].notna().all()

    new_train.to_csv(public / "train.csv", index=False)
    new_test.to_csv(public / "test.csv", index=False)
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
