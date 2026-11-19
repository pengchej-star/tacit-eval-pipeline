# evidence/registry.md — one definition per check, shared across nodes

E01  The pipeline crashes, produces invalid outputs, or regressed sharply after integration.
     how: Inspect the latest traceback, prediction shapes and ranges, and score history.
     used at: T
E02  Recent score movements cannot be attributed confidently to a specific change.
     how: Inspect version diffs, repeated-run scores, validation design, and whether a complete baseline exists.
     used at: T
E03  Error analysis or ablation history points to missing signal or a mismatch in supplied inputs.
     how: Inspect raw samples, input transformations, subgroup errors, and prior feature or data ablations.
     used at: T
E04  The current single-model quality has plateaued and alternative compatible predictors exist.
     how: Inspect standalone validation results, current architecture, and available trained checkpoints.
     used at: T
E05  A trainable model has a measurable optimization or generalization limitation.
     how: Read learning curves, objective definitions, fitting configuration, and validation errors.
     used at: T
E06  Multiple valid prediction sources exist and their combination may improve held-out errors.
     how: Inspect aligned per-model predictions, standalone scores, error correlations, and the active blend.
     used at: T
E07  Valid continuous predictions do not match the target scale or required output form.
     how: Inspect target values, predicted distributions, subgroup residuals, and the scoring definition.
     used at: T
E08  Resource limits or fragile repeated execution block reliable model comparisons.
     how: Inspect runtime profiles, memory peaks, failures, and repeated code edits.
     used at: T
E09  Sample identifiers or feature columns differ between prediction sources or stages.
     how: Compare ordered identifiers, join cardinalities, feature names, and matrix shapes at each handoff.
     used at: T.1
E10  A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
     how: Compare the checkpoint metadata and saved configuration with the instantiated model, tokenizer vocabulary, and load report.
     used at: T.1
E11  The executed ensemble does not match its configured members or weights.
     how: Trace member identifiers and accumulation counts and recompute the blend of a few saved rows by hand.
     used at: T.1
E12  Written predictions have the wrong direction, range, normalization, or source variable.
     how: Compare the metric definition and submission schema with raw logits, activated outputs, and the actual saved file.
     used at: T.1
E13  Execution stops at an import, file access, device operation, or library call.
     how: Read the first traceback and inspect the relevant installed package, artifact path, argument types, and tensor devices.
     used at: T.1
E14  Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
     how: Trace flags and stage outputs on a few identified samples and compare intermediate prediction hashes and provenance.
     used at: T.1
E15  The first failing operation cannot import a module or locate a required file.
     how: Read the traceback and compare mounted files, import paths, and installed versions with the configured dependencies.
     used at: T.1.5
E16  The failing call mixes devices or requests unavailable acceleration.
     how: Inspect device attributes, accelerator availability, and the exact error at the failed model call.
     used at: T.1.5
E17  The failing call uses an unsupported method, argument, or type.
     how: Compare the failing call and runtime object types with the locally available function signature and expected return structure.
     used at: T.1.5
E18  Multiple edits, noisy scores, or a regression obscure the effect of the latest experiment.
     how: Review edit history alongside scores and available saved configurations.
     used at: T.2
E19  Local model rankings are unreliable or the split ignores known sampling structure.
     how: Inspect fold membership, sample identifiers, target histograms, and train-versus-test population information.
     used at: T.2
E20  Training selects models using a surrogate metric or incorrectly configured callback.
     how: Compare callback calculations, prediction shapes, maximize/minimize flags, and monitored datasets against the task metric definition.
     used at: T.2
E21  The raw dataset structure and prediction unit have not been established.
     how: Compare the schema, sample rows, identifier counts, and task output requirements with existing exploratory summaries.
     used at: T.2
E22  Several factors changed in the same scored run.
     how: Compare the two run configurations and count independently changed settings, features, and members.
     used at: T.2.1
E23  Observed gains are comparable to prior run-to-run variation or the evaluation set is very small.
     how: Read unchanged-run scores, sample counts, seed settings, and artifact timestamps; compare the spread with the claimed gain.
     used at: T.2.1
E24  A recent change caused a large regression and a verified earlier configuration is recoverable.
     how: Compare the regression with historical variation and locate the earlier code, weights, feature list, and preprocessing settings.
     used at: T.2.1
E25  Repeated nearby settings fail to improve beyond the measured noise level.
     how: Inspect the search log for improvement size and direction across successive neighboring trials.
     used at: T.2.1
E26  No complete and scored end-to-end baseline exists.
     how: Check whether one run has produced aligned predictions, the intended metric, and a valid saved submission.
     used at: T.2.1
E27  One scalar control remains uncertain and earlier trials show a directional response.
     how: Inspect the logged parameter values and corresponding validation scores for a bracket around a local optimum.
     used at: T.2.1
E28  Existing checkpoint results show uncertain agreement between validation and external evaluation.
     how: Tabulate paired validation and external scores by checkpoint with preprocessing held fixed and inspect rank agreement.
     used at: T.2.1
E29  The current baseline is far behind existing evidence and several coupled improvements form a compatible replacement.
     how: Compare the current baseline score and design with available trajectory evidence and verify that the replacement components share compatible inputs and outputs.
     used at: T.2.1
E30  Samples share entities, topics, overlapping windows, or other dependence groups.
     how: Count repeated group identifiers and check group overlap between existing training and validation folds.
     used at: T.2.2
