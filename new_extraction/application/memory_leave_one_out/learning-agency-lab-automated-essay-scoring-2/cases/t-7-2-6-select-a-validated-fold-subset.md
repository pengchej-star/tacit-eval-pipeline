# Select a validated fold subset  `T.7.2.6`   10 edits, 0 experts
10 scored cases, median improvement -0.00040, 3 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v92→v98   Treat fold inclusion as a discrete search variable: toggle each fold in/out, evaluate on the held-out metric, and keep the subset that scores best. Start by removing any fold that causes errors or is suspected weak, then try adding it back to confirm the effect.
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.45486 → 0.45076 (-0.00410)
- expert 18426209 (Expert) · commonlitreadabilityprize · v8→v9   Replace automatic checkpoint discovery with an explicit list of checkpoint paths. Annotate each with its known validation score. This makes the ensemble deterministic and allows selective exclusion of weak folds. Verify the effect by submitting and comparing against the previous score.
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.45918 → 0.45856 (-0.00062)
- expert 18350823 (Expert) · commonlitreadabilityprize · v2→v4   Before increasing the number of folds in the ensemble, verify that a trained checkpoint exists for every fold index and that each fold's random seed and data split are correctly assigned. Test the expanded ensemble and revert if the score worsens, as the issue is likely infrastructure (missing or mi
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.46275 → 0.46448 (+0.00173)
- expert 7018718 (Expert) · google · v11→v13   Test removing a subset of fold models while keeping the blending method fixed. If the score drops, restore all folds. Avoid changing both the model subset and the blending method simultaneously, because the confounded result is uninterpretable.
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.38408 → 0.38367 (-0.00040)
- expert 7573212 (Contributor) · google · v5→v7   Be cautious: dropping folds from a K-fold ensemble usually hurts because it reduces the effective training data and increases variance. If no local validation metric guides fold weighting, prefer equal-weight averaging. Leaderboard probing of fold subsets is unreliable due to noise and risks overfit
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✗ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.38598 → 0.37898 (-0.00700)
- expert 7606235 (Master) · google · v15→v23   Test small ensembles (2–3 checkpoints) against the best single checkpoint on the leaderboard. If the ensemble consistently scores below the best single checkpoint, the weaker folds are adding noise that hurts ranking quality. In that case, keep the single best checkpoint rather than averaging, or tr
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.38524 → 0.38785 (+0.00261)
- expert 50376011 (Grandmaster) · hms · v55→v57   Remove the explicit fold restriction and let the inference script average over all available fold checkpoints. If the first submission shows a small regression, re-run before concluding the change is harmful, since leaderboard noise can mask small improvements.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.34467 → 0.34376 (-0.00091)
- expert 50376011 (Grandmaster) · hms · v126→v142   Sweep individual checkpoints first to rank them by solo performance, then try small ensembles of the top-performing members. Re-submit the same configuration multiple times to estimate submission variance before concluding one config beats another. Only trust improvements that exceed the observed no
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.27192 → 0.26480 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v184→v188   Test each candidate checkpoint individually and in small combinations, submitting multiple times for the same config when feasible. Prefer combinations that consistently score well across runs over single-run winners. Start with the best individual members, then add members incrementally; if adding 
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.24841 → 0.24815 (-0.00026)
- expert 50376011 (Grandmaster) · hms · v192→v199   Run a systematic single-checkpoint sweep: submit each fold checkpoint alone, record its standalone score, then rank them. Use these rankings to select the top-performing members for the final ensemble and drop weak ones. Expect that no single checkpoint will beat a well-chosen ensemble, but the swee
    evidence: ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.23903 → 0.24449 (+0.00546)