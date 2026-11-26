# equity · opus · cheatsheet

run equity__claude__claude-opus-5-5__memory__30min__j11280923; 17 steps; best 0.68422 (higher is better); final 0.68422

Knowledge the agent reports using (from the cheatsheet):
- T.5.2: T.5.2.3 Rank-normalize before blending (applied): C-index is ordering-based and members (Cox margins, KM-target regressions) have incompatible scales, so I rank-normalized each model's predictions before a weighted blend, choosing weights by OOF stratified C-index.

-   0.0 min · step   1 · READS CHEATSHEET: `cd /kaggle/input/equity-post-hct-survival-predictions; ls; head -c 600 sample_submission.csv; wc -l *.csv; grep -i -A5 "evaluat" description.md | head -30; ls /`
-   0.1 min · step   2 · READS CHEATSHEET: `cd /workspace/memory; grep -n "ensembl\|rank" taxonomy.md | head -20; ls cases | grep -i "t-5" | head; nvidia-smi --query-gpu=name --format=csv; head -3 /kaggle`
-   0.1 min · step   3 · READS CHEATSHEET: `cd /workspace/memory; head -c 1500 cases/t-5-2-3-rank-normalize-before-blending.md; echo; head -c 1200 attention/t-5-2-*.md | head -40`
-   1.5 min · step   5 · ERROR (call took 1.0 min): Traceback (most recent call last): |   File "/workspace/s/run.py", line 49, in <module> |     add(nm,f) |   File "/workspace/s/run.py", line 43, in add |     po,pt=fit(a,b); o[b]=po; p+=pt/5 |           ^^^^^^^^ |   File "/workspace/s/run.py", line 48, in f |     
-   1.6 min · step   5 · says: Newer pandas uses a `str` dtype, so the `== object` check missed the categorical columns. Fixing that now.
-   3.3 min · step   7 · KILL: `cd /workspace/s; pkill -f run.py; sed -i 's/return -m.predict(X.iloc\[b\]),-m.predict(Xt)/return m.predict(X.iloc[b]),m.predict(Xt)/; s/s=-1 if loss==.RMSE. els`
-   5.1 min · step   8 · says: The old process may still be running because `pkill` isn't available here. I'll find it through `/proc`.
-   5.2 min · step  10 · KILL: `kill 139; sleep 45; grep -v -i "warn\|potential\|- \|^$\|return func\|shown once" /workspace/s/log.txt`
-   6.0 min · step  10 · says: With the sign fixed, LightGBM on a KM target scores about 0.672 in 5-fold CV (stratified C-index, mean minus std). The XGBoost Cox model scores 0.668. CatBoost is still running.
-   8.2 min · step  13 · says: CatBoost on CPU is slow, and no submission file has been written yet. I'll wait for this run to finish.
-  14.0 min · step  14 · SUBMISSION 0.6842  (new best)
-  18.4 min · step  15 · SUBMISSION 0.68422  (new best)
-  18.5 min · step  15 · says: I've written `/kaggle/working/submission.csv`. It's a rank-normalized blend of six models and scores **0.6766** on the competition metric in 5-fold cross-validation on the training data. Test labels aren't available, so I have no leaderboard score. The file has the right shape (2,880 rows, ID and prediction columns) with no missing values. Higher predictions mean an event is expected sooner.  **In
-  18.6 min · step  15 · says: Bagging over more seeds is cheap here: three extra seeds each of the XGBoost Cox and XGBoost KM models, all on GPU.
-  27.4 min · step  17 · says: Seed bagging didn't improve the score, so I left the submission unchanged. Averaging three seeds moved the XGBoost models only slightly: Cox went from 0.6684 to 0.6685 and the KM-target model from 0.6747 to 0.6749. The best blend with them scored 0.67663, effectively the same as the current one, and that best blend doesn't use either seed-averaged model.  The submission is still the six-model rank
