# Add leakage-free auxiliary predictions  `T.3.1.7`   14 edits, 0 experts
10 scored cases (improvement signed by each competition's direction), median -0.00067, 4 improved


- expert 28984551 · amex · v6→v9   Load each saved model collection, generate out-of-fold and test predictions from every model group within the same CV split structure, average predictions within each group across folds, then blend group-level averages into a final prediction. Verify column references and accumulation logic carefull
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.78979 → 0.79520 (higher is better; improved by 0.00541)
- expert 17616127 · commonlitreadabilityprize · v44→v45   Add auxiliary outputs (e.g., binned logits, classification probabilities) as extra stacking features and retrain the meta-learner on OOF data. If the gain is negligible or the score remains below the simpler blend, the extra features are not helping and may be adding noise; revert to the simpler com
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.46571 → 0.46489 (lower is better; improved by 0.00083)
- expert 17616127 · commonlitreadabilityprize · v91→v92   When adding new base-model features to a pre-trained meta-learner, retrain the meta-learner on the expanded feature set rather than just appending features to models fitted on fewer inputs. If the meta-learner was trained without those features, feeding them at inference time creates a train/test mi
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.45039 → 0.45486 (lower is better; worse by 0.00448)
- expert 17616127 · commonlitreadabilityprize · v100→v105   When changing the set of base models fed to a pre-trained meta-learner, retrain the meta-learner on the new feature set rather than reusing old weights. If retraining is not possible, keep the meta-learner inputs identical to what it was trained on and blend the meta-learner output with new model pr
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.45001 → 0.45982 (lower is better; worse by 0.00980)
- expert 17616127 · commonlitreadabilityprize · v125→v130   Implement a retrieval feature generator that encodes texts with a pretrained bi-encoder, finds top-k nearest training examples, and uses their labels as features for the meta-learner. Compare the new ensemble score against the baseline. If the retrieval-augmented version scores worse, keep the origi
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
    leaderboard score 0.44825 → 0.45693 (lower is better; worse by 0.00868)
- expert 18851026 · commonlitreadabilityprize · v4→v5   Add pretrained-model embeddings (e.g., from backbone hidden states) as extra meta-features, normalize all meta-features, introduce a second regularized linear meta-learner (e.g., ridge regression) alongside the existing one, use stratified cross-validation for meta-training, and blend the two meta-l
    evidence: ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value. | ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.46423 → 0.45816 (lower is better; improved by 0.00607)
- expert 18757376 · commonlitreadabilityprize · v3→v4   Treat this as a probe: add the handcrafted features and an additional meta-learner in one step, then check the leaderboard. If the score worsens, the extra features likely add noise or cause overfitting in the meta-learner on the small dataset, and should be reverted. Avoid bundling too many changes
    evidence: ✓ Text structure or error patterns vary with the target beyond the current representation. | ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.46300 → 0.46496 (lower is better; worse by 0.00196)
- expert 55431616 · learning · v24→v28   Build a stacking pipeline: run inference from multiple fold-specific transformer checkpoints, average their softmax/regression outputs, and feed those as additional features into the tree model. Use per-fold checkpoints with their own tokenizers to avoid data leakage and ensure consistency. If live 
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score n/a → n/a (higher is better)
- expert 59253662 · learning · v26→v29   Merge the new model's OOF predictions into the training feature matrix and its test predictions into the test feature matrix. Submit and compare against the previous best. If the score regresses, the new stacking member may be redundant or noisy relative to existing features, and should be removed o
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.81897 → 0.81830 (higher is better; worse by 0.00067)
- expert 60197293 · learning · v37→v44   Merge the transformer's OOF predictions as additional columns into the tree model's feature matrix for both train and test. After submitting, compare against the baseline without those features. If the score does not improve, suspect that the transformer predictions are noisy or redundant with exist
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score n/a → 0.81754 (higher is better)
- expert 55987255 · learning · v80→v88   Before committing many iterations, validate the new feature source on local CV first. Dense embeddings from a pretrained encoder plus a linear stacking regressor can introduce noise or distribution mismatch if the external data's label semantics differ from the target. If the stacked features hurt t
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
    leaderboard score 0.82029 → 0.81560 (higher is better; worse by 0.00469)
- expert 55987255 · learning · v148→v152   Encode texts with pretrained embedding models, train a lightweight regressor (e.g., ridge regression) on the auxiliary dataset's labels, and append those predictions as new features for the main model. Submit to verify the gain, and keep the block only if the leaderboard confirms improvement.
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
    leaderboard score 0.80885 → 0.80950 (higher is better; improved by 0.00065)
- expert 55987255 · learning · v156→v160   Use cross-validated out-of-fold predictions for the training set to avoid target leakage in stacking. If runtime or implementation complexity is prohibitive, verify with a held-out validation set that full-train predictions do not inflate the primary model's apparent performance. Always measure the 
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Lexical frequency or local word patterns are absent or poorly covered by current features.
    leaderboard score n/a → n/a (higher is better)
- expert 55987255 · learning · v163→v164   Compute out-of-fold predictions from the base model inside the same notebook using the same cross-validation splits, collect them into a dataframe, and join them as features for the meta-learner. This ensures predictions are always fresh and aligned with the current data/splits.
    evidence: ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.80174 → n/a (higher is better)