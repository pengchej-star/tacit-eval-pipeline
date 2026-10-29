"""Grader for equity-post-hct-survival-predictions: race-stratified concordance index (higher is better).

Metric source: Kaggle's official metric notebook for this competition, "eefs-concordance-index"
(https://www.kaggle.com/code/metric/eefs-concordance-index, pulled with
`kaggle kernels pull metric/eefs-concordance-index` on 2026-10-29). `score()` below is copied verbatim
from it; only ParticipantVisibleError is made a subclass of MLE-bench's InvalidSubmissionError.

    score = mean(C_g) - std(C_g)   over race_group g (population std, ddof=0)
    C_g   = lifelines.utils.concordance_index(efs_time, -prediction, efs) within group g

So `prediction` is a RISK score: higher prediction = event expected sooner. A constant prediction
gives C_g = 0.5 in every group, hence a score of 0.5.

Kaggle's scorer aligns submission and solution rows by ID before calling score(); grade() does the same.
Requires lifelines (`pip install lifelines`).
"""

import numpy as np
import pandas as pd
import pandas.api.types
from lifelines.utils import concordance_index

from mlebench.grade_helpers import InvalidSubmissionError

ID, PRED = "ID", "prediction"


class ParticipantVisibleError(InvalidSubmissionError):
    pass


# ---- verbatim from https://www.kaggle.com/code/metric/eefs-concordance-index ----
def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:
    """
    >>> import pandas as pd
    >>> row_id_column_name = "id"
    >>> y_pred = {'prediction': {0: 1.0, 1: 0.0, 2: 1.0}}
    >>> y_pred = pd.DataFrame(y_pred)
    >>> y_pred.insert(0, row_id_column_name, range(len(y_pred)))
    >>> y_true = { 'efs': {0: 1.0, 1: 0.0, 2: 0.0}, 'efs_time': {0: 25.1234,1: 250.1234,2: 2500.1234}, 'race_group': {0: 'race_group_1', 1: 'race_group_1', 2: 'race_group_1'}}
    >>> y_true = pd.DataFrame(y_true)
    >>> y_true.insert(0, row_id_column_name, range(len(y_true)))
    >>> score(y_true.copy(), y_pred.copy(), row_id_column_name)
    0.75
    """

    del solution[row_id_column_name]
    del submission[row_id_column_name]

    event_label = 'efs'
    interval_label = 'efs_time'
    prediction_label = 'prediction'
    for col in submission.columns:
        if not pandas.api.types.is_numeric_dtype(submission[col]):
            raise ParticipantVisibleError(f'Submission column {col} must be a number')
    # Merging solution and submission dfs on ID
    merged_df = pd.concat([solution, submission], axis=1)
    merged_df.reset_index(inplace=True)
    merged_df_race_dict = dict(merged_df.groupby(['race_group']).groups)
    metric_list = []
    for race in merged_df_race_dict.keys():
        # Retrieving values from y_test based on index
        indices = sorted(merged_df_race_dict[race])
        merged_df_race = merged_df.iloc[indices]
        # Calculate the concordance index
        c_index_race = concordance_index(
                        merged_df_race[interval_label],
                        -merged_df_race[prediction_label],
                        merged_df_race[event_label])
        metric_list.append(c_index_race)
    return float(np.mean(metric_list)-np.sqrt(np.var(metric_list)))
# ---- end verbatim ----


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    for col in (ID, "efs", "efs_time", "race_group"):
        assert col in answers.columns, f"answers need column {col}"
    assert answers[ID].is_unique

    for col in (ID, PRED):
        if col not in submission.columns:
            raise InvalidSubmissionError(f"Submission must have a '{col}' column")
    if len(submission) != len(answers):
        raise InvalidSubmissionError(f"Submission has {len(submission)} rows, expected {len(answers)}")
    if not submission[ID].is_unique:
        raise InvalidSubmissionError("Submission IDs must be unique")
    if set(submission[ID].astype(str)) != set(answers[ID].astype(str)):
        raise InvalidSubmissionError("Submission IDs must match the test IDs")
    if not pd.api.types.is_numeric_dtype(submission[PRED]):
        raise InvalidSubmissionError(f"'{PRED}' must be numeric")
    if not np.isfinite(submission[PRED].to_numpy(dtype=float)).all():
        raise InvalidSubmissionError(f"'{PRED}' must not contain NaN or inf")

    # Align rows by ID (both sorted the same way, fresh 0..n-1 index), then call the official score().
    key = lambda df: df.assign(_key=df[ID].astype(str)).sort_values("_key").reset_index(drop=True)
    solution = key(answers)[[ID, "efs", "efs_time", "race_group"]]
    sub = key(submission)
    sub = pd.DataFrame({ID: np.arange(len(sub)), PRED: sub[PRED].astype(float)})
    return score(solution.copy(), sub, ID)
