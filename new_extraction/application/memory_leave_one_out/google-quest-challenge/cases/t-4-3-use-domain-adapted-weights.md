# Use domain-adapted weights  `T.4.3`   2 edits, 0 experts
2 scored cases, median improvement +0.00925, 2 improved


- expert 13848868 (Grandmaster) · ranzcr · v40→v41   Swap in a backbone that was pretrained on data from the same domain (e.g., medical images for a medical task). When doing so, also re-tune the input resolution (often reducing it to match the pretraining resolution) and simplify post-processing, since the better-calibrated features may not need rank
    evidence: ✓ The current model is underpowered or a different inductive bias is supported by prior errors. | ✓ Compatible weights pretrained on relevant domain data are available. | ✓ The proposed weights were trained with a different input pipeline than the current one.
    leaderboard score 0.95889 → 0.96470 (+0.00581)
- expert 55621328 (Master) · learning · v51→v52   Re-attempt the larger backbone after adjusting ensemble blend weights and checkpoint selection to accommodate the different prediction scale/distribution of the larger model. A single well-chosen large checkpoint with properly calibrated blending can outperform a multi-seed ensemble of smaller model
    evidence: ✓ Compatible checkpoints differ in training history or validation quality. | ✓ The current model is underpowered or a different inductive bias is supported by prior errors. | ✓ Compatible weights pretrained on relevant domain data are available.
    leaderboard score 0.81053 → 0.81978 (+0.00925)