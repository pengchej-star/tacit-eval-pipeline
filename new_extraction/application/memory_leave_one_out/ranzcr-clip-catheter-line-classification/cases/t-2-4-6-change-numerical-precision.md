# Change numerical precision  `T.2.4.6`   3 edits, 0 experts
3 scored cases, median improvement -0.00001, 1 improved


- expert 17371717 (Master) · commonlitreadabilityprize · v8→v9   Cast the model to half precision before running inference and compare the metric against full precision. For typical transformer regression tasks the score change is negligible, so half precision can be safely adopted to save memory and time.
    evidence: ✓ Memory grows as successive models or framework stages are loaded. | ✓ Stored arrays or activations dominate memory and a precision reference is available. | ✗ The previous version failed to produce a submission (no LB score), so a re-run with no or minimal code changes is the cheapest way to obtain feedback.
    leaderboard score 0.47270 → 0.47268 (-0.00001)
- expert 50376011 (Grandmaster) · hms · v210→v211   Test inference with mixed precision disabled (full FP32). If the score worsens or stays the same, keep mixed precision for its speed benefit. In this case the score got worse, indicating that the precision difference was not the bottleneck and the run-to-run variance or other factors dominated.
    evidence: ✓ Stored arrays or activations dominate memory and a precision reference is available. | ✗ The previous version failed to produce a submission (no LB score), so a re-run with no or minimal code changes is the cheapest way to obtain feedback.
    leaderboard score 0.25194 → 0.25970 (+0.00776)
- expert 55621328 (Master) · learning · v105→v106   Test mixed-precision inference in isolation (without changing other variables like blend weights). If the metric drops even slightly, revert to full precision for the final submission, because regression outputs near rounding boundaries are sensitive to small numerical perturbations from lower preci
    evidence: ✓ Stored arrays or activations dominate memory and a precision reference is available.
    leaderboard score 0.82994 → 0.82916 (-0.00078)