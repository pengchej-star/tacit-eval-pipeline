# American Express - Default Prediction

Link: https://www.kaggle.com/competitions/amex-default-prediction  (overview, data and evaluation tabs)
Metric direction: higher is better

## Official description (overview + evaluation + data)
<!-- TODO: paste the official Kaggle text here (Overview, Evaluation, Data description). -->


## Summary from our notes
American Express Default Prediction (Kaggle, 2022). Predict the probability that a credit-card customer defaults, from up to 13 monthly statements per customer (~190 anonymised numeric/categorical features in groups D_ delinquency, S_ spend, P_ payment, B_ balance, R_ risk). ~459k customers in train, ~925k in test; one prediction per customer. Metric M = 0.5 * (normalised Gini + default rate captured at the top 4% of predictions), higher is better. The raw CSV is 16 GB, so most notebooks use compressed feather/parquet versions and aggregate the monthly rows per customer (last / mean / std / diff features) before GBDT.
