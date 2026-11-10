# CommonLit Readability Prize

## Overview

Can machine learning identify the appropriate reading level of a passage of text, and help inspire learning?
CommonLit, a nonprofit education technology organization, wants to help teachers and students find reading
passages of appropriate difficulty for grades 3-12 classroom use. Current readability formulas (e.g.
Flesch-Kincaid) lack construct and theoretical validity. In this competition you build algorithms that rate
the complexity of literary excerpts.

## Evaluation

Submissions are scored on the root mean squared error (RMSE) between the predicted and the true `target`:

RMSE = sqrt( (1/n) * sum_i (y_i - y_hat_i)^2 )

Lower is better.

## Submission File

For each `id` in the test set, predict a value for `target`. The file must contain a header and have the
following format:

```
id,target
eaf8e7355,0.0
60ecc9777,0.5
c0f722661,-2.0
etc.
```

## Data

- `train.csv` - the training set
- `test.csv` - the test set
- `sample_submission.csv` - a sample submission file in the correct format

Columns

- `id` - unique ID for the excerpt
- `url_legal` - URL of source (blank in many rows)
- `license` - license of source material (blank in many rows)
- `excerpt` - text to predict reading ease of
- `target` - reading ease (higher means easier to read)
- `standard_error` - measure of spread of scores among multiple raters for each excerpt (train only)

Note on this version of the data: the test set is a random 10% of the original competition's training data
(the original competition's test set is not public), and `train.csv` holds the remaining 90%.
