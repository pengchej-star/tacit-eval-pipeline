### Per episode: the expert's step and what each agent chose

Cell: match with the gold (✓ yes, ~ partial, ✗ no) · the agent's node · score on our split (lower is better for commonlit and hms).

| case | expert's next step | gold nodes | gold possible? | Opus no | Opus cheat | Haiku no | Haiku cheat |
|---|---|---|---|---|---|---|---|
| commonlit 18423958 v4->v8 | v4->v5: go back from ALBERT-large to RoBERTa-base (768-dim head, the commonlit-roberta-0467 checkpoints that scored 0.462 in v3) and start stacking/blending | T.2.1.3, T.5.2.2, T.6.1.1, T.6.2.2.2 | partial | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 |
| commonlit 18426209 v3->v5 | v3->v4: blend weights 0.6/0.4 -> 0.5/0.5; v4->v5: add a new mean-pooling RoBERTa member (5 fold checkpoints) to the blend. The broken RoBERTa-large swap of v3 is not debugged | T.6.2.2.1, T.6.1.1 | no | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 |
| gquest 7253130 v3->v5 | v3->v4: learning rate 3e-5 -> 1e-5 and head dropout 0.2 -> 0.1 (v4->v5: dropout back to 0.2) | T.5.3, T.5.2 | yes | ✗ T.7.2 · 0.458 | ~ T.5.3 · 0.423 | ✗ T.3.4.3 · 0.430 | ✗ T.4.4.1 · 0.426 |
| hms 49524919 v54->v55 | v54->v55: add a 2D EfficientNet spectrogram model family and average it with the 1D EEGNet folds | T.5.1.1 | no | ~ T.5.1.5 · 0.868 | ✗ T.6 · 0.869 | ✗ T.5.3 · 0.887 | ✗ T.6 · 0.889 |
| hms 52551258 v2->v3 | v2->v3: replace the single FastViT model with an ensemble of pretrained EEG CNN-RNN checkpoints from hms-models, plus Butterworth filtering and spectrograms computed from raw EEG, in one refactor | T.4.1.1, T.5.1.1 | forced | ✓ T.4.1.1 · 1.052 | ✓ T.4.1.1 · 0.876 | ✗ T.6 · FAIL | ✗ T.6 · TIMEOUT |
| hms 53762022 v8->v9 | v8->v9: v8 submitted one model alone as a diagnostic (0.684); v9 rebuilds that model's pipeline (bandpass/montage/spectrogram features, StratifiedGroupKFold, new OOF and inference) instead of returning to the blend | T.2.4.2, T.3.1, T.5.1.3 | no | – no result | ✗ T.5.1.4 · 0.857 | ✗ T.5.1.4 · FAIL | ✗ T.5.1.4 · FAIL |
| hms 52200959 v34->v38 | v34->v35 has no code change; v35->v36: remove the early os._exit so models 2 and 3 run again and the three families are blended; v37->v38: weights from (1 - LB), normalized | T.5.1.4, T.5.3.2 | yes | ✓ T.5.1.4 · FAIL | ✓ T.5.1.4 · 0.515 | ✗ T.5.2.3 · TIMEOUT | ✓ T.5.1.4 · TIMEOUT |
| ranzcr 13521245 v6->v10 | v6->v7: load a better trained checkpoint (ranzcr-efficientnet-tpu-training/model.h5) and set the test resize to match it; v8->v9: test resize index 6 -> 7 | T.5.3, T.1.1.3, T.4.3.4 | forced | ✗ T.7.3.4 · 0.868 | ✓ T.1.1.3 · 0.865 | ✗ T.7.3.4 · 0.868 | ✗ T.7.3.4 · 0.868 |
| hms 50496431 v29->v32 | v29->v30: remove the in-notebook spectrogram generation and fix a lead-name bug in brain_leads; v30->v31: add NetOneImage (EfficientNet-B3 on its own spectrograms) to the ensemble; v32: identical re-run | T.5.1.1, T.2.3, T.1.10 | no | ✗ T.2.2.2 · 0.762 | ~ T.5.1.4 · 1.410 | ~ T.1.6 · FAIL | ✗ T.2.2.2 · FAIL |

