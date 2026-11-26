# hms · haiku · no cheatsheet

run hms__claude__claude-haiku-5-5__30min__20261120-105600; 21 steps; best 0.6995 (lower is better); final 0.72001

-   0.1 min · step   2 · says: Test has 1,693 unique EEGs and the sample has 9,850 rows, so I'll write a prior-based baseline first, then try a model.
-   0.2 min · step   3 · SUBMISSION 1.54891  (new best)
-   0.3 min · step   3 · says: Baseline is on disk. Next I'll try a spectrogram-feature LightGBM with soft labels and patient-grouped CV.
-   2.4 min · step   4 · says: Features are built (10,024 train and 1,114 test spectrograms). Next I'll train a patient-grouped LightGBM with soft-label targets and compare its CV KL against the prior.
-   5.8 min · step   5 · says: The LightGBM model cuts grouped-CV KL from 1.22 (prior) to 0.90. I'll validate the file and promote it to the submission before trying anything else.
-   6.3 min · step   6 · SUBMISSION 0.84605  (new best)
-   6.7 min · step   6 · says: The LightGBM submission is valid and in place. With the remaining time I'll try a small 2D CNN on the raw spectrograms, validate it on one grouped holdout, and blend it with LightGBM only if the blend helps.
-   9.4 min · step   7 · ERROR (call took 1.3 min): Traceback (most recent call last): |   File "/workspace/cnn.py", line 51, in <module> |     P=np.mean([pred(train(np.arange(len(Y))),) for _ in range(2)],0) |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/workspace/cnn.py", lin
-   9.4 min · step   7 · says: The CNN holdout KL is NaN and the final prediction call has a bug. The likely NaN source is missing values in the spectrograms, so I'll zero-fill them and fix the call.
-  11.1 min · step   8 · says: The CNN's fold-0 holdout KL is 0.654, against 0.908 for LightGBM on the same fold split, so the CNN is clearly stronger. I'll write its predictions as the submission in the same row order and validate them.
-  11.2 min · step   9 · SUBMISSION 0.72393  (new best)
-  11.3 min · step  10 · says: About 11 minutes of the 30 have passed. I'll test whether 20 epochs beats the 12-epoch CNN on the same fold, and only replace the submission if it does.
-  12.5 min · step  11 · says: The 20-epoch variant scored 0.657, slightly worse than 12 epochs (0.654), so I'm keeping the 12-epoch submission. Next I'll check whether blending the CNN with LightGBM improves on the same holdout fold.
-  12.8 min · step  12 · says: The blend helps slightly on this one fold (0.6533 at 0.8 CNN weight vs 0.6543 CNN alone). I'll write the 0.8/0.2 blend as the submission and validate it.
-  12.9 min · step  13 · says: The blend is in place and validated. About 13 minutes have elapsed, so I'll try one more cheap gain: averaging five grouped-fold CNNs for test predictions, which costs about 3 minutes.
-  12.9 min · step  13 · SUBMISSION 0.6995  (new best)
-  15.1 min · step  14 · says: Five fold-models are done. I'll average them with the full-data CNN predictions, blend 0.8 with LightGBM 0.2, and validate the result.
-  15.1 min · step  15 · SUBMISSION 0.71021
-  15.2 min · step  15 · says: About 15 minutes are used. I'll add a second five-fold CNN ensemble with different seeds to reduce variance, then re-blend.
-  17.3 min · step  16 · SUBMISSION 0.71164
-  17.4 min · step  16 · says: Two five-fold ensembles are blended in and the submission is valid. About 17 minutes have elapsed, so I'll run one more seed set to reduce variance further, then finish.
-  19.5 min · step  17 · SUBMISSION 0.71472
-  19.6 min · step  17 · says: The submission is current at 16:15, with about 10 minutes left on the timer. I'll add another CNN seed set and re-blend.
-  21.7 min · step  18 · SUBMISSION 0.71642
-  21.8 min · step  18 · says: About 22 minutes are used. I'll run one more seed set and re-blend.
-  24.0 min · step  19 · says: The submission at `/kaggle/working/submission.csv` is a blend of 6 CNN ensembles (80%) and LightGBM (20%). It has 9,850 rows and matches the sample submission's columns and eeg_id order, and each row sums to 1.  Estimated scores (KL, lower is better), measured on one grouped holdout fold:  | Model | Holdout KL | |---|---| | Class-prior baseline (5-fold OOF) | 1.222 | | LightGBM on spectrogram summ
-  24.0 min · step  19 · SUBMISSION 0.7175
-  24.1 min · step  19 · says: About 6 minutes remain. I'll add one more CNN seed set and re-blend, keeping the current submission in place until the new one passes validation.
-  26.3 min · step  20 · says: I added a seventh CNN seed set, and the submission is re-blended and validated at `/kaggle/working/submission.csv`. It has 9,850 rows, matching columns and eeg_id order, and each row sums to 1.  The final model is 80% an average of 7 CNN ensembles and 20% LightGBM. The blend weight was picked on a single holdout fold, and the 7-model ensemble itself was not validated. The last validated number is 
-  26.3 min · step  20 · SUBMISSION 0.71939
-  26.4 min · step  20 · says: About 4 minutes remain. A seed set takes roughly 2 minutes, so I'll run one more with a hard timeout and re-blend only if it finishes.
-  28.5 min · step  21 · SUBMISSION 0.72001
-  28.6 min · step  21 · says: The submission at `/kaggle/working/submission.csv` now uses 8 CNN ensembles (80%) blended with LightGBM (20%). It passed the same checks as before: 9,850 rows, matching columns and eeg_id order, no NaNs, and rows that sum to 1.  The blend weight was chosen on one holdout fold, and the 8-model ensemble has not been validated on a holdout. The last validated number is 0.653 KL for the single-CNN + L
