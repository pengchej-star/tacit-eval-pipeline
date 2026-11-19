# evidence/registry.md — one definition per check, shared across nodes

E01  Checkpoint keys or tensor dimensions do not match the instantiated model.
     how: Inspect load-state diagnostics and compare the saved architecture configuration with inference construction.
     used at: T.1.1
E02  Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact.
     how: Compare tokenizer files, vocabulary size, token IDs, and encoded examples with the training configuration.
     used at: T.1.1
E03  The same raw sample receives different feature values in training and inference.
     how: Run a saved sample through both preprocessing paths and compare feature arrays, scaling, and category mappings.
     used at: T.1.1
E04  Prediction or feature arrays were concatenated without an identifier-based alignment check.
     how: Inspect joins, indices, and ordered sample IDs around concatenation and submission construction.
     used at: T.1.1
E05  A small-batch run raises an API, shape, or variable-reference exception.
     how: Read the first traceback and inspect the failing call’s arguments and return values.
     used at: T.1.2
E06  Required files or packages are absent or incompatible in the submission environment.
     how: Check artifact manifests, paths, imports, package versions, and file permissions.
     used at: T.1.2
E07  The blended output disagrees with a direct recomputation from saved member arrays.
     how: Recompute a few rows independently and inspect active members, axes, denominators, and output variable names.
     used at: T.1.2
E08  The notebook completes but its output is missing, stale, or based on placeholder inputs.
     how: Inspect the written file, input paths, debug flags, row IDs, and final writer call.
     used at: T.1.2
E09  Scores suggest reversed risk ordering or outputs violate the metric’s required interpretation.
     how: Compare prediction ranges and orientation with labels and the task’s scoring code.
     used at: T.1.2
E10  The traceback identifies incompatible devices or unsupported accelerator settings.
     how: Inspect tensor devices and each model library’s configured backend.
     used at: T.1.2
E11  Some members fail to load or predict but verified cached outputs or a valid reduced ensemble are available.
     how: Inspect failed-member logs, cached prediction provenance, row IDs, and remaining member coverage.
     used at: T.1.2
E12  A newly integrated path has never completed on representative data.
     how: Check run logs for one complete pass including output generation.
     used at: T.1.3
E13  A previously verified configuration exists and recent bundled edits caused a large regression.
     how: Compare versioned configurations, artifacts, and scores around the regression.
     used at: T.1.3
E14  Repeated branches and implicit configuration make model dispatch or data flow inconsistent.
     how: Inspect duplicate inference functions, commented toggles, shared state, and inconsistent branch settings.
     used at: T.1.3
E15  No end-to-end baseline can be reproduced from the current implementation.
     how: Attempt the smallest complete run and inspect whether a verified configuration or prediction reference exists.
     used at: T.1.3
E16  The loaded model or transformed inputs differ from the training artifacts.
     how: Compare model, tokenizer, and preprocessing manifests for training and inference.
     used at: T.1
E17  There is a traceback, missing output, or incorrect ensemble calculation.
     how: Inspect execution logs and recompute several final prediction rows.
     used at: T.1
E18  The code runs but repeated refactors have made the effective configuration uncertain.
     how: Trace active branches and compare current outputs with the last verified snapshot.
     used at: T.1
E19  The score comparison changed multiple settings or artifacts simultaneously.
     how: Diff the compared configurations and checkpoint manifests.
     used at: T.2.1
E20  The claimed gain is comparable to variation already observed across unchanged runs.
     how: Compare the candidate delta with repeated baseline scores and prediction differences.
     used at: T.2.1
E21  Identical configurations produce different predictions because random operations are unseeded.
     how: Inspect RNG setup, data loading, stochastic inference, and optimization logs.
     used at: T.2.1
E22  Recent trials along the same lever repeatedly tie or worsen the best validated result.
     how: Review the trial table and uncertainty estimates for that lever.
     used at: T.2.1
E23  The best tested parameter lies at a range boundary or a changed setting invalidates an earlier optimum.
     how: Inspect parameter-score tables and known coupled settings.
     used at: T.2.1
E24  A representative local validation set is available but candidates are being ranked only by submissions.
     how: Compare validation coverage with the task population and inspect experiment logs.
     used at: T.2.1
E25  The prediction unit, history lengths, or missingness structure has not been established.
     how: Inspect the existing data audit and schema summaries for those quantities.
     used at: T.2.1
E26  The complete pipeline has no task-metric evaluation despite multiple implementation iterations.
     how: Inspect run records for a scored end-to-end baseline.
     used at: T.2.1
E27  The component being tuned has a tiny blend weight and its changes cannot materially move the combined predictions.
     how: Inspect blend coefficients and compare component perturbations with observed score variation.
     used at: T.2.1
E28  Labels or binned regression targets are unevenly represented across current folds.
     how: Tabulate label counts and target quantiles by fold.
     used at: T.2.2
E29  Rows share entities, overlapping signals, or near-duplicate content across folds.
     how: Join entity IDs or inspect similarity clusters and count cross-fold overlap.
     used at: T.2.2
E30  The expected test population matches only an identifiable subset of training data.
     how: Compare task metadata and train/test source or subgroup distributions.
     used at: T.2.2
E31  Stacking or calibration currently uses predictions fitted on their own training labels.
     how: Trace prediction provenance and fold indices.
     used at: T.2.2
E32  A large fixed holdout removes training examples without changing model selection decisions.
     how: Inspect holdout size, learning curves, and whether validation is used for selection or stopping.
     used at: T.2.2
E33  Examples are approximately independent and no source shift or target-stratum imbalance requires a specialized split.
     how: Audit entity overlap, train/test source distributions, and fold label counts.
     used at: T.2.2
E34  The current callback differs from the official scoring function or uses the wrong direction.
     how: Compute both metrics on saved labels and predictions and inspect early-stopping configuration.
     used at: T.2.3
E35  The task metric fluctuates sharply between adjacent iterations while a smooth proxy is stable.
     how: Plot both validation curves from the same run.
     used at: T.2.3
E36  Full folds or repetitions dominate development time before code correctness is established.
     how: Inspect stage timings and the number of redundant full training runs.
     used at: T.2.4
E37  The expensive upstream computation is unchanged across downstream trials.
     how: Compare upstream configuration hashes and stage timings across runs.
     used at: T.2.4
E38  Peak memory grows with the full dataset or feature matrix size.
     how: Inspect memory traces and the lifetime of whole-dataset arrays.
     used at: T.2.4
E39  Memory grows as successive models or framework stages are loaded.
     how: Inspect allocated memory before and after each model and retained references.
     used at: T.2.4
E40  A single inference batch exceeds device memory or padding dominates its size.
     how: Inspect batch shapes, sequence lengths, and memory at the failed batch.
     used at: T.2.4
E41  Stored arrays or activations dominate memory and a precision reference is available.
     how: Measure dtype-specific memory and compare saved full-precision predictions.
     used at: T.2.4
E42  Profiling identifies a CPU-bound computation with an available equivalent accelerated implementation.
     how: Inspect timing profiles, installed APIs, and a small parity comparison.
     used at: T.2.4
E43  A full fold-training loop exceeds a session limit but individual folds fit.
     how: Compare per-fold runtime with session limits and inspect completed checkpoint inventory.
     used at: T.2.4
E44  Repeated device transfers or repeated per-group computation dominate a transformation.
     how: Profile transfers and count redundant conversions inside group loops.
     used at: T.2.4
E45  Score changes cannot be attributed because runs differ in several factors or fluctuate on repetition.
     how: Inspect version diffs, run manifests, and repeated scores.
     used at: T.2