E31  Fold target distributions differ despite otherwise exchangeable sampling units.
     how: Compare per-fold label histograms, minority counts, and target quantiles and verify no required grouping is broken.
     used at: T.2.2
E32  An identifiable training subgroup differs from the expected test population.
     how: Compare source or prompt labels and their feature and target distributions with the task description and available test metadata.
     used at: T.2.2
E33  Current folds leave too little fitting data or unstable validation and out-of-fold coverage.
     how: Inspect train and validation counts per fold, coverage of out-of-fold predictions, and fold-score variance.
     used at: T.2.2
E34  Related observations cross current train and validation boundaries.
     how: Intersect entity or group identifiers across each split and inspect overlapping source windows.
     used at: T.2.2
E35  The training examples have imbalance, questionable labels, or incomplete coverage.
     how: Inspect class counts, source groups, duplicate identifiers, annotation confidence, and available auxiliary data.
     used at: T.3
E36  The current feature set omits identifiable temporal, semantic, or domain information.
     how: Compare raw fields with the feature schema and inspect residual errors by available signal.
     used at: T.3
E37  New features increased dimensionality or earlier ablations suggest some features hurt.
     how: Inspect feature counts, importance estimates, cached selection lists, and prior removal results.
     used at: T.3
E38  Current transformations may discard useful information or differ from checkpoint training.
     how: Compare raw inputs and inference transformations with the training configuration.
     used at: T.3
E39  Low-confidence labels, duplicates, or a mismatched source subset can be identified.
     how: Inspect annotation agreement, duplicate groups, source labels, and errors by quality stratum.
     used at: T.3.1
E40  Rare classes or relevant subgroups contribute too little to the current objective.
     how: Compare sample counts, per-group errors, metric weighting, and current loss weights.
     used at: T.3.1
E41  The training set is small or imbalanced and plausible label-preserving transformations exist.
     how: Inspect class coverage and sample examples under the proposed transform and check the task invariances.
     used at: T.3.1
E42  Additional labeled data cover relevant cases with compatible targets.
     how: Compare source schemas, label definitions, quality indicators, and overlap with existing training samples.
     used at: T.3.1
E43  Unlabeled in-domain data and a sufficiently reliable teacher are available.
     how: Inspect teacher validation accuracy, pseudo-label confidence and coverage, and earlier supervised versus pseudo-labeled results.
     used at: T.3.1
E44  A minority subgroup matches the expected test population and is currently underrepresented.
     how: Compare source-group membership, input distributions, and known test metadata.
     used at: T.3.1
E45  A prior augmentation trial degraded validation without improving minority-group errors.
     how: Inspect controlled augmented versus unaugmented validation and per-group residuals.
     used at: T.3.1
E46  Multiple observations describe each prediction entity but only a narrow summary is used.
     how: Inspect records per entity, timestamps, current aggregation functions, and missing-value patterns.
     used at: T.3.2
E47  Existing aggregates discard ordering or relationships among related fields.
     how: Inspect ordered histories, related feature groups, and the current derived-feature list.
     used at: T.3.2
E48  Text structure or metadata relevant to the target is absent from current representations.
     how: Inspect raw documents and metadata alongside existing feature families and errors by length or structure.
     used at: T.3.2
E49  Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner.
     how: Inspect vocabulary size, document frequencies, n-gram coverage, and decomposition convergence logs.
     used at: T.3.2
E50  Available pretrained representations encode information missing from the current tabular features.
     how: Inspect available encoder outputs, out-of-fold provenance, feature dimensionality, and prior feature-source ablations.
     used at: T.3.2
E51  Available signal channels or temporal resolutions are not represented by the current inputs.
     how: Inspect channel mappings, signal windows, existing transforms, and trained branch input requirements.
     used at: T.3.2
E52  Several trained input branches exist and one may add little or harmful information.
     how: Inspect existing modality ablations and check that branch toggles have compatible model configurations.
     used at: T.3.2
E53  All model-derived training features were produced by models that saw their own target rows.
     how: Match base-model training identifiers against identifiers of each stored prediction row.
     used at: T.3.2
E54  A ranked feature list exists but its cutoff has not been validated for the current pipeline.
     how: Inspect importance stability across folds and previous cutoff-versus-score results.
     used at: T.3.3
E55  A named feature group is redundant, noisy, or was removed before a regression.
     how: Inspect group-level ablation results, missingness, correlations, and the version in which the group changed.
     used at: T.3.3
E56  A cached selection list predates new features or refers to absent columns.
     how: Compare the stored feature-list names and provenance with the current generated schema and fold definitions.
     used at: T.3.3
E57  The only feature importance ranking was computed on data used to evaluate the selected model.
     how: Trace fold membership in feature selection and downstream validation.
     used at: T.3.3
E58  Inference transforms differ from those used to train the loaded checkpoint.
     how: Diff saved training and inference transform configurations and compare transformed versions of the same example.
     used at: T.3.4
E59  Image detail is lost at the current resolution or nearby compatible sizes remain untested.
     how: Inspect image and object sizes, trained resolution, prior resolution scores, and memory usage.
     used at: T.3.4
E60  Current text formatting removes useful content or omits relevant context.
     how: Inspect tokenized examples, truncation lengths, whitespace handling, and the formatting used during training.
     used at: T.3.4
