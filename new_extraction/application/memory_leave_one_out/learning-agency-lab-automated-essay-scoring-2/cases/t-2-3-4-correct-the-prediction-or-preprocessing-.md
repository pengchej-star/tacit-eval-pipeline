# Correct the prediction or preprocessing API  `T.2.3.4`   4 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00000, 0 improved


- expert 28093671 · amex · v12→v15   Check which API was used to train the model. The low-level API's model object typically has only a generic `.predict()` method that returns probabilities when the objective is a classification loss. The scikit-learn wrapper adds `.predict_proba()`. Mixing them causes attribute errors. Match the pred
    evidence: ✓ The called method or argument belongs to a different API wrapper than the instantiated object.
    leaderboard score n/a → n/a (higher is better)
- expert 17616127 · commonlitreadabilityprize · v137→v139   After changing any keyword argument in a function call, verify the exact parameter name in the function definition. Add a sanity-check print or assertion on the function's return shape/value before using it downstream. A large unexpected score drop after a 'minor' change is a strong signal of such a
    evidence: ✓ The called method or argument belongs to a different API wrapper than the instantiated object. | ✓ A stacking feature or ensemble member produces outputs with a different row count than the main prediction dataframe.
    leaderboard score 0.44975 → 0.46975 (lower is better; worse by 0.02000)
- expert 17371717 · commonlitreadabilityprize · v1→v2   Replace manual preprocessing with the library's native parameter. Submit or validate to confirm the output is equivalent or better, establishing a clean baseline before making architectural changes.
    evidence: ✗ Prediction units or monotonic direction disagree with the labels or other members. | ✗ Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator. | ✓ The called method or argument belongs to a different API wrapper than the instantiated object. | ✗ A stacking feature or ensemble member produces outputs with a different row count than the main prediction dataframe.
    leaderboard score 0.47570 → 0.47570 (lower is better; unchanged by 0.00000)
- expert 15164527 · ranzcr · v1→v2   Verify that every submodule's attribute name in the class definition exactly matches the name used in forward(), in checkpoint state-dict keys, and in any layer-replacement code. Print or diff the model's state_dict keys against the checkpoint keys to catch mismatches.
    evidence: ✓ The called method or argument belongs to a different API wrapper than the instantiated object.
    leaderboard score n/a → n/a (higher is better)