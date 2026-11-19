# Compare matched checkpoint variants  `T.5.1.5`   18 edits, 0 experts
15 scored cases (improvement signed by each competition's direction), median +0.00063, 11 improved


- expert 18426209 · commonlitreadabilityprize · v7→v9   Swap the checkpoint source directory and submit to measure the effect. If the score regresses, pin the exact checkpoint file paths rather than using dynamic file discovery (glob), so that only the best-performing fold checkpoints are loaded. Compare the new LB against the previous best before commit
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Existing models share an architecture but alternative training or feature recipes yield different errors. | ✓ Removing or disabling previously validated members caused a regression. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.45658 → 0.45856 (lower is better; worse by 0.00198)
- expert 18426209 · commonlitreadabilityprize · v8→v9   Replace automatic checkpoint discovery with an explicit list of checkpoint paths. Annotate each with its known validation score. This makes the ensemble deterministic and allows selective exclusion of weak folds. Verify the effect by submitting and comparing against the previous score.
    evidence: ✓ Removing or disabling previously validated members caused a regression. | ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.45918 → 0.45856 (lower is better; improved by 0.00062)
- expert 18350823 · commonlitreadabilityprize · v3→v5   Swap checkpoint directories one at a time and submit to the leaderboard, keeping all other inference settings constant. If a checkpoint degrades the score, revert immediately. Avoid changing multiple factors (e.g., dropout settings and checkpoint source) simultaneously, as it confounds which change 
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful. | ✓ Removing or disabling previously validated members caused a regression.
    leaderboard score n/a → 0.46275 (lower is better)
- expert 18350823 · commonlitreadabilityprize · v14→v15   Swap only the checkpoint path for that one component, keep everything else fixed, and also write out the single-component predictions to a separate file. Submit the full ensemble to measure the marginal effect of the checkpoint change. This isolates the checkpoint quality from other blend-weight or 
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.46250 → 0.46161 (lower is better; improved by 0.00088)
- expert 17371717 · commonlitreadabilityprize · v23→v24   Swap in each candidate checkpoint one at a time and submit to the leaderboard (or evaluate on a reliable local validation set). Keep the checkpoint that scores best. Expect that different seeds can shift the score noticeably even with the same architecture and training recipe, so this probe is worth
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.46690 → 0.46940 (lower is better; worse by 0.00250)
- expert 73937748 · equity · v63→v64   Point the inference code at the new checkpoints so their predictions replace the old ones in the stack, and double the number of optimizer trials for the meta-learner. Expect only marginal gains; verify on the leaderboard before committing to the change.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.69305 → 0.69312 (higher is better; improved by 0.00007)
- expert 7018718 · google · v4→v8   Sweep checkpoints one at a time by changing only the checkpoint path, submitting each to the leaderboard. Keep the one that scores best. This is cheap when inference is fast relative to training and the number of candidates is small.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.37851 → 0.38615 (higher is better; improved by 0.00765)
- expert 7018718 · google · v18→v20   Swap the checkpoint path, re-run inference locally, and inspect validation outputs or prediction distributions before spending a leaderboard submission. If the local signals are not clearly better than the current best, skip submission and try another checkpoint or approach.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.38508 → n/a (higher is better)
- expert 7018718 · google · v26→v27   Systematically swap checkpoints while keeping the rest of the inference pipeline constant. Expect meaningful variance across runs; do not abandon a pipeline change based on a single checkpoint's poor result. The score difference between checkpoints of the same setup can exceed the difference between
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.37970 → 0.38820 (higher is better; improved by 0.00850)
- expert 7573212 · google · v10→v13   Hold all code constant and vary only which checkpoint files are loaded. Test individual checkpoints first to gauge their standalone quality, then try averaging predictions from multiple checkpoints. Use leaderboard scores to guide selection, keeping iterations minimal.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.39027 → 0.39071 (higher is better; improved by 0.00044)
- expert 6803050 · google · v39→v49   Sweep checkpoint variants one at a time across all folds, then vary ensemble size (full k-fold vs. subsets). Submit each configuration to measure its effect. Track that more folds do not always help—if some folds are weaker, including them dilutes the ensemble. Keep the configuration that scores bes
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful. | ✓ Existing models share an architecture but alternative training or feature recipes yield different errors. | ✓ Some available members may add noise or redundancy despite acceptable standalone scores. | ✓ Removing or disabling previously validated members caused a regression. | ✗ A candidate improves standalone score but adds no gain in prior fixed-weight inclusion tests.
    leaderboard score 0.38287 → 0.36824 (higher is better; worse by 0.01463)
- expert 7606235 · google · v8→v15   Submit each fold checkpoint individually and record the test/leaderboard score. Expect meaningful variance across folds (here ~0.005 spread on a correlation metric). Select the best-performing single fold before attempting ensembles, as not all folds contribute equally.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score n/a → 0.38524 (higher is better)
- expert 55621328 · learning · v36→v37   Change both levers at once: switch to a different trained checkpoint and simultaneously re-tune the rounding thresholds. If the combined change improves the score, follow up by isolating each lever to understand individual contributions. This is efficient when submission budget is limited and the tw
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.81031 → 0.81536 (higher is better; improved by 0.00505)
- expert 55621328 · learning · v37→v45   First sweep individual checkpoints one at a time to identify the strongest single variant. Then expand the ensemble by adding all folds of that variant. Finally, add checkpoints from different random seeds of the same variant. At each step, submit and keep the change only if the metric improves; rev
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Existing models share an architecture but alternative training or feature recipes yield different errors. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful. | ✓ A candidate improves standalone score but adds no gain in prior fixed-weight inclusion tests.
    leaderboard score 0.81536 → 0.81599 (higher is better; improved by 0.00063)
- expert 55621328 · learning · v46→v47   Swap in last-epoch snapshots while keeping everything else fixed. If the score drops, prefer best-validation checkpoints; the gap indicates how much the model overfits in later epochs and whether early stopping is essential for this task.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.81880 → 0.81727 (higher is better; worse by 0.00153)
- expert 55621328 · learning · v103→v104   Try both checkpoint variants in the inference ensemble and compare scores. Final-epoch checkpoints can sometimes generalize better when the validation set distribution differs from the test set, so do not assume early stopping is always superior.
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.82467 → 0.82726 (higher is better; improved by 0.00259)
- expert 55621328 · learning · v108→v109   Swap one factor at a time (checkpoint set, blend weights, batch size) and submit. Track each combination's score against the running best. When a new variant scores close to but below the best, note it as a viable ensemble candidate rather than discarding it, since it may complement other models in 
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.81837 → 0.82798 (higher is better; improved by 0.00961)
- expert 15082684 · ranzcr · v24→v29   Sweep checkpoints one at a time, prioritizing those with the highest local validation scores. Submit each to verify leaderboard alignment. When two checkpoints from different runs share the same validation score and produce nearly identical leaderboard scores, treat local CV as a reliable proxy and 
    evidence: ✓ Several compatible trained checkpoints differ in seed, recipe or training stage. | ✓ Fold quality or training-regime mismatch may make some available checkpoints harmful.
    leaderboard score 0.96249 → 0.96901 (higher is better; improved by 0.00652)