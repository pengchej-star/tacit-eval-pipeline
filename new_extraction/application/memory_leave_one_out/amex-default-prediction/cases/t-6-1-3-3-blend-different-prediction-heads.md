# Blend different prediction heads  `T.6.1.3.3`   5 edits, 0 experts
3 scored cases, median improvement -0.00362, 1 improved


- expert 18426209 (Expert) · commonlitreadabilityprize · v4→v5   Instead of debugging the broken backbone swap, add a new ensemble member that uses a different pooling strategy (e.g., mean pooling vs. attention pooling) on the same or similar backbone, average its predictions across multiple folds, and blend it with the surviving models. This can surpass the prev
    evidence: ✓ The backbone is fixed but differently trained pooling or head variants are available.
    leaderboard score n/a → 0.46021
- expert 18837555 (Expert) · commonlitreadabilityprize · v6→v7   Add the new-head variant's predictions to the ensemble via simple averaging. If the score does not improve, the variant may be too correlated with existing members or slightly weaker; consider giving it lower weight or dropping it rather than equal-weight averaging.
    evidence: ✓ Current members use similar algorithms and have strongly correlated held-out residuals. | ✓ The backbone is fixed but differently trained pooling or head variants are available.
    leaderboard score n/a → 0.46076
- expert 18837555 (Expert) · commonlitreadabilityprize · v7→v12   Add one new model variant at a time to a simple average ensemble, each using a structurally different prediction head (e.g., different hidden-layer pooling or attention mechanisms) over the same backbone. Submit after each addition to confirm the new member improves the score. Continue adding member
    evidence: ✓ The backbone is fixed but differently trained pooling or head variants are available.
    leaderboard score 0.46076 → 0.45714 (-0.00362)
- expert 18851026 (Master) · commonlitreadabilityprize · v11→v15   Before adding the new variant to the final blend, compare its standalone cross-validation performance against existing members. If its individual performance is weaker or highly correlated with an existing member, adding it may hurt rather than help. Only include it if it demonstrably reduces CV err
    evidence: ✓ The backbone is fixed but differently trained pooling or head variants are available. | ✓ Current members use similar algorithms and have strongly correlated held-out residuals. | ✗ A candidate’s held-out errors are almost identical to those of an existing member.
    leaderboard score 0.45786 → 0.46134 (+0.00348)
- expert 17371717 (Master) · commonlitreadabilityprize · v4→v5   Design several head variants that differ in pooling mechanism (e.g., attention pooling vs. mean+max pooling), regularization strategy (e.g., single dropout vs. multisample dropout), and initialization. Train each variant across the same cross-validation folds, then average their predictions at infer
    evidence: ✓ Current members use similar algorithms and have strongly correlated held-out residuals. | ✓ The backbone is fixed but differently trained pooling or head variants are available.
    leaderboard score 0.47649 → 0.47148 (-0.00500)