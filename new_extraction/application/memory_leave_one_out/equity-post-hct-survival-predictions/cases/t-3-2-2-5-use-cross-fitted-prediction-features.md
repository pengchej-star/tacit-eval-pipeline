# Use cross-fitted prediction features  `T.3.2.2.5`   12 edits, 0 experts
7 scored cases (improvement signed by each competition's direction), median -0.00469, 2 improved


- expert 17616127 · commonlitreadabilityprize · v44→v45   Add auxiliary outputs (e.g., binned logits, classification probabilities) as extra stacking features and retrain the meta-learner on OOF data. If the gain is negligible or the score remains below the simpler blend, the extra features are not helping and may be adding noise; revert to the simpler com
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.46571 → 0.46489 (lower is better; improved by 0.00083)
- expert 17616127 · commonlitreadabilityprize · v125→v130   Implement a retrieval feature generator that encodes texts with a pretrained bi-encoder, finds top-k nearest training examples, and uses their labels as features for the meta-learner. Compare the new ensemble score against the baseline. If the retrieval-augmented version scores worse, keep the origi
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.44825 → 0.45693 (lower is better; worse by 0.00868)
- expert 52551258 · hms · v7→v9   Test the complex variant on the leaderboard. If it scores worse, revert promptly. Do not assume added complexity helps; treat it as a probe and keep the simpler model as the default unless the complex one clearly wins.
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.32513 → 0.36957 (lower is better; worse by 0.04445)
- expert 55431616 · learning · v24→v28   Build a stacking pipeline: run inference from multiple fold-specific transformer checkpoints, average their softmax/regression outputs, and feed those as additional features into the tree model. Use per-fold checkpoints with their own tokenizers to avoid data leakage and ensure consistency. If live 
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available. | ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score n/a → n/a (higher is better)
- expert 59253662 · learning · v26→v29   Merge the new model's OOF predictions into the training feature matrix and its test predictions into the test feature matrix. Submit and compare against the previous best. If the score regresses, the new stacking member may be redundant or noisy relative to existing features, and should be removed o
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.81897 → 0.81830 (higher is better; worse by 0.00067)
- expert 58130512 · learning · v29→v30   Use the pretrained model's out-of-fold scalar predictions (or low-dimensional task outputs) rather than its full hidden vectors as stacking features. These are lower-dimensional, already task-aligned, and less prone to overfitting in the downstream model.
    evidence: ✓ The current features lack contextual semantics and suitable pretrained encoders are available. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.82105 → n/a (higher is better)
- expert 60197293 · learning · v37→v44   Merge the transformer's OOF predictions as additional columns into the tree model's feature matrix for both train and test. After submitting, compare against the baseline without those features. If the score does not improve, suspect that the transformer predictions are noisy or redundant with exist
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score n/a → 0.81754 (higher is better)
- expert 55987255 · learning · v38→v39   Before committing, treat this as a probe: submit the blended prediction and compare against the baseline. Autoregressive models prompted to output scores often produce noisy, poorly calibrated ordinal predictions that degrade ensemble quality. If the score drops substantially, pivot to extracting th
    evidence: ✗ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✗ The target depends on document structure or language quality not explicitly represented. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.81711 → 0.71784 (higher is better; worse by 0.09927)
- expert 55987255 · learning · v80→v88   Before committing many iterations, validate the new feature source on local CV first. Dense embeddings from a pretrained encoder plus a linear stacking regressor can introduce noise or distribution mismatch if the external data's label semantics differ from the target. If the stacked features hurt t
    evidence: ✓ The current features lack contextual semantics and suitable pretrained encoders are available. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.82029 → 0.81560 (higher is better; worse by 0.00469)
- expert 55987255 · learning · v148→v152   Encode texts with pretrained embedding models, train a lightweight regressor (e.g., ridge regression) on the auxiliary dataset's labels, and append those predictions as new features for the main model. Submit to verify the gain, and keep the block only if the leaderboard confirms improvement.
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score 0.80885 → 0.80950 (higher is better; improved by 0.00065)
- expert 55987255 · learning · v156→v160   Use cross-validated out-of-fold predictions for the training set to avoid target leakage in stacking. If runtime or implementation complexity is prohibitive, verify with a held-out validation set that full-train predictions do not inflate the primary model's apparent performance. Always measure the 
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score n/a → n/a (higher is better)
- expert 55987255 · learning · v163→v164   Compute out-of-fold predictions from the base model inside the same notebook using the same cross-validation splits, collect them into a dataframe, and join them as features for the meta-learner. This ensures predictions are always fresh and aligned with the current data/splits.
    evidence: ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
    leaderboard score 0.80174 → n/a (higher is better)