E61  Missing values, unseen categories, or unsuitable numeric scales reach a model that cannot handle them.
     how: Inspect dtypes, non-finite counts, category coverage, numeric ranges, and the learner input requirements.
     used at: T.3.4
E62  Spectrograms lose relevant detail or their dynamic range is dominated by artifacts.
     how: Inspect signal spectra and rendered spectrograms, transform parameters, and the trained input representation.
     used at: T.3.4
E63  The current crop or window excludes potentially relevant neighboring context.
     how: Inspect target timestamps, raw window lengths, crop coordinates, and prior center-only versus context results.
     used at: T.3.4
E64  Known noise frequencies or problematic passbands are present in raw signals.
     how: Inspect power spectra, sample rate, filter response, and the filtering configuration used during training.
     used at: T.3.4
E65  Missing or non-finite values reach a learner with a known missing-value policy.
     how: Count missing values by feature and group and inspect native missing-value support and the fitted imputer.
     used at: T.3.4.4
E66  Numeric range, resolution, or precision may suppress useful distinctions.
     how: Inspect feature ranges, quantization, outliers, and the downstream learner sensitivity to scale.
     used at: T.3.4.4
E67  Compatible checkpoints differ in training history or validation quality.
     how: Read checkpoint manifests, epoch and stage metrics, and prior standalone comparisons.
     used at: T.4
E68  The current model is underpowered or a different inductive bias is supported by prior errors.
     how: Inspect learning curves, standalone model results, available trained configurations, and input modality.
     used at: T.4
E69  Compatible weights pretrained on relevant domain data are available.
     how: Inspect checkpoint training provenance and compare domain vocabulary or image characteristics with the target data.
     used at: T.4
E70  A strong backbone uses a limited head or cannot yet combine available branches.
     how: Inspect the model forward pass, head dimensions, pooled representations, and current branch outputs.
     used at: T.4
E71  The proposed weights were trained with a different input pipeline than the current one.
     how: Compare training artifact configuration with the current preprocessing and tokenizer.
     used at: T.4
E72  The current pooling or linear head discards useful spatial, temporal, or hidden-layer information.
     how: Inspect the pooling implementation and head capacity and compare existing head-variant results.
     used at: T.4.4
E73  Extra heads or layers have failed controlled comparisons or overfit.
     how: Inspect head ablations and the training-versus-validation gap for the complex variant.
     used at: T.4.4
E74  Targets are ordered, bounded, or have a useful auxiliary labeling formulation.
     how: Inspect target support and correlations and the current output activation and loss.
     used at: T.4.4
E75  Multiple aligned input branches provide complementary representations.
     how: Inspect branch dimensions, modality ablations, and whether current fusion discards branch identity.
     used at: T.4.4
E76  Tree models show underfitting or overfitting associated with depth or leaf count.
     how: Compare training and validation curves and earlier capacity trials on the same feature set.
     used at: T.5
E77  Training fit exceeds validation fit or newly added features increase instability.
     how: Inspect the generalization gap, current penalties and sampling rates, and previous regularization trials.
     used at: T.5
E78  Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective.
     how: Inspect per-step losses, gradient scale if logged, current schedule, and stopping time.
     used at: T.5
E79  Training stops before convergence or continues after validation deterioration.
     how: Inspect best versus final iteration, patience, maximum budget, and validation trajectories.
     used at: T.5
E80  The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
     how: Compare the objective with metric penalties and inspect per-target residuals and custom gradient behavior.
     used at: T.5
E81  The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
     how: Inspect target semantics, event and censoring indicators, group distributions, and current transformation code.
     used at: T.5
E82  The current boosting procedure has plateaued or its interface blocks required training controls.
     how: Inspect supported early stopping and metric callbacks and results from tuned standard boosting.
     used at: T.5
E83  A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
     how: Inspect that component training code for fold boundaries, validation monitoring, saved models, and out-of-fold coverage.
     used at: T.5
E84  A lower learning rate was introduced without increasing the iteration budget.
     how: Compare learning rate, maximum rounds, best iteration, and patience before and after the change.
     used at: T.5
E85  Available candidates differ in quality or diversity and the current membership is not settled.
     how: Read member manifests and prior standalone and leave-one-out comparisons.
     used at: T.6
E86  A single run or view is unstable and compatible repeated predictions are available.
     how: Inspect fold and seed checkpoints, stochastic layers, view invariances, and per-replica scores.
     used at: T.6
E87  Member outputs have different scales or the current combination is not supported by validation.
     how: Inspect output distributions, metric invariances, and availability of aligned out-of-fold predictions.
     used at: T.6
E88  A candidate has nonredundant errors and plausible standalone quality.
     how: Compare aligned validation residuals and standalone scores with those of current members.
     used at: T.6.1
E89  One member is consistently weak and a compatible replacement is available.
     how: Inspect standalone and marginal scores for the existing member and candidate checkpoints.
     used at: T.6.1
E90  A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
     how: Inspect error correlations and existing standalone, removal, and full-ensemble scores.
     used at: T.6.1
E91  A previously better ensemble lost members during a recent change.
     how: Compare saved member lists and the corresponding verified ensemble scores.
     used at: T.6.1
E92  Available fold checkpoints differ in quality or some are currently unused.
     how: Check checkpoint existence, split provenance, fold scores, and the current inference fold list.
     used at: T.6.2
