# Stream data and release model memory  `T.1.2.1`   35 edits, 0 experts
12 scored cases, median improvement +0.00000, 4 improved


- expert 27389424 (Grandmaster) · amex · v5→v6   Split the test set into chunks by sample ID, run all ensemble members on each chunk, average within the chunk, and concatenate the averaged results. This keeps peak memory proportional to chunk size rather than full test size times number of models.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → n/a
- expert 27836972 (Expert) · amex · v64→v67   Convert the entire dataframe to CPU once before the loop rather than per group. Within each group, precompute the minimal slice needed (e.g., last N rows) and apply the transformation once, then extract per-column values from the precomputed result instead of recomputing per column.
    evidence: ✓ Repeated trials recompute identical upstream features or predictions. | ✗ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✗ A final artifact is being generated with development-only fold or sample limits still enabled.
    leaderboard score n/a → 0.79497
- expert 27502740 (Grandmaster) · amex · v1→v2   Pre-partition the test data into multiple files. At inference time, loop over each partition: load it, run the model, store only the predictions (a small array), then delete the loaded data and force garbage collection before loading the next partition. Concatenate all partial predictions at the end
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → 0.79421
- expert 27502740 (Grandmaster) · amex · v5→v6   Before training, upcast low-precision float columns to a higher-precision type, round to a fixed number of decimal places that preserves meaningful variation, then cast back. Apply identically to train and test. Verify on the leaderboard that the rounding level chosen does not discard useful signal.
    evidence: ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score 0.79418 → 0.79501 (+0.00083)
- expert 27799930 (Contributor) · amex · v20→v23   Partition the test data into chunks by entity ID boundaries, read only the required columns for each chunk, run the full feature-engineering and prediction pipeline per chunk, free memory explicitly between chunks, and concatenate the per-chunk predictions at the end. Increase the number of chunks i
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✗ The current trial needs pipeline feedback before a full fold and estimator budget is justified. | ✓ A final artifact is being generated with development-only fold or sample limits still enabled.
    leaderboard score n/a → n/a
- expert 27799930 (Contributor) · amex · v39→v44   Downcast every column to the smallest dtype that fits its range (e.g., 64-bit floats to 32-bit, counts to 8-bit integers). Delete every intermediate DataFrame immediately after it is merged or consumed, and call the garbage collector explicitly. In the CV loop, index into the master DataFrame with .
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → n/a
- expert 27799930 (Contributor) · amex · v46→v50   Split the aggregation into multiple smaller groupby calls, merge results incrementally, delete each intermediate after merging, and force garbage collection. Additionally, downcast resulting columns to the smallest sufficient dtype (e.g., small integers for counts) to reduce the final footprint.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v11→v12   Split customers into train/holdout by ID before training. Serialize fitted preprocessing objects and each fold's trained model to disk. After training, delete training data from memory and force garbage collection. Load only the holdout partition, apply the saved preprocessors, run inference with ea
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Repeated trials recompute identical upstream features or predictions.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v19→v24   Split the test set into chunks by unique entity IDs. Run feature engineering inside the per-chunk loop rather than on the full dataset. After predicting each chunk, explicitly delete intermediate objects and force garbage collection. Collect lightweight prediction DataFrames per chunk and concatenat
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ A final artifact is being generated with development-only fold or sample limits still enabled. | ✓ Repeated trials recompute identical upstream features or predictions.
    leaderboard score n/a → n/a
- expert 75924487 (Master) · equity · v5→v6   After each model finishes inference, explicitly delete its objects and invoke garbage collection before loading the next model. Apply this pattern inside any loop that iterates over model variants.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → 0.69331
- expert 73937748 (Master) · equity · v35→v36   Loop over model variants one at a time: load the artifact, generate and store only the lightweight prediction arrays, then explicitly delete the model object and trigger garbage collection before proceeding to the next variant.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → 0.69026
- expert 7548275 (Expert) · google · v6→v9   Decouple feature extraction from prediction: precompute embeddings offline, save them, then at inference time load only the embeddings and run multiple lighter models (e.g., a recurrent model, a shallow neural network, the original model) sequentially with explicit memory cleanup between them. This 
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✓ Repeated trials recompute identical upstream features or predictions. | ✓ A final artifact is being generated with development-only fold or sample limits still enabled.
    leaderboard score n/a → n/a
