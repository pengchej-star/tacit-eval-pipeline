# American Express - Default Prediction

## Overview

Credit default prediction is central to managing risk in consumer lending. In this competition you predict
the probability that a customer does not pay back their credit card balance amount in the future, based on
their monthly customer profile. The target binary variable is calculated by observing an 18-month
performance window after the latest credit card statement: if the customer does not pay the due amount in
120 days after their latest statement date, it is considered a default event.

## Evaluation

The evaluation metric, M, is the mean of two measures of rank ordering: the Normalized Gini Coefficient, G,
and the default rate captured at 4%, D.

M = 0.5 * (G + D)

The default rate captured at 4% is the percentage of the positive labels (defaults) captured within the
highest-ranked 4% of the predictions, and represents a sensitivity/recall statistic.

For both sub-metrics G and D, the negative labels are given a weight of 20 to adjust for downsampling.

This metric has a maximum value of 1.0. Higher is better.

## Submission File

For each `customer_ID` in the test set, predict a probability for the `target` variable. The file must
contain a header and have the following format:

```
customer_ID,prediction
00000469ba478561f23a92a868bd366de6f6527a684c9a2e78fb826dcac3b9b7,0.01
00001bf2e77ff879fab36aa4fac689b9ba411dae63ae397d4263dafa1daedef5,0.22
0000210045da4f81e5f122c6bde5c2a617d03eef67f82c5e400fc98e7bd43ce8,0.98
etc.
```

## Data

The data contains aggregated profile features for each customer at each statement date. Features are
anonymized and normalized, and fall into the following general categories:

- `D_*` = Delinquency variables
- `S_*` = Spend variables
- `P_*` = Payment variables
- `B_*` = Balance variables
- `R_*` = Risk variables

with the following features being categorical:
`['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_63', 'D_64', 'D_66', 'D_68']`

Your task is to predict, for each `customer_ID`, the probability of a future payment default (`target = 1`).

Files

- `train_data.csv` - training data with multiple statement dates per `customer_ID`
- `train_labels.csv` - `target` label for each `customer_ID`
- `test_data.csv` - corresponding test data; your objective is to predict the target label for each
  `customer_ID`
- `sample_submission.csv` - a sample submission file in the correct format

Note on this version of the data: the test customers are a random 10% of the original competition's training
customers (the original competition's test labels are not public); all statements of a customer are on the
same side of the split.
