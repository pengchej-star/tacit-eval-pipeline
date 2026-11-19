# Match input normalization to the learner  `T.4.1.3`   5 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00904, 3 improved


- expert 73937748 · equity · v12→v13   Try disabling standard scaling of numeric features when the pipeline uses only tree-based models. If the score stays the same or improves, remove scaling permanently to simplify the pipeline.
    evidence: ✓ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score 0.68793 → 0.68805 (higher is better; improved by 0.00012)
- expert 49524919 · hms · v26→v27   Apply channel-wise instance normalization (zero-mean, unit-variance per channel per sample) instead of global transforms. This aligns each channel's distribution independently, which better suits multi-channel spectrograms where channels have heterogeneous scales.
    evidence: ✓ Input scales differ markedly across features or from the pretrained backbone’s expected distribution. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score 0.47345 → 0.45265 (lower is better; improved by 0.02080)
- expert 49576186 · hms · v24→v26   Apply the exact per-channel mean and standard deviation normalization that the pretrained backbone was trained with. This typically recovers a significant portion of the performance gap, but may not fully close it if the underlying representation change (e.g., colormap vs. original channels) is subo
    evidence: ✓ Input scales differ markedly across features or from the pretrained backbone’s expected distribution. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score 0.37436 → 0.36532 (lower is better; improved by 0.00904)
- expert 52200959 · hms · v33→v34   Fill missing values, clip extreme values, apply a log-transform to compress dynamic range, then z-score normalize. Resize to a resolution the pretrained backbone expects. This chain brings the distribution closer to what ImageNet-pretrained weights assume and avoids numerical issues from raw spectro
    evidence: ✓ A selected learner receives NaN or infinite values it cannot handle natively. | ✓ Input scales differ markedly across features or from the pretrained backbone’s expected distribution. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score n/a → 0.41865 (lower is better)
- expert 15082684 · ranzcr · v17→v18   Compute the channel-wise mean and standard deviation on the training set and use those values for normalization at both training and inference. For single-channel images replicated to three channels, use the same statistic for all channels. Verify the statistics match between training and inference 
    evidence: ✓ Input scales differ markedly across features or from the pretrained backbone’s expected distribution. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score n/a → 0.96509 (higher is better)