E93  Independent training seeds produce materially different errors.
     how: Compare per-seed held-out predictions and scores and confirm checkpoints come from distinct training runs.
     used at: T.6.2
E94  The task has valid input symmetries or multiple aligned views of the same target.
     how: Inspect examples, label invariance, trained augmentations, and earlier view-specific scores.
     used at: T.6.2
E95  Dropout or other random inference operations are active or being proposed.
     how: Inspect evaluation mode and compare repeated forward passes with identical inputs and weights.
     used at: T.6.2
E96  Repeated forward passes with the same weights and inputs are numerically identical.
     how: Compare arrays from existing identical-input reruns and inspect evaluation mode.
     used at: T.6.2
E97  Available fold checkpoints were trained with incompatible feature layouts.
     how: Compare saved fold configurations and input schemas.
     used at: T.6.2
E98  Member quality is similar or previous nonuniform weights fail to beat equal weighting.
     how: Compare standalone and blend scores and uncertainty around the claimed weighted gain.
     used at: T.6.3
E99  Members differ in quality or residual patterns and the current blend has not been retuned after a component change.
     how: Inspect aligned saved predictions, standalone and blend results, and the change log; record whether evaluation comes from held-out data or only a small public set.
     used at: T.6.3
E100  An auxiliary prediction has a stable residual correction that may require subtraction.
     how: Inspect residual correlations and prior small positive and negative coefficient probes on held-out data.
     used at: T.6.3
E101  The metric is ranking-based and member prediction scales or calibrations differ.
     how: Read the metric definition and compare member quantiles, rank correlations, and previous rank-versus-raw scores.
     used at: T.6.3
E102  Models output class distributions and confidence differs across members.
     how: Inspect saved logits and probabilities, row sums, and whether the metric penalizes probability calibration.
     used at: T.6.3
E103  Probability tails or output scale differences dominate an arithmetic blend.
     how: Inspect per-member probability histograms and held-out errors in high-confidence and low-confidence regions.
     used at: T.6.3
E104  Enough aligned out-of-fold examples exist to learn complementary prediction relationships.
     how: Verify each training row was excluded from its base-model fit and inspect sample count relative to meta-feature count.
     used at: T.6.3
E105  The only evaluation feedback is a small public subset and many weights have already been tried.
     how: Inspect public sample-count information and the number and spread of prior weight-search results.
     used at: T.6.3
E106  Base predictions contain misaligned rows or inconsistent target direction.
     how: Compare identifier order and held-out target correlations for every component.
     used at: T.6.3
E107  The target is ordinal and the metric depends on discrete label agreement.
     how: Inspect unique target levels and metric penalties and compare existing rounding and threshold results.
     used at: T.7
E108  Ordinal label frequencies are approximately known and the metric is sensitive to the marginal prediction distribution.
     how: Inspect observed target frequencies, current rounded prediction frequencies, and the metric definition, including penalties for distribution mismatch.
     used at: T.7
E109  Predictions have systematic bias or scale mismatch relevant to the metric or downstream rounding.
     how: Inspect calibration plots, held-out residual mean, prediction bounds, and the output activation definition.
     used at: T.7
E110  Observable groups or auxiliary outputs reveal stable group-specific residual bias.
     how: Inspect held-out residuals by group and confirm the group or auxiliary signal is available at test time.
     used at: T.7
E111  Previous postprocessing gains vanished after a model change or the transform preserves a metric-invariant ordering.
     how: Inspect previous mapping ablations, current prediction distributions, and whether the metric is invariant to the proposed transform.
     used at: T.7
E112  Group-specific thresholds were tuned on very few held-out samples.
     how: Count validation examples per threshold group and inspect threshold variability across folds.
     used at: T.7
E113  Full runs are slow and new code frequently fails before producing predictions.
     how: Inspect stage runtimes and recent failures and identify a small subset that exercises all active stages.
     used at: T.8
E114  Most runtime repeats upstream computation unchanged by the current experiment.
     how: Inspect stage timings and compare feature, model, and preprocessing configuration hashes across recent runs.
     used at: T.8
E115  Peak memory grows with full datasets or simultaneously retained models.
     how: Read memory logs and inspect tensor and dataframe lifetimes and whether grouping crosses chunk boundaries.
     used at: T.8
E116  Padding, oversized batches, or full precision dominate inference memory or runtime.
     how: Inspect length histograms, utilization, out-of-memory traces, batch normalization mode, and numerical sensitivity.
     used at: T.8
E117  Frequent variant edits cause stale paths, mismatched parameters, or accidental component omissions.
     how: Inspect duplicated loading logic, configuration diffs, and recurring integration failures.
     used at: T.8
E118  Dead code or intertwined stages obstruct iteration despite a working prediction baseline.
     how: Inspect active call paths and duplicated stages and confirm baseline predictions are saved for equivalence checks.
     used at: T.8
E119  Profiling shows repeated metric computation dominates fitting or blend search.
     how: Read function-level runtime profiles and compare metric-call time with model and data-processing time.
     used at: T.8
E120  A signal-processing backend fails in the available environment or dominates feature runtime.
     how: Inspect backend imports, supported operations, package versions, device availability, and timing of the signal transform.
     used at: T.8
