# Use simple rounding  `T.7.2.2`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00245, 1 improved


- expert 58130512 · learning · v96→v97   Try replacing optimized ordinal thresholds with simple clip-and-round as a baseline. If the simpler approach scores comparably or better on the leaderboard, the threshold optimization is overfitting and should be removed or regularized.
    evidence: ✓ Targets occupy discrete ordered levels and the metric is sensitive to class boundaries or ties. | ✗ The metric is unchanged by strictly monotone rescaling and no discretization gain has been established. | ✓ A new checkpoint or blend has shifted the prediction distribution since thresholds were fitted. | ✓ Simple/naive rounding has not yet been tested as a baseline to quantify the value added by optimized thresholds. | ✓ The threshold-fitting population has a different label distribution than the test set, biasing the fitted thresholds.
    leaderboard score 0.81933 → 0.82179 (higher is better; improved by 0.00245)