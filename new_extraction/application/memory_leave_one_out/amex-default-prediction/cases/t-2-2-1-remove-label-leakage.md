# Remove label leakage  `T.2.2.1`   2 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00009, 1 improved


- expert 73937748 · equity · v13→v15   Before fitting any auxiliary model used to create target labels, explicitly drop identifier and index columns. After writing the fix, verify it is effective by checking that the variable actually used downstream is the cleaned one, not the original dataframe. A quick sanity check: print the column l
    evidence: ✓ Repeated entities or target columns enter supposedly unsupervised feature construction. | ✗ The practitioner lacks a proper offline validation setup and is using indirect proxies (filenames, LB submissions) to rank models.
    leaderboard score 0.68805 → 0.68814 (higher is better; improved by 0.00009)
- expert 60197293 · learning · v88→v92   Before appending external columns to the feature list, explicitly drop all non-feature columns (identifiers, raw text, target labels). Print the resulting column names to verify. If a large score regression occurs after adding features, inspect whether identifier or target columns leaked into the fe
    evidence: ✓ A training feature uses held-out labels or predictions made on its own training rows. | ✓ Repeated entities or target columns enter supposedly unsupervised feature construction. | ✓ The practitioner lacks a proper offline validation setup and is using indirect proxies (filenames, LB submissions) to rank models.
    leaderboard score n/a → 0.81738 (higher is better)