# equity · haiku · no cheatsheet

run equity__claude__claude-haiku-5-5__30min__20261120-103249; 24 steps; best 0.68158 (higher is better); final 0.68158

-   0.1 min · step   2 · says: Data is 25,920 train rows and 2,880 test rows, with censored survival targets and a per-race-group C-index metric. I'll start with an XGBoost Cox model, evaluated with 5-fold CV using the competition's stratified metric.
-   0.3 min · step   3 · says: XGBoost crashed in its CUDA backend, so I'm rerunning the same script on CPU.
-   0.5 min · step   4 · SUBMISSION 0.67147  (new best)
-   0.6 min · step   4 · says: Baseline is in place: OOF C-index 0.667 (mean minus std across race groups). XGBoost reported that `enable_categorical` was unused, so the string columns may not have been encoded. I'll switch to explicit integer codes and try two depths, keeping whichever scores higher in OOF.
-   0.9 min · step   5 · says: Integer-coded features scored 0.6681 OOF versus 0.6671 before, so I'll promote that submission. Next I'll try an XGBoost AFT model and check whether blending it with the Cox model helps.
-   1.0 min · step   6 · SUBMISSION 0.6773  (new best)
-   1.3 min · step   6 · says: The blend scores 0.669 OOF against 0.6681 for Cox alone. I'll promote it after checking the file format, then check the elapsed time before trying more.
-   1.4 min · step   7 · says: The submission validates. About 2 minutes into the 30-minute window, I'll try one more model family: CatBoost with native categorical handling and a Cox loss, blended into the current ensemble.
-   1.4 min · step   7 · SUBMISSION 0.67724
-   1.5 min · step   8 · ERROR (call took 0.0 min): Traceback (most recent call last): |   File "_catboost.pyx", line 2687, in _catboost.get_cat_factor_bytes_representation |   File "_catboost.pyx", line 2180, in _catboost.get_id_object_bytes_string_representation | _catboost.CatBoostError: bad object for i
-   1.6 min · step   8 · says: CatBoost failed on NaN values in categorical columns. I'll fill those with a `"missing"` token, then compute CatBoost OOF and blend it with the existing XGBoost Cox and AFT out-of-fold predictions, writing a candidate only if it beats the current 0.669.
-   3.7 min · step   9 · says: The CatBoost run is still going in the background, so I'll wait for it to finish rather than start a second copy.
-   4.6 min · step  11 · says: The three-model blend reaches 0.6702 OOF, above the current 0.669. The script is now fitting the final models, so I'll wait for it to write the candidate.
-   4.6 min · step  12 · ERROR (call took 0.0 min): 
-   4.7 min · step  12 · says: `pgrep` isn't available here, so that wait returned early. I'll check for the output file directly.
-   5.2 min · step  13 · says: The background job finished and wrote `sub_run4.csv`. I'll validate it against the sample format before promoting it.
-   5.3 min · step  14 · says: The three-model blend is promoted and valid at 15:38, about 7 minutes into the 30-minute window. I'll try one more variant: a shallower CatBoost with a lower learning rate, blended with the same XGBoost models.
-   5.3 min · step  14 · SUBMISSION 0.67763  (new best)
-   7.9 min · step  16 · ERROR (call took 2.5 min): Traceback (most recent call last): |     print('cb4',best,'catboost',round(score(ocb)[0],4),'cox',round(score(oc)[0],4),'aft',round(score(oa)[0],4)) | NameError: name 'best' is not defined | Fri Nov 20 15:40:46 UTC 2026
-   8.0 min · step  16 · says: The variant crashed on a bug in my sed edit: the print line refers to `best` before it's defined. I'll fix that and rerun it. There's still time in the 30-minute window.
-  12.8 min · step  17 · says: The shallower CatBoost scored lower (blend 0.6692 vs 0.6702), so the promoted submission stays. About 16 minutes remain, so I'll try the opposite direction: a deeper CatBoost (depth 8).
-  17.0 min · step  18 · says: The depth-8 CatBoost blend scores 0.6710 OOF, above the promoted 0.6702. The script's log line still says "wrote sub_run4", but the output path was changed to `sub_run6.csv`. I'll confirm the file exists and validate it before promoting.
-  17.0 min · step  19 · SUBMISSION 0.67875  (new best)
-  17.1 min · step  19 · says: The depth-8 blend is promoted. Roughly 10 minutes of the window remain, so I'll try one last variant, depth 10, and promote it only if it beats 0.6710.
-  21.9 min · step  20 · says: The depth-10 blend scores 0.6721, above the promoted 0.6710. I'll check whether its file was written, then validate and promote it.
-  22.4 min · step  21 · says: The final submission is in place at `/kaggle/working/submission.csv`. It's a three-model blend with 5-fold OOF C-index **0.672** (mean minus std across race groups). A constant prediction scores 0.5, and my first XGBoost baseline scored 0.667.  **Final model:** rank-averaged blend of - CatBoost with a Cox loss, depth 10, 800 iterations, weight 0.6 - XGBoost Cox, depth 4, weight 0.2 - XGBoost AFT (
-  22.4 min · step  21 · SUBMISSION 0.68158  (new best)
-  22.5 min · step  21 · says: About 7 minutes remain, so I'll try one more CatBoost variant (depth 12) with a hard timeout. The script promotes its output only if OOF beats 0.6721 and the file validates, and the current submission stays in place otherwise.
-  28.3 min · step  22 · says: The poll ended with no result lines, so I'll check the log and whether the job is still running.
-  28.8 min · step  23 · says: Fold 3 finished, but the job's 6-minute timeout may kill it before the final fit. The current submission is still valid either way, so I'll wait for the job to finish or time out.
-  29.9 min · step  24 · ERROR (call took 0.8 min): 