E46  Current validation leaks related samples or misrepresents the test population.
     how: Audit fold assignments and train/test population summaries.
     used at: T.2
E47  The training selection metric does not match the task or is unstable between iterations.
     how: Inspect metric code and learning curves.
     used at: T.2
E48  Runtime or memory prevents completing representative comparisons.
     how: Inspect stage timings and memory failures.
     used at: T.2
E49  Specific training groups contain duplicate observations, unreliable labels, or a distribution absent at test time.
     how: Inspect duplicate IDs, annotator agreement, outlier diagnostics, and source distributions.
     used at: T.3.1
E50  Additional labeled data has compatible inputs and target semantics.
     how: Compare auxiliary schemas, label definitions, and source distributions.
     used at: T.3.1
E51  Unlabeled examples and a validated teacher are available.
     how: Inspect unlabeled coverage, teacher validation scores, and pseudo-label confidence.
     used at: T.3.1
E52  The configuration is fixed and a retained holdout is no longer needed for fitting decisions.
     how: Inspect selection records and whether final training still excludes held-out labels.
     used at: T.3.1
E53  A relevant class or test-matching subgroup is underrepresented in training.
     how: Compare class and source frequencies with the expected test population.
     used at: T.3.1
E54  Some observed times are censored rather than completed events.
     how: Inspect event indicators, follow-up times, and the metric’s risk interpretation.
     used at: T.3.2
E55  The score explicitly aggregates performance across groups with different outcome distributions.
     how: Read the scoring function and compare group-specific event and target distributions.
     used at: T.3.2
E56  Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values.
     how: Inspect unique labels and the scoring penalty for ordinal errors.
     used at: T.3.2
E57  The existing target transform includes tunable scaling or centering constants.
     how: Inspect target-construction code and fold-level target distributions.
     used at: T.3.2
E58  Available training rows differ in quality, source relevance, or labeling status.
     how: Inspect duplicate, confidence, label, and source summaries.
     used at: T.3
E59  The learned target does not directly express censoring, ordering, or the subgroup objective.
     how: Compare target-construction code with label semantics and the metric.
     used at: T.3
E60  The current model uses raw repeated rows without an entity-level baseline.
     how: Compare the prediction unit with row IDs and current aggregation code.
     used at: T.4.1
E61  Multiple observations exist but only one record per entity reaches the model.
     how: Inspect records per entity and feature provenance.
     used at: T.4.1
E62  Global summaries discard recency or the order of meaningful changes.
     how: Compare dated trajectories with the current feature definitions.
     used at: T.4.1
E63  Related variables encode a meaningful contrast not explicit in the current features.
     how: Inspect variable definitions and joint distributions for proposed interactions.
     used at: T.4.1
E64  Useful lexical patterns are excluded or rare n-grams dominate the feature space.
     how: Inspect vocabulary coverage, n-gram settings, and feature frequencies.
     used at: T.4.2
E65  The current representation has lexical features but little contextual semantic information.
     how: Inspect feature provenance and errors requiring meaning rather than word counts.
     used at: T.4.2
E66  Text length, structure, or linguistic quality is relevant but absent from current features.
     how: Inspect task labels, sample texts, and existing feature definitions.
     used at: T.4.2
E67  Sparse representations are large and latent topics or low-dimensional summaries are available.
     how: Inspect matrix dimensions and existing decomposition outputs.
     used at: T.4.2
E68  Formatting, metadata, or input truncation may obscure task-relevant content.
     how: Inspect tokenized examples, truncation statistics, and metadata coverage at train and test time.
     used at: T.4.2
E69  Related labeled texts or auxiliary predictions can provide information absent from current features.
     how: Inspect neighbor relevance or auxiliary-model validation and coverage.
     used at: T.4.2
E70  A local language model can produce parseable task scores but their predictive value is unverified.
     how: Inspect representative generated outputs, parse failures, and held-out score correlations.
     used at: T.4.2
E71  Current time-frequency bins merge potentially informative frequencies or time events.
     how: Inspect spectrograms, transform parameters, and characteristic signal durations.
     used at: T.4.3
E72  The current crop omits relevant context or includes long irrelevant regions.
     how: Plot the crop boundaries over example signals or spectrograms.
     used at: T.4.3
E73  Signals contain identifiable narrow-band artifacts or passband-sensitive information.
     how: Inspect power spectra and current filter responses.
     used at: T.4.3
E74  Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
     how: Plot amplitude distributions and compare preprocessing with the training configuration.
     used at: T.4.3
E75  Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone.
     how: Inspect input tensors and the correspondence between channels, time, and image axes.
     used at: T.4.3
E76  An available raw or transformed modality contains information absent from the active branch.
     how: Inspect modality availability and prior single-branch validation results.
     used at: T.4.3
E77  A large engineered feature matrix contains low-importance or redundant dimensions.
     how: Inspect cross-fold importance stability and retained-feature validation curves.
     used at: T.4.4
E78  One recently added or removed feature block has uncertain marginal value.
     how: Inspect feature provenance and prior controlled ablations.
     used at: T.4.4
E79  Some columns are nearly empty or arbitrary identifiers treated as meaningful measurements.
     how: Inspect missingness, cardinality, and feature semantics.
     used at: T.4.4
E80  The learner supports missing values and is insensitive to feature scaling.
     how: Inspect the model’s configured feature handling and compare preprocessing ablations.
     used at: T.4.4
E81  A model requires finite inputs or the test set contains unseen categories.
     how: Inspect model requirements, NaN checks, and train/test category differences.
     used at: T.4.4
E82  Fine numerical variation appears noisy relative to meaningful feature resolution.
     how: Inspect measurement precision and repeated-value distributions.
     used at: T.4.4
E83  The prediction unit has repeated dated tabular observations.
     how: Inspect entity IDs, row counts, and timestamp coverage.
     used at: T.4
E84  Inputs contain text whose lexical, semantic, or structural information is not fully represented.
     how: Inspect raw examples and current feature extraction.
     used at: T.4
E85  Inputs include raw signals or images derived from signals.
     how: Inspect input schemas and transform code.
     used at: T.4
E86  The current feature matrix is large, sparse, or processed inconsistently with the learner.
     how: Inspect feature dimensions, missingness, and preprocessing requirements.
     used at: T.4
E87  The current tabular learner has plateaued on a stable feature set.
     how: Inspect same-feature trial results and validation errors.
     used at: T.5.1
E88  Standard boosting is tuned but residual overfitting remains.
     how: Inspect train–validation curves and previous regularization trials.
     used at: T.5.1
E89  Alternative pretrained backbones or capacities are available with compatible task inputs.
     how: Inspect artifact configurations, model sizes, and existing validation comparisons.
     used at: T.5.1
E90  Fixed embeddings or survival covariates provide a compact representation with limited labels.
     how: Inspect feature dimensions, label count, and target semantics.
     used at: T.5.1
E91  The wrapper prevents configuring the required custom callback or iteration selection.
     how: Inspect the active API and unsupported training arguments.
     used at: T.5.1
E92  Dataset wrapping and prediction-method differences are causing integration errors without a need for native-only controls.
     how: Inspect fitting and prediction calls and their tracebacks.
     used at: T.5.1
E93  The current head discards useful token, layer, or channel information.
     how: Inspect pooling code and hidden-state shapes.
     used at: T.5.2
E94  A related target can be derived from the training labels without test leakage.
     how: Inspect label definitions and auxiliary-target construction.
     used at: T.5.2
