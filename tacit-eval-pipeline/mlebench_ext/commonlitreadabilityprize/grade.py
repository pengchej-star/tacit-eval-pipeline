"""Grader for commonlitreadabilityprize: root mean squared error (lower is better).

Metric source: the competition's Evaluation page ("Submissions are scored on the root mean squared
error", https://www.kaggle.com/competitions/commonlitreadabilityprize/overview/evaluation). RMSE has no
special official code, so sklearn's root_mean_squared_error is used, as in the official MLE-bench RMSE
entries (e.g. petfinder-pawpularity-score).
"""

import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error

from mlebench.grade_helpers import InvalidSubmissionError

ID, TARGET = "id", "target"


def prepare_for_metric(submission: pd.DataFrame, answers: pd.DataFrame) -> dict:
    assert ID in answers.columns and TARGET in answers.columns, "answers need id and target"
    assert answers[ID].is_unique and answers[TARGET].notna().all()

    for col in (ID, TARGET):
        if col not in submission.columns:
            raise InvalidSubmissionError(f"Submission must have a '{col}' column")
    if len(submission) != len(answers):
        raise InvalidSubmissionError(
            f"Submission has {len(submission)} rows, expected {len(answers)}"
        )
    if not submission[ID].is_unique:
        raise InvalidSubmissionError("Submission ids must be unique")
    if set(submission[ID].astype(str)) != set(answers[ID].astype(str)):
        raise InvalidSubmissionError("Submission ids must match the test ids")
    if not pd.api.types.is_numeric_dtype(submission[TARGET]):
        raise InvalidSubmissionError(f"'{TARGET}' must be numeric")
    if not np.isfinite(submission[TARGET].to_numpy(dtype=float)).all():
        raise InvalidSubmissionError(f"'{TARGET}' must not contain NaN or inf")

    submission = submission.assign(**{ID: submission[ID].astype(str)}).sort_values(ID)
    answers = answers.assign(**{ID: answers[ID].astype(str)}).sort_values(ID)
    return {
        "y_true": answers[TARGET].to_numpy(dtype=float),
        "y_pred": submission[TARGET].to_numpy(dtype=float),
    }


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    return float(root_mean_squared_error(**prepare_for_metric(submission, answers)))