E121  Profiling or loop inspection shows the same conversion or transformation repeats for each group or column.
     how: Inspect nested loops and time the repeated host/device conversion or transformation on a representative subset.
     used at: T.8
E122  The dataset or feature matrix is too large even with only one model loaded.
     how: Compare peak memory with dataset size and inspect which rows must stay together for entity-level features.
     used at: T.8.3
E123  Memory accumulates across completed models or feature stages.
     how: Inspect live object references and GPU or host memory after each stage; identify objects no later stage uses.
     used at: T.8.3
E124  The failing call uses a different API level or wrapper than expected by the consuming code.
     how: Check whether the model or object was created with a high-level wrapper (e.g., sklearn API) while the failing code expects the low-level native API, or vice versa.
     used at: T.1.5
E125  Two or more independent runs produced near-identical CV scores, enabling a direct test of CV-to-LB agreement.
     how: Check whether multiple checkpoints or runs with matching CV scores are available to validate local evaluation against the leaderboard.
     used at: T.2
E126  The inference-time architecture (e.g., pooling) does not match the training-time architecture of the loaded checkpoint.
     how: Compare the pooling/architecture settings used during training of each checkpoint with those configured at inference time.
     used at: T.2
E127  The submission file format (row ordering, column names, index) may be preventing a valid leaderboard score.
     how: Check whether the submission CSV matches the expected format, ordering, and ID alignment required by the competition.
     used at: T.2
E128  A known code bug (variable name error, type mismatch, uninitialized variable, or incorrect construction) is corrupting results or blocking execution.
     how: Inspect recent code changes for typos, wrong variable references, uninitialized accumulators, type mismatches, or incorrect API calls that would crash or silently produce wrong outputs.
     used at: T.2
E129  The baseline score is far from competitive, justifying bundling multiple well-motivated improvements before fine-grained ablation.
     how: Compare the current score to known competitive thresholds and assess whether the gap is large enough to warrant batching changes.
     used at: T.2
E130  The blend/ensemble weight search has run many iterations with diminishing returns.
     how: Review the history of blend-weight experiments and check whether recent iterations are producing negligible score changes.
     used at: T.2
E131  The pipeline depends on external cached artifacts that may be stale or cause reproducibility issues.
     how: Check whether cached files, precomputed features, or external datasets are outdated relative to the current pipeline version.
     used at: T.2
E132  A more complex validation scheme (e.g., nested CV) did not clearly outperform the simpler scheme, suggesting the added complexity is not warranted.
     how: Compare scores from the complex validation approach against the simpler baseline to determine if the complexity is justified.
     used at: T.2
E133  The practitioner is relying solely on leaderboard submissions rather than local cross-validation to evaluate modeling changes.
     how: Check whether a local CV loop exists and is being used to evaluate hyperparameter or model changes before submitting to the leaderboard.
     used at: T.2
E134  The current number of CV folds makes each experiment too slow for rapid iteration.
     how: Estimate wall-clock time per full CV run and assess whether reducing folds or using a faster evaluation strategy would enable more experiments.
     used at: T.2
E135  Current CV fold count or split ratio makes iteration (runtime/memory) impractically slow.
     how: Check wall-clock time and memory usage of the current CV loop and whether reducing folds or increasing holdout would allow faster experimentation.
     used at: T.2.2
E136  The model's blend weight is small enough that individual overfitting from the validation design has limited impact on the final ensemble score.
     how: Check the model's weight in the ensemble and estimate how much a CV design flaw could propagate to the blended prediction.
     used at: T.2.2
E137  The current model type or hyperparameters differ from those used when the validation split was last tuned, so the optimal split may have changed.
     how: Compare the current model configuration to the one used when holdout size or fold count was last varied.
     used at: T.2.2
E138  The feature matrix passed to the CV splitter contains non-feature columns (identifiers, targets, or metadata) that should have been excluded.
     how: Inspect the DataFrame columns passed to the splitter and verify none are identifiers, targets, or other non-feature columns.
     used at: T.2.2
E139  The grouping method used for group-aware CV does not capture the actual dependence structure (e.g., topic/text similarity) well.
     how: Check whether the clustering input (e.g., raw features vs. TF-IDF) actually reflects the semantic similarity that defines dependence groups.
     used at: T.2.2
E140  The CV split call references variables or DataFrames that are misaligned with the actual in-memory data used for training.
     how: Verify that the DataFrame/array variables in the split call match the ones used in the training loop body.
     used at: T.2.2
E141  The CV splitter object has not been properly instantiated or imported before the CV loop executes.
     how: Check that the splitter class is imported and an instance is created with correct parameters before .split() is called.
     used at: T.2.2
E142  The KMeans predict call uses the same feature subset as the KMeans fit call.
     how: Compare columns/features passed to KMeans.fit() vs. KMeans.predict() to ensure consistency.
     used at: T.2.2
E143  Alternative approaches (e.g., sample weighting) to address the distribution mismatch were already tried and failed, justifying a fold-structure change.
     how: Review prior experiment logs for attempts to address the same issue with simpler methods and their outcomes.
     used at: T.2.2
E144  The validation design change is bundled with other simultaneous changes (hyperparameters, GPU config, callbacks), making it impossible to isolate its effect.
     how: Check whether the current edit changes only the CV split or also modifies model hyperparameters, training infrastructure, or other settings.
     used at: T.2.2