- expert 7613444 (Contributor) · google · v7→v11   Train folds incrementally across separate runs by gating the CV loop to execute only untrained fold indices, saving model weights after each fold. In a final inference-only run, load all saved fold checkpoints, generate predictions from each, and average them. This decouples training cost from ensem
    evidence: ✓ A final artifact is being generated with development-only fold or sample limits still enabled. | ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Repeated trials recompute identical upstream features or predictions. | ✗ The current trial needs pipeline feedback before a full fold and estimator budget is justified.
    leaderboard score n/a → 0.39956
- expert 7613444 (Contributor) · google · v12→v14   Use a fold-index conditional inside the CV loop to skip already-completed folds and train only the remaining ones each session. Save each fold's weights to persistent storage. Across successive runs, widen the conditional to cover additional folds until all are trained, then switch to inference mode
    evidence: ✓ A final artifact is being generated with development-only fold or sample limits still enabled. | ✓ Repeated trials recompute identical upstream features or predictions.
    leaderboard score 0.40047 → n/a
- expert 7670859 (Contributor) · google · v16→v17   Halve the inference batch size from the previous setting and re-run. If it still fails, halve again. Choose the largest power-of-two batch size that completes without memory errors to balance throughput and stability.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → n/a
- expert 7670859 (Contributor) · google · v20→v23   After each model's embedding extraction, explicitly delete all large intermediate arrays, invoke the framework's session/cache clearing functions, and call the garbage collector before loading the next model. Keep only the final condensed feature arrays needed downstream.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Repeated trials recompute identical upstream features or predictions. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score 0.39130 → n/a
- expert 50376011 (Grandmaster) · hms · v72→v77   Change only one variable per submission so regressions can be attributed. When a regression appears after toggling an infrastructure/init call, check whether it silently overrides inference parameters such as batch size, precision mode, or data-loading settings. Disable the call, verify the paramete
    evidence: ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✓ The current trial needs pipeline feedback before a full fold and estimator budget is justified.
    leaderboard score 0.33319 → 0.36160 (+0.02841)
- expert 50376011 (Grandmaster) · hms · v77→v79   Change only one variable at a time when possible. If a large batch size degrades the score, revert to the smaller default; large batches can cause silent OOM issues or numerical differences that hurt predictions, especially on limited GPU memory.
    evidence: ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.36160 → 0.33044 (-0.03116)
- expert 50376011 (Grandmaster) · hms · v210→v211   Test inference with mixed precision disabled (full FP32). If the score worsens or stays the same, keep mixed precision for its speed benefit. In this case the score got worse, indicating that the precision difference was not the bottleneck and the run-to-run variance or other factors dominated.
    evidence: none recorded
    leaderboard score 0.25194 → 0.25970 (+0.00776)
- expert 50376011 (Grandmaster) · hms · v221→v222   When expanding the number of ensemble members, proportionally reduce the inference batch size to keep peak memory within budget. Process one model at a time, accumulate predictions, and average at the end.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.24562 → 0.23868 (-0.00694)
- expert 55621328 (Master) · learning · v76→v78   Sort or bucket the inference dataset by token length so each batch contains sequences of similar length, minimizing padding. After inference, re-map predictions to the original sample identifiers to avoid alignment errors.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.82461 → 0.82461 (+0.00000)
- expert 55621328 (Master) · learning · v105→v106   Test mixed-precision inference in isolation (without changing other variables like blend weights). If the metric drops even slightly, revert to full precision for the final submission, because regression outputs near rounding boundaries are sensitive to small numerical perturbations from lower preci
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.82994 → 0.82916 (-0.00078)
- expert 55431616 (Grandmaster) · learning · v27→v28   Enumerate checkpoints explicitly rather than using file-system glob patterns. Initialize the tokenizer and preprocess data inside each checkpoint's inference loop to guarantee compatibility. Free model memory (garbage collection, cache clearing) between checkpoints. Average the per-checkpoint output
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score n/a → n/a
- expert 58130512 (Master) · learning · v45→v48   Avoid explicit `del` on model/trainer objects that may be referenced elsewhere. Instead, let them go out of scope naturally and call the GPU cache-clearing function plus the language-level garbage collector. Verify by running the full pipeline end-to-end; if OOM persists, isolate extraction in a sub
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✓ A final artifact is being generated with development-only fold or sample limits still enabled.
    leaderboard score n/a → n/a
