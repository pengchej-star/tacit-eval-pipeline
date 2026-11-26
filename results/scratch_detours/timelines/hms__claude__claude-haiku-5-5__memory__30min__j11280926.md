# hms · haiku · cheatsheet

run hms__claude__claude-haiku-5-5__memory__30min__j11280926; 35 steps; best 0.86365 (lower is better); final 0.87143

Knowledge the agent reports using (from the cheatsheet): none

-   0.0 min · step   1 · READS CHEATSHEET: `date; ls -la /kaggle/input/hms-harmful-brain-activity-classification; cat /kaggle/input/hms-harmful-brain-activity-classification/description.md | head -c 5000;`
-   0.0 min · step   2 · READS CHEATSHEET: `cat /workspace/memory/taxonomy.md`
-   0.2 min · step   5 · says: Time budget is 30 minutes, so I'll write a prior-based baseline submission first, then try a fast spectrogram-feature model.
-   0.3 min · step   6 · SUBMISSION 1.48867  (new best)
-   0.4 min · step   6 · says: Baseline is written. Next I'll extract per-spectrogram summary features (mean and std of log power over time) in parallel, then train LightGBM on them.
-   0.6 min · step  12 · says: While extraction runs, I'll write the training script. It uses soft-label LightGBM (each class replicated with its vote-fraction weight), grouped 5-fold CV by patient, and the KL metric.
-   0.8 min · step  16 · says: The background job's output file is empty, so I'll check whether the process is still alive.
-   0.8 min · step  17 · says: The extraction was wrapped in `timeout 100`, so it was likely killed before finishing. Checking the other output file to confirm.
-   0.8 min · step  18 · ERROR (call took 0.0 min): 
-   0.9 min · step  18 · says: The `timeout 100` I wrapped around the extraction killed it after 100 seconds, before it could finish. I'll rerun it without the timeout, logging to a file.
-   2.8 min · step  20 · says: The feature file is written (11,138 spectrograms: 10,024 train + 1,114 test). The earlier monitor notifications were from the stale wait loops, so I'm ignoring them. Next I'll run the CV training in the background.
-   7.3 min · step  22 · SUBMISSION 0.88654  (new best)
-   7.4 min · step  22 · says: OOF KL is 1.051 against a 1.259 prior baseline. I'll check the clock and the submission, then record memory use honestly.
-   7.4 min · step  23 · says: The submission validates: columns and row count match, no NaNs, and rows sum to 1. About 8 minutes of the 30 have passed. I'll try one cheap improvement, more boosting rounds, writing to a separate file and only promoting it if OOF KL improves.
-  17.3 min · step  25 · says: The longer run overfits (OOF KL 1.073 vs 1.051), so I'll keep the original submission. One quick try with fewer rounds, promoted only if it beats 1.051.
-  19.6 min · step  26 · says: 200 rounds gives OOF KL 0.998, better than 400 rounds (1.051). I'll promote it and try 100 rounds.
-  19.6 min · step  27 · SUBMISSION 0.86543  (new best)
-  20.9 min · step  27 · says: 100 rounds gives OOF KL 0.967, the best so far. I'll promote it and try 50 rounds with the remaining time.
-  20.9 min · step  28 · SUBMISSION 0.86365  (new best)
-  21.6 min · step  29 · says: Submission is valid at 22 of 30 minutes. I have a few minutes left, so I'll try two more variants of the same model.
-  23.8 min · step  30 · says: Variant f (31 leaves, 100 rounds) is best at OOF KL 0.958. I'll promote it and validate.
-  23.8 min · step  31 · SUBMISSION 0.87315
-  23.9 min · step  31 · says: Variant f is promoted and validated at 24 minutes. One more regularization variant with the remaining time.
-  24.6 min · step  32 · says: Variant h (15 leaves, 120 rounds) scored 0.962, so variant f stays as the final submission. About 25 of the 30 minutes are used. I'll stop here rather than start another run that might not finish before the timer.  ## Result  `/kaggle/working/submission.csv` is the LightGBM model from variant f. It matches `sample_submission.csv` in columns, row count, and `eeg_id` order, has no NaNs, and each row
-  24.6 min · step  32 · says: About 5 minutes remain, so I'll try one cheap ensemble: average the OOF predictions of the two best configs (31 leaves and 15 leaves) and promote the blend only if its OOF KL beats 0.958.
-  26.0 min · step  34 · says: The submission now uses a blend of two LightGBM configs (31 leaves and 15 leaves), and its out-of-fold KL is **0.9545**, down from 0.9577 for the single model. The file passes the format checks: columns and row order match the sample, there are no NaNs, and every row sums to 1.  I'm stopping here with about 4 minutes left. The next step would be another config in the blend, but a run takes about 4
-  26.0 min · step  33 · SUBMISSION 0.87982
-  26.1 min · step  34 · says: About 4 minutes remain. I'll try a three-way blend by adding the 63-leaf, 100-round config, and promote it only if OOF KL beats 0.9545.
-  28.6 min · step  35 · says: The three-way blend is promoted. Its out-of-fold KL is **0.9527**, down from 0.9545 for the two-way blend. The file passes the format checks: columns and row order match the sample, there are no NaNs, and every row sums to 1.  I'm stopping now because about 3 minutes remain, which is not enough for another blend run plus validation. The submission on disk is valid.
-  28.6 min · step  35 · SUBMISSION 0.87143
