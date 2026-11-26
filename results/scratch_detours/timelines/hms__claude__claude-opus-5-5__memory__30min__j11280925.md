# hms · opus · cheatsheet

run hms__claude__claude-opus-5-5__memory__30min__j11280925; 30 steps; best 0.7854 (lower is better); final 0.7854

Knowledge the agent reports using (from the cheatsheet):
- T.2.4: T.2.4.2 Use disjoint group-aware folds (applied): Rows share patient_id/eeg_id; used GroupKFold by patient, one sample per eeg_id.
- T.3.3: T.3.3 Change training examples (fine-tune on high-agreement subset) (applied): Second stage trained on samples with >=10 votes; this lowered held-out KL on high-vote samples from ~0.40 to ~0.30-0.33 but raised it on all samples.

-   0.0 min · step   1 · READS CHEATSHEET: `cd /kaggle/input/hms-harmful-brain-activity-classification; ls; head -3 train.csv test.csv sample_submission.csv; wc -l *.csv; ls train_spectrograms | wc -l; ls`
-   0.2 min · step   3 · READS CHEATSHEET: `cd /kaggle/input/hms-harmful-brain-activity-classification; python -c " import pandas as pd t=pd.read_csv('test.csv') for i in range(3):   r=t.drop_duplicates('`
-   0.5 min · step   4 · READS CHEATSHEET: `cd /kaggle/input/hms-harmful-brain-activity-classification; python -c " import pandas as pd tr=pd.read_csv('train.csv') g=tr.groupby('eeg_id').eeg_label_offset_`
-   1.0 min · step   5 · says: Plan: one sample per eeg_id (votes averaged), Kaggle spectrogram 10-min window + EEG 50s bipolar raw, train a CNN with KL loss, GroupKFold by patient. Preprocessing first.
-   1.5 min · step   7 · ERROR (call took 0.0 min): Traceback (most recent call last): |   File "/workspace/prep.py", line 27, in <module> |     y=g[V].sum(); y=y.div(y.sum(1),axis=0).loc[mid.eeg_id] |                                                ^^^^^^^^^^ |   File "/scratch/pengchej/envs/kaggle-run-gpu/li
-   1.5 min · step   7 · says: Pandas apply dropped the group column; fix with iloc-based middle pick.
-   3.0 min · step   9 · says: Writing a prior-based fallback submission while preprocessing runs.
-   3.0 min · step  10 · SUBMISSION 1.48867  (new best)
-  10.0 min · step  14 · says: ~11 min elapsed. Quick timing test on fold 0.
-  11.3 min · step  15 · says: Each epoch takes about 45s, so running 5 folds one after another won't fit. I'll run 5 single-fold processes in parallel on the GPU instead.
-  11.3 min · step  16 · KILL: `cd /workspace; pkill -f train.py; sleep 3; for f in 0 1 2 3 4; do nohup python train.py efficientnet_b0 4 b0f$f $f > b0f$f.log 2>&1 & done; sleep 110; grep -h f`
-  14.8 min · step  18 · KILL: `cd /workspace; for p in /proc/[0-9]*; do c=$(tr '\0' ' ' < $p/cmdline 2>/dev/null); case "$c" in *"train.py efficientnet_b0 5 b0"*) echo kill ${p#/proc/}; kill `
-  14.8 min · step  18 · ERROR (call took 0.0 min): 
-  16.7 min · step  20 · ERROR (call took 0.8 min): OutOfMemoryError: CUDA out of memory. Tried to allocate 42.00 MiB. GPU 0 has a total capacity of 95.01 GiB of which 9.69 MiB is free. Process 705 has 23.23 GiB memory in use. Including non-PyTorch memory, this process has 15.55 GiB memory in use. Pro
-  19.7 min · step  23 · says: Each epoch takes about 117s with two folds running together, so both should finish in about 4–5 minutes. Writing the submission script meanwhile.
-  21.6 min · step  25 · says: The submission is written from the 2-fold ensemble. About 8 minutes are left, which is enough to train folds 2 and 3 (~4 min) and add them to the ensemble.
-  21.6 min · step  25 · SUBMISSION 0.79941  (new best)
-  25.5 min · step  28 · SUBMISSION 0.78931  (new best)
-  25.7 min · step  28 · says: The submission is saved at `/kaggle/working/submission.csv`: the average of four EfficientNet-B0 models, one per fold. It has 9,851 rows and matches the sample submission's columns. The fifth fold wasn't trained because time ran out.  **Validation scores (KL divergence, lower is better)**  | Fold | All held-out samples | High-agreement samples (≥10 votes) | |---|---|---| | 0 | 0.76 | 0.30 | | 1 | 
-  25.8 min · step  28 · says: About 4 minutes are left, which is just enough to try training the missing fifth fold. The current submission stays in place unless the run finishes.
-  27.8 min · step  30 · says: The fifth fold finished in time, so `/kaggle/working/submission.csv` is now the average of all five folds. It has 9,851 rows and passes the column and missing-value checks.  Fold 4 scored 0.56 KL on all held-out samples and 0.32 on the high-agreement ones (≥10 votes), in line with the other folds. The trade-off from before still holds: the second stage on high-agreement samples improved that subse
-  27.8 min · step  30 · SUBMISSION 0.7854  (new best)