E95  Multiple input branches are reduced by a fixed combination that may discard information.
     how: Inspect branch dimensions and current fusion operations.
     used at: T.5.2
E96  Order or long-range interactions remain important after convolutional or pooled feature extraction.
     how: Inspect feature sequences and validation errors associated with temporal structure.
     used at: T.5.2
E97  The neural feature extractor is narrow or explicitly truncates usable feature channels.
     how: Inspect layer widths, feature slicing, and training errors.
     used at: T.5.2
E98  The current model family or pretrained capacity has plateaued despite a stable implementation.
     how: Inspect controlled model comparisons and recent tuning curves.
     used at: T.5
E99  Useful model representations are being discarded or combined by an inadequate head.
     how: Inspect hidden-state handling and branch fusion code.
     used at: T.5
E100  Several compatible trained states are already available and differ in validation quality.
     how: Inspect checkpoint manifests, stopping criteria, and per-checkpoint scores.
     used at: T.5
E101  Training error remains high with shallow or small trees.
     how: Inspect training and validation errors together with depth and leaf settings.
     used at: T.6.1
E102  Training fit is strong but validation worsens as complexity grows.
     how: Inspect learning curves and capacity sweeps.
     used at: T.6.1
E103  Trees repeatedly use the same dominant rows or feature groups.
     how: Inspect row/column sampling settings and feature-use concentration.
     used at: T.6.1
E104  A reduced learning rate exhausts the iteration budget before convergence.
     how: Inspect best iteration, stopping reason, and loss curves.
     used at: T.6.1
E105  Training loss diverges, oscillates, or converges too slowly under the current schedule.
     how: Plot learning rate and losses by training step.
     used at: T.6.2
E106  Stable learning-rate trials have plateaued with the same optimizer.
     how: Inspect optimizer configuration and controlled learning-rate trials.
     used at: T.6.2
E107  Training improves while held-out performance degrades on a small labeled dataset.
     how: Compare training and validation curves and current dropout or decay settings.
     used at: T.6.2
E108  A transformation can vary inputs while preserving or consistently mixing target meaning.
     how: Inspect sample transformations and their label construction.
     used at: T.6.2
E109  The current loss does not reflect the task’s ranking, distributional, or ordinal target semantics.
     how: Compare loss code, output activation, labels, and the scoring function.
     used at: T.6.3
E110  Class or subgroup imbalance affects errors under the evaluation metric.
     how: Inspect label frequencies and group-specific validation errors.
     used at: T.6.3
E111  A tree learner is limited by capacity, regularization, or boosting convergence.
     how: Inspect tree parameters and learning curves.
     used at: T.6
E112  A neural learner shows unstable optimization or a training–validation gap.
     how: Inspect neural training curves and optimizer settings.
     used at: T.6
E113  The loss or weighting does not match label semantics or the evaluated population.
     how: Inspect the objective and per-class or subgroup errors.
     used at: T.6
E114  Validation is still improving at the training limit or stopping reacts to brief fluctuations.
     how: Inspect epoch or iteration curves, stopping reasons, and the current maximum duration.
     used at: T.6
E115  An available model makes useful errors different from the current ensemble.
     how: Compare aligned out-of-fold residual correlations and incremental validation blends.
     used at: T.7.1
E116  A component has a compatible retrained variant with better controlled validation results.
     how: Compare the two checkpoints under identical preprocessing and member settings.
     used at: T.7.1
E117  Members are weak, redundant, or untested after the ensemble changed.
     how: Inspect standalone scores, residual correlations, and previous leave-one-out results.
     used at: T.7.1
E118  A meta-learner exists and candidate out-of-fold features add information absent from its current matrix.
     how: Inspect prediction provenance, feature correlation, and fold alignment.
     used at: T.7.1
E119  Component quality is similar and fitted weights are unstable across validation folds.
     how: Compare standalone scores and fold-specific weight solutions.
     used at: T.7.2
E120  Components have unequal validated quality and their combination changes the metric.
     how: Evaluate endpoints and a coarse blend grid on aligned held-out predictions.
     used at: T.7.2
E121  The auxiliary source is substantially weaker than the established baseline.
     how: Compare standalone scores and residual information on the same rows.
     used at: T.7.2
E122  An auxiliary source is negatively associated with the baseline residual after controlling for the base prediction.
     how: Measure held-out residual association and compare zero-weight with signed pilot blends.
     used at: T.7.2
E123  Leakage-free out-of-fold predictions and enough examples to fit a combiner are available.
     how: Audit fold provenance and compare meta-feature count with validation sample size.
     used at: T.7.2
E124  A fitted stacker underfits or overfits while its input predictions remain fixed.
     how: Inspect stacker training–validation gaps and penalty-search boundary results.
     used at: T.7.2
E125  The metric depends on ordering and member outputs have incompatible scales or outliers.
     how: Inspect the scoring code and per-member output quantiles.
     used at: T.7.2
E126  Members predict class distributions and stored logits are available.
     how: Inspect output tensors, link functions, and row-sum checks.
     used at: T.7.2
E127  Only part of an available compatible cross-validation checkpoint set is used.
     how: Inspect fold manifests, active checkpoint lists, and per-fold quality.
     used at: T.7.3
E128  Fold quality differs consistently on comparable validation evidence.
     how: Inspect fold metrics and sample difficulty before interpreting score differences.
     used at: T.7.3
E129  Independent training seeds produce materially different errors.
     how: Compare repeated training scores and aligned predictions across seeds.
     used at: T.7.3
E130  Input transformations preserve target meaning and were supported by the training representation.
     how: Inspect training augmentation and transformed examples, including channel semantics.
     used at: T.7.3
E131  The model has usable stochastic layers and repeated inference is intended to sample them.
     how: Inspect evaluation/training mode and verify predictions differ across controlled forward passes.
     used at: T.7.3
E132  Several compatible training snapshots of one model are available for weight averaging.
     how: Compare checkpoint parameter names and shapes, training trajectory, and saved validation results.
     used at: T.7.3
E133  Stochastic layers are active at inference without a validated repeated-pass strategy.
     how: Inspect model mode and compare repeated forward passes on a fixed input batch.
     used at: T.7.3
E134  New or redundant prediction sources exist whose marginal contribution is unknown.
     how: Inspect member inventory and controlled addition or ablation results.
     used at: T.7
E135  The prediction sources are fixed but weighting or output-scale handling is unvalidated.
     how: Inspect saved predictions and combination trials.
     used at: T.7
E136  Compatible fold, seed, or input-view predictions can reduce observed variance.
     how: Inspect available checkpoint groups and repeated-prediction differences.
     used at: T.7
E137  Optimized cutpoints vary strongly across folds or regress against fixed boundaries.
     how: Compare fold-specific thresholds and held-out scores with simple rounding.
     used at: T.8.1
E138  Labels are ordinal and held-out continuous predictions have systematic boundary errors.
     how: Inspect confusion around label boundaries and out-of-fold prediction histograms.
     used at: T.8.1
E139  A reliable expected label-frequency distribution is known for the evaluation population.
     how: Compare source-specific label frequencies and prior validation of distribution matching.
     used at: T.8.1
E140  Groups show different calibration errors and have enough calibration examples per label.
     how: Inspect group-wise residuals, label counts, and threshold stability.
     used at: T.8.1
E141  Discretization creates constant columns or large tied groups under a rank metric.
     how: Count unique predictions per target and run the scoring function on those columns.
     used at: T.8.1
E142  Subgroup-specific thresholds regress or depend on inaccurate group predictions.
     how: Inspect prior global-versus-group validation scores and group-assignment accuracy.
     used at: T.8.1
