# Remove harmful custom cleaning  `T.4.4.2`   2 edits, 0 experts

- expert 7670859 (Contributor) · google · v31→v33   Test heavy text cleaning as a probe: add it in one version and compare the metric. Expect that pretrained embeddings are robust to surface noise, so aggressive cleaning (removing punctuation, rewriting contractions, correcting spelling) often removes useful signal or mismatches the pretraining distr
    evidence: ✓ Custom normalization changes text beyond the tokenizer’s training assumptions.
    leaderboard score 0.39358 → n/a
- expert 7670859 (Contributor) · google · v33→v34   Revert the custom text cleaning and rely on the pretrained model's own tokenization. However, be careful that the revert does not accidentally remove other beneficial code or change hyperparameters simultaneously—make the revert minimal and isolated so you can attribute any score change to the prepr
    evidence: ✓ Custom normalization changes text beyond the tokenizer’s training assumptions.
    leaderboard score n/a → 0.37520