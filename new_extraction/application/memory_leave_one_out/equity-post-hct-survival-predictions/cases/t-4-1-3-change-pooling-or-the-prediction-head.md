# Change pooling or the prediction head  `T.4.1.3`   18 edits, 0 experts
14 scored cases (improvement signed by each competition's direction), median -0.00079, 6 improved


- expert 13848868 · ranzcr · v6→v9   Add a channel/spatial attention block before pooling and a hidden fully-connected layer with nonlinearity and dropout between pooling and the output. Introduce one component at a time and submit to isolate each component's contribution.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.93869 → 0.94301 (higher is better; improved by 0.00432)
- expert 13848868 · ranzcr · v16→v21   Replace the per-class multi-head design with a single shared classification head. Evaluate with the same fold ensemble. An initial score drop may occur if checkpoints are mismatched; ensure weights correspond to the new architecture before concluding the comparison.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.94293 → 0.95233 (higher is better; improved by 0.00940)
- expert 13848868 · ranzcr · v22→v27   Swap in the new block at a small capacity first, then increase capacity, comparing each variant's score to the original. If no configuration matches or exceeds the original block's score after a few trials, revert to the original rather than continuing to tune the replacement.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.95140 → 0.94944 (higher is better; worse by 0.00196)
- expert 13848868 · ranzcr · v28→v30   Revert to the earlier attention block while keeping all other changes fixed, and test with both post-processing options (rank-averaging on/off). If the reverted block scores lower than the current best under both settings, discard it and return to the better block, optionally scaling its capacity up
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.94904 → 0.94719 (higher is better; worse by 0.00185)
- expert 18550705 · commonlitreadabilityprize · v1→v2   Replace the default single-layer pooling with a weighted combination of all hidden layers, then apply both mean and max pooling over the sequence dimension and concatenate them. Add a learned attention pooling head on top. Try backbone families with different pretraining objectives (causal LM, permu
    evidence: ✓ A suitable alternative pretrained family or size is available and current representation quality has plateaued. | ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.45966 → 0.45681 (lower is better; improved by 0.00285)
- expert 18757376 · commonlitreadabilityprize · v2→v3   Insert a layer normalization step between the pooled representation and the final linear layer. This stabilizes the scale of features entering the regressor and can yield a small but consistent improvement, especially on small datasets where output variance is high.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.46324 → 0.46300 (lower is better; improved by 0.00024)
- expert 18757376 · commonlitreadabilityprize · v6→v7   Swap the pooling layer (e.g., from mean pooling to attention pooling), add normalization before the regression head, and reinitialize the last few encoder layers. Evaluate on local CV before submitting; if the change does not clearly improve CV, revert rather than assuming it will help on the leader
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.46094 → n/a (lower is better)
- expert 17371717 · commonlitreadabilityprize · v2→v4   Test each head modification (attention pooling, multi-dropout uncertainty) as a separate submission. Expect that on small noisy datasets, individual head changes may not improve and can slightly hurt; their value may only materialize when ensembled with diverse variants. Do not commit to a complex h
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information. | ✗ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score 0.47570 → 0.47649 (lower is better; worse by 0.00079)
- expert 17371717 · commonlitreadabilityprize · v9→v11   Be cautious about changing the model head architecture at inference time without retraining checkpoints to match. If checkpoints were trained with a simpler head, loading them into a more complex head will likely degrade performance. Verify architecture-checkpoint compatibility before submitting, an
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.47268 → 0.47606 (lower is better; worse by 0.00338)
- expert 17371717 · commonlitreadabilityprize · v19→v20   Add a parallel classification head that predicts the target binned into discrete categories. Train with both regression and classification losses. At inference, use the regression output (or blend both). This can regularize the model and provide complementary signal, especially on small datasets.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score n/a → 0.46543 (lower is better)
- expert 17371717 · commonlitreadabilityprize · v30→v33   Sweep pooling variants (e.g., mean-only vs. concatenated mean+max over hidden layers) jointly with checkpoint versions, changing one factor at a time. Compare leaderboard or validation scores for each combination to identify the correct pairing, since using the wrong pooling for a given checkpoint w
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.47074 → 0.46357 (lower is better; improved by 0.00717)
- expert 17371717 · commonlitreadabilityprize · v33→v36   Test the model with and without the auxiliary classification head while keeping other factors fixed. If the regression-only configuration scores better, drop the auxiliary head—on small datasets the extra head can introduce noise that outweighs its regularization benefit.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.46357 → 0.47147 (lower is better; worse by 0.00790)
- expert 6803050 · google · v27→v30   Try loading the joint checkpoints and adapting the inference architecture to include the auxiliary head. Compare leaderboard scores against the single-head baseline. If the joint model underperforms, revert to the simpler single-head architecture—auxiliary heads that help training do not always help
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information. | ✓ A suitable alternative pretrained family or size is available and current representation quality has plateaued. | ✗ The same feature matrix supports a learner with a different inductive bias or boosting strategy. | ✗ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score n/a → 0.35475 (higher is better)
- expert 7240226 · google · v7→v10   Remove or disable the normalization layer and re-evaluate. If the score recovers, the layer is the cause. Avoid batch normalization in small-batch fine-tuning heads; if normalization is needed, prefer layer normalization or dropout instead.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.38697 → 0.38588 (higher is better; worse by 0.00109)
- expert 49576186 · hms · v103→v105   Test with and without truncation on the leaderboard. If the full-dimensional vector degrades the score, revert to the truncated version — the extra dimensions may introduce noise or overfitting when the classification head is small relative to the feature dimension.
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.27315 → 0.28170 (lower is better; worse by 0.00856)
- expert 49576186 · hms · v131→v133   Add the attention block and test on the leaderboard or validation set. If the score regresses, revert the change rather than trying to tune it extensively — the added complexity may not suit the data scale or the existing feature representation. Isolate architectural changes from preprocessing chang
    evidence: ✓ The backbone is strong but pooling or task heads may discard useful information. | ✓ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score 0.26637 → 0.28049 (lower is better; worse by 0.01412)
- expert 15082684 · ranzcr · v15→v16   Switch from a single shared head to a multi-head architecture with per-group spatial attention modules, so each label group gets a dedicated prediction pathway. Load backbone weights from a strong pretrained or distilled model and fine-tune the new heads. This changes the modeling capacity rather th
    evidence: ✗ A suitable alternative pretrained family or size is available and current representation quality has plateaued. | ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score n/a → 0.95870 (higher is better)
- expert 13702907 · ranzcr · v15→v16   Simultaneously reduce the dropout rate (e.g., roughly halve it) and swap in a checkpoint trained with different or longer training. Changing two correlated levers together is acceptable when each alone is cheap to test and the plateau is persistent.
    evidence: ✓ A suitable alternative pretrained family or size is available and current representation quality has plateaued. | ✓ The backbone is strong but pooling or task heads may discard useful information.
    leaderboard score 0.94937 → 0.95396 (higher is better; improved by 0.00460)