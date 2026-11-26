# ranzcr · opus · no cheatsheet

run ranzcr__claude__claude-opus-5-5__30min__20261120-104714; 18 steps; best 0.92984 (higher is better); final 0.92915

-   8.5 min · step   5 · says: Epoch 1 gets val AUC 0.901, and each epoch takes about 165 s, so all 6 epochs should finish around minute 25. I'm saving a submission after every epoch.
-   8.5 min · step   6 · ERROR (call took 0.0 min): 
-   8.6 min · step   7 · SUBMISSION 0.89082  (new best)
-  13.7 min · step   8 · SUBMISSION 0.9234  (new best)
-  17.5 min · step   9 · SUBMISSION 0.92053
-  24.2 min · step  11 · says: The blend gives the best validation score, 0.919, so I'm using it as the submission.
-  24.3 min · step  12 · SUBMISSION 0.92984  (new best)
-  24.4 min · step  12 · says: The final submission is at `/kaggle/working/submission.csv` and scores **0.919 mean AUC** on my validation split. It has the required 3,009 rows and the same columns as the sample submission.  It is a blend of two EfficientNet-B3 models, both trained on grayscale X-rays shrunk to 384×384: - **6-epoch run (30% weight):** it peaked at 0.916 after 4 epochs, then overfit and ended at 0.902. I only kep
-  24.5 min · step  12 · says: With about 6 minutes left there isn't time to train another model, so I'll use the time to tune the blend weights (raw and rank-averaged) on validation.
-  24.6 min · step  13 · says: Rank averaging at 0.3/0.7 does a little better, so I'll switch to it.
-  24.6 min · step  14 · SUBMISSION 0.92924
-  24.7 min · step  14 · says: I switched the final submission to a rank-averaged blend, which raised validation mean AUC from 0.919 to **0.920**. Instead of averaging the two models' probabilities, it averages each image's rank within each label. The models and the 30/70 weighting are unchanged.  I tested weights from 0.2 to 0.5 for the weaker 6-epoch model. Rank averaging came out slightly ahead of plain averaging at every we
-  24.9 min · step  14 · says: I'm leaving the submission as it is. With about 5 minutes left, nothing I could still do is likely to help:  - **No new models or extra mirror-image passes:** the training script never saved the model weights. The only outputs are the prediction files, so even re-predicting with what's already trained would mean training again, which takes about 2.5 minutes per epoch. - **No further blend tuning:*
-  25.1 min · step  15 · says: I checked the submission again and it's valid, so I'm keeping it as the final version. The file has 3,009 rows, its columns and image IDs match `sample_submission.csv` exactly in the same order, and there are no missing values.  It is the 0.3/0.7 rank-averaged blend of the two EfficientNet-B3 models, which scored **0.920** mean AUC on my validation split.  My reasoning for stopping is unchanged. T
-  25.2 min · step  15 · says: I'll try one more thing that can't harm the current file: a 1-epoch EfficientNet-B3 run (about 2.5 minutes). I'll only blend it in if it raises the validation score.
-  28.1 min · step  17 · SUBMISSION 0.92915
-  28.2 min · step  18 · says: I trained a third model in the remaining time and added it to the blend. Validation mean AUC went from **0.920 to 0.922**.  - **New model:** a 1-epoch EfficientNet-B3 run. On its own it only reached 0.891, but it adds some variety to the ensemble. - **Blend:** the new model gets 10% weight on top of the existing 0.3/0.7 rank-averaged blend of the first two models. - **Weight choice:** 20% actually