E143  Held-out residuals have a systematic offset or scale error relevant to the metric.
     how: Plot predicted versus observed values and check the metric’s invariance to monotonic transforms.
     used at: T.8.2
E144  Predicted class proportions or confidence disagree systematically with held-out soft labels.
     how: Compare reliability plots and predicted versus target class distributions.
     used at: T.8.2
E145  An auxiliary output predicts residual errors of the main output.
     how: Measure residual association on held-out data and verify shared row IDs.
     used at: T.8.2
E146  A metadata-defined subset has a reproducible error pattern and its defining fields exist at test time.
     how: Inspect subgroup residuals and train/test metadata availability.
     used at: T.8.2
E147  The metric is invariant to the proposed rescaling and no calibration defect has been demonstrated.
     how: Inspect the metric definition and compare held-out ranks before and after the transform.
     used at: T.8.2
E148  Allowed outputs are discrete or quasi-discrete and the metric rewards their correct ordering or agreement.
     how: Inspect labels, output constraints, and scoring code.
     used at: T.8
E149  Outputs remain continuous or probabilistic but exhibit a systematic held-out calibration defect.
     how: Inspect residual plots and probability reliability summaries.
     used at: T.8
E150  The current pipeline crashes or produces missing, incompatible, or implausible predictions.
     how: Inspect tracebacks, artifact compatibility, prediction ranges, and submission rows.
     used at: T
E151  Existing comparisons are confounded, noisy, unrepresentative, or too expensive to complete.
     how: Inspect trial diffs, repeated scores, validation membership, and runtime logs.
     used at: T
E152  Training labels, population coverage, or target construction fail to represent the evaluated outcome.
     how: Inspect source distributions, label quality, censoring, and target definitions.
     used at: T
E153  Available input information is discarded or obscured by current feature construction.
     how: Compare raw examples with feature provenance and error slices.
     used at: T
E154  The current model has plateaued and compatible alternative learners or checkpoints exist.
     how: Inspect controlled model trials and artifact inventory.
     used at: T
E155  Training diagnostics show underfitting, overfitting, unstable convergence, or objective mismatch.
     how: Inspect learning curves, capacities, objectives, and per-group errors.
     used at: T
E156  Multiple validated prediction sources or compatible repeated views have complementary errors.
     how: Compare aligned held-out predictions and residual correlations.
     used at: T
E157  Predictions show an output-scale or label-boundary mismatch despite a valid model.
     how: Inspect calibration plots, ordinal confusion, and output requirements.
     used at: T
E158  Train/test feature computation is asymmetric — some derived columns or transformations are applied to training data but not to test data (or vice versa).
     how: Compare the feature-engineering code paths for train and test: check that every derived column, encoding, and transformation applied during training is also applied identically at prediction time.
     used at: T.1
E159  The leaderboard score is approximately (1 − expected), indicating a sign or ordering inversion in the predictions rather than a model or execution failure.
     how: Compare the submitted score against the expected local CV score; if the public score ≈ 1 − CV score (or the ranking is perfectly inverted), check whether prediction probabilities or labels have been flipped.
     used at: T.1
E160  Checkpoint or model artifact file paths do not resolve to existing files in the current environment.
     how: Verify that all referenced checkpoint/model file paths exist and are accessible in the inference environment.
     used at: T.1.1
E161  Configuration or logging references point to the wrong model name or architecture, indicating a copy-paste error that may affect runtime settings.
     how: Check that model name strings in config, logging, and weight-loading code all refer to the intended architecture.
     used at: T.1.1
E162  The mask token position index is not correctly computed, typed, or propagated from tokenization through the dataset to the model forward pass.
     how: Trace the mask_token_indexes value from the encoding function through the dataset and collator to the model, checking type (scalar vs list) and presence at each stage.
     used at: T.1.1
E163  A config file default value differs from the setting used when the checkpoint was trained.
     how: Compare each config parameter's current default against the value recorded or implied during checkpoint training (e.g., use_cope, n_labels).
     used at: T.1.1
E164  Column renaming or aliasing has introduced duplicate column names in the feature matrix.
     how: Check that all column names in the final feature DataFrame are unique after any renaming or aggregation aliasing steps.
     used at: T.1.1
E165  Marginal gains from recent incremental changes are declining toward zero, suggesting diminishing returns in the current search direction.
     how: Compare score improvements across the last several iterations; if gains are shrinking and approaching zero, the sweep is near saturation.
     used at: T.2
E166  Multiple configurations have been evaluated locally without leaderboard submission, indicating local validation is being used to screen candidates.
     how: Check whether recent hyperparameter runs were submitted or only evaluated via local validation.
     used at: T.2
E167  Training diagnostics (e.g., loss curves, convergence plots) are not being captured or visualized, preventing diagnosis of training issues.
     how: Check whether training loss or other diagnostic metrics are logged and available for inspection.
     used at: T.2
E168  A code bug (e.g., logic inversion, type error, wrong variable) causes the pipeline to select wrong data or crash before producing valid results.
     how: Inspect recent code changes for obvious logical errors, inversions, or type mismatches that corrupt the evaluation.
     used at: T.2
E169  A global initialization or library call silently overrides user-specified configuration parameters, invalidating the intended experiment.
     how: Check whether any init calls or library defaults override the explicitly set hyperparameters.
     used at: T.2
E170  Intermediate artifacts (e.g., logits, component predictions) needed for planned experiments are not cached or saved, blocking the experiment.
     how: Check whether the intermediate outputs required for the next evaluation step have been persisted from prior runs.
     used at: T.2
E171  Local OOF predictions are available but not being used for offline evaluation, causing unnecessary leaderboard submissions for tuning.
     how: Check whether OOF predictions exist locally and whether weight/blend tuning is being done via LB submissions instead of local evaluation.
     used at: T.2
E172  No offline validation metric is available, so each candidate evaluation requires a leaderboard submission.
     how: Check whether a local validation score can be computed or if the only feedback mechanism is the leaderboard.
     used at: T.2
E173  The feature representation used for grouping or clustering does not capture the relevant structure (e.g., text similarity) as well as an alternative representation would.
     how: Compare the current clustering input features against alternative representations that better capture the task-relevant structure.
     used at: T.2
E174  Ground-truth or curated group labels are available externally and could replace synthetic/unsupervised groupings for more reliable evaluation splits.
     how: Check whether an external dataset with actual labels (topic, source, etc.) is accessible to replace unsupervised cluster assignments.
     used at: T.2
E175  Stacking or auxiliary features are loaded from external pre-computed files rather than generated in-pipeline, risking staleness or file-not-found errors.
     how: Check whether auxiliary feature files are generated within the current pipeline or loaded from external pre-computed sources.
     used at: T.2
E176  A model component lacks proper fold-wise training and held-out prediction infrastructure, contaminating OOF estimates used for evaluation or ensembling.
     how: Check whether each model component produces OOF predictions from properly held-out fold models rather than in-sample predictions.
     used at: T.2
E177  A non-feature column (e.g., essay_id or target) is included in the feature matrix passed to the CV splitter or clustering step, causing incorrect group assignments or leakage.
     how: Inspect the columns passed to KMeans.fit() or the CV splitter and check whether non-feature columns (IDs, targets) are present.
     used at: T.2.2
E178  The KMeans clustering input is malformed (e.g., non-numeric data or column names instead of feature values), producing meaningless cluster assignments.
     how: Check the dtype and shape of the array passed to KMeans.fit() to confirm it contains valid numeric feature values.
     used at: T.2.2
