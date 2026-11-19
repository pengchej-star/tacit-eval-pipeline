# Repair the metric callback  `T.1.2.3`   4 edits, 0 experts

- expert 27389424 · amex · v82→v85   Enable a fast debug mode to run the pipeline quickly, inspect the metric function call for correctness (especially that both labels and predictions are passed), fix any argument errors, and serialize per-fold predictions and indices to disk so they can be independently verified offline.
    evidence: ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)
- expert 27502740 · amex · v3→v4   At the entry of any custom metric function, flatten the prediction array (e.g., ravel) so it is always 1-D, regardless of the shape the framework supplies. This prevents shape-mismatch errors in downstream sorting and arithmetic.
    evidence: ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)
- expert 27502740 · amex · v7→v8   At the top of any custom metric function, unconditionally flatten or squeeze the prediction array to 1-D (e.g., ravel). This defensive step costs nothing and prevents recurring shape-mismatch bugs whenever the metric is reused with a different model or framework.
    evidence: ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → 0.79461 (higher is better)
- expert 27825577 · amex · v21→v25   Make exactly one change per run: first fix naming/typos, then fix which helper is called, then fix the return format. Inspect the printed metric name and value after each change. Do not combine multiple fixes in one iteration, because compounding changes obscures which fix resolved which issue.
    evidence: ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)