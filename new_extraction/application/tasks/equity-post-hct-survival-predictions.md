# Equity in post-HCT Survival Predictions

Link: https://www.kaggle.com/competitions/equity-post-hct-survival-predictions  (overview, data and evaluation tabs)
Metric direction: higher is better

## Official description (overview + evaluation + data)
<!-- TODO: paste the official Kaggle text here (Overview, Evaluation, Data description). -->


## Summary from our notes
CIBMTR - Equity in post-HCT Survival Predictions (Kaggle, 2024-25). Predict a risk score for survival after allogeneic hematopoietic cell transplantation from ~28.8k patients with 57 clinical/demographic features (including race_group). Targets: efs (event indicator) and efs_time. Metric: stratified concordance index = mean of the C-index within each race group minus its standard deviation across groups, higher is better, so both accuracy and equal performance across race groups matter. Typical solutions transform the survival target (Kaplan-Meier, Nelson-Aalen, Cox partial hazard) and regress it with GBDTs / NNs, then ensemble.