E145  The CV implementation has index remapping or slicing bugs that corrupt the actual train/validation fold composition.
     how: Trace the index arrays through the split logic and verify that train and validation sets are disjoint and cover the intended samples.
     used at: T.2.2
E146  The expert has no leaderboard or recorded validation scores to guide the feature-selection sweep direction.
     how: Check whether any prior submissions or recorded validation scores exist that can inform which direction (more or fewer features) to move in the sweep.
     used at: T.3.3
E147  The feature importance ranking is aggregated across CV folds (e.g., median) rather than computed on a single fold, improving stability.
     how: Inspect how the importance scores were computed — single fold vs. aggregated across multiple folds.
     used at: T.3.3
E148  The expert is incrementally stepping through retention ratios without a systematic grid search or recorded comparison of validation scores across ratios.
     how: Check whether the sweep over retention ratios follows a systematic plan with recorded scores at each step, or is blind incremental stepping.
     used at: T.3.3
E149  A previously submitted score at a nearby retention ratio provides a concrete baseline for comparison.
     how: Check whether a submitted or validated score exists at a neighboring retention ratio that can serve as a baseline for the next step.
     used at: T.3.3
E150  The expert has already tried this exact retention ratio in a previous pipeline version.
     how: Check version history for whether the same top_ratio or feature count was previously tested.
     used at: T.3.3
E151  The score has been monotonically increasing as the retention fraction increases through the sweep, suggesting the optimum has not yet been reached.
     how: Review the sequence of scores at each tested retention ratio to see if the trend is still increasing.
     used at: T.3.3
E152  The new feature implementation contains a data leakage or cross-contamination bug (e.g., test data references train-only columns).
     how: Inspect the feature engineering code for references that leak information across train/test boundaries.
     used at: T.3.3
E153  A previously tried feature-selection strategy (e.g., SHAP) consistently outperformed the current one (e.g., LGB importance) across submissions.
     how: Compare leaderboard or validation scores across different feature-selection strategies used in prior versions.
     used at: T.3.3
E154  The intent is a batch-then-prune strategy: add a broad set of candidate features first, then selectively remove subsets, rather than selecting from the existing set.
     how: Check whether the current edit is the 'add batch' phase of a two-phase strategy, with pruning planned for subsequent steps.
     used at: T.3.3
E155  A previous edit that dropped derived features led to a measurable score improvement, establishing that simpler feature sets perform better.
     how: Check version history for cases where removing derived/aggregation features improved the score.
     used at: T.3.3
E156  The training loop has variable-usage bugs (e.g., wrong variable names in fit/predict/metric calls) that corrupt validation scores used to guide feature selection.
     how: Inspect the training code for incorrect variable references that would make validation scores unreliable.
     used at: T.3.3
E157  Duplicated inline feature-engineering or aggregation code makes it error-prone to add or remove feature groups consistently.
     how: Check whether feature construction code is duplicated in multiple places, risking inconsistent additions/removals.
     used at: T.3.3
E158  There exist columns with very high missing-value rates that have not yet been explicitly addressed in the retention policy.
     how: Check the candidate feature set for columns with extreme missingness that should be considered for removal.
     used at: T.3.3
E159  Changing the feature count in either direction from the current best degraded the score, suggesting the optimal count is near the current value.
     how: Review whether both increasing and decreasing feature count from the best-known configuration led to worse scores.
     used at: T.3.3
E160  The previous feature selection code failed to execute at runtime, so the ranked list was never actually produced and must be regenerated.
     how: Check whether the prior version's selection code ran successfully or failed, leaving no valid ranked list.
     used at: T.3.3
E161  Hyperparameters were tuned for the previous feature set size and may be suboptimal for the new retention policy.
     how: Check whether model hyperparameters (learning rate, regularization, num_leaves, etc.) were re-tuned after changing the feature set.
     used at: T.3.3
E162  The actual code edit changes a model hyperparameter (e.g., max_depth) rather than the feature retention cutoff.
     how: Compare the diff to confirm whether the edit modifies the feature selection threshold or a model hyperparameter instead.
     used at: T.3.3
E163  A column rename or feature-naming convention introduced duplicate column names, causing silent data corruption.
     how: Check whether the feature naming scheme produces unique names for all generated columns.
     used at: T.3.3
E164  Run-to-run variance is large enough that observed score differences between transformation settings may be noise rather than signal.
     how: Compare score differences between transformation variants against the magnitude of run-to-run score fluctuations from repeated identical submissions.
     used at: T.3.4
E165  The current edit changes a different lever than the input transformation (e.g., fold count or ensemble composition), not the transformation itself.
     how: Compare the stated intent (change input transformation) against what the edit actually modifies.
     used at: T.3.4
E166  A specific preprocessing toggle (e.g., rank conversion, log scaling) has been compared across runs and one setting consistently dominates.
     how: Review scored runs that differ only in the preprocessing toggle to see if one setting consistently outperforms the other.
     used at: T.3.4
E167  The input data's inherent channel structure (e.g., grayscale replicated to 3 channels) means channel-wise normalization statistics should be identical.
     how: Check whether the input modality is single-channel replicated to multi-channel, making per-channel normalization differences meaningless.
     used at: T.3.4
E168  A previous normalization or preprocessing parameter change caused a score regression, suggesting the change should be reverted.
     how: Check the score history for the most recent normalization/preprocessing parameter change and whether it regressed performance.
     used at: T.3.4
