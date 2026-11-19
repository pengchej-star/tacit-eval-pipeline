# Change text cleaning or input framing  `T.4.2.5`   16 edits, 0 experts
10 scored cases, median improvement -0.00035, 4 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v9→v10   Test changing the random seed and increasing the maximum token length at inference. Expect minimal impact: seed affects only stochastic elements (e.g., dropout if left on), and longer tokens help only if inputs were being truncated. If the gap to the ensemble persists, return to ensembling rather th
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score n/a → 0.48130
- expert 17371717 (Master) · commonlitreadabilityprize · v21→v23   Try the paired-input approach and measure validation or leaderboard impact. If it hurts performance, revert the pairing but keep any simpler architectural improvements (e.g., a cleaner attention pooling) that emerged during the experiment. Paired encoding adds sequence length and may confuse a model
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content. | ✗ The current representation has lexical features but little contextual semantic information.
    leaderboard score 0.46533 → 0.46690 (+0.00157)
- expert 7018718 (Expert) · google · v20→v25   Toggle the preprocessing feature on and off across multiple saved checkpoints and compare leaderboard scores. If the effect is inconsistent across checkpoints (sometimes positive, sometimes negative), the preprocessing is likely interacting with training-time conditions and should only be used with 
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score n/a → 0.38272
- expert 7018718 (Expert) · google · v27→v31   Perform a small grid sweep: change one factor at a time (disable preprocessing, swap checkpoint, re-enable preprocessing) and submit each variant. Track which combination of checkpoint and preprocessing flags reproduces or exceeds the best score. If no variant improves, revert to the best-known conf
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content. | ✗ The current representation has lexical features but little contextual semantic information.
    leaderboard score 0.38820 → 0.38356 (-0.00464)
- expert 7018718 (Expert) · google · v27→v30   Test the preprocessing toggle with each candidate checkpoint independently rather than assuming the effect is additive. If the benefit varies across checkpoints, always evaluate the full cross-product of preprocessing flags and checkpoints before concluding which combination is best.
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content. | ✗ The current representation has lexical features but little contextual semantic information.
    leaderboard score 0.38820 → 0.38503 (-0.00317)
- expert 7613444 (Contributor) · google · v2→v5   Separate the two semantically distinct text segments into dedicated input streams through the pretrained encoder, each with its own tokenization and segment handling, rather than concatenating everything into one sequence. Use a loss function (e.g., binary cross-entropy for bounded targets) that mat
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.38542 → 0.39802 (+0.01260)
- expert 7670859 (Contributor) · google · v31→v33   Test heavy text cleaning as a probe: add it in one version and compare the metric. Expect that pretrained embeddings are robust to surface noise, so aggressive cleaning (removing punctuation, rewriting contractions, correcting spelling) often removes useful signal or mismatches the pretraining distr
    evidence: ✗ The current representation has lexical features but little contextual semantic information. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.39358 → n/a
- expert 7670859 (Contributor) · google · v33→v34   Revert the custom text cleaning and rely on the pretrained model's own tokenization. However, be careful that the revert does not accidentally remove other beneficial code or change hyperparameters simultaneously—make the revert minimal and isolated so you can attribute any score change to the prepr
    evidence: ✗ The current representation has lexical features but little contextual semantic information. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score n/a → 0.37520
- expert 7240226 (Contributor) · google · v6→v7   One-hot encode the categorical metadata, concatenate it with the text encoder's pooled output, and feed the combined vector into the prediction head. Evaluate on the leaderboard or validation to confirm the gain.
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.38126 → 0.38697 (+0.00571)
- expert 7613444 (Contributor) · google · v6→v7   Remove the sparse categorical input branch and rely on a small set of dense engineered numeric features as auxiliary inputs. Evaluate whether the simpler model matches or exceeds the previous score; if so, keep the simpler version to reduce overfitting risk.
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.39832 → n/a
- expert 60264017 (Master) · learning · v6→v8   Prepend or append a structured prompt to each input that encodes metadata about the example (e.g., which sub-population it belongs to or task-specific label descriptions). Implement this as a config-driven template in the tokenization step so it can be toggled and varied across experiments without c
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.82875 → n/a
- expert 55621328 (Master) · learning · v114→v115   Test metadata-conditioned checkpoints against the unconditional baseline on the leaderboard. If the score drops substantially, treat it as evidence that the metadata partitioning introduces overfitting to training-set category distributions and revert to the unconditional model.
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.82840 → 0.80119 (-0.02721)
- expert 55621328 (Master) · learning · v125→v129   Build the new inference script, submit it alone to get a baseline score, then submit the previous best script alone under the same conditions, and compare. Toggle between them and fine-tune post-processing weights on whichever scores higher. Keep both scripts available so you can quickly switch back
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.81897 → 0.82845 (+0.00948)
- expert 55621328 (Master) · learning · v137→v140   Add a binary indicator column identifying the data source, set it to the known test-source value for inference, and modify the tokenization/prompt to inject source-specific label text. Evaluate on the leaderboard; if the score does not improve, revert or try alternative approaches rather than iterat
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.82918 → 0.82694 (-0.00224)
- expert 60197293 (Expert) · learning · v93→v94   Test contraction expansion and a large class-weight parameter together. If the score drops, revert: rank-correlation metrics like quadratic weighted kappa are not directly improved by class rebalancing, and aggressive positive-class weighting can distort predicted values in a regression setup. Probe
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.81872 → 0.81836 (-0.00035)
- expert 60197293 (Expert) · learning · v101→v124   Before investing many iterations on infrastructure, create a minimal prototype: apply the preprocessing to a small sample, inspect outputs, and run a single offline validation fold. If the validation metric does not improve, abandon the idea early. Do not iterate on submission-level evaluation while
    evidence: ✓ Formatting, metadata, or input truncation may obscure task-relevant content. | ✓ Related labeled texts or auxiliary predictions can provide information absent from current features. | ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.82142 → 0.81847 (-0.00295)