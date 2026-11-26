# aes2 · haiku · no cheatsheet

run learning__claude__claude-haiku-5-5__30min__20261120-095613; 27 steps; best 0.83062 (higher is better); final 0.83062

-   0.0 min · step   1 · says: The data is 1,731 test rows with a QWK metric. I'll start with a fast TF-IDF baseline so a valid submission exists early, then try something stronger.
-   0.9 min · step   3 · says: Baseline is saved at OOF QWK 0.785. Next I'll check whether a pretrained transformer can be downloaded, since it should beat TF-IDF.
-   0.9 min · step   3 · SUBMISSION 0.79453  (new best)
-   1.1 min · step   4 · says: Weights download fine. I'll fine-tune DeBERTa-v3-base for regression on one 80/20 split (2 epochs, bf16) in the background, since 5 folds won't fit in the time left. Then I'll blend it with the ridge model on the held-out split.
-   2.7 min · step   5 · says: The loss went to NaN at step 200. I'll stop the run and check whether the log shows a single bad batch or a steady divergence.
-   2.7 min · step   6 · KILL: `pkill -f deberta.py; sleep 3; grep -v Warning /workspace/code/deb.log | tail -12; python -c " import pandas as pd; tr=pd.read_csv('/kaggle/input/learning-agency`
-   2.8 min · step   6 · says: `pkill` isn't available, so I'll kill the process by PID. I'll also switch the training to fp32 with TF32 to rule out bf16 overflow as the cause of the NaN.
-   2.8 min · step   7 · KILL: `for p in $(ps -eo pid,args | grep "[d]eberta.py" | awk '{print $1}'); do kill $p; done; sleep 3 cd /workspace/code && sed -i "s/with torch.autocast('cuda',dtype`
-   4.9 min · step   7 · says: The shell chain got backgrounded, and `ps` doesn't exist here, so the old run may still be alive. I'll find the processes through `/proc` before doing anything else.
-   4.9 min · step   8 · says: Two DeBERTa processes (PIDs 200 and 373) are running and both write to `deb.log`, so the earlier chained command relaunched on top of the old one. I'll kill both and confirm the script edits before starting a single clean run.
-   4.9 min · step   9 · KILL: `for d in /proc/[0-9]*; do c=$(tr '\0' ' ' < $d/cmdline 2>/dev/null); case "$c" in "python deberta.py"*) kill ${d#/proc/};; esac; done; sleep 5; nvidia-smi --que`
-   5.1 min · step   9 · says: Both runs are stopped and the GPU is clear. Training is now fp32; the predict path still uses bf16 autocast, which is fine for inference. I'll launch one clean run.
-   6.8 min · step  10 · says: The notification is for the earlier background shell that has already exited, so it doesn't change anything. The real problem is that outputs are non-finite even in fp32, so the weights are probably already NaN. I'll check the loss history to see where it started.
-   6.8 min · step  11 · KILL: `cd /workspace/code; grep -E "^[0-9]+ [0-9]+ " deb.log | head; grep -c nonfinite deb.log; grep -m1 -n nonfinite deb.log; for d in /proc/[0-9]*; do c=$(tr '\0' ' `
-   6.9 min · step  11 · says: The loss was finite at step 0 and non-finite at step 1, which points at the first optimizer update or its gradients rather than bf16. I'll check gradient norms and parameter finiteness right after step 0, with a fallback to a different backbone if that's not the cause.
-   7.1 min · step  12 · says: The gradient norm is `float16`, so the model weights loaded in fp16 (the checkpoint's stored dtype). fp16 AdamW updates overflow to NaN. I'll force fp32 weights and relaunch.
-   8.9 min · step  13 · says: Training is stable now: loss is finite and falling, at about 53 s per 200 steps. Two epochs should take roughly 7 minutes, so I'll wait for it to finish.
-   9.0 min · step  16 · says: The harness blocks chained sleeps, so I'll load the Monitor tool and use an until-loop to wait for completion.
-   9.1 min · step  18 · says: While the model trains, I'll prepare the blend script. It will combine the DeBERTa and TF-IDF predictions on the shared validation fold and tune thresholds for the blend.
-   9.2 min · step  20 · says: The DeBERTa run is still going, and I'm waiting on the monitor to report completion.
-  15.0 min · step  20 · says: DeBERTa finished. Epoch 0 scored 0.807 on the held-out fold and epoch 1 scored 0.797, so the saved predictions come from the final epoch. Now I'll blend it with TF-IDF on that same fold.
-  15.2 min · step  21 · SUBMISSION 0.82655  (new best)
-  15.3 min · step  21 · says: The blend is written. I'll verify the submission format against the sample before stopping.
-  15.4 min · step  22 · says: The submission is written and validated at `/kaggle/working/submission.csv`. Its columns, row count and essay_id order match `sample_submission.csv`, with no missing scores.  **Result:** estimated QWK about 0.83 on a single 20% holdout fold (fold 0 of a 5-fold split). That number is optimistic because the blend weight and rounding thresholds were tuned on the same fold.  **What's in the submission
-  15.4 min · step  22 · says: About 15 minutes remain, so I'll run one more DeBERTa fold (fold 1) for an extra test-prediction ensemble member. Four folds won't fit in the time left. The current submission stays in place until a blend succeeds.
-  16.5 min · step  23 · says: Fold 1 is training with a finite loss. It takes about 8 minutes, so I'll wait on a monitor for completion.
-  16.5 min · step  24 · says: Waiting for the fold 1 run to finish.
-  23.5 min · step  24 · says: Fold 1 finished at 0.812 holdout QWK. Next I'll blend on the union of the two DeBERTa holdout folds, averaging the two models' test predictions.
-  23.8 min · step  25 · SUBMISSION 0.83062  (new best)
-  23.9 min · step  25 · says: The submission is updated and validated: holdout QWK 0.826 across two folds, against 0.829 for the single-fold blend. The two-fold number is more reliable since it isn't tuned on one split. I'll start fold 2 now and re-blend if it finishes before the timer ends.
-  24.7 min · step  27 · says: Fold 2 is training; I'll re-blend when its monitor reports.
