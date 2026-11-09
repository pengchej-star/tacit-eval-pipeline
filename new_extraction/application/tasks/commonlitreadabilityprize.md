# CommonLit Readability Prize

Link: https://www.kaggle.com/competitions/commonlitreadabilityprize  (overview, data and evaluation tabs)
Metric direction: lower is better

## Official description (overview + evaluation + data)
<!-- TODO: paste the official Kaggle text here (Overview, Evaluation, Data description). -->


## Summary from our notes
CommonLit Readability Prize (Kaggle, 2021). Predict a continuous readability score (target, roughly -4 to 2, with a per-row standard_error) for 2,834 short literary/informational text excerpts. Metric RMSE, lower is better. The public leaderboard uses only ~7 rows, the private set ~2,000. Small, noisy data: solutions are fine-tuned transformers (RoBERTa/DeBERTa/ELECTRA) with careful CV, layer-wise learning rates, frequent validation during an epoch, and ensembling of seeds/folds/backbones.