- expert 58130512 (Master) · learning · v48→v49   Append each trained model to a collection (list), immediately delete the original named variable, and force garbage collection. Pass the collection to the downstream consumer rather than individual references.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✗ A final artifact is being generated with development-only fold or sample limits still enabled.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v8→v9   Before training the tree model, explicitly clear the deep-learning framework session and force garbage collection. Pin the tree model to CPU to avoid GPU memory contention. This isolates the training environment and provides a stable baseline for further tuning.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → 0.81798
- expert 55987255 (Master) · learning · v41→v46   Start with several candidate models, then prune to the smallest set that fits within resource limits. Reduce topic-model dimensionality proportionally. When changing dimensionality parameters, ensure all downstream references (column name lists, feature selection lists) are updated consistently to a
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v65→v75   Apply a column-type downcasting utility to each intermediate DataFrame immediately after creation. Explicitly delete large intermediates and call garbage collection after each merge step. Cast the final training matrix to a reduced-precision float type. If memory is still tight, reduce the number of
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score n/a → n/a
- expert 15372370 (Expert) · ranzcr · v3→v4   Reduce the batch size to fit within memory constraints and verify that the metric is unchanged. This is safe whenever the model's forward pass does not depend on batch statistics at inference time.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.96342 → 0.96341 (-0.00001)
- expert 15164527 (Expert) · ranzcr · v2→v4   Explicitly delete each model object (and call garbage collection / cache clearing) immediately after its inference is complete, before loading the next model. If OOM still occurs, reduce the inference batch size by half and retry.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score n/a → 0.96642
- expert 15164527 (Expert) · ranzcr · v5→v6   After each model finishes inference, explicitly delete the model object and its intermediate tensors, then call the runtime's garbage collector and GPU cache-clearing function before loading the next model. This prevents accumulated allocations from causing out-of-memory errors.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.96679 → 0.96755 (+0.00076)
- expert 15173072 (Contributor) · ranzcr · v13→v14   Increase the inference batch size as much as GPU memory allows for speed. Expect identical predictions and scores, since eval-mode batch norm and deterministic forward passes are independent of batch size.
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.96062 → 0.96062 (+0.00000)
- expert 50496431 (Grandmaster) · hms · v62→v68   Start with a conservatively small batch size (e.g., one-eighth of the default) for the new model. Only increase after verifying that checkpoint loading is strict (no missing/unexpected keys) and that model configuration parameters exactly match the trained checkpoint. A sudden catastrophic score is 
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist. | ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors. | ✓ The current trial needs pipeline feedback before a full fold and estimator budget is justified.
    leaderboard score n/a → 0.30784
- expert 50496431 (Grandmaster) · hms · v102→v104   Implement flip TTA inside the model's forward pass by concatenating original and flipped inputs along the batch dimension, running one forward pass, then averaging paired outputs. Halve the dataloader batch size to keep total GPU memory roughly constant. Evaluate the upgraded member both in isolatio
    evidence: ✓ Peak memory is reached while several models or intermediate matrices coexist.
    leaderboard score 0.28002 → 0.27115 (-0.00887)
- expert 50496431 (Grandmaster) · hms · v213→v214   Ensure inference DataLoaders use the same batch size as configured/expected. When debugging a score regression caused by multiple simultaneous changes, isolate infrastructure settings (batch size, data loading) as a separate variable—they can have outsized, non-obvious effects on predictions.
    evidence: ✓ Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
    leaderboard score 0.26971 → 0.22478 (-0.04493)