# Control randomness  `T.2.1.3`   4 edits, 0 experts
2 scored cases, median improvement -0.00038, 0 improved


- expert 77129691 (Master) · equity · v2→v3   Seed all RNG sources (language-level, array library, framework CPU and GPU) and enable deterministic backend flags. Be aware this can slightly hurt performance: deterministic GPU kernels may be slower or change optimization trajectories, and locking seeds removes beneficial stochastic diversity in e
    evidence: ✓ Identical configurations produce different predictions because random operations are unseeded. | ✗ The complete pipeline has no task-metric evaluation despite multiple implementation iterations.
    leaderboard score 0.69005 → 0.68967 (-0.00038)
- expert 75584724 (Master) · equity · v14→v15   Save the best-found weights as hard-coded constants behind a configuration flag. At submission time, enable the flag to skip the stochastic search and apply fixed weights directly, guaranteeing identical outputs every run.
    evidence: ✓ The claimed gain is comparable to variation already observed across unchanged runs. | ✓ Identical configurations produce different predictions because random operations are unseeded. | ✓ Recent trials along the same lever repeatedly tie or worsen the best validated result. | ✗ A representative local validation set is available but candidates are being ranked only by submissions. | ✗ The complete pipeline has no task-metric evaluation despite multiple implementation iterations.
    leaderboard score 0.69419 → n/a
- expert 75924487 (Master) · equity · v3→v4   Audit every stochastic call in the pipeline—data transforms, splits, weight initialization—and pass a fixed seed to each. Verify reproducibility by running twice and confirming identical out-of-fold predictions before drawing conclusions from variant comparisons.
    evidence: ✓ The claimed gain is comparable to variation already observed across unchanged runs. | ✓ Identical configurations produce different predictions because random operations are unseeded. | ✗ The complete pipeline has no task-metric evaluation despite multiple implementation iterations.
    leaderboard score 0.69213 → n/a
- expert 50376011 (Grandmaster) · hms · v12→v14   Test worker count changes in isolation (same model, same data) to confirm scores are stable. If scores shift, fix the worker count and random seeds. If stable, treat worker count as a performance-only knob and vary it freely.
    evidence: ✓ The score comparison changed multiple settings or artifacts simultaneously. | ✓ The claimed gain is comparable to variation already observed across unchanged runs. | ✓ Identical configurations produce different predictions because random operations are unseeded. | ✗ The complete pipeline has no task-metric evaluation despite multiple implementation iterations.
    leaderboard score 0.45471 → 0.42003 (-0.03468)