E179  Converting the sparse TF-IDF matrix to dense for KMeans causes a memory error, requiring a sparse-compatible approach.
     how: Check whether .toarray() is called on the TF-IDF matrix and whether the resulting dense array fits in available memory.
     used at: T.2.2
E180  The number of distinct topic/group labels is known and can inform the choice of n_splits for group-based CV.
     how: Count the number of unique group labels and compare to the current n_splits setting.
     used at: T.2.2
E181  Topic or prompt metadata from the dataset is already available and was previously used as group labels in the pipeline.
     how: Check whether topic/prompt columns from the parquet dataset have been used as GroupKFold labels in recent pipeline versions.
     used at: T.2.2
E182  The alternative CV/OOF implementation repeatedly fails to run or submit, making it impractical as a validation strategy.
     how: Review recent submission attempts for the alternative OOF approach and check whether they produced runtime or submission errors.
     used at: T.2.2
E183  Per-sample weighting was already attempted and did not improve CV/LB performance, motivating a fold-structure change instead.
     how: Check recent experiment logs for sample-weighting attempts and whether they yielded score improvements.
     used at: T.2.2
E184  Forcing representative-subgroup rows into both train and validation sides of every fold will make validation scores more reflective of test performance.
     how: Check whether a known OOD or minority subpopulation exists that should appear in every fold's validation set to match expected test distribution.
     used at: T.2.2
E185  GroupKFold by prompt produced a worse LB score than StratifiedKFold with forced minority-subpopulation inclusion in a previous comparison.
     how: Compare LB scores from GroupKFold-by-prompt versions versus StratifiedKFold with forced inclusion versions in the experiment log.
     used at: T.2.2
E186  The previous ad-hoc index augmentation logic for forcing subpopulation samples into folds was fragile and could be replaced by a principled group-based split.
     how: Review the current fold-construction code for manual index manipulation that could be replaced by a standard grouped or stratified splitter.
     used at: T.2.2
E187  The existing ensemble members use a specific KFold configuration (n_splits, seed) that the new member must match for fold alignment.
     how: Check whether other ensemble components depend on a shared fold structure and whether the new split would break OOF alignment.
     used at: T.2.2
E188  The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
     how: Check whether the current eval_metric was already configured to a suitable proxy in a previous code version, making further changes redundant.
     used at: T.2.3
E189  A previously deleted or out-of-scope variable is still referenced downstream, causing a runtime error.
     how: Inspect the code for references to variables that were deleted, renamed, or never defined in the current scope.
     used at: T.2.4
E190  Reducing the number of seed replicas meaningfully reduces peak GPU memory without losing too much ensemble diversity.
     how: Estimate memory per replica and check whether halving replicas frees enough memory to fit within device limits.
     used at: T.2.4
E191  The current hyperparameter ceiling (e.g., n_estimators) is too low for the model to converge, requiring a higher ceiling with early stopping.
     how: Check training logs for whether the model hit the iteration cap without early stopping triggering.
     used at: T.2.4
E192  The data can be partitioned by entity ID boundaries so that each chunk is independently processable through the pipeline.
     how: Check whether the aggregation/feature pipeline has no cross-entity dependencies, allowing chunked processing.
     used at: T.2.4
E193  A previous version already split a memory-heavy operation into multiple calls, indicating the single-call approach caused OOM.
     how: Review version history for evidence that the monolithic call was previously refactored due to memory failures.
     used at: T.2.4
E194  The GPU library's public API for a required function fails at runtime, requiring use of an internal/private API path or CPU fallback.
     how: Check runtime error logs for import or API call failures on the GPU code path.
     used at: T.2.4
E195  A global initialization routine overrides manually-set configuration values, preventing experimentation with those parameters.
     how: Trace the initialization code to see if it resets the parameter after the manual assignment.
     used at: T.2.4
E196  The previous version failed to produce a submission (no LB score), so a re-run with no or minimal code changes is the cheapest way to obtain feedback.
     how: Check whether the last version produced a valid submission file and LB score.
     used at: T.2.4
E197  Cached artifacts loaded from disk may not contain the expected columns or variables, requiring a fallback path.
     how: Inspect the cached file contents against the expected schema or variable list.
     used at: T.2.4
E198  The fold count does not evenly divide the data or exceeds the memory/time budget, requiring adjustment.
     how: Check whether the chosen fold count causes uneven splits or pushes total runtime/memory beyond session limits.
     used at: T.2.4
E199  The test set size at submission time can be detected to automatically distinguish debug/public-test from full private-test runs.
     how: Check whether the test file row count or file size differs between environments and can gate pipeline behaviour.
     used at: T.2.4
E200  The save/load toggle for cached features is inconsistent across versions, leaving the cache stale or the pipeline broken.
     how: Verify that the save path was executed in a prior version and the load path references the same file with matching schema.
     used at: T.2.4
E201  Trained model objects are not persisted to disk, requiring full retraining when only inference or ensembling code changes.
     how: Check whether model checkpoints are saved after training and whether the inference path can load them independently.
     used at: T.2.4
E202  The model is currently trained on a subset of the available labeled data rather than the full labeled set.
     how: Check whether the training routine uses a strict train split (e.g., X_train, y_train) instead of the complete labeled dataset (X, y).
     used at: T.3
E203  Pseudo-labeling has already been validated as beneficial for at least one model family in this pipeline.
     how: Check past experiment logs to see whether pseudo-labeling was tried and yielded a measurable improvement for any model component.
     used at: T.3
E204  A holdout split is currently active and the expert is considering refitting on full data for final submission.
     how: Check whether the current pipeline reserves a validation holdout and whether the expert intends to retrain on all labeled data for the submission model.
     used at: T.3
E205  The current pipeline trains on all data without a holdout, leaving no local validation signal for iterating.
     how: Check whether the training routine uses all labeled rows with no reserved validation set, removing the ability to locally evaluate changes.
     used at: T.3
E206  A baseline score from a prior filtering strategy (e.g., union/OR-based) is available to compare against the proposed filtering change.
     how: Check whether a recorded score from the previous filtering approach exists so the effect of the new membership change can be measured.
     used at: T.3.1
E207  The proposed membership change risks reducing the training set size enough to cause underfitting.
     how: Estimate the resulting training set size after the membership change and assess whether it is large enough to support the model's capacity.
     used at: T.3.1
E208  The effect of the most recent training-membership change has not yet been scored, so its impact is unknown.
     how: Check whether the last membership edit has been evaluated on the leaderboard or a holdout before making further changes.
     used at: T.3.1
E209  Previous attempts to add auxiliary/extra labeled data worsened or failed to improve the score.
     how: Review past experiment logs to see whether incorporating extra data degraded performance relative to the baseline without it.
     used at: T.3.1
E210  Auxiliary data is isolated into a separate training stage to prevent contamination of later fine-tuning stages.
     how: Check whether the training pipeline separates extra data into a dedicated early stage rather than mixing it with the primary data throughout.
     used at: T.3.1
E211  Previous attempts to add auxiliary/extra data improved the score, supporting their inclusion.
     how: Review past experiment logs to confirm whether incorporating extra data yielded a better score than the baseline without it.
     used at: T.3.1
E212  The score impact of adding extra data is ambiguous or inconclusive across prior experiments, warranting a controlled comparison.
     how: Check whether past results with and without extra data are mixed or confounded, making the net effect unclear.
     used at: T.3.1
