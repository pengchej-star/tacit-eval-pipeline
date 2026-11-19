# Remove unavailable or leaking inputs  `T.2.2.5`   2 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00009, 1 improved


- expert 73937748 · equity · v13→v15   Before fitting any auxiliary model used to create target labels, explicitly drop identifier and index columns. After writing the fix, verify it is effective by checking that the variable actually used downstream is the cleaned one, not the original dataframe. A quick sanity check: print the column l
    evidence: ✓ A preprocessing or target-building step consumes identifiers or labels unavailable at prediction time. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa). | ✓ A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence.
    leaderboard score 0.68805 → 0.68814 (higher is better; improved by 0.00009)
- expert 53424936 · hms · v19→v20   Audit every preprocessing function for dependencies on label-derived quantities. Replace any such dependency with a test-compatible default (e.g., a fixed canonical offset). After fixing, verify the score recovers or improves beyond the simpler baseline.
    evidence: ✓ A preprocessing or target-building step consumes identifiers or labels unavailable at prediction time.
    leaderboard score n/a → 0.22756 (lower is better)