E169  Previous sweeps of the candidate transformation parameter show diminishing or inconsistent returns, suggesting the search space is too flat to navigate via probing.
     how: Review the score trajectory across recent parameter sweep submissions to see if improvements are within noise.
     used at: T.3.4
E170  The inference model architecture definition includes layers or branches not present in the trained checkpoint, causing load mismatches.
     how: Compare the model class definition used at inference against the architecture that produced the checkpoint weights.
     used at: T.3.4
E171  The edit changes model configuration (backbone, layers) in addition to the input transformation, confounding the intended single-variable experiment.
     how: Diff the edit to check whether any model architecture parameters changed alongside the intended transformation change.
     used at: T.3.4
E172  The current clipping or thresholding parameter may be too loose or too tight, and an alternative value could better balance outlier removal with signal preservation.
     how: Check whether the current clipping threshold removes meaningful signal or lets through extreme outliers by examining the data distribution.
     used at: T.3.4
E173  A recently introduced transformation parameter has not been ablated in isolation because other changes were made simultaneously.
     how: Check the edit history to see if the parameter in question was introduced alongside other changes, preventing isolated attribution.
     used at: T.3.4
E174  A duplicated or redundant preprocessing step is applied multiple times, corrupting the signal before model input.
     how: Trace the preprocessing pipeline to check if any step (e.g., filtering, normalization) is applied more than once.
     used at: T.3.4
E175  A transformation parameter axis or dimension has not yet been explored despite other axes having been swept.
     how: Review which transformation parameters have been swept and identify any that remain at their default/initial value.
     used at: T.3.4
E176  The current score is substantially worse than the best achieved, indicating recent transformation changes have not been recovered from.
     how: Compare the current leaderboard score against the historical best to assess whether recent changes regressed performance significantly.
     used at: T.3.4
E177  The best-scoring version used a specific normalization method (e.g., linear clip-and-scale vs log) that differs from the current one.
     how: Compare the normalization method in the current version against the one used in the best-scoring historical version.
     used at: T.3.4
E178  Derived features from the candidate transformation are highly correlated with features already present, adding redundancy rather than new information.
     how: Compute correlation between the new derived features and existing features to check for redundancy.
     used at: T.3.4
E179  The transformation code contains a bug (e.g., wrong axis, wrong variable) that prevents it from functioning as intended.
     how: Review the transformation implementation for coding errors that would silently produce incorrect output.
     used at: T.3.4
E180  The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
     how: Compare the architecture definition used during checkpoint training against the current inference-time model; verify that layer dimensions and structure match.
     used at: T.4.4
E181  Reinitializing the last N transformer layers is a viable fine-tuning strategy for small datasets that the current pipeline does not employ.
     how: Review literature on partial reinitialization for transfer learning and check whether the current fine-tuning script freezes or reinitializes any backbone layers.
     used at: T.4.4
E182  The ordinal/ranking prediction approach has not yet been validated end-to-end with a leaderboard submission using up-to-date checkpoints.
     how: Check submission history for any ordinal-head runs and whether the latest available ordinal checkpoints have been evaluated.
     used at: T.4.4
E183  A candidate member was trained at a different input resolution than the current inference resolution, creating a potential mismatch or a complementary view.
     how: Compare the training resolution of each checkpoint against the inference resolution currently configured.
     used at: T.6
E184  Aggregation rule tuning (weights, rank-averaging, transforms) has been explored and is showing diminishing returns.
     how: Review the history of aggregation-rule changes and whether recent adjustments still yield meaningful score improvements.
     used at: T.6
E185  The contribution of a specific ensemble component (TTA, stacking layer, individual member) has not been isolated by ablation.
     how: Check whether the component in question has been submitted or evaluated in isolation versus only as part of a larger combination.
     used at: T.6
E186  There is a code bug in the aggregation step (wrong weights, wrong column references, stray control-flow statements) that corrupts the ensemble output.
     how: Inspect the blending/averaging code for mismatched array shapes, wrong variable names, stray break/continue, or incorrect column references.
     used at: T.6
E187  Blend weights are stale or heuristic because new members were added or existing members were updated since the last calibration.
     how: Check whether the current weight vector was tuned after the most recent change to ensemble membership or checkpoint versions.
     used at: T.6
E188  Runtime or memory budget is insufficient to run all desired ensemble members at the current per-sample cost.
     how: Estimate total inference time and peak memory for the planned ensemble and compare against the competition kernel limits.
     used at: T.6
E189  A candidate member requires a preprocessing step (e.g., spectrogram generation) that is currently missing or misconfigured in the pipeline.
     how: Verify that every preprocessing dependency for each candidate member is present and correctly wired before running inference.
     used at: T.6
E190  Preprocessing parameters were changed simultaneously with ensemble composition, confounding the effect of each change.
     how: Review recent edit history to see if preprocessing and membership changes were made in the same version without independent evaluation.
     used at: T.6
E191  Previous weight adjustments have shown meaningful score sensitivity, indicating that weight tuning is a high-leverage intervention.
     how: Review the score delta attributable to weight-only changes across recent submission versions.
     used at: T.6