E213  A weak ensemble member trained without pseudo-labels degraded ensemble performance, suggesting it needs retraining with pseudo-labels before inclusion.
     how: Check whether the candidate member was trained with pseudo-labels; if not, its poor standalone quality may explain ensemble degradation.
     used at: T.3.1
E214  Oversampling the matching subset outperformed full filtering in prior experiments.
     how: Review whether partial rebalancing (oversampling) was tested against hard filtering and which yielded a better score.
     used at: T.3.1
E215  The evaluation metric penalizes synthetic oversampling or rebalancing strategies that distort ordinal calibration.
     how: Check whether the metric (e.g., QWK) rewards calibrated ordinal predictions, making naive oversampling counterproductive.
     used at: T.3.1
E216  Feature count sweeps around the current best have not improved the score, suggesting the current selection granularity is near-optimal.
     how: Compare leaderboard scores across feature-count variants (e.g., more and fewer than current best) and check whether any outperform the baseline.
     used at: T.4
E217  A recently added feature group's marginal contribution has not been measured in isolation.
     how: Run an ablation removing only the new feature group and compare validation/LB score to the version with it included.
     used at: T.4
E218  The precomputed feature-selection artifact was generated on a different feature space than the current one and may omit or misrank features.
     how: Compare the column set used when the selection artifact was created against the current feature matrix and check for mismatches.
     used at: T.4
E219  Domain-specific composite or interaction features (e.g., risk scores, interaction terms) are absent and could provide informative signal.
     how: Review the feature matrix for the presence of known domain-relevant composite variables and interaction terms.
     used at: T.4
E220  Different ensemble member models would benefit from tailored feature representations rather than a single shared feature set.
     how: Check whether all ensemble components currently consume the same feature matrix and whether any would improve with a model-specific representation.
     used at: T.4
E221  The checkpoint loading mechanism may select unintended or suboptimal files (e.g., via glob patterns or directory mismatches).
     how: Inspect the checkpoint loading code (glob patterns, directory paths) and verify the actually loaded file matches the intended one.
     used at: T.5
E222  Reinitializing or unfreezing specific layers (e.g., last N transformer layers) is a viable technique to reduce overfitting for the current data regime.
     how: Check whether the dataset size and fine-tuning setup would benefit from partial reinitialization, referencing known best practices.
     used at: T.5
E223  The current edit isolates the checkpoint/model change by holding all other settings (post-processing, TTA, data pipeline) constant.
     how: Diff the current edit against the previous version and confirm only the model/checkpoint variable changed.
     used at: T.5
E224  Previous checkpoint or model swaps have caused score regressions, indicating that newer or larger is not always better and systematic comparison is needed.
     how: Review the history of checkpoint/model swaps and their leaderboard scores to identify regressions.
     used at: T.5
E225  Previous checkpoint comparisons were confounded by simultaneous changes to other settings (TTA, post-processing, data pipeline).
     how: Review version history to check whether prior checkpoint swaps also changed other variables.
     used at: T.5
E226  The checkpoint/model sweep is being conducted in a systematic sequential order so regressions are quickly detected.
     how: Inspect the sweep plan or version history to confirm an orderly progression through candidates.
     used at: T.5
E227  The actual edit matches the stated intent (e.g., scaling model size vs. merely swapping a checkpoint within the same size).
     how: Compare the intent description with the actual code diff to verify alignment.
     used at: T.5
E228  A later training stage (e.g., stage 3 vs. stage 2) may be overfitting, and an earlier-stage checkpoint could generalize better.
     how: Compare validation and leaderboard scores across training stages to detect overfitting in later stages.
     used at: T.5
E229  Other recently tried improvements (e.g., TTA) yielded only marginal gains, suggesting checkpoint/model selection may offer a larger improvement.
     how: Compare the magnitude of recent gains from non-model changes against expected gains from model replacement.
     used at: T.5
E230  A different model class or architecture variant with matching checkpoints is available but has not yet been tried.
     how: Inventory available model classes and their checkpoints; check which have not been evaluated.
     used at: T.5
E231  Multiple fold checkpoints from the same experiment are available and can be ensembled together rather than tested individually.
     how: Check the checkpoint directory for multiple fold files and whether the inference pipeline supports multi-fold ensembling.
     used at: T.5
E232  All available checkpoints of this type have already been evaluated on the leaderboard, leaving no untested variants.
     how: Cross-reference the list of available checkpoints against the submission history.
     used at: T.5
E233  The replacement model/checkpoint requires a different output transformation or inference code path that the current pipeline does not support.
     how: Check whether the new model's output format (e.g., logits vs. probabilities, different head) matches the current post-processing code.
     used at: T.5
E234  The replacement learner has a known implementation bug (e.g., in its custom metric or objective) that would prevent correct training or inference.
     how: Review issue trackers, code comments, or prior experiment logs for known bugs in the candidate model's implementation.
     used at: T.5
E235  The best-scoring configuration used a specific mix of checkpoint variants across folds, and untested per-fold alternatives may improve individual fold contributions.
     how: Map which checkpoint variant was used for each fold in the best submission and identify untested per-fold alternatives.
     used at: T.5
E236  The replacement fully swaps out one model family for another (rather than blending/adding alongside), risking loss of complementary signal from the removed component.
     how: Check whether the edit removes an existing model entirely rather than adding the alternative as an additional ensemble member.
     used at: T.5.1
E237  A known variant of the current learner family (e.g., DART for boosting) offers built-in regularization that may address the current limitation.
     how: Identify whether a closely related algorithmic variant within the same library exists that directly targets the observed issue (e.g., dropout boosting for overfitting).
     used at: T.5.1
E238  The alternative learner is significantly slower per iteration/fold, making full cross-validation or hyperparameter search impractical within time/compute constraints.
     how: Estimate wall-clock cost of the alternative relative to the current learner for the same CV/tuning protocol.
     used at: T.5.1
E239  The alternative learner variant has known incompatibilities with standard training utilities (e.g., early stopping, callbacks) that require special handling.
     how: Check documentation or prior experience for known conflicts between the alternative and the training pipeline's control mechanisms.
     used at: T.5.1
E240  The proposed alternative was already tried and reverted in a prior iteration, so the replacement has already been evaluated.
     how: Review edit history to determine whether the same alternative was previously attempted and its outcome.
     used at: T.5.1
E241  The prior attempt with this alternative confounded multiple hyperparameter changes, so a controlled re-test isolating only the model swap is warranted.
     how: Check whether previous trials of the alternative changed additional hyperparameters simultaneously, preventing clean attribution.
     used at: T.5.1
E242  The current model variant has reached a strong, stable best score that serves as a clear baseline for evaluating the alternative.
     how: Verify that the incumbent model's best score is well-established and not still improving rapidly.
     used at: T.5.1
E243  A smaller capacity increase already improved performance, suggesting further scaling up may yield additional gains.
     how: Check whether an intermediate-capacity variant showed improvement over the smallest, motivating a further scale-up.
     used at: T.5.1
E244  Disabling other ensemble members allows isolating the replaced component's contribution to diagnose whether the architecture swap helps.
     how: Check whether the evaluation setup can isolate the swapped model's effect from ensemble interactions.
     used at: T.5.1
E245  The input representation is low-information or non-standard (e.g., synthetic channels), limiting the benefit of a higher-capacity backbone.
     how: Assess whether the input data's information content is sufficient to exploit the additional capacity of the larger alternative.
     used at: T.5.1
E246  A larger-capacity variant of the alternative has already been tested and scored worse than a smaller variant, confirming diminishing or negative returns from scaling.
     how: Review leaderboard or CV results comparing different capacity levels of the same backbone family.
     used at: T.5.1
