# Align prediction units and direction  `T.2.3.1`   7 edits, 0 experts
4 scored cases, median improvement +0.00222, 4 improved


- expert 27389424 (Grandmaster) · amex · v7→v8   Verify that the submission contains properly calibrated probabilities by applying the appropriate inverse-link function (e.g., sigmoid for binary classification) to raw model outputs. Plot histograms of both raw and transformed predictions to confirm the distribution is in [0,1] and has a sensible s
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members. | ✗ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator. | ✗ The called method or argument belongs to a different API wrapper than the instantiated object.
    leaderboard score n/a → 0.78358
- expert 28984551 (Contributor) · amex · v12→v13   Use the classifier variant of the model and extract class probabilities (not raw predictions) as stacking features. This keeps all base-learner outputs on the same [0,1] probability scale, improving ensemble coherence and typically the final metric.
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members. | ✓ The called method or argument belongs to a different API wrapper than the instantiated object.
    leaderboard score 0.79232 → 0.79279 (+0.00047)
- expert 77129691 (Master) · equity · v1→v2   Negate the predictions and resubmit. If the score jumps to roughly (1 − old_score), the sign was inverted. Always verify whether the evaluation expects higher predictions to mean higher risk or longer survival, and align accordingly.
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members. | ✗ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.
    leaderboard score 0.29019 → 0.69005 (+0.39986)
- expert 75145694 (Expert) · equity · v20→v21   Before blending, verify that all model outputs share the same monotonic direction with respect to the target. Compute rank correlations between each model's predictions and the others; if one is negatively correlated, negate its outputs. Add an explicit sign-correction step in the blending pipeline 
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members. | ✓ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.
    leaderboard score 0.68959 → 0.68978 (+0.00020)
- expert 75145694 (Expert) · equity · v36→v38   Before blending, verify the new model's prediction direction by checking its standalone concordance or correlation with the target. If the metric is sign-sensitive (e.g., concordance index), negate or rank-transform the predictions and compare. Add debug prints of prediction statistics to catch the 
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members. | ✓ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.
    leaderboard score n/a → 0.69283
- expert 75145694 (Expert) · equity · v41→v46   Isolate each member by running it solo or adding members one at a time. When a member degrades the blend, inspect its preprocessing pipeline (missing value handling, categorical encoding, fold-averaging logic) for mismatches with what the model expects. Fix each member's pipeline before re-enabling 
    evidence: ✓ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator. | ✓ Inputs or intermediate network outputs contain non-finite values. | ✓ The called method or argument belongs to a different API wrapper than the instantiated object.
    leaderboard score 0.69056 → 0.69277 (+0.00222)
- expert 15173072 (Contributor) · ranzcr · v11→v12   Check whether the training labels were scaled (e.g., percentages vs. fractions). If so, apply the inverse scaling to predictions before submission. A dramatic score jump after rescaling confirms the mismatch. Always verify that the prediction range matches what the model was trained to output.
    evidence: ✓ Prediction units or monotonic direction disagree with the labels or other members.
    leaderboard score n/a → 0.95987