# gquest · opus · no cheatsheet

run google__claude__claude-opus-5-5__30min__20261120-105301; 35 steps; best 0.40716 (higher is better); final 0.40716

-   0.0 min · step   1 · ERROR (call took 0.0 min): 
-   1.9 min · step   5 · says: First epoch gave a NaN score, which points to NaN predictions. Stopping the run to debug.
-   1.9 min · step   6 · KILL: `cd /workspace; pkill -f train.py; ls -la --time-style=full-iso deb.log; head -20 deb.log | grep -v -i warn`
-   2.0 min · step   7 · KILL: `cd /workspace; kill $(pgrep -f train.py) 2>/dev/null || ps aux|grep train.py|grep -v grep|awk '{print $2}'|xargs kill; sleep 2; nvidia-smi --query-gpu=memory.us`
-   2.1 min · step   8 · KILL: `for p in /proc/[0-9]*; do grep -q train.py $p/cmdline 2>/dev/null && echo ${p#/proc/} && kill ${p#/proc/}; done; date`
-   2.4 min · step  10 · KILL: `kill 300; sleep 3; nvidia-smi --query-gpu=memory.used --format=csv,noheader; cd /workspace; python - <<'EOF' 2>&1 | grep -v -i warn | tail -5 import torch from `
-   2.9 min · step  11 · says: Meanwhile, I'll write a quick TF-IDF+ridge baseline submission as a safety net.
-   3.3 min · step  12 · SUBMISSION 0.37476  (new best)
-   5.4 min · step  14 · says: Seeing "0 1 nan" seconds after epoch 0 suggests the old fp16 process is still alive and writing to the same log. Checking.
-   5.8 min · step  15 · says: Old process (PID 97) is still running; killing it so it stops overwriting the new run's files.
-   5.9 min · step  16 · KILL: `kill 97; sleep 3; nvidia-smi --query-compute-apps=pid,used_memory --format=csv`
-   6.2 min · step  16 · says: Only the new run is left now. Fold 0, epoch 0 scored 0.30 Spearman, and each epoch takes about 2 min. Waiting for fold 0 to finish.
-   7.4 min · step  17 · says: Epochs take ~1 min now, so DeBERTa should be done around 16:07. I'll start a second backbone (roberta-base) alongside it to ensemble with.
-  10.2 min · step  19 · says: Started around 15:52, so the deadline is about 16:22. Writing a blend from the partial predictions now so a usable submission is on disk.
-  10.2 min · step  20 · SUBMISSION 0.38512  (new best)
-  16.7 min · step  21 · says: Both models finished: DeBERTa CV 0.353, RoBERTa CV 0.365. There are about 12 minutes left, so I'm starting a third backbone (ELECTRA-base) and checking the OOF blend in the meantime.
-  16.7 min · step  22 · SUBMISSION 0.38936  (new best)
-  16.8 min · step  22 · says: The DeBERTa+RoBERTa blend scores 0.369 OOF and is saved as the submission. Next I'll add ELECTRA to the blend, using its partial folds if it doesn't finish in time.
-  19.9 min · step  24 · says: ELECTRA hurts the blend (0.321 CV), so I'm leaving it out. The final blend is 0.4·DeBERTa + 0.6·RoBERTa, averaged over ranks.
-  20.0 min · step  25 · SUBMISSION 0.38992  (new best)
-  20.1 min · step  25 · says: About 9 minutes are left. I'll train a second RoBERTa seed (about 6–7 min) and fold it in only if it finishes.
-  23.4 min · step  28 · SUBMISSION 0.39028  (new best)
-  23.5 min · step  28 · says: The submission is saved at `/kaggle/working/submission.csv`. It's a rank-averaged blend of DeBERTa-v3-base (weight 0.3) and two RoBERTa-base runs with different seeds (0.35 each), and scores **0.371 mean Spearman** on out-of-fold predictions. The file has 608 rows, the same columns and IDs as the sample, and no missing values.  All models were fine-tuned the same way: - **Input:** the question (ca
-  23.6 min · step  28 · says: With about 6 minutes left, a quick option is to tune the blend weights separately for each of the 30 targets on the out-of-fold predictions. I'll only keep it if the score clearly improves.
-  23.9 min · step  30 · says: I tried tuning the blend weights separately for each of the 30 targets, and it didn't help. Out-of-fold Spearman went from 0.3710 to 0.3714, below the 0.001 gain I'd set for keeping it, so I discarded it. A gain that small would probably not hold on the test set.  The submission is unchanged: the 3-model blend of DeBERTa and two RoBERTa seeds, at **0.371 mean Spearman** out-of-fold. I re-checked `
-  24.0 min · step  30 · says: About 5 minutes remain, which is enough for one cheap experiment: a TF-IDF + ridge model trained on the same folds. It makes different kinds of errors from the transformers, so a small weight in the blend might help. I'll only keep it if out-of-fold Spearman improves by more than 0.001.
-  24.4 min · step  31 · SUBMISSION 0.40407  (new best)
-  24.5 min · step  31 · says: The gain was still rising at weight 0.2, so I'll try higher ridge weights.
-  25.0 min · step  33 · says: Adding a TF-IDF + ridge model to the blend raised the score from **0.371 to 0.377** mean Spearman on out-of-fold predictions. The new blend is saved as the submission.  The ridge model scores only 0.307 on its own, well below the transformers. It still helps because it gets different questions wrong than they do. It was cross-validated on the same 5 question-grouped folds as the transformers, so t
-  25.1 min · step  33 · says: With about 5 minutes left, I'll try one more cheap change: a stronger ridge model, using a tuned regularisation strength and character n-gram features. I'll only keep it if the blend's out-of-fold score improves by more than 0.001.
-  28.6 min · step  34 · SUBMISSION 0.40716  (new best)
-  28.7 min · step  35 · says: The stronger ridge model raised the blend's out-of-fold score from **0.3768 to 0.3787** mean Spearman, and the new blend is saved as the submission. I added character n-gram features and raised the regularisation strength from 3 to 10. That took the ridge model alone from 0.306 to 0.321.  | Ridge setup | Ridge alone | Blend at weight 0.25 | |---|---|---| | Word n-grams, alpha 3 (previous) | 0.307 
