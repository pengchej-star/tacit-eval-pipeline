"""Grader for amex-default-prediction: the AMEX metric M (higher is better).

    M = 0.5 * (G + D)
    G = normalized Gini coefficient, negatives (target 0) weighted 20x
    D = default rate captured at 4%: share of all positives found in the top-ranked predictions that
        make up 4% of the (weighted) population

Metric source: the Python version of the metric published by Kaggle staff and linked from the
competition's Evaluation page, "Amex Competition Metric (Python)"
(https://www.kaggle.com/code/inversion/amex-competition-metric-python, pulled with
`kaggle kernels pull inversion/amex-competition-metric-python` on 2026-10-29). amex_metric() below is
copied verbatim from it. It takes y_true with a `target` column and y_pred with a `prediction` column,
both indexed by customer_ID. A perfect ranking scores 1.0.
"""

import numpy as np
import pandas as pd

from mlebench.grade_helpers import InvalidSubmissionError

ID, TARGET, PRED = "customer_ID", "target", "prediction"


# ---- verbatim from https://www.kaggle.com/code/inversion/amex-competition-metric-python ----
def amex_metric(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:

    def top_four_percent_captured(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = (pd.concat([y_true, y_pred], axis='columns')
              .sort_values('prediction', ascending=False))
        df['weight'] = df['target'].apply(lambda x: 20 if x==0 else 1)
        four_pct_cutoff = int(0.04 * df['weight'].sum())
        df['weight_cumsum'] = df['weight'].cumsum()
        df_cutoff = df.loc[df['weight_cumsum'] <= four_pct_cutoff]
        return (df_cutoff['target'] == 1).sum() / (df['target'] == 1).sum()

    def weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        df = (pd.concat([y_true, y_pred], axis='columns')
              .sort_values('prediction', ascending=False))
        df['weight'] = df['target'].apply(lambda x: 20 if x==0 else 1)
        df['random'] = (df['weight'] / df['weight'].sum()).cumsum()
        total_pos = (df['target'] * df['weight']).sum()
        df['cum_pos_found'] = (df['target'] * df['weight']).cumsum()
        df['lorentz'] = df['cum_pos_found'] / total_pos
        df['gini'] = (df['lorentz'] - df['random']) * df['weight']
        return df['gini'].sum()

    def normalized_weighted_gini(y_true: pd.DataFrame, y_pred: pd.DataFrame) -> float:
        y_true_pred = y_true.rename(columns={'target': 'prediction'})
        return weighted_gini(y_true, y_pred) / weighted_gini(y_true, y_true_pred)

    g = normalized_weighted_gini(y_true, y_pred)
    d = top_four_percent_captured(y_true, y_pred)

    return 0.5 * (g + d)
# ---- end verbatim ----


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    assert ID in answers.columns and TARGET in answers.columns, "answers need customer_ID and target"
    assert answers[ID].is_unique

    for col in (ID, PRED):
        if col not in submission.columns:
            raise InvalidSubmissionError(f"Submission must have a '{col}' column")
    if len(submission) != len(answers):
        raise InvalidSubmissionError(f"Submission has {len(submission)} rows, expected {len(answers)}")
    if not submission[ID].is_unique:
        raise InvalidSubmissionError("Submission customer_IDs must be unique")
    if set(submission[ID].astype(str)) != set(answers[ID].astype(str)):
        raise InvalidSubmissionError("Submission customer_IDs must match the test customer_IDs")
    if not pd.api.types.is_numeric_dtype(submission[PRED]):
        raise InvalidSubmissionError(f"'{PRED}' must be numeric")
    if not np.isfinite(submission[PRED].to_numpy(dtype=float)).all():
        raise InvalidSubmissionError(f"'{PRED}' must not contain NaN or inf")

    # Same row order for both (sorted by customer_ID), indexed by customer_ID as in the metric notebook.
    y_true = answers.assign(**{ID: answers[ID].astype(str)}).set_index(ID).sort_index()[[TARGET]]
    y_pred = submission.assign(**{ID: submission[ID].astype(str)}).set_index(ID).loc[y_true.index, [PRED]]
    y_pred = y_pred.astype(float)
    return float(amex_metric(y_true, y_pred))
