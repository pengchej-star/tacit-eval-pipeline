# Process complete entities in chunks  `T.7.2`   5 edits, 0 experts

- expert 27389424 (Grandmaster) · amex · v5→v6   Split the test set into chunks by sample ID, run all ensemble members on each chunk, average within the chunk, and concatenate the averaged results. This keeps peak memory proportional to chunk size rather than full test size times number of models.
    evidence: ✓ The full dataset or feature matrix exceeds available memory.
    leaderboard score n/a → n/a
- expert 27502740 (Grandmaster) · amex · v1→v2   Pre-partition the test data into multiple files. At inference time, loop over each partition: load it, run the model, store only the predictions (a small array), then delete the loaded data and force garbage collection before loading the next partition. Concatenate all partial predictions at the end
    evidence: ✓ The full dataset or feature matrix exceeds available memory.
    leaderboard score n/a → 0.79421
- expert 27799930 (Contributor) · amex · v20→v23   Partition the test data into chunks by entity ID boundaries, read only the required columns for each chunk, run the full feature-engineering and prediction pipeline per chunk, free memory explicitly between chunks, and concatenate the per-chunk predictions at the end. Increase the number of chunks i
    evidence: ✓ The full dataset or feature matrix exceeds available memory. | ✓ Peak memory rises across successive model or feature stages.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v11→v12   Split customers into train/holdout by ID before training. Serialize fitted preprocessing objects and each fold's trained model to disk. After training, delete training data from memory and force garbage collection. Load only the holdout partition, apply the saved preprocessors, run inference with ea
    evidence: ✓ The full dataset or feature matrix exceeds available memory. | ✓ Peak memory rises across successive model or feature stages. | ✓ Most run time recomputes artifacts unchanged by the current experiment.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v19→v24   Split the test set into chunks by unique entity IDs. Run feature engineering inside the per-chunk loop rather than on the full dataset. After predicting each chunk, explicitly delete intermediate objects and force garbage collection. Collect lightweight prediction DataFrames per chunk and concatenat
    evidence: ✓ The full dataset or feature matrix exceeds available memory. | ✓ Peak memory rises across successive model or feature stages. | ✓ Most run time recomputes artifacts unchanged by the current experiment.
    leaderboard score n/a → n/a