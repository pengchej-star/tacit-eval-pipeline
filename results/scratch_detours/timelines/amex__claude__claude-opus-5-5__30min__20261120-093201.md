# amex · opus · no cheatsheet

run amex__claude__claude-opus-5-5__30min__20261120-093201; 38 steps; best 0.78727 (higher is better); final 0.78646

-   1.5 min · step   4 · says: Fast. Run training.
-   3.5 min · step   5 · ERROR (call took 2.0 min): Traceback (most recent call last): |   File "/scratch/pengchej/envs/kaggle-run-gpu/lib/python3.11/site-packages/xgboost/data.py", line 408, in pandas_feature_info |     new_feature_types.append(_pandas_dtype_mapper[dtype.name]) |                           
-   3.6 min · step   5 · says: Pandas 3 string dtype. Use category codes instead.
-   5.0 min · step   6 · SUBMISSION 0.78505  (new best)
-   5.8 min · step   8 · says: Fold 1: 0.7935. Run CatBoost GPU concurrently for a blend.
-   6.7 min · step  11 · SUBMISSION 0.7866  (new best)
-   8.7 min · step  11 · SUBMISSION 0.78727  (new best)
-   8.8 min · step  11 · says: Around 12 minutes have gone by. Both models should be done near the 20-minute mark, and then I'll blend them.
-  10.4 min · step  12 · SUBMISSION 0.78669
-  12.6 min · step  12 · SUBMISSION 0.78673
-  13.3 min · step  13 · SUBMISSION 0.78675
-  13.6 min · step  14 · says: The final submission is a 50/50 rank-average blend of XGBoost and CatBoost, saved at `/kaggle/working/submission.csv`. Its out-of-fold AMEX score is **0.7943**, using 5-fold cross-validation on the training set; I have no test-set score.  I checked the file against the sample: same columns, same 45,892 customer IDs, no missing predictions.  **Pipeline:** - **Features** (`fe.py`): one row per custo
-  13.7 min · step  14 · says: I'll use the time to train two more models in parallel, then blend whatever finishes: LightGBM on the CPU and a second XGBoost on the GPU with a different seed and settings. Each fold is saved as it finishes.
-  13.9 min · step  15 · says: Next I'll write a blend script that only uses folds that have finished, and wait for the first ones.
-  16.4 min · step  17 · says: The second XGBoost has finished 3 folds, and LightGBM hasn't finished any yet. I'll blend now with what's available.
-  16.5 min · step  18 · says: Grid-searched weights (0.1/0.6/0.3) are noisy on this subset; equal weights are nearly as good and more robust. I'll write the equal-weight blend instead.
-  16.7 min · step  19 · says: I'll wait briefly for a 4th XGBoost fold, then re-blend if it lands in time.
-  16.7 min · step  19 · SUBMISSION 0.78567
-  17.3 min · step  20 · SUBMISSION 0.78683
-  17.5 min · step  21 · says: The submission is now an equal-weight rank average of three models: the original XGBoost, CatBoost, and a second XGBoost. On the customers where all three have out-of-fold predictions, the blend scores **0.7952**. That's up from **0.7943** for the earlier two-model blend.  The two numbers aren't measured on exactly the same rows. The second XGBoost had finished 4 of its 5 folds at blend time, so t
-  17.6 min · step  23 · ERROR (call took 0.0 min): 
-  17.8 min · step  24 · says: Line 23 uses `NF` before line 27 defines it, so the script will crash. I'll fix it and relaunch.
-  18.7 min · step  26 · says: The second XGBoost now has all 5 folds (out-of-fold score 0.7910). I'll re-blend the three models using every training row.
-  18.8 min · step  27 · SUBMISSION 0.78656
-  18.9 min · step  27 · says: The submission is the equal-weight blend of the three models, now that each has all 5 folds. Its out-of-fold score over all 413,021 training customers is **0.7943**. That's essentially the same as the earlier two-model blend (0.7943). The 0.7952 I reported last turn was too optimistic: it was measured on only the 80% of customers the 4 finished folds covered.  | Model | Out-of-fold score | |---|--
-  19.1 min · step  27 · says: With about 11 minutes left, I'll run one more XGBoost on the same folds, with a different seed and column sampling, saving after each fold. I'll blend it in only if at least 3 folds finish in time.
-  19.2 min · step  28 · says: While that trains, I'll make the blend script skip the weight grid search when there are 4 models. That grid has about 286 combinations and would take too long, and I'm using equal weights anyway.
-  21.1 min · step  30 · SUBMISSION 0.78629
-  21.2 min · step  30 · says: On the same three folds, the four-model blend scores 0.7954 against 0.7948 for three models, so the new model helps. I'll wait briefly for its 4th fold and re-blend.
-  21.8 min · step  31 · SUBMISSION 0.78644
-  22.2 min · step  32 · says: The final submission is now an equal-weight rank average of four models. On the same 80% of training customers, adding the fourth model raises the out-of-fold score from **0.7952** (three models) to **0.7956**. That's about +0.0004, a real but small gain. Over all training customers the three-model blend scored 0.7943. The four-model blend can't be scored on every row, because the new model finish
-  25.8 min · step  35 · says: The third XGBoost was killed again when my turn ended, so `setsid` didn't help. It takes about 1.5 minutes per fold, so I'll run its last fold in the foreground now.
-  26.8 min · step  37 · SUBMISSION 0.78646
-  26.9 min · step  37 · says: The final submission is an equal-weight rank average of four models, each now trained on all 5 folds. Its out-of-fold score over all 413,021 training customers is **0.7947**, up from 0.7943 for the three-model blend scored the same way.  | Model | Out-of-fold score (all folds) | |---|---| | XGBoost | 0.7919 | | CatBoost | 0.7914 | | XGBoost, second variant | 0.7910 | | XGBoost, third variant | 0.7
-  27.1 min · step  37 · says: With about 3 minutes left, nothing new would finish safely, so I'm only re-checking that the submission file is still valid.
-  27.2 min · step  38 · says: I've stopped here: with about 3 minutes left, no new model or fold would finish in time. The submission at `/kaggle/working/submission.csv` is the final one. It's the equal-weight rank average of four models, each trained on all 5 folds, with an out-of-fold AMEX score of **0.7947** across all 413,021 training customers.  I re-checked the file: same columns as the sample, all 45,892 customer IDs, n
