# Changes to new_extraction (Nov 7)

Code: `extraction/new_extraction/`. Commit `cc38323` is the Nov 4 version, unchanged; the changes are in `e3347ed` and `e308801`.
Four files changed: `visits.py`, `prompts.py`, `data.py`, `config.yaml`.

```bash
git diff cc38323 e308801 -- extraction/new_extraction
```

`data/` and `out/` are not in git; copy them from your own folder.

## What changed

1. **Step 5 is masked** (`visits.py`, `prompts.py`).
   - The LLM is no longer shown the option taken (`Taken:`), the edit's own goal, labels and summary, or the episode item text.
   - Each (edit, decision node) is asked in a separate call, because listing the walk reveals the option taken at every node above.
   - The option taken is still recorded in each visit record by the program, so steps 6–8 and the export are unchanged.
   - New prompts: `VISIT_MASKED` and `NEW_CHECKS_RULE_MASKED`. The original `VISIT` is kept.
2. **Switch `visits.masked`** in `config.yaml`. The default `true` gives the masked step 5 above; `false` runs the Nov 4 step 5 unchanged (checked: all 214 RANZCR prompts are identical to the original).
   - The two modes use different cache files: `5_visits_masked_r*.jsonl` and `4b_new_checks_masked.jsonl` for masked, the original names for unmasked.
   - Use a different `--suffix` to run both side by side.
3. **Shuffled checks** (masked mode only): the checks are listed in a random order per call, so `order` / "check first" no longer just follow the list order.
4. **Optional notebook at v_old** (masked mode only).
   - Set `paths.notebooks` to TraceML's `human/` folder (`<key_id>/versions/vNNN.ipynb`), and step 5 also shows the notebook just before the edit, cut to `context.code_max` characters.
   - The default `null` turns this off. The loader is `data.notebook_text()`.
5. **Looser level-0 merge cap**: `cluster.max_dist` goes from `[0.30, 0.60]` to `[0.38, 0.60]`. In the pooled run, 35% of items had no neighbour within 0.30 and could never merge.

Nothing else changed: skeleton, clustering, merge into the skeleton, desiderata, scores, enough, returns and export follow the Nov 4 logic.

## Cost note

Masked mode makes about 4× as many calls (RANZCR: 850 per round instead of 214), but each call is shorter. Expect roughly 1.5–3× the cost of the original step 5, more with notebooks on.

## Why

See `demo/` in this repo:
- `blind_visit_pilot/`: with the answer shown vs hidden, about 32% of labels change. Hidden-answer records predict held-out experts' choices no better than the majority guess (36% vs 36%).
- `yaqing_fragmentation.md`: why the pooled clustering fragments.
