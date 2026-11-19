# Add a different input representation  `T.7.2.2`   18 edits, 0 experts
13 scored cases (improvement signed by each competition's direction), median +0.00299, 11 improved


- expert 18426209 · commonlitreadabilityprize · v4→v5   Instead of debugging the broken backbone swap, add a new ensemble member that uses a different pooling strategy (e.g., mean pooling vs. attention pooling) on the same or similar backbone, average its predictions across multiple folds, and blend it with the surviving models. This can surpass the prev
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score n/a → 0.46021 (lower is better)
- expert 18837555 · commonlitreadabilityprize · v7→v12   Add one new model variant at a time to a simple average ensemble, each using a structurally different prediction head (e.g., different hidden-layer pooling or attention mechanisms) over the same backbone. Submit after each addition to confirm the new member improves the score. Continue adding member
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.46076 → 0.45714 (lower is better; improved by 0.00362)
- expert 17371717 · commonlitreadabilityprize · v4→v5   Design several head variants that differ in pooling mechanism (e.g., attention pooling vs. mean+max pooling), regularization strategy (e.g., single dropout vs. multisample dropout), and initialization. Train each variant across the same cross-validation folds, then average their predictions at infer
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.47649 → 0.47148 (lower is better; improved by 0.00500)
- expert 75924487 · equity · v3→v4   Create a variant of an existing model by toggling a feature-engineering step (e.g., automated feature generation or domain transforms) while keeping the architecture identical. Save out-of-fold predictions from both the original and the variant as separate ensemble members. This adds diversity witho
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.69213 → n/a (higher is better)
- expert 75145694 · equity · v28→v29   Create experiment-specific feature pipelines so each member model gets tailored features. Compute multiple survival-derived labels (e.g., cumulative hazard and survival probability transforms) as alternative regression targets. Standardize numeric features per-experiment. Expect small but consistent
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.69133 → 0.69139 (higher is better; improved by 0.00006)
- expert 73937748 · equity · v20→v21   Pair the new model with a dedicated, richer feature-engineering pipeline that includes domain-driven interactions and composites not used by existing members. This increases both feature-level and model-level diversity in the ensemble, amplifying the benefit of adding the new member beyond what eith
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.68894 → 0.69032 (higher is better; improved by 0.00138)
- expert 73937748 · equity · v59→v60   Run the same model architecture on two or more distinct input representations (e.g., raw features vs. engineered features) and treat each run's out-of-fold predictions as a separate ensemble member. Feed all variants into the meta-learner so it can exploit the complementary information.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score n/a → 0.69283 (higher is better)
- expert 7573212 · google · v9→v10   Build both model variants, run inference with each using their respective fold weights, and take a simple average of their predictions. Models that differ in input structure tend to produce less correlated errors, so even a naive average can yield meaningful gains.
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score n/a → 0.39027 (higher is better)
- expert 49524919 · hms · v54→v55   Stack or average the fold-level predictions of both model families into a single submission. Expect a large gain (potentially much larger than any single-model tuning step) because the models make partially uncorrelated errors on different input views. Prioritize this multi-modal ensemble before fur
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.41624 → 0.29864 (lower is better; improved by 0.11760)
- expert 49524919 · hms · v90→v95   Build and debug the new-modality pipeline in isolation first, verify each model individually by submitting its standalone predictions, then blend the new modality into the existing ensemble at a small weight (e.g., 10–20%). Even if the new modality is much weaker alone, a small blend weight can stil
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.26809 → 0.35192 (lower is better; worse by 0.08383)
- expert 49524919 · hms · v120→v122   First test the new feature representation with a single model to gauge standalone quality. If standalone performance is substantially worse than the current best ensemble, the new representation may not add enough diversity to help. Verify by checking whether blending it in improves or hurts the com
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.24466 → 0.26600 (lower is better; worse by 0.02133)
- expert 49524919 · hms · v136→v139   Create multi-resolution feature extraction (e.g., spectrograms at several window lengths), train or load models on these features, and blend their predictions into the existing ensemble. Rebalance blend weights to accommodate the new model group.
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.24011 → 0.23959 (lower is better; improved by 0.00053)
- expert 49524919 · hms · v162→v170   First evaluate the new-resolution model in isolation by disabling other ensemble members to confirm it has reasonable standalone performance. Then try multiple backbone architectures for that resolution. Finally re-enable all members and tune blend weights. Only adopt the new member if the full blen
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.22875 → 0.22780 (lower is better; improved by 0.00095)
- expert 50496431 · hms · v17→v18   Generate a different spectrogram variant (e.g., mel-spectrogram vs. STFT spectrogram) from the raw signals, precompute and cache the results, train or load additional backbone architectures on this new representation, and blend their predictions into the existing ensemble. Diversity in both input re
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.34713 → 0.34209 (lower is better; improved by 0.00504)
- expert 50496431 · hms · v17→v18   Continue adding representations that are qualitatively different from existing ones (different spectral transforms, different channel groupings) as long as each addition produces a measurable improvement. Expect diminishing returns but do not stop prematurely—even late-stage additions of a genuinely
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.34713 → 0.34209 (lower is better; improved by 0.00504)
- expert 50496431 · hms · v30→v32   Add a new model that uses a distinct feature extraction front-end (different transform library, resolution, or representation) on the same raw data. Wire it into the ensemble averaging. If the first submission score is unexpectedly poor, re-run without code changes to rule out transient infrastructu
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.39658 → 0.35396 (lower is better; improved by 0.04262)
- expert 50496431 · hms · v182→v183   Train or obtain model weights under a different but reasonable preprocessing variant (e.g., a different filter type or parameter). At inference, parameterize the data pipeline so each model receives its matching preprocessing, then include the new model's predictions in the ensemble. Verify that the
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score 0.23243 → 0.22944 (lower is better; improved by 0.00299)
- expert 50496431 · hms · v190→v192   Create a model variant that uses an alternative signal filter for preprocessing, train it separately, and add its predictions to the ensemble. The variant alone need not outperform existing members; evaluate its contribution only within the full weighted ensemble, as diversity gains may only appear 
    evidence: ✓ An available modality, feature set, or preprocessing variant is absent from current members. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score n/a → 0.22694 (lower is better)