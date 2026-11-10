# Phase 3: grader smoke test

Done 2026-10-08 on a Babel CPU node, MLE-bench commit `507f92e`, env `tacit-eval`.

## Commands

```bash
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh && conda activate tacit-eval
C=/data/user_data/pengchej/mlebench-cache
for c in google-quest-challenge learning-agency-lab-automated-essay-scoring-2; do
  mlebench prepare -c $c --keep-raw --data-dir $C      # --keep-raw keeps the original Kaggle files in $C/$c/raw
  mlebench grade-sample $C/$c/prepared/public/sample_submission.csv $c --data-dir $C
done
```

Both downloads finished in seconds (gquest zip 4.9 MB, aes2 zip 11.9 MB). MLE-bench verified the zip
checksum and the checksums of all prepared files against its stored values. Disk use: gquest 16 MB, aes2 47 MB.

## Prepared layout

```
<cache>/google-quest-challenge/
  raw/       train.csv  test.csv  sample_submission.csv          # original Kaggle files
  prepared/public/   train.csv  test.csv  sample_submission.csv  description.md
  prepared/private/  test.csv                                    # answers: never expose to run code
<cache>/learning-agency-lab-automated-essay-scoring-2/
  raw/       train.csv  test.csv  sample_submission.csv
  prepared/public/   train.csv  test.csv  sample_submission.csv  description.md
  prepared/private/  answers.csv                                 # answers: never expose to run code
```

## grade-sample results

| comp | score on `sample_submission.csv` | valid | direction | MLE-bench median / bronze / gold |
|---|---:|---|---|---|
| google-quest-challenge | -0.01016 | yes | higher is better | 0.357 / 0.375 / 0.423 |
| learning-agency-lab-automated-essay-scoring-2 | 0.01323 | yes | higher is better | 0.828 / 0.835 / 0.836 |

The sample submissions are constant predictions (all 0 for gquest, all 4 for aes2), so near-zero scores are
what we expect. The point is that grading runs end to end and returns a number.

## Do the prepared files look like what the notebooks expect?

Compared `raw/*.csv` (the original Kaggle files) with `prepared/public/*.csv`:

| comp | file | Kaggle original (rows × cols) | MLE-bench public (rows × cols) | same columns, order and dtypes? |
|---|---|---|---|---|
| gquest | train.csv | 6,079 × 41 | 5,471 × 41 | yes |
| gquest | test.csv | 476 × 11 | 608 × 11 | yes |
| gquest | sample_submission.csv | 476 × 31 | 608 × 31 | yes |
| aes2 | train.csv | 17,307 × 3 | 15,576 × 3 | yes |
| aes2 | test.csv | **3** × 2 | 1,731 × 2 | yes |
| aes2 | sample_submission.csv | 3 × 2 | 1,731 × 2 | yes |

Also checked: no id appears in both public train and public test, and the ids in `sample_submission.csv`
are exactly the ids in `test.csv`.

What this means for re-running notebooks:

- **The column schemas match**, so code that reads `/kaggle/input/<slug>/{train,test,sample_submission}.csv` by
  column name should work unchanged once the paths are mapped.
- **Row counts differ.** MLE-bench holds out ~10% of Kaggle's *train* set as its test set (the real Kaggle test
  labels are not public). Code that hard-codes row counts (e.g. 476 for gquest) would break. The aes2 Kaggle
  `test.csv` only has 3 rows because it was a code competition with a hidden test set. On Kaggle the notebooks
  were re-run against ~8k hidden essays, and here they will see 1,731.
- **Train is ~10% smaller** than on Kaggle, which alone can shift scores a little. This is another reason
  Kaggle scores are not comparable to ours.