E247  Run-to-run variance has been measured and is small relative to the expected gain from the model swap, so score differences are likely signal rather than noise.
     how: Compare observed submission variance (identical resubmissions) against the magnitude of expected improvement from the alternative.
     used at: T.5.1
E248  The model being replaced was part of the best-scoring ensemble configuration, and its prior displacement caused a regression.
     how: Check whether removing or replacing this specific model previously led to a score drop.
     used at: T.5.1
E249  The alternative model requires reduced batch size or other resource adjustments to fit within hardware constraints.
     how: Check whether the alternative's memory/compute footprint exceeds current hardware limits at the current batch size.
     used at: T.5.1
E250  A prior full-swap attempt was not submitted or failed, motivating a more incremental (selective/staged) replacement strategy.
     how: Check edit history for incomplete or failed attempts at the same swap that suggest a staged approach is needed.
     used at: T.5.1
E251  The alternative model's hyperparameters have not been separately optimized, so initial results may underestimate its true potential.
     how: Check whether the alternative was evaluated with tuned hyperparameters or only with defaults/transferred settings.
     used at: T.5.1
E252  An earlier attempt with this alternative scored poorly, but the pipeline has since been substantially improved, warranting a re-evaluation.
     how: Check whether the pipeline context (features, preprocessing, training protocol) has changed significantly since the last trial of this alternative.
     used at: T.5.1
E253  A specific capacity variant of the alternative has not yet been tested in the current pipeline.
     how: Check the edit/submission history for whether this particular variant has been evaluated under current conditions.
     used at: T.5.1
E254  Historical best scores were achieved with a specific model variant, providing evidence for which alternative to try.
     how: Review the leaderboard history to identify which model variant achieved the highest score.
     used at: T.5.1
E255  In a previous pipeline version, larger backbones consistently outperformed smaller ones, establishing a scaling trend.
     how: Review historical results across backbone sizes in the prior pipeline to determine the capacity-performance relationship.
     used at: T.5.1
E256  The capacity-performance scaling relationship has reversed in the current pipeline compared to the previous one.
     how: Compare backbone size vs. score trends between the old and new pipeline versions.
     used at: T.5.1
E257  A previous attempt with this alternative in the current pipeline scored worse than expected, but potential fixes or confounds warrant a retry.
     how: Check whether the prior poor result could be attributed to a fixable issue rather than inherent unsuitability.
     used at: T.5.1
E258  The alternative model was built but never submitted/evaluated on the leaderboard, so its true performance is unknown.
     how: Check whether the alternative has an actual leaderboard or holdout score, or only local/CV results.
     used at: T.5.1
E259  The alternative model family was given a fair trial and scored substantially worse than the current learner on the same task.
     how: Review prior evaluation results comparing the alternative to the incumbent under comparable conditions.
     used at: T.5.1
E260  The alternative learner offers hardware acceleration (e.g., GPU training) that could speed up hyperparameter sweeps compared to the current setup.
     how: Check whether the alternative supports GPU or other acceleration not currently utilized.
     used at: T.5.1
E261  The alternative architecture has been tested with multiple configurations and all score below the current best.
     how: Count how many distinct configurations of the alternative have been evaluated and whether any matched or exceeded the incumbent.
     used at: T.5.1
E262  A previous change to the aggregation head degraded performance, indicating the current head design is suboptimal.
     how: Check experiment logs for whether prior head modifications caused score regressions.
     used at: T.5.2
E263  Public or known solutions for this task use auxiliary classification heads alongside regression to regularize on small data.
     how: Review public notebooks, papers, or competition solutions to see if auxiliary heads are a common effective strategy.
     used at: T.5.2
E264  The proposed aggregation head is incompatible with existing trained checkpoints, requiring retraining or architectural bridging.
     how: Check whether the new head's input/output shapes and variable names match the saved checkpoint structure.
     used at: T.5.2
E265  The auxiliary classification head is effectively disabled by the current configuration (e.g., num_bins=1).
     how: Inspect the model config to see if the auxiliary head parameters render it a no-op.
     used at: T.5.2
E266  The auxiliary binning/classification head has shown inconsistent benefit across different checkpoint and pooling configurations.
     how: Review experiment logs comparing runs with and without the auxiliary head across different model variants.
     used at: T.5.2
E267  The aggregation head lacks normalization layers (e.g., LayerNorm, BatchNorm) before the final projection, causing scale variance or training instability.
     how: Inspect the head architecture for the presence and correct wiring of normalization layers between pooling and the regression output.
     used at: T.5.2
E268  The multi-branch fusion strategy (concatenation vs. averaging) has been tested but its isolated contribution is unclear or underperforming.
     how: Review experiment history for runs comparing concatenation fusion, averaging fusion, and single-head baselines with controlled variables.
     used at: T.5.2
E269  Batch normalization in the head is causing training instability or score degradation due to small batch sizes or incorrect wiring.
     how: Check whether BatchNorm layers in the head are correctly applied to the tensor flow and whether batch sizes are large enough for stable statistics.
     used at: T.5.2
E270  Previous augmentation changes (e.g., spectrogram blackout, time-cropping/masking) did not clearly improve scores and need further iteration or reversion.
     how: Compare held-out scores from augmentation variants (v158 time-cropping, v160-v161 blackout) against the baseline to determine if any augmentation yielded a clear improvement.
     used at: T.6.2
E271  Multiple hyperparameters were changed simultaneously in a previous edit, so individual effects are confounded and need isolated testing.
     how: Review the changelog to see whether the last edit altered more than one training control (e.g., learning rate and dropout together), preventing attribution of the score change to either one alone.
     used at: T.6.2
E272  Learning rates on both sides of the current best have been tried, enabling a bisection/narrowing search strategy.
     how: Check the log of tried learning rates and their scores to confirm that values both above and below the current best have been evaluated, supporting a narrowing search.
     used at: T.6.2
E273  A previously tried hyperparameter value was tested under different regularization settings, so retrying it with current regularization is warranted.
     how: Check whether a previously evaluated learning rate (or other hyperparameter) was tested before the current regularization (e.g., dropout) was tuned, meaning its earlier result may not reflect its potential under current settings.
     used at: T.6.2
E274  No degradation has yet been observed from increasing class weight in the current sweep, so the sweep should continue upward.
     how: Check local validation scores across the class-weight sweep so far and confirm none have degraded relative to the starting point.
     used at: T.6.3
E275  The class-weight sweep has only been evaluated in a fast/debug local mode without leaderboard submission, so no external signal confirms the weight changes help.
     how: Check whether any of the weight-sweep runs were submitted to the leaderboard or only evaluated locally in reduced-fold/debug mode.
     used at: T.6.3
E276  The previous best class-weight value did not clearly outperform nearby alternatives in local validation, motivating further exploration in a different direction.
     how: Compare local validation scores of the current best weight against neighboring values and check whether the advantage is statistically clear.
     used at: T.6.3
E277  The expert has already swept the weighting parameter through a wide range and is now narrowing into a fine-grained region near the best-performing value.
     how: Review the history of weight values tried and confirm both extreme and moderate values have been tested, with the search now focusing on a narrow neighborhood.
     used at: T.6.3
E278  The previous class-weight setting has been evaluated and the pre-planned sweep schedule calls for the next step.
     how: Check whether a systematic sweep plan exists and the next value in that plan has not yet been tested.
     used at: T.6.3