### Counts (runs with a result)

| | match ✓ | partial ~ | no ✗ | same top-level branch as gold |
|---|---|---|---|---|
| opus no cheatsheet | 3 | 1 | 4 | 5 of 8 |
| opus cheatsheet | 4 | 2 | 3 | 7 of 9 |
| haiku no cheatsheet | 1 | 1 | 7 | 5 of 9 |
| haiku cheatsheet | 2 | 0 | 7 | 4 of 9 |

### Cheatsheet runs: did the agent open the gold part of the tree?

| case | model | match | opened gold node | opened gold branch | nodes opened | knowledge the agent reports |
|---|---|---|---|---|---|---|
| commonlit 18423958 | opus | ✓ | yes | yes | T.2.1 Choose the next experiment; T.2.1.3 Restore the last verified configuration | T.2.1: T.2.1.3 Restore the last verified configuration (applied) |
| commonlit 18423958 | haiku | ✓ | yes | yes | T.5.2 Choose backbone scale or family; T.5.2.1 Increase backbone capacity | T.5.2: T.5.2.2 Retain or adopt the smaller backbone (applied) |
| commonlit 18426209 | opus | ✗ | no | no | T.5.2 Choose backbone scale or family; T.5.2.2 Retain or adopt the smaller backbone | T.5.2: T.5.2.2 Retain or adopt the smaller backbone (applied) |
| commonlit 18426209 | haiku | ✗ | no | no | T.5.2 Choose backbone scale or family; T.5.2.2 Retain or adopt the smaller backbone | T.5.2: T.5.2.2 Retain or adopt the smaller backbone (applied) |
| gquest 7253130 | opus | ~ | yes | yes | T.5.3 Tune optimizer and learning schedule | T.5: T.5.3 Tune optimizer and learning schedule (applied); T.1.5: T.1.5.1 Repair imports and artifact paths (applied) |
| gquest 7253130 | haiku | ✗ | no | no | (taxonomy only) | (none) |
| hms 49524919 | opus | ✗ | no | yes | T.5.2 Reduce prediction variance; T.5.2.5 Average compatible training snapshots | T.5.2: T.5.2.5 Average compatible training snapshots (not applied) |
| hms 49524919 | haiku | ✗ | no | yes | T.5.3 Choose aggregation | T.5.3: T.5.3.1 Use a uniform arithmetic average (not applied) |
| hms 52551258 | opus | ✓ | no | no | T.1.2 Match the model to its checkpoint | (none) |
| hms 52551258 | haiku | ✗ | no | no | T.6 Calibrate final outputs | T.6: Calibrate final outputs (applied) |
| hms 53762022 | opus | ✗ | no | no | (taxonomy only) | T.5.1: T.5.1.4 Restore validated ensemble members (applied) |
| hms 53762022 | haiku | ✗ | no | no | (taxonomy only) | (none) |
| hms 52200959 | opus | ✓ | yes | yes | T.5.1 Choose ensemble membership; T.5.1.4 Restore validated ensemble members | T.5.1: T.5.1.4 Restore validated ensemble members (applied) |
| hms 52200959 | haiku | ✓ | no | no | (taxonomy only) | (none) |
| ranzcr 13521245 | opus | ✓ | yes | yes | T.1.1 Restore model and input compatibility; T.1.1.3 Restore training preprocessing; T.7.3 Change repeated-model aggregation | T.1.1: T.1.1.3 Restore training preprocessing (applied); T.7.3: T.7.3.4 Average valid input views (not applied) |
| ranzcr 13521245 | haiku | ✗ | no | yes | T.1.2 Repair execution and output assembly; T.7.3.4 Average valid input views | T.7.3: T.7.3.4 Average valid input views (applied) |
| hms 50496431 | opus | ~ | yes | yes | T.5.1 Choose ensemble membership; T.5.1.4 Restore validated ensemble members | T.5.1: T.5.1.4 Restore validated ensemble members (applied) |
| hms 50496431 | haiku | ✗ | no | yes | T Choose the next intervention; T.2.2 Resolve attribution; T.2.2.2 Restore the last verified configuration | T.2.2: T.2.2.2 Restore the last verified configuration (applied) |
