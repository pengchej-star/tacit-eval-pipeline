# commonlit · opus · no cheatsheet

run commonlitrea__claude__claude-opus-5-5__30min__20261120-100351; 32 steps; best 0.51878 (lower is better); final 0.51878

-   0.0 min · step   1 · ERROR (call took 0.0 min): 
-   0.2 min · step   3 · SUBMISSION 1.04884  (new best)
-   3.6 min · step   9 · says: Deberta run produced no valid validation score (likely NaN). Debugging quickly.
-   6.9 min · step  14 · says: The model is loading in fp16 weights (training in fp16 → NaN). Forcing fp32.
-   7.6 min · step  15 · says: Fixed. Launching the full 5-fold DeBERTa-v3-large run.
-   7.7 min · step  16 · says: Per-fold timing (~3.5 min) means 5 folds finish near the deadline; restarting with per-fold checkpointing of test preds so partial results are usable.
-   7.7 min · step  17 · KILL: `cd /workspace; pkill -f train.py; sleep 2; sed -i 's|    tp+=tpf/5;del m,opt;torch.cuda.empty_cache()|    tp+=tpf;np.save(f"te_{TAG}_part.npy",tp/(f+1));np.save`
-   8.0 min · step  20 · KILL: `kill 776; sleep 1; ls /proc/776 >/dev/null 2>&1 && echo alive || echo killed`
-   8.1 min · step  20 · says: While it runs, I'll set up a watcher that writes the submission from the partial test predictions after each fold.
-  10.8 min · step  21 · ERROR (call took 2.7 min): 
-  10.9 min · step  21 · SUBMISSION 0.55881  (new best)
-  13.8 min · step  23 · SUBMISSION 0.56044
-  16.6 min · step  23 · SUBMISSION 0.54339  (new best)
-  19.5 min · step  23 · SUBMISSION 0.53523  (new best)
-  22.4 min · step  24 · SUBMISSION 0.53905
-  22.6 min · step  24 · says: The final submission is in `/kaggle/working/submission.csv`. It's the average of 5 DeBERTa-v3-large models, one per cross-validation fold, and scores **0.516 RMSE** on out-of-fold predictions. For scale, the targets have a standard deviation of 1.03, so predicting the mean every time would score about 1.03. The file has 284 rows plus a header and matches the sample submission's columns.  - **Model
-  22.8 min · step  24 · says: About 7 minutes left. The weakest fold (fold 4, RMSE 0.575) is the clearest thing to fix, so I'll retrain just that fold with a different seed. That takes about 3.5 minutes. If it scores better, I'll swap it into the average.
-  22.8 min · step  25 · KILL: `cd /workspace; for p in /proc/[0-9]*; do c=$(tr '\0' ' ' < $p/cmdline 2>/dev/null); [[ $c == *"while true"* ]] && kill ${p#/proc/}; done sed -e 's/for f,(a,b) i`
-  22.8 min · step  25 · ERROR (call took 0.0 min): 
-  22.9 min · step  25 · says: My loop that killed the old watcher also matched the shell running it, so that command killed itself. Running the remaining steps again:
-  25.9 min · step  27 · says: The retrain scored 0.555 on fold 4, better than the original 0.575. I'll add it as a sixth model in the test average and weight fold 4's two runs together like one fold.
-  26.0 min · step  28 · SUBMISSION 0.53909
-  26.1 min · step  28 · says: I used the extra time to retrain the weakest fold, and the out-of-fold RMSE improved from 0.516 to **0.511**. The new submission is in `/kaggle/working/submission.csv`, with all 284 rows and the required columns.  - **What I did:** I retrained fold 4, the worst one at 0.575, with a different random seed. The new run scored 0.555 on that fold. - **What changed in the submission:** the test predicti
-  26.2 min · step  28 · says: Four minutes isn't enough for another transformer fold, so I'll try a quick CPU-only blend: a TF-IDF ridge regression stacked with the DeBERTa out-of-fold predictions. I'll only use it if cross-validation improves.
-  26.3 min · step  29 · SUBMISSION 0.53968
-  26.4 min · step  29 · says: The TF-IDF blend added almost nothing: out-of-fold RMSE moved from 0.5113 to **0.5110**, which is within noise. I wrote it to `/kaggle/working/submission.csv` anyway, still 284 rows with the required columns, because it at least doesn't make things worse.  - **The blend:** a TF-IDF ridge regression on the excerpt text scored only 0.754 RMSE alone, far behind DeBERTa's 0.511. The best mixing weight
-  26.5 min · step  29 · says: With 3 minutes left, I'll check whether a linear rescaling of the DeBERTa predictions helps; averaging tends to shrink predictions toward the mean. I'll fit and score it with cross-validation and only apply it if it clearly helps.
-  26.7 min · step  30 · says: I checked a cross-validated linear rescaling of the predictions and decided not to apply it, so the final submission is unchanged from the last step. `/kaggle/working/submission.csv` is still valid: 284 rows, no missing values.  The fit came out at almost exactly slope 1 with a shift of −0.04, so it is really just a small offset. It would move RMSE from 0.5113 to 0.5100, too small and too much lik
-  26.8 min · step  30 · says: A training run won't fit in 3 minutes, so I'll try one last cheap stack: simple readability features (word and sentence length, syllables) plus the DeBERTa predictions, fed to a ridge model. I'll only apply it if nested cross-validation shows a real gain.
-  27.0 min · step  31 · says: The stack lowers cross-validated RMSE from 0.511 to 0.504, a real gain, so I'm applying it to the test predictions.
-  27.1 min · step  32 · says: The final submission improved again: out-of-fold RMSE went from 0.511 to **0.504** by combining the DeBERTa predictions with simple readability features. `/kaggle/working/submission.csv` has been rewritten and passes the format checks (284 rows, no missing values).  - **What I added:** six hand-made text features per excerpt: words per sentence, characters per word, syllables per word, share of wo
-  27.1 min · step  32 · SUBMISSION 0.51878  (new best)