E192  The current weight search is restricted (e.g., positive-only) in a way that prevents the optimizer from exploiting anti-correlated member residuals.
     how: Inspect the optimizer constraints and check whether allowing negative or unconstrained weights could improve the objective on validation.
     used at: T.6
E193  A secondary model's high-confidence discrete predictions can identify specific samples where the primary model's continuous output should be overridden or corrected.
     how: Check whether a classification model's top-confidence bin predictions flag regression outliers that, when corrected, improve the metric.
     used at: T.7
E194  The current correction or mapping was tuned on earlier training statistics and may be overfitting to those statistics rather than generalizing.
     how: Check whether the full (undampened) correction was already applied in a previous version and whether it shows signs of overfitting to training-set statistics.
     used at: T.7
E195  Previous parameter changes in the same direction showed monotonic improvement, suggesting further extrapolation may continue the trend.
     how: Check whether prior incremental changes to the mapping parameter showed a consistent improvement trend that motivates further movement in the same direction.
     used at: T.7
E196  The current mapping parameters were introduced simultaneously with another change and their isolated effect has never been measured.
     how: Check whether the output mapping parameters were bundled with other changes and whether their individual contribution has been ablated.
     used at: T.7
E197  The mapping parameters were tuned for an earlier model checkpoint and need revalidation on the current checkpoint before deciding to keep or remove them.
     how: Check whether the output mapping was calibrated against a previous model version and has not been re-tested with the current model.
     used at: T.7
E198  A previous threshold or mapping parameter change produced a meaningful leaderboard improvement, suggesting further sweeping of that parameter is productive.
     how: Check whether the last change to the mapping parameter yielded a measurable score gain, motivating continued search in that region.
     used at: T.7
E199  The submission file has formatting issues (wrong columns, extra columns, incorrect column names) that prevent valid submission.
     how: Check whether the output file conforms to the required submission format (correct column names, no extra columns).
     used at: T.7
E200  The output mapping code references a column or variable name that does not exist at runtime, causing a crash.
     how: Check whether the postprocessing code references column names or variables that are actually present in the DataFrame at the point of execution.
     used at: T.7
E201  The current mapping values (e.g., blend weights or rounding thresholds) correspond to naive defaults (e.g., uniform midpoints) rather than optimized values.
     how: Check whether the mapping parameters are set to simple default values rather than having been optimized for the metric.
     used at: T.7
E202  Public or known high-scoring solutions for this task use the proposed output mapping technique as a standard practice.
     how: Check whether the proposed mapping approach (e.g., optimized rounding thresholds) is a well-known technique used in top solutions for similar tasks.
     used at: T.7
E203  The current fold construction or data subset used for threshold optimization has changed from a previously successful configuration, and reverting may recover performance.
     how: Check whether recent changes to fold construction or the optimization subset coincided with a score drop, suggesting the mapping should be re-tuned on the original data split.
     used at: T.7
E204  Optimizing the output mapping on a specific data subset (e.g., difficulty-based) previously outperformed full-set optimization.
     how: Check whether subset-specific threshold optimization (e.g., on a difficulty stratum) yielded better leaderboard scores than optimizing on the full validation set.
     used at: T.7
E205  Subset-specific threshold optimization may not generalize when the cross-validation scheme or data split changes.
     how: Check whether the subset used for threshold optimization is stable across CV scheme changes and whether the optimized thresholds transfer.
     used at: T.7
E206  Combining a model's event-probability output with its time-to-event output (e.g., as a hazard-like ratio) may produce a better-ranked score than either output alone.
     how: Check whether the model produces both a probability and a continuous prediction that can be algebraically combined into a hazard-like quantity for improved ranking.
     used at: T.7
E207  A model produces multiple output heads (e.g., classifier and regressor) and the current combination logic for merging them may be suboptimal or adding noise.
     how: Check whether a multi-head model's outputs are being combined in a way that could introduce noise, and whether a different combination strategy would be better.
     used at: T.7
E208  A simple combination of the multi-head outputs (e.g., negation and stacking) is a reasonable first attempt before exploring more sophisticated strategies.
     how: Check whether the simplest combination of available model outputs has been tried as a baseline before investing in complex combination logic.
     used at: T.7
E209  The output mapping change (e.g., temperature scaling) also affects the training gradient landscape, not just inference, potentially changing learned representations.
     how: Check whether the proposed mapping change is applied during training (not just inference) and could alter the model's learned weights and discrimination.
     used at: T.7
E210  Multiple values of the current mapping parameter have already been tried, providing a search history to guide the next choice.
     how: Check whether the expert has already tested several values of this specific parameter and what the resulting score trajectory looks like.
     used at: T.7
E211  Per-batch or per-chunk memory from large batch sizes still causes OOM after releasing completed model stages.
     how: After freeing completed models/stages, check whether the remaining per-batch or per-chunk allocation alone exceeds available memory due to large batch sizes.
     used at: T.8.3
E212  Per-chunk preprocessing encounters categories not present in the chunk but present in the dtype's category list, causing incorrect add_categories logic.
     how: When processing data in chunks, check whether the categorical dtype's category list diverges from the categories actually observed in each chunk, leading to erroneous category handling.
     used at: T.8.3
E213  Premature deletion of a variable (e.g., X_train_fold) causes errors because a later pipeline stage still references it.
     how: Before inserting `del` statements for memory reduction, verify that no downstream code still holds a reference to or requires the deleted object.
     used at: T.8.3