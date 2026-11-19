# Change text preparation  `T.3.2.2.1`   15 edits, 0 experts
10 scored cases, median improvement -0.00035, 4 improved


- expert 17371717 (Master) · commonlitreadabilityprize · v21→v23   Try the paired-input approach and measure validation or leaderboard impact. If it hurts performance, revert the pairing but keep any simpler architectural improvements (e.g., a cleaner attention pooling) that emerged during the experiment. Paired encoding adds sequence length and may confuse a model
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata. | ✗ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score 0.46533 → 0.46690 (+0.00157)
- expert 7018718 (Expert) · google · v20→v25   Toggle the preprocessing feature on and off across multiple saved checkpoints and compare leaderboard scores. If the effect is inconsistent across checkpoints (sometimes positive, sometimes negative), the preprocessing is likely interacting with training-time conditions and should only be used with 
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score n/a → 0.38272
- expert 7018718 (Expert) · google · v27→v31   Perform a small grid sweep: change one factor at a time (disable preprocessing, swap checkpoint, re-enable preprocessing) and submit each variant. Track which combination of checkpoint and preprocessing flags reproduces or exceeds the best score. If no variant improves, revert to the best-known conf
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.38820 → 0.38356 (-0.00464)
- expert 7613444 (Contributor) · google · v2→v5   Separate the two semantically distinct text segments into dedicated input streams through the pretrained encoder, each with its own tokenization and segment handling, rather than concatenating everything into one sequence. Use a loss function (e.g., binary cross-entropy for bounded targets) that mat
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.38542 → 0.39802 (+0.01260)
- expert 7670859 (Contributor) · google · v31→v33   Test heavy text cleaning as a probe: add it in one version and compare the metric. Expect that pretrained embeddings are robust to surface noise, so aggressive cleaning (removing punctuation, rewriting contractions, correcting spelling) often removes useful signal or mismatches the pretraining distr
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata. | ✗ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score 0.39358 → n/a
- expert 60264017 (Master) · learning · v6→v8   Prepend or append a structured prompt to each input that encodes metadata about the example (e.g., which sub-population it belongs to or task-specific label descriptions). Implement this as a config-driven template in the tokenization step so it can be toggled and varied across experiments without c
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.82875 → n/a
- expert 55621328 (Master) · learning · v8→v9   Add special whitespace tokens (e.g., newline characters) to the tokenizer as added tokens, ensuring the inference tokenizer matches the one used during fine-tuning. Verify the tokenizer vocabulary size matches the model's embedding layer.
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.78266 → n/a
- expert 55621328 (Master) · learning · v18→v22   Isolate each candidate change (e.g., special token additions, prompt templates, text preprocessing) and toggle them independently across submissions. Submit with one change at a time to attribute the score impact to each factor. When two changes interact, test all four combinations to find the best 
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.70865 → 0.73480 (+0.02614)
- expert 55621328 (Master) · learning · v109→v111   Treat major inference pipeline changes (new tokenizer vocabulary, new special tokens, new model wrapper) as high-risk. Submit them only after verifying on a local validation set that predictions are reasonable. If the score drops sharply, revert to the known-good pipeline before trying incremental f
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata. | ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.82798 → 0.80843 (-0.01955)
- expert 55621328 (Master) · learning · v114→v115   Test metadata-conditioned checkpoints against the unconditional baseline on the leaderboard. If the score drops substantially, treat it as evidence that the metadata partitioning introduces overfitting to training-set category distributions and revert to the unconditional model.
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.82840 → 0.80119 (-0.02721)
- expert 55621328 (Master) · learning · v125→v129   Build the new inference script, submit it alone to get a baseline score, then submit the previous best script alone under the same conditions, and compare. Toggle between them and fine-tune post-processing weights on whichever scores higher. Keep both scripts available so you can quickly switch back
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.81897 → 0.82845 (+0.00948)
- expert 55621328 (Master) · learning · v137→v140   Add a binary indicator column identifying the data source, set it to the known test-source value for inference, and modify the tokenization/prompt to inject source-specific label text. Evaluate on the leaderboard; if the score does not improve, revert or try alternative approaches rather than iterat
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.82918 → 0.82694 (-0.00224)
- expert 55621328 (Master) · learning · v143→v145   To isolate the preprocessing effect, toggle it off while keeping the same checkpoints and inference setup that produced the best score. Changing the model simultaneously confounds the result and makes the ablation uninformative.
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score n/a → 0.81937
- expert 60197293 (Expert) · learning · v93→v94   Test contraction expansion and a large class-weight parameter together. If the score drops, revert: rank-correlation metrics like quadratic weighted kappa are not directly improved by class rebalancing, and aggressive positive-class weighting can distort predicted values in a regression setup. Probe
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.81872 → 0.81836 (-0.00035)
- expert 60197293 (Expert) · learning · v101→v124   Before investing many iterations on infrastructure, create a minimal prototype: apply the preprocessing to a small sample, inspect outputs, and run a single offline validation fold. If the validation metric does not improve, abandon the idea early. Do not iterate on submission-level evaluation while
    evidence: ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata. | ✓ The target depends on document structure or language quality not explicitly represented. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score 0.82142 → 0.81847 (-0.00295)