E279  Previous weight values in one direction (e.g., above 1.0) did not yield improvements, suggesting the optimal weight lies in the opposite direction.
     how: Review submitted or validated scores for weight values above 1.0 and confirm none improved over the baseline.
     used at: T.6.3
E280  The previously added sample/class weights failed to improve validation performance or caused instability, motivating a revert.
     how: Compare validation scores before and after adding the sample weights and check for degradation or training instability.
     used at: T.6.3
E281  An extreme weighting parameter value performed poorly (not submitted), so the search should return to the neighborhood of the previously best value.
     how: Check whether the extreme value was submitted or scored well locally; if not, confirm the best-known value and plan to search near it.
     used at: T.6.3
E282  The best-known score used a specific weighting parameter value combined with another setting; reverting to that value while simplifying the other setting may recover or exceed that score.
     how: Identify the exact parameter combination that produced the best score and check whether the current configuration has drifted from it.
     used at: T.6.3
E283  Dropout or other stochastic layers may be active/inactive at inference, so toggling their parameters may or may not change predictions.
     how: Check whether the model is in eval mode and whether stochastic layers (e.g., dropout) actually affect inference outputs.
     used at: T.7
E284  Some TTA augmentation variants may not preserve the semantic meaning of the input and could degrade rather than improve predictions.
     how: Verify that each TTA transform (e.g., spectral flip, time reversal) is semantically valid for the data domain.
     used at: T.7
E285  The ensemble membership has been inadvertently changed (members added or removed) and no longer matches the known-best configuration.
     how: Compare the current ensemble member list against the last validated best configuration.
     used at: T.7
E286  The cross-validation pipeline has bugs (e.g., index mapping errors) that prevent valid out-of-fold predictions from being generated.
     how: Inspect the CV loop for index-mapping or accumulation bugs that would corrupt OOF predictions.
     used at: T.7
E287  The submission format requires predictions to be bounded probability-like values (e.g., in [0,1]).
     how: Check the competition or task submission requirements to see whether outputs must be probabilities or bounded in a specific range.
     used at: T.8
E288  The evaluation metric is invariant to monotonic transformations, making certain calibration adjustments (e.g., clipping) irrelevant to the score.
     how: Determine whether the metric (e.g., Spearman correlation) is rank-based or otherwise invariant to monotonic transforms, which would render bounding/clipping operations score-neutral.
     used at: T.8
E289  Public high-scoring solutions or known best practices for this task use threshold optimization (e.g., Nelder-Mead on OOF) to maximize the evaluation metric.
     how: Check public kernels, competition discussions, or prior experiments for evidence that optimized thresholds outperform naive rounding.
     used at: T.8.1
E290  No naive-rounding baseline score exists yet to compare against optimized thresholds.
     how: Check whether a simple rounding baseline (e.g., round to nearest integer) has been scored on the leaderboard or validation set.
     used at: T.8.1
E291  Simple rounding produced substantially worse scores than optimized threshold rounding, confirming the value of threshold optimization.
     how: Compare leaderboard or CV scores between naive rounding and optimized thresholds.
     used at: T.8.1
E292  The discretization code path has a bug (missing column, name inconsistency, or incorrect guard) that prevents it from executing correctly.
     how: Trace the code to verify that all required columns/variables are populated and named consistently at the point the discretization function is called.
     used at: T.8.1
E293  The current threshold values are already optimized on OOF/validation data (not just naive midpoints).
     how: Inspect the code or logs to determine whether the threshold array was produced by an optimization routine or is a set of fixed midpoints.
     used at: T.8.1
E294  Out-of-fold predictions are available from cross-validation to serve as the optimization target for threshold tuning.
     how: Check whether OOF prediction files exist and cover the full training set for the current model/checkpoint.
     used at: T.8.1
E295  Complex post-processing may interact with the training objective; simplifying to clip+round first would isolate each component's effect.
     how: Check whether the current post-processing was validated independently of other pipeline changes.
     used at: T.8.1
E296  The training objective or model predictions are currently unstable or incorrect, making threshold tuning premature.
     how: Inspect training logs and OOF prediction distributions for signs of instability, divergence, or incorrect loss computation.
     used at: T.8.1
E297  The base model predictions have meaningful per-target variation and ordering before applying discretization.
     how: Compute standard deviation and rank correlation of raw predictions per target column to confirm they are not degenerate.
     used at: T.8.1
E298  The target column has only two distinct label values, making a simple threshold binarization the appropriate discretization.
     how: Count distinct values in the training labels for each target column.
     used at: T.8.1
E299  A per-column epsilon/coefficient merging approach was previously validated to produce meaningful score improvements.
     how: Review experiment logs for prior per-column coefficient tuning results and their LB/CV impact.
     used at: T.8.1
E300  Discretized columns have inconsistent scales that may not match submission format expectations.
     how: Check whether the submission format requires specific value ranges (e.g., 0-1) and whether the discretized outputs conform.
     used at: T.8.1
E301  The threshold or heuristic used to detect degenerate/constant columns is fragile and may misclassify columns.
     how: Test the detection criterion (e.g., std < 0.05) against actual column distributions to check for false positives/negatives.
     used at: T.8.1
E302  A curated explicit column list for post-processing scored higher than a dynamic all-columns approach.
     how: Compare LB/CV scores between the curated column list version and the dynamic version.
     used at: T.8.1
E303  Some threshold conditions have gaps or overlaps that leave certain prediction ranges without an assigned discrete label.
     how: Enumerate all threshold intervals and verify they partition the full prediction range without gaps or overlaps.
     used at: T.8.1
E304  Multiple thresholds are being changed simultaneously rather than incrementally, making it impossible to attribute score changes to individual threshold adjustments.
     how: Count how many thresholds differ between the current and previous iteration and compare against the intended incremental tuning strategy.
     used at: T.8.1
E305  A zero-variance or anchor example exists in the data that can serve as a fixed reference point for bias correction.
     how: Check whether any training/calibration examples have zero or near-zero uncertainty (e.g., standard_error==0) that could anchor an offset correction.
     used at: T.8.2
E306  The calibration/evaluation set is too small to reliably estimate correction parameters, risking overfitting the calibration.
     how: Check the number of held-out or evaluation samples relative to the number of calibration parameters being fit.
     used at: T.8.2
E307  The proposed per-class or per-subset correction factors have not been tested in isolation to confirm they individually help.
     how: Check whether each calibration component has been ablated independently against the target metric.
     used at: T.8.2
E308  The newer model checkpoint is already better calibrated, making the previously helpful correction unnecessary or harmful.
     how: Compare raw (uncalibrated) outputs of the current model against the previous model to see if the systematic defect has already been reduced.
     used at: T.8.2
E309  Raw model outputs include boundary values (exactly 0 or 1) or out-of-range values that could cause numerical issues during calibration transforms.
     how: Inspect the distribution of raw predictions for clipping at boundaries or values outside the expected range.
     used at: T.8.2
E310  The calibration hyperparameter has not been fully swept; the current best value sits at the boundary of the explored range.
     how: Check whether the best-performing calibration parameter is at the edge of the search range, suggesting further exploration in that direction.
     used at: T.8.2
E311  The calibration transform is applied inside the training loop (not purely post-hoc), so it may alter gradient flow or interact with ensembling rather than being a simple monotonic rescaling.
     how: Check whether the calibration step is applied after all training and ensembling, or whether it is embedded in the forward pass where it could affect optimization.
     used at: T.8.2
E312  The proposed correction magnitude has not been validated against a held-out or cross-validation metric.
     how: Check whether the correction value was chosen based on measured residual statistics or is an arbitrary guess.
     used at: T.8.2