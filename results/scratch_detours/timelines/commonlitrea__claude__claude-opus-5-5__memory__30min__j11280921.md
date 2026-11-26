# commonlit · opus · cheatsheet

run commonlitrea__claude__claude-opus-5-5__memory__30min__j11280921; 26 steps; best 0.51995 (lower is better); final 0.52353

Knowledge the agent reports using (from the cheatsheet):
- T.5.2: T.5.2.1 Increase backbone capacity (applied): Read backbone attention file; chose large pretrained transformer (deberta-v3-large) over TF-IDF ridge baseline given small text regression dataset; validated by fold-0 RMSE 0.536 vs 0.783
- T.6.2.2: T.6.2.2.2 Tune blend coefficients (not applied): Grid-searched OOF blend weight between deberta-v3-large and roberta-large (0.5/0.5, OOF 0.501); superseded by equal weights in final 3-model blend
- T.6.1: T.6.1.1 Add a complementary ensemble member (applied): Added electra-large as third 5-fold member; equal weights chosen over NNLS (0.4976 vs 0.4972, negligible gain); then added deberta-v3-base as 4th member, equal 4-way average OOF used if better

-   0.0 min · step   1 · READS CHEATSHEET: `cd /kaggle/input/commonlitreadabilityprize; ls; wc -l *.csv; head -c 600 sample_submission.csv; nvidia-smi --query-gpu=name,memory.total --format=csv; ls /works`
-   0.1 min · step   2 · READS CHEATSHEET: `cd /workspace/memory; sed -n 68,200p taxonomy.md | grep -n "T\.[0-9]" | head -60; ls cases | grep -i -E "fine|pretrain|backbone" ; head -3 /kaggle/input/commonl`
-   0.1 min · step   3 · READS CHEATSHEET: `cd /workspace/memory; head -40 attention/t-4-1-*.md 2>/dev/null | head -40; ls attention | head -50`
-   0.1 min · step   4 · READS CHEATSHEET: `cd /workspace/memory; head -30 attention/t-5-2-choose-backbone-scale-or-family.md; ls cases | grep t-5-2; python -c "import transformers;print(transformers.__ve`
-   0.2 min · step   4 · ERROR (call took 0.0 min): 
-   0.9 min · step   6 · SUBMISSION 0.74889  (new best)
-   1.0 min · step   6 · says: Baseline TF-IDF ridge saved (CV RMSE 0.783). Now fine-tuning deberta-v3-large, 5-fold, with frequent evaluation.
-   2.9 min · step   9 · says: Fold 0 never beat 9, so the predictions are probably NaN. Stopping the run to debug.
-   2.9 min · step  10 · KILL: `pkill -f ft.py; cd /workspace; grep -v -E "Loading|UNEXP|^\||Key|---" dl.log | tail -20`
-   3.2 min · step  11 · says: The model loads in fp16 weights by default, which breaks AdamW. I'll force float32.
-   3.2 min · step  12 · KILL: `cd /workspace; for p in /proc/[0-9]*; do grep -q "ft.py" $p/cmdline 2>/dev/null && kill ${p#/proc/}; done; sed -i 's/s.b=AutoModel.from_pretrained(MN)/s.b=AutoM`
-   6.7 min · step  13 · says: The stale fp16 process (265) was still running alongside the new run. Killing it.
-   6.7 min · step  14 · KILL: `kill 265; sleep 2; nvidia-smi --query-compute-apps=pid --format=csv; ls /workspace/out`
-   6.8 min · step  14 · says: Fold 0 RMSE is 0.536, against 0.783 for the ridge baseline. Each fold takes about 3 minutes, so all 5 should finish around 02:08. Next I'm writing the combine script and knowledge_used.json.
-   6.9 min · step  15 · SUBMISSION 0.54866  (new best)
-  11.3 min · step  16 · SUBMISSION 0.52811  (new best)
-  12.8 min · step  17 · says: DeBERTa-v3-large's 5-fold mean RMSE is about 0.533, and that ensemble is now the submission. A roberta-large run started for blending and should finish around 02:09.
-  12.8 min · step  17 · SUBMISSION 0.53314
-  17.3 min · step  19 · SUBMISSION 0.51995  (new best)
-  17.4 min · step  19 · says: The blend comes out at 0.501 OOF RMSE with weights 0.5/0.5, and it's saved as the submission. About 8 minutes remain, so I'm adding electra-large as a third member.
-  21.9 min · step  21 · SUBMISSION 0.52134
-  22.0 min · step  22 · says: A smaller backbone trains fast, so I'm using the last few minutes on deberta-v3-base as a possible fourth member.
-  25.6 min · step  24 · SUBMISSION 0.52353
-  25.7 min · step  24 · says: The final submission is an equal-weight average of four fine-tuned transformers, and it scores RMSE 0.493 on out-of-fold predictions. A TF-IDF + ridge baseline scored 0.783. It's saved at `/kaggle/working/submission.csv` with 284 rows plus the header, matching the sample submission.  Each model was trained 5-fold, with folds split evenly across target ranges. Out-of-fold RMSE per model:  | Model |
-  25.8 min · step  24 · says: With about 4 minutes left, I'll check whether the TF-IDF ridge model adds anything to the blend.
-  26.0 min · step  25 · says: I tried adding the TF-IDF + ridge model to the blend in the last few minutes, and it didn't help. At every weight I tested (2–15%), the score was no better than without it, so I left the submission as it was.  The final submission is still the equal-weight average of the four fine-tuned transformers: deberta-v3-large, roberta-large, electra-large and deberta-v3-base. It scores RMSE 0.493 on out-of
-  26.1 min · step  25 · says: A deberta-v3-base run takes about 3.5 minutes, which just fits. I'll train a second one with a different learning rate (2e-5) and blend it in only if the out-of-fold score improves.
-  29.5 min · step  26 · says: The second deberta-v3-base run (learning rate 2e-5) didn't help. On its own it scored 0.534 RMSE out-of-fold. Adding it to the blend gave 0.4937, slightly worse than the four-model blend's 0.4934, so I left the submission unchanged.  The final submission is still the equal-weight average of deberta-v3-large, roberta-large, electra-large and deberta-v3-base. It scores RMSE 0.493 on out-of-fold pred
