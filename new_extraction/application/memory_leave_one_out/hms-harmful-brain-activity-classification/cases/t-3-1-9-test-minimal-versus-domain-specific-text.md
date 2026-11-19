# Test minimal versus domain-specific text cleaning  `T.3.1.9`   9 edits, 0 experts
6 scored cases (improvement signed by each competition's direction), median -0.00295, 1 improved


- expert 7018718 · google · v20→v25   Toggle the preprocessing feature on and off across multiple saved checkpoints and compare leaderboard scores. If the effect is inconsistent across checkpoints (sometimes positive, sometimes negative), the preprocessing is likely interacting with training-time conditions and should only be used with 
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint. | ✓ A meaningful fraction of task-relevant text is truncated.
    leaderboard score n/a → 0.38272 (higher is better)
- expert 7018718 · google · v27→v31   Perform a small grid sweep: change one factor at a time (disable preprocessing, swap checkpoint, re-enable preprocessing) and submit each variant. Track which combination of checkpoint and preprocessing flags reproduces or exceeds the best score. If no variant improves, revert to the best-known conf
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.38820 → 0.38356 (higher is better; worse by 0.00464)
- expert 7018718 · google · v27→v30   Test the preprocessing toggle with each candidate checkpoint independently rather than assuming the effect is additive. If the benefit varies across checkpoints, always evaluate the full cross-product of preprocessing flags and checkpoints before concluding which combination is best.
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.38820 → 0.38503 (higher is better; worse by 0.00317)
- expert 7670859 · google · v31→v33   Test heavy text cleaning as a probe: add it in one version and compare the metric. Expect that pretrained embeddings are robust to surface noise, so aggressive cleaning (removing punctuation, rewriting contractions, correcting spelling) often removes useful signal or mismatches the pretraining distr
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.39358 → n/a (higher is better)
- expert 55621328 · learning · v8→v9   Add special whitespace tokens (e.g., newline characters) to the tokenizer as added tokens, ensuring the inference tokenizer matches the one used during fine-tuning. Verify the tokenizer vocabulary size matches the model's embedding layer.
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.78266 → n/a (higher is better)
- expert 55621328 · learning · v104→v105   Apply the same text normalization at inference time that was used during training, and use the corresponding checkpoints. This ensures the tokenizer sees the same character distributions it was fine-tuned on. Verify with a leaderboard or validation check that the alignment improves the score.
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.82726 → 0.82994 (higher is better; improved by 0.00268)
- expert 55621328 · learning · v109→v111   Treat major inference pipeline changes (new tokenizer vocabulary, new special tokens, new model wrapper) as high-risk. Submit them only after verifying on a local validation set that predictions are reasonable. If the score drops sharply, revert to the known-good pipeline before trying incremental f
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.82798 → 0.80843 (higher is better; worse by 0.01955)
- expert 60197293 · learning · v93→v94   Test contraction expansion and a large class-weight parameter together. If the score drops, revert: rank-correlation metrics like quadratic weighted kappa are not directly improved by class rebalancing, and aggressive positive-class weighting can distort predicted values in a regression setup. Probe
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint.
    leaderboard score 0.81872 → 0.81836 (higher is better; worse by 0.00035)
- expert 60197293 · learning · v101→v124   Before investing many iterations on infrastructure, create a minimal prototype: apply the preprocessing to a small sample, inspect outputs, and run a single offline validation fold. If the validation metric does not improve, abandon the idea early. Do not iterate on submission-level evaluation while
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint. | ✓ Text structure or error patterns vary with the target beyond the current representation. | ✓ Another model or related labeled source provides predictive information absent from current inputs. | ✓ Lexical frequency or local word patterns are absent or poorly covered by current features.
    leaderboard score 0.82142 → 0.81847 (higher is better; worse by 0.00295)