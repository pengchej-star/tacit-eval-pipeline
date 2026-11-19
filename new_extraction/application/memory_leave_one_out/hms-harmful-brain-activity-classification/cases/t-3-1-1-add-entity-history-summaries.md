# Add entity-history summaries  `T.3.1.1`   8 edits, 0 experts
2 scored cases, median improvement +0.03065, 2 improved


- expert 27836972 (Expert) · amex · v2→v5   Start with the simplest possible aggregation (e.g., just the mean for numeric columns and count for categorical columns) to get an end-to-end working pipeline and a baseline score. Once that succeeds, incrementally add richer statistics (std, min, max, last value, nunique) one or two at a time, veri
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used.
    leaderboard score n/a → 0.76283
- expert 27836972 (Expert) · amex · v5→v6   Add at minimum the last value, min, max, median, and count of unique values as groupby aggregation functions for numeric and categorical columns. This set captures recency, range, central tendency, and diversity. Expect a large score jump (several percentage points) over a mean-only baseline; furthe
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Order and recency contain variation that full-history summaries conceal.
    leaderboard score 0.76283 → 0.79348 (+0.03065)
- expert 27799930 (Contributor) · amex · v1→v11   Aggregate numeric columns with last/mean/std and categorical columns with last/count/nunique per entity. Drop columns with very high missingness, fill remaining NaNs, implement the competition metric as a custom evaluation function, and run stratified k-fold CV. Collect out-of-fold predicted probabi
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v14→v20   Test adding one aggregation at a time (e.g., sum, variance) and submit or validate each independently. Redundant aggregations (sum ≈ mean × count, var ≈ std²) rarely help tree models and can dilute signal by increasing dimensionality. If the score does not improve, revert immediately rather than sta
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used.
    leaderboard score 0.79425 → n/a
- expert 28093671 (Contributor) · amex · v7→v9   Sample a manageable fraction of entities, use a fast columnar file format, and iterate in two phases: first add EDA plots and ad-hoc imputation/aggregation to understand distributions and missingness; then strip out the verbose exploration cells, suppress warnings, and replace ad-hoc steps with form
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need. | ✓ Related columns or metadata imply a signal not expressed in the present features.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v34→v37   Replace a manually curated feature list with automatic aggregations over all numeric columns (mean, std, min, max, last) and all categorical columns (count, last, nunique). This broadens the feature space substantially. Simultaneously simplify the pipeline by removing preprocessing steps (scaling, i
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → 0.79304
- expert 27656049 (Expert) · amex · v1→v7   Build the pipeline in small incremental steps: first get data loading and cleaning working (drop high-missing columns, encode categoricals), then add the aggregation logic (e.g., keep last row per entity), then add model training with early stopping, then enable hardware acceleration and tune tree c
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v10→v12   Group by entity and compute simple aggregates (mean, standard deviation) of the top-ranked numeric features, then join these back to the last-record row. Use a feature-importance or SHAP ranking to restrict aggregation to the most predictive columns (e.g., top 200) to control dimensionality and nois
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used.
    leaderboard score 0.78731 → 0.79152 (+0.00420)