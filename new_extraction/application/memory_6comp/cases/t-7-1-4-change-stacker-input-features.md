# Change stacker input features  `T.7.1.4`   21 edits, 0 experts
15 scored cases, median improvement +0.00015, 9 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v44→v45   Add auxiliary outputs (e.g., binned logits, classification probabilities) as extra stacking features and retrain the meta-learner on OOF data. If the gain is negligible or the score remains below the simpler blend, the extra features are not helping and may be adding noise; revert to the simpler com
    evidence: ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.46571 → 0.46489 (-0.00083)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v91→v92   When adding new base-model features to a pre-trained meta-learner, retrain the meta-learner on the expanded feature set rather than just appending features to models fitted on fewer inputs. If the meta-learner was trained without those features, feeding them at inference time creates a train/test mi
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.45039 → 0.45486 (+0.00448)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v100→v105   When changing the set of base models fed to a pre-trained meta-learner, retrain the meta-learner on the new feature set rather than reusing old weights. If retraining is not possible, keep the meta-learner inputs identical to what it was trained on and blend the meta-learner output with new model pr
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ Members are weak, redundant, or untested after the ensemble changed.
    leaderboard score 0.45001 → 0.45982 (+0.00980)
- expert 18851026 (Master) · commonlitreadabilityprize · v4→v5   Add pretrained-model embeddings (e.g., from backbone hidden states) as extra meta-features, normalize all meta-features, introduce a second regularized linear meta-learner (e.g., ridge regression) alongside the existing one, use stratified cross-validation for meta-training, and blend the two meta-l
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.46423 → 0.45816 (-0.00607)
- expert 18851026 (Master) · commonlitreadabilityprize · v9→v10   Extract embeddings from the new backbone using the same inference pipeline, normalize them consistently, and add them as additional meta-features to the existing stacking learners. Evaluate on the leaderboard or CV to confirm the gain from backbone diversity.
    evidence: ✓ An available model makes useful errors different from the current ensemble. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.45852 → 0.45773 (-0.00079)
- expert 18851026 (Master) · commonlitreadabilityprize · v15→v18   When adding a new embedding source, verify row counts match, re-derive blend weights (e.g., via cross-validation), and confirm the new component actually reduces CV error before submitting. More diversity does not guarantee improvement if the blending formula is not re-optimized.
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ An available model makes useful errors different from the current ensemble.
    leaderboard score 0.46134 → n/a
- expert 18757376 (Expert) · commonlitreadabilityprize · v3→v4   Treat this as a probe: add the handcrafted features and an additional meta-learner in one step, then check the leaderboard. If the score worsens, the extra features likely add noise or cause overfitting in the meta-learner on the small dataset, and should be reverted. Avoid bundling too many changes
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.46300 → 0.46496 (+0.00196)
- expert 18757376 (Expert) · commonlitreadabilityprize · v3→v4   Keep the meta-stage simple (linear or low-capacity models, few input features) when the dataset is small. Adding handcrafted features and flexible meta-learners increases overfitting risk at the stacking level. If a probe shows degradation, revert and instead focus on improving or diversifying the b
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.46300 → 0.46496 (+0.00196)
- expert 18757376 (Expert) · commonlitreadabilityprize · v9→v10   Iteratively remove small groups of hand-engineered features from the stacker input and check the leaderboard or validation metric. Drop features whose removal improves the score; they are adding noise rather than signal. Prioritize removing features that are weakly correlated with the target or redu
    evidence: ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.46321 → 0.46236 (-0.00085)
- expert 75924487 (Master) · equity · v1→v2   Curate the set of base-model predictions fed to the meta-learner by explicitly listing which columns to keep. Remove models that are redundant or underperforming. Re-submit to verify the gain, since stochastic meta-learner training can cause score variance between identical runs.
    evidence: ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.69156 → 0.69159 (+0.00003)
- expert 75924487 (Master) · equity · v6→v8   Run an A/B test: submit once with all base-model outputs and once with a hand-picked subset. Compare leaderboard or validation scores. If the curated subset wins, keep it; weak or redundant members add noise that the meta-learner cannot fully ignore.
    evidence: ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.69331 → 0.69347 (+0.00015)
- expert 73937748 (Master) · equity · v58→v60   Remove redundant or low-value base learners from the same model family to reduce noise in the meta-learner's input. Then create diversity within the strong alternative model family by running it with and without feature engineering, producing distinct prediction sets. Stack the pruned, more diverse 
    evidence: ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.69177 → 0.69283 (+0.00105)
- expert 75924487 (Master) · equity · v10→v12   Add new members incrementally rather than in a single large batch. After each addition, check the validation metric. A large simultaneous expansion of ensemble inputs can introduce correlated or noisy members that degrade the meta-learner, as evidenced by a score drop when many columns are added at 
    evidence: ✓ An available model makes useful errors different from the current ensemble. | ✓ Members are weak, redundant, or untested after the ensemble changed. | ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.69408 → 0.69305 (-0.00104)
- expert 55431616 (Grandmaster) · learning · v24→v28   Build a stacking pipeline: run inference from multiple fold-specific transformer checkpoints, average their softmax/regression outputs, and feed those as additional features into the tree model. Use per-fold checkpoints with their own tokenizers to avoid data leakage and ensure consistency. If live 
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ An available model makes useful errors different from the current ensemble.
    leaderboard score n/a → n/a
- expert 59253662 (Contributor) · learning · v11→v16   Extract character-level and word-level n-gram features via sparse vectorizers, convert to dense, and concatenate with existing features. Generate out-of-fold predictions from the deep model for training rows and averaged ensemble predictions for test rows, appending these as additional numeric featu
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ An available model makes useful errors different from the current ensemble.
    leaderboard score 0.78393 → 0.80920 (+0.02527)
- expert 59253662 (Contributor) · learning · v26→v29   Merge the new model's OOF predictions into the training feature matrix and its test predictions into the test feature matrix. Submit and compare against the previous best. If the score regresses, the new stacking member may be redundant or noisy relative to existing features, and should be removed o
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.81897 → 0.81830 (-0.00067)
- expert 58130512 (Master) · learning · v29→v30   Use the pretrained model's out-of-fold scalar predictions (or low-dimensional task outputs) rather than its full hidden vectors as stacking features. These are lower-dimensional, already task-aligned, and less prone to overfitting in the downstream model.
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
    leaderboard score 0.82105 → n/a
- expert 60197293 (Expert) · learning · v37→v44   Merge the transformer's OOF predictions as additional columns into the tree model's feature matrix for both train and test. After submitting, compare against the baseline without those features. If the score does not improve, suspect that the transformer predictions are noisy or redundant with exist
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ An available model makes useful errors different from the current ensemble.
    leaderboard score n/a → 0.81754
- expert 60197293 (Expert) · learning · v81→v93   Use a simple integer or bitmask flag to toggle groups of stacked features on/off. Sweep each combination with leaderboard or held-out evaluation. Start with the full set, then remove groups one at a time; keep only the subset that improves the metric. Fewer stacked features often outperform more.
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ Members are weak, redundant, or untested after the ensemble changed.
    leaderboard score n/a → 0.81872
- expert 55987255 (Master) · learning · v148→v152   Encode texts with pretrained embedding models, train a lightweight regressor (e.g., ridge regression) on the auxiliary dataset's labels, and append those predictions as new features for the main model. Submit to verify the gain, and keep the block only if the leaderboard confirms improvement.
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ Members are weak, redundant, or untested after the ensemble changed.
    leaderboard score 0.80885 → 0.80950 (+0.00065)
- expert 55987255 (Master) · learning · v139→v148   Before committing to a complex multi-model ensemble, validate each component independently on local CV. Add the transformer predictions as a feature to the existing pipeline first rather than replacing the submission logic. If the combined score regresses, check alignment of predictions, post-proces
    evidence: ✓ A meta-learner exists and candidate out-of-fold features add information absent from its current matrix. | ✓ Members are weak, redundant, or untested after the ensemble changed.
    leaderboard score n/a → 0.80885