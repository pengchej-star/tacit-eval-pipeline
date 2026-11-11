# Add history summaries  `T.4.1.2`   5 edits, 0 experts
2 scored cases, median improvement +0.03065, 2 improved


- expert 27836972 (Expert) · amex · v5→v6   Add at minimum the last value, min, max, median, and count of unique values as groupby aggregation functions for numeric and categorical columns. This set captures recency, range, central tendency, and diversity. Expect a large score jump (several percentage points) over a mean-only baseline; furthe
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✓ Multiple observations exist but only one record per entity reaches the model. | ✓ Global summaries discard recency or the order of meaningful changes.
    leaderboard score 0.76283 → 0.79348 (+0.03065)
- expert 27836972 (Expert) · amex · v30→v31   Create difference features between aggregations (e.g., last minus mean, capturing recent deviation from the average) and discretized/rounded copies of continuous features (capturing coarse-grained patterns). Remove the original fine-grained columns that the rounded versions replace to keep feature c
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✗ Multiple observations exist but only one record per entity reaches the model. | ✓ Global summaries discard recency or the order of meaningful changes. | ✓ Related variables encode a meaningful contrast not explicit in the current features.
    leaderboard score n/a → 0.79492
- expert 27825577 (Expert) · amex · v14→v20   Test adding one aggregation at a time (e.g., sum, variance) and submit or validate each independently. Redundant aggregations (sum ≈ mean × count, var ≈ std²) rarely help tree models and can dilute signal by increasing dimensionality. If the score does not improve, revert immediately rather than sta
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✗ Multiple observations exist but only one record per entity reaches the model.
    leaderboard score 0.79425 → n/a
- expert 28093671 (Contributor) · amex · v34→v37   Replace a manually curated feature list with automatic aggregations over all numeric columns (mean, std, min, max, last) and all categorical columns (count, last, nunique). This broadens the feature space substantially. Simultaneously simplify the pipeline by removing preprocessing steps (scaling, i
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✓ Multiple observations exist but only one record per entity reaches the model.
    leaderboard score n/a → 0.79304
- expert 27656049 (Expert) · amex · v10→v12   Group by entity and compute simple aggregates (mean, standard deviation) of the top-ranked numeric features, then join these back to the last-record row. Use a feature-importance or SHAP ranking to restrict aggregation to the most predictive columns (e.g., top 200) to control dimensionality and nois
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✓ Multiple observations exist but only one record per entity reaches the model.
    leaderboard score 0.78731 → 0.79152 (+0.00420)