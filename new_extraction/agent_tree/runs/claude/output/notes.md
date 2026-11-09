# Notes
**Clustering.** 1674 items were assigned by a weighted keyword scorer over the `general` fields (goal weighted 3x, context+action 1x) into ~31 leaves, with small regex sub-splits for the big groups (blend weights, regression handling, integrity, post-processing, input pipeline). No embeddings or manual per-item review: sampled leaves look coherent, but a few percent of items are probably misfiled, mostly at the boundaries between ensemble membership / blend weights / debugging.

**Uncertain / poorly defined.**
- T.7 (process) is not a true "what to change" decision; its children are situations rather than alternatives. T.7.1 and T.7.2 splits are keyword-based.
- T.5.2 mixes noise/non-determinism and checkpoint-vs-leaderboard reliability items.
- T.2.1.x (weights) sub-splits overlap; T.1.3 (select members) overlaps with T.2.1.
- Desiderata are concise and partly prior-driven; weights are judgement-based. Leaves have no desiderata (only decision nodes).
- Three items with no keyword hits were placed by hand (date feature, consistency checks, inference notebook).

**Items per top-level branch:** see counts below.
- T.1 Change which models are in the ensemble 260
- T.2 Change how predictions are combined 281
- T.3 Change the model or its training 271
- T.4 Change the data or features 185
- T.5 Change validation and evaluation practice 136
- T.6 Change inference-time behaviour and post-processing 110
- T.7 Improve the experiment process 431
