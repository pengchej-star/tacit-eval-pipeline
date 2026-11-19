# evidence/registry.md — one definition per check, shared across nodes

E01  The checkpoint reports missing keys or incompatible layer dimensions.
     how: Compare the saved state dictionary and configuration with the instantiated model and loading log.
     used at: T.1.1
E02  The model loads, but tokenization, normalization, feature order, or input shape differs from training.
     how: Compare a fixed example processed by the saved training pipeline and the inference pipeline.
     used at: T.1.1
E03  Execution stops at an import, file lookup, API call, or device transfer.
     how: Read the first exception and inspect the installed version, resolved file path, and tensor devices.
     used at: T.1.1
E04  Joined features or prediction files have different identifier order or coverage.
     how: Compare identifier sets and ordered hashes before and after each merge; inspect duplicate keys.
     used at: T.1.2
E05  Some enabled models are skipped, repeated, or assigned the wrong fold or weight.
     how: Log model and fold identifiers, prediction checksums, accumulator updates, and the sum of active weights.
     used at: T.1.2
E06  The first divergent value appears inside feature construction or the model forward pass.
     how: Trace one known example through shapes, axes, derived columns, and intermediate values.
     used at: T.1.2
E07  Internal predictions are plausible but the exported values, sign, or schema are wrong.
     how: Compare the saved file with the final array and the required prediction convention and row identifiers.
     used at: T.1.2
E08  Failure begins when loading a new artifact or moving to another environment.
     how: Locate the first failure in the log and compare the artifact and environment manifests.
     used at: T.1
E09  The notebook runs but produces implausible, missing, or invariant predictions.
     how: Inspect output variance, member checksums, sample identifiers, and a known labeled batch.
     used at: T.1
E10  Several new components have never completed an end-to-end run.
     how: Check whether a representative small batch has passed through loading, preprocessing, prediction, and export.
     used at: T.1
E11  Several factors changed between the two configurations being compared.
     how: Diff configuration, feature lists, checkpoints, and preprocessing code for the two runs.
     used at: T.2.1
E12  A large regression follows changes to a previously reproducible working configuration.
     how: Compare the regression with the last saved configuration and its repeated-run range.
     used at: T.2.1
E13  Unchanged runs vary by as much as the claimed improvement.
     how: Compare repeat-run score ranges and prediction checksums with candidate deltas.
     used at: T.2.1
E14  Recent probes of the same lever fail to exceed the established noise floor.
     how: Review the run ledger for repeated non-improvements and their uncertainty.
     used at: T.2.1
E15  The target distribution is imbalanced and ordinary random folds omit rare levels.
     how: Tabulate target frequencies per candidate fold, binning continuous targets only for splitting.
     used at: T.2.2
E16  Rows share an entity, prompt, overlapping window, or other dependence that would cross random folds.
     how: Inspect identifiers, overlap, and within-group similarity across proposed train and validation partitions.
     used at: T.2.2
E17  A known training subpopulation resembles the test population more than the rest.
     how: Compare task metadata and feature or label distributions across source groups and test examples.
     used at: T.2.2
E18  The holdout removes a large share of usable training data or nested folds duplicate expensive fitting.
     how: Inspect split sizes and training plans, including how tuning is separated from evaluation.
     used at: T.2.2
E19  Recent score changes cannot be attributed to a single change or exceed neither repeat noise nor a plateau.
     how: Inspect configuration diffs and the recent score ledger.
     used at: T.2
E20  The current validation partition leaks related examples or misrepresents the test population.
     how: Audit split membership against entity identifiers, source metadata, and target distributions.
     used at: T.2
E21  Training selects models using a different metric, direction, or output convention from evaluation.
     how: Compare callback outputs on a fixed labeled batch with an independent implementation of the task metric.
     used at: T.2
E22  Configurations with better local validation repeatedly perform worse on external evaluation.
     how: Compare paired local and external scores for the same checkpoints and inspect preprocessing and population differences.
     used at: T.2
E23  Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.
     how: Count overlaps and inspect annotation confidence and per-source validation errors.
     used at: T.3.1
E24  Rare labels or the test-like subgroup receive little influence under the current loss.
     how: Compare class counts, subgroup weights, and per-group error contributions.
     used at: T.3.1
E25  Minority examples are sparse but interpolation is meaningful in the current feature space.
     how: Inspect nearest neighbors, feature types, label compatibility, and fold boundaries.
     used at: T.3.1
E26  Compatible extra labeled examples exist but differ in quality or source.
     how: Inspect auxiliary labels, identifier overlap, feature schemas, and source distributions.
     used at: T.3.1
E27  Unlabeled examples and a validated teacher are available.
     how: Inspect unlabeled coverage and teacher confidence or held-out accuracy.
     used at: T.3.1
E28  Training overfits and label-preserving perturbations are supported by the input semantics.
     how: Compare training and validation curves and inspect transformed examples with their labels.
     used at: T.3.1
E29  Each prediction entity has multiple records but the model sees only one record or a few summaries.
     how: Compare records per entity with the current aggregation specification.
     used at: T.3.2.1
E30  Time order and recent changes are discarded by current summaries.
     how: Inspect timestamp coverage and whether existing features distinguish different orderings of the same values.
     used at: T.3.2.1
E31  Related measurements have meaningful contrasts not encoded in the current features.
     how: Inspect the column definitions and their pairwise differences or ratios against the target.
     used at: T.3.2.1
E32  Missingness, category handling, quantization, or scaling differs between model families.
     how: Inspect feature dtypes, missing rates, encoder behavior, and model input requirements.
     used at: T.3.2.1
E33  Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
     how: Inspect raw text, processed text, and tokenizer output for representative samples.
     used at: T.3.2.2
E34  Lexical frequency or topic information is absent or dominated by very rare n-grams.
     how: Inspect vocabulary frequencies, sparsity, and the existing representation blocks.
     used at: T.3.2.2
E35  The target depends on document structure or language quality not explicitly represented.
     how: Review task labels and inspect paragraph, sentence, and linguistic statistics against residual errors.
     used at: T.3.2.2
E36  The current features lack contextual semantics and suitable pretrained encoders are available.
     how: Inspect existing feature blocks and held-out errors involving semantically similar but lexically different examples.
     used at: T.3.2.2
E37  Compatible out-of-fold predictions or leakage-safe auxiliary labels exist.
     how: Verify identifier coverage, fold provenance, and that each training prediction excludes its own label.
     used at: T.3.2.2
E38  Discriminative image detail is lost at the current resolution and the checkpoint supports another size.
     how: Inspect resized examples and the checkpoint’s spatial input constraints.
     used at: T.3.2.3
E39  The input window includes irrelevant context or misses the labeled interval or region.
     how: Compare crop boundaries and timestamps with annotation scope and visualized samples.
     used at: T.3.2.3
E40  Relevant frequency structure is unresolved or blurred by the current transform.
     how: Inspect spectrograms under candidate FFT, hop, and frequency ranges and the checkpoint recipe.
     used at: T.3.2.3
E41  Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
     how: Plot amplitude distributions, power spectra, and normalization statistics against training values.
     used at: T.3.2.3
E42  Unused channels or modalities contain potentially complementary information, or existing branches may be redundant.
     how: Inspect channel definitions, per-branch ablations, and alignment with the same labeled interval.
     used at: T.3.2.3
E43  The raw input consists of repeated numeric or categorical observations per entity.
     how: Inspect the schema, entity identifiers, and rows per entity.
     used at: T.3.2
E44  The task is driven by text and the current representation misses lexical, semantic, or structural information.
     how: Inspect raw examples and current feature extraction code.
     used at: T.3.2
E45  The input is an image, signal, or spectrogram whose spatial or temporal representation is configurable.
     how: Inspect tensor shapes, raw signal channels, and transform settings.
     used at: T.3.2
E46  An importance-ranked list exists but its retention count is arbitrary or aggressive.
     how: Inspect the importance curve, current cutoff, and prior validation scores by retained count.
     used at: T.3.3
E47  A recognizable feature block was recently added or removed with uncertain benefit.
     how: Compare feature manifests and validation ablations of that block.
     used at: T.3.3
E48  Feature sources changed after the selection artifact was fitted, or selection used validation labels.
     how: Compare artifact provenance and selected names with the current schema and fold membership.
     used at: T.3.3
E49  The training population contains questionable labels, imbalance, or unused compatible examples.
     how: Inspect label confidence, source counts, and augmentation or external-data availability.
     used at: T.3
E50  Current inputs discard available temporal, semantic, spatial, or domain information.
     how: Compare raw examples and task semantics with the feature or tensor construction code.
     used at: T.3
E51  Many feature blocks are redundant, noisy, or absent from a stale selection artifact.
     how: Inspect feature counts, importances, ablations, and selection provenance.
     used at: T.3
E52  A suitable alternative pretrained family or size is available and current representation quality has plateaued.
     how: Inspect available checkpoints, pretraining domain, and standalone validation results.
     used at: T.4.1
E53  The same feature matrix supports a learner with a different inductive bias or boosting strategy.
     how: Inspect input requirements and prior family-level validation results on fixed folds.
     used at: T.4.1
E54  The backbone is strong but pooling or task heads may discard useful information.
     how: Inspect forward-pass pooling and head outputs along with their validation ablations.
     used at: T.4.1
E55  Multiple aligned feature branches are already available but fusion collapses their information.
     how: Inspect branch dimensions and whether addition, concatenation, or a learned merger feeds the classifier.
     used at: T.4.1
E56  The current loss ignores ordinal, pairwise, distributional, or multi-output evaluation structure.
     how: Compare label semantics and metric definition with the loss, output activation, and gradient code.
     used at: T.4.2
E57  Regression target location or scale varies across folds or poorly matches the model output range.
     how: Compare fold target means, scales, and existing inverse transforms.
     used at: T.4.2
E58  Training fits well but validation worsens as depth or leaf count increases.
     how: Inspect fixed-fold learning curves and previous depth or leaf sweeps.
     used at: T.4.3
E59  Generalization degrades despite adequate convergence and a fixed feature set.
     how: Inspect the train-validation gap and previous penalty, dropout, or subsampling ablations.
     used at: T.4.3
E60  Loss is unstable or learning is too slow at the current step size.
     how: Inspect training loss, gradient behavior, and learning-rate schedule logs.
     used at: T.4.3
E61  Training hits its round limit or stops while the monitored metric is still improving.
     how: Inspect best iteration, patience, maximum budget, and validation curve.
     used at: T.4.3
E62  Several compatible snapshots already exist but have not been compared under one inference configuration.
     how: Inspect checkpoint manifests and earlier comparisons for matching preprocessing and aggregation.
     used at: T.4.3
E63  The current representation or inductive bias limits quality despite a converged fit.
     how: Review family-level ablations, training curves, and available pretrained artifacts.
     used at: T.4
E64  Target construction or the loss is poorly aligned with the label and metric semantics.
     how: Read target-building code, loss implementation, and the metric definition.
     used at: T.4
E65  The family is suitable but capacity, convergence, or checkpoint selection remains unresolved.
     how: Inspect learning curves and the controlled parameter and checkpoint trial ledger.
     used at: T.4
E66  A plausible candidate has errors different from the current ensemble on the same validation rows.
     how: Compare residual correlations and candidate standalone predictions with existing members.
     used at: T.5.1
E67  A member or group has weak or redundant marginal contribution in earlier ablations.
     how: Inspect fixed-composition leave-one-out results and prediction correlations.
     used at: T.5.1
E68  The full blend has never been compared with its strongest member under the same evaluation.
     how: Check the run ledger for matched standalone and ensemble scores.
     used at: T.5.1
E69  Compatible unused fold checkpoints exist or fold quality varies substantially.
     how: Inspect fold manifests and per-fold validation or ablation scores.
     used at: T.5.1
E70  Independent training seeds produce materially different errors on the same examples.
     how: Compare seed-level prediction residuals and repeated training scores.
     used at: T.5.1
E71  Weight estimates are unstable or no independent out-of-fold predictions support fitting them.
     how: Inspect weight variation across folds and the provenance of available training predictions.
     used at: T.5.2
E72  Members have unequal quality and aligned validation predictions are available.
     how: Compare standalone and blended scores on the same held-out rows.
     used at: T.5.2
E73  The metric uses ordering and members have incompatible score scales or outliers.
     how: Read the metric and inspect per-member score distributions and rank correlations.
     used at: T.5.2
E74  The metric evaluates class distributions and logits or calibrated probabilities are available.
     how: Inspect model output activation, class sums, and the metric’s probability requirements.
     used at: T.5.2
E75  Sufficient cross-fitted predictions exist to learn a stable combination without leakage.
     how: Verify fold provenance, sample count relative to meta-features, and held-out meta-model evaluation.
     used at: T.5.2
E76  A known spatial or channel symmetry preserves the target.
     how: Inspect task semantics and transformed samples, including physiological channel mappings.
     used at: T.5.3
E77  Several crops or resolutions retain complementary labeled content.
     how: Inspect label scope, crop coverage, and existing per-view prediction differences.
     used at: T.5.3
E78  The model supports stochastic inference and its repeated passes differ meaningfully.
     how: Inspect evaluation mode and dropout activation, then compare repeated outputs on a fixed batch.
     used at: T.5.3
E79  Compatible snapshots from the same architecture and training trajectory are available.
     how: Inspect parameter shapes, snapshot provenance, and any normalization statistics required after averaging.
     used at: T.5.3
E80  The pool includes untested candidates, redundant members, or unused folds or seeds.
     how: Review member manifests and their marginal contribution tests.
     used at: T.5
E81  The current members are fixed but scale, weights, or combination method remain unresolved.
     how: Inspect member distributions and controlled blend comparisons.
     used at: T.5
E82  The input has valid alternate views or the checkpoint supports useful repeated inference.
     how: Inspect augmentation semantics and fixed-example multi-view outputs.
     used at: T.5
E83  Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
     how: Inspect label support, validation predictions near boundaries, and the metric definition.
     used at: T.6.1
E84  Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
     how: Compare label-frequency estimates across independent folds and documented test-population information.
     used at: T.6.1
E85  Groups or output columns show distinct calibration with adequate held-out sample counts.
     how: Plot per-group prediction-to-label relationships and count calibration examples per group.
     used at: T.6.1
E86  Binning creates constant predictions or many ties in columns scored by a rank metric.
     how: Count distinct predictions and inspect variance and tie frequency before and after discretization.
     used at: T.6.1
E87  Validation residuals show a systematic location or scale error.
     how: Plot predicted versus observed values and residual means on held-out data, checking metric invariances.
     used at: T.6.2
E88  Probability vectors are valid but classwise calibration is consistently biased.
     how: Inspect reliability curves and predicted versus observed class mass on held-out data.
     used at: T.6.2
E89  An auxiliary classifier or metadata rule identifies a subset with reproducible directional residuals.
     how: Measure held-out correction effects within the flagged subset and outside it.
     used at: T.6.2
E90  The required labels are discrete or the rank metric is sensitive to ties created by target granularity.
     how: Inspect target support and the official scoring calculation present in the task or local code.
     used at: T.6
E91  Valid continuous or probability predictions have a reproducible calibration or subgroup bias.
     how: Inspect held-out residual plots, class calibration, and subgroup errors.
     used at: T.6
E92  The complete dataset or feature matrix dominates memory, but independent row groups can be processed separately.
     how: Inspect allocation sizes and whether group-level operations can preserve complete entity histories within chunks.
     used at: T.7.1
E93  Memory accumulates across finished models or framework stages.
     how: Compare memory usage before and after each model and inspect live references to completed-stage objects.
     used at: T.7.1
E94  A single forward batch exceeds memory or padding wastes most tokens.
     how: Profile per-batch allocations, sequence lengths, and numerical precision.
     used at: T.7.1
E95  Runs fail or become unstable at a measured memory peak.
     how: Inspect memory logs and the stage and batch that exhaust available RAM or accelerator memory.
     used at: T.7
E96  Repeated trials recompute identical upstream features or base predictions.
     how: Compare artifact inputs and configuration hashes across trials and profile stage runtimes.
     used at: T.7
E97  A full run is expensive before basic correctness or a coarse candidate can be assessed.
     how: Compare a small-run execution path and parameter budget with the full training or inference configuration.
     used at: T.7
E98  Repeated manual path, flag, or member-list edits cause configuration drift.
     how: Inspect code duplication and prior failures involving inconsistent configuration.
     used at: T.7
E99  Profiling identifies a computational kernel whose output can be checked independently.
     how: Measure per-function runtime and compare candidate backend results on the same fixed input.
     used at: T.7
E100  The current execution fails or produces implausible predictions.
     how: Run a small labeled batch and inspect errors, output ranges, and submission alignment.
     used at: T
E101  The score signal is confounded, noisy, or unrepresentative of test conditions.
     how: Inspect recent run diffs, repeat scores, and validation membership.
     used at: T
E102  Available examples or raw inputs contain useful information missing or distorted in the training matrix.
     how: Compare label quality, raw samples, and feature construction with observed validation errors.
     used at: T
E103  A valid, evaluable model shows underfitting, overfitting, objective mismatch, or a weak representation.
     how: Inspect learning curves, objective code, and standalone comparisons on fixed validation data.
     used at: T
E104  Several valid predictors or label-preserving views have complementary errors.
     how: Compare aligned held-out predictions, residual correlations, and view semantics.
     used at: T
E105  Validated predictions have a systematic calibration or discrete-label mismatch.
     how: Inspect held-out residuals, target support, and probability calibration.
     used at: T
E106  Runtime or memory prevents completing informative experiments or full inference.
     how: Profile the current pipeline and identify the failing or dominant resource-consuming stage.
     used at: T
E107  The checkpoint loading process conflicts with or is undermined by default weight initialization (e.g., pretrained=True overriding custom weights, strict=False masking mismatches).
     how: Compare model creation flags and checkpoint loading calls to verify custom weights are actually applied without conflict.
     used at: T.1
E108  The model is not set to the correct inference mode (e.g., model.eval() missing), causing stochastic layers to behave incorrectly.
     how: Check whether model.eval() or equivalent is called before inference.
     used at: T.1
E109  Inference preprocessing parameters or logic differ from what was used during training, creating a train-test mismatch.
     how: Compare each preprocessing step (normalization, padding, filtering, tokenization, transforms) between training and inference code.
     used at: T.1
E110  There is a Python syntax error (wrong literal, missing comma, bad formatting) in newly added code that prevents parsing.
     how: Run or lint the modified code to check for syntax errors.
     used at: T.1
E111  A method or keyword argument is called using the wrong API variant (e.g., native vs wrapper, wrong method name on the model object).
     how: Verify that method names and keyword arguments match the actual class/object being used.
     used at: T.1
E112  Variable or column names introduced or modified in recent edits do not match what downstream code references, causing NameError or KeyError.
     how: Trace variable and column names from definition through all downstream references.
     used at: T.1
E113  A stray control-flow statement (continue, break, return) left from debugging alters the execution path.
     how: Search for leftover debugging artifacts in the code.
     used at: T.1
E114  A class or function lacks proper initialization or handling for the test/inference code path, causing an AttributeError.
     how: Check that constructors and functions handle test-mode arguments correctly.
     used at: T.1
E115  A previous fix attempt left structural issues (indentation, branching) that still cause incorrect execution.
     how: Review the diff of the last fix to verify structural correctness.
     used at: T.1
E116  The model's final layer already applies an activation (e.g., softmax/sigmoid), making post-processing activation redundant or harmful.
     how: Check whether the model output already includes an activation before applying one in post-processing.
     used at: T.1
E117  A required import or dependency (module, function, class) is missing, causing a NameError or ImportError before the pipeline completes.
     how: Check that all referenced names are imported or defined before use.
     used at: T.1
E118  An intermediate variable or object is deleted or goes out of scope before a downstream step that still needs it.
     how: Check for del statements or scope exits that remove objects still referenced later.
     used at: T.1
E119  A feature extraction step fails on edge-case inputs (empty splits, missing values, zero denominators) producing errors or NaNs.
     how: Check feature computation for robustness to empty or degenerate inputs.
     used at: T.1
E120  Feature columns computed for the training set are missing from the test set (or vice versa), causing a shape or key mismatch at prediction time.
     how: Compare the column sets of train and test DataFrames before model prediction.
     used at: T.1
E121  A function signature or calling convention does not match between definition and call site.
     how: Compare function definitions with their call sites for argument mismatches.
     used at: T.1
E122  A type mismatch (numpy array vs DataFrame, tensor vs scalar) causes a downstream operation to fail.
     how: Check that objects passed between pipeline stages have the expected types.
     used at: T.1
E123  The model graph construction fails because layers are not properly connected or input layers are missing.
     how: Check that the model's computational graph is fully specified with proper Input layers and layer connections.
     used at: T.1
E124  Using load_model (which bundles architecture + weights) avoids the architecture recreation step that create_model + load_weights may introduce.
     how: Compare whether the loading strategy (load_model vs create_model+load_weights) matches how the checkpoint was saved.
     used at: T.1.1
E125  The notebook lacks code to write predictions into the submission dataframe and save submission.csv.
     how: Check whether the post-prediction code that populates and saves the submission file is present and correct.
     used at: T.1.1
E126  The post-processing or aggregation step references the wrong prediction variable or output.
     how: Check that downstream code references the correct model output variable names.
     used at: T.1.1
E127  The mismatched keys are auxiliary (e.g., extra loss head) and not needed at inference, so they can be safely ignored via strict=False.
     how: Inspect the missing/unexpected keys to determine if they belong to training-only components.
     used at: T.1.1
E128  Precomputed prediction files from external scripts are available and can bypass the broken in-notebook model pipeline.
     how: Check whether pre-generated prediction CSVs or arrays exist in the input directory that can substitute for running the model.
     used at: T.1.1
E129  A try/except fallback silently swallows model loading or inference failures, causing missing or zero predictions to be averaged into the ensemble.
     how: Check whether error-handling blocks mask load or inference failures instead of surfacing them.
     used at: T.1.1
E130  A framework or library API behaves differently from the expected pandas/numpy semantics (e.g., inplace, indexing), causing silent data corruption.
     how: Compare the actual return value or in-place mutation of each library call against the expected behavior; check whether cuDF, polars, or other drop-in replacements diverge from pandas semantics.
     used at: T.1.2
E131  Duplicate or conflicting code paths load or construct the same data, causing ambiguity about which version is actually used.
     how: Search for redundant loading/construction blocks for the same variable and verify which one's output persists downstream.
     used at: T.1.2
E132  Non-feature columns (e.g., IDs, targets, raw text) are inadvertently included in the model input feature matrix.
     how: Compare the feature_names list or DataFrame columns passed to the model against the intended feature schema; check for ID, target, or metadata columns.
     used at: T.1.2
E133  A feature used during training is conditionally excluded or missing at test time due to a flag or path difference.
     how: Diff the feature columns present at train time vs. test/inference time and check conditional flags that gate feature inclusion.
     used at: T.1.2
E134  The loaded dataframe is actually the training set (or wrong split) instead of the intended test set, detectable by row count.
     how: Check the row count of the loaded dataframe against the expected test set size; a training-sized count indicates the wrong file was loaded.
     used at: T.1.2
E135  The encoder or transformer fitted on training data encounters unseen categories at test time, causing errors or silent misencoding.
     how: Check whether the OHE or label encoder's handle_unknown setting accommodates new categories, and whether test categorical values are a subset of training values.
     used at: T.1.2
E136  Untested checkpoints or nearby epochs from existing runs remain that could better map the CV-to-LB relationship.
     how: Check whether there are saved checkpoints (e.g., from different epochs or rounds) that have not yet been evaluated on the leaderboard or local validation.
     used at: T.2
E137  Fold-level predictions and indices are not persisted to disk, preventing independent offline recomputation of the metric.
     how: Check whether the pipeline saves per-fold out-of-fold predictions and fold indices so the CV metric can be recomputed and audited outside the training loop.
     used at: T.2
E138  A previously fixed bug in the custom metric or pipeline code has been inadvertently reintroduced by a later edit.
     how: Diff the current metric/evaluation code against the version where the bug was fixed to see if the fix is still present.
     used at: T.2
E139  Early-stopping patience or the absence of early stopping causes the model to overfit or underfit the training metric, undermining validation signal.
     how: Check whether early-stopping rounds are set appropriately—too long may overfit, too short may underfit, and absent early stopping may render the validation split useless.
     used at: T.2
E140  The pipeline contains a runtime error (undefined variable, argument mismatch, missing import, or broken reference) that prevents training or inference from completing.
     how: Attempt a dry-run or trace through the code to confirm that all variable references, function signatures, and imports resolve without error.
     used at: T.2
E141  Ground-truth group labels (e.g., topic or source) are available and could replace synthetic or proxy groups in the cross-validation split.
     how: Check whether the competition data or an accessible auxiliary dataset provides true group identifiers that should be used for GroupKFold instead of derived clusters.
     used at: T.2
E142  Sample weighting has already been tried without improvement, suggesting fold composition (grouping/stratification) rather than gradient weighting is the bottleneck.
     how: Review experiment logs to see if sample weighting was tested and whether the result points to fold structure as the remaining issue.
     used at: T.2
E143  The feature matrix passed to the CV splitter or clustering algorithm includes non-feature columns (e.g., target, identifiers) that corrupt group assignments.
     how: Inspect the columns of the DataFrame/array fed to KMeans.fit() or the CV splitter and verify no target, ID, or group columns are included.
     used at: T.2.2
E144  The input representation used for unsupervised grouping (e.g., engineered features vs. TF-IDF) may not capture the similarity axis most relevant to the prediction setting.
     how: Compare cluster coherence or CV-to-test agreement when grouping is derived from different feature representations (e.g., engineered features vs. TF-IDF vectors).
     used at: T.2.2
E145  A pre-existing or external source of group/topic labels is available that could replace unsupervised cluster assignments.
     how: Check whether the dataset or supplementary files contain reliable topic, prompt, or source labels that define natural groups.
     used at: T.2.2
E146  The synthetic (unsupervised) grouping does not align with the actual data-generating groups, making group-aware CV unreliable as a proxy for the test setting.
     how: Compare unsupervised cluster assignments against known data-generating factors (e.g., prompts, sources) and check whether group-aware CV improves CV-to-LB agreement.
     used at: T.2.2
E147  The fold construction logic inadvertently adds special-case indices to the validation fold, causing data leakage or biased validation estimates.
     how: Trace the code that appends distributional-outlier or special subpopulation indices and verify they are added only to training folds, not validation folds.
     used at: T.2.2
E148  Feature engineering code contains bugs, reference errors, or incomplete implementations that produce incorrect or missing features.
     how: Check whether recently added or modified feature-computation steps have variable errors, index misalignment, or were abandoned mid-implementation.
     used at: T.3
E149  Preprocessing steps (imputation, scaling, outlier removal) are unnecessary or harmful for the current model type.
     how: Check whether the model (e.g., tree-based) handles raw/missing values natively, making certain preprocessing steps distortive.
     used at: T.3
E150  A stacked or meta-feature is trained on the same data used for CV, introducing target leakage.
     how: Check whether any derived feature (e.g., stacked model predictions) was fit on the full training set rather than out-of-fold.
     used at: T.3
E151  Previous augmentation attempts beyond the current minimal setup degraded performance.
     how: Check whether stronger or additional augmentation variants have already been tried and hurt the score relative to the mild-augmentation baseline.
     used at: T.3.1
E152  The class-weight or scale_pos_weight parameter is incompatible with the current objective function (e.g., regression instead of classification).
     how: Check whether the loss-reweighting parameter being tuned is actually supported and correctly applied by the chosen objective/loss function.
     used at: T.3.1
E153  A KNN-based prediction method is available that can augment the learned representation with nearest-neighbor lookup from training embeddings.
     how: Check whether the modeling framework supports a retrieval-augmented or KNN-based prediction approach (e.g., kNN-LM, RETRO) that supplements the current representation with similarity-based lookups over stored training embeddings.
     used at: T.3.2
E154  Public high-scoring solutions for this competition commonly use rich groupby aggregations and lag features as standard feature engineering.
     how: Check whether public notebooks and top solutions use aggregation patterns (mean/std/min/max/last/nunique, lag/diff) that are not yet implemented.
     used at: T.3.2.1
E155  A proposed aggregation (e.g., var) is mathematically redundant with an existing one (e.g., std) for the current model family.
     how: Check whether the new aggregation is a monotonic transform of an existing aggregation for tree-based models.
     used at: T.3.2.1
E156  Adding many aggregations caused pipeline failures or excessive complexity that prevented end-to-end execution.
     how: Check whether prior complex aggregation sets broke the pipeline or produced column inconsistencies.
     used at: T.3.2.1
E157  Previous S_2 temporal encoding variants have consistently failed to improve over the baseline.
     how: Review whether any S_2-derived feature (days-since-max, mean, last, scaling) has ever improved the score.
     used at: T.3.2.1
E158  An aggregation type applied to numeric features has not yet been applied to categorical features (or vice versa).
     how: Check whether aggregations like 'first' or 'nunique' are applied consistently across both numeric and categorical column sets.
     used at: T.3.2.1
E159  Previously added lag-difference and lag-ratio features failed to improve the score over the simpler aggregation baseline.
     how: Check whether any lag/diff/ratio temporal feature has ever improved the score compared to the base aggregation set.
     used at: T.3.2.1
E160  Previous interaction and derived feature attempts have consistently failed to improve the score, suggesting the tree model already captures these relationships.
     how: Review the score history for all interaction/derived feature additions and check whether any improved over the best baseline.
     used at: T.3.2.1
E161  Specific features are suspected to be weakly correlated with the target or redundant with existing model outputs, based on importance analysis or domain knowledge.
     how: Check feature importance rankings or correlation analysis to identify individual features (e.g., conjunction_b, preposition_b) that appear redundant or weakly predictive.
     used at: T.3.3
E162  Recent hyperparameter changes (e.g., regularization, min_child_samples) may have shifted the optimal feature-selection ratio, requiring a fresh sweep.
     how: Compare the hyperparameter settings used during the last feature-selection sweep with the current settings; if they differ materially, the old sweep results may be invalid.
     used at: T.3.3
E163  The evaluation metric was recently changed, potentially invalidating previous feature-selection sweep results and requiring a fresh sweep.
     how: Check whether the metric used to evaluate feature-selection decisions matches the metric currently in use; a metric change means old comparisons are no longer valid.
     used at: T.3.3
E164  There exist columns with very high missing-value rates that have not yet been explicitly considered for removal.
     how: Compute missing-value rates per column and check whether any high-missingness columns remain in the feature set without explicit justification.
     used at: T.3.3
E165  Features derived from multiple preprocessing variants of the same source are highly correlated and could be consolidated or deduplicated.
     how: Check pairwise correlations among features derived from the same raw source (e.g., different text preprocessing variants) to see if they are near-duplicates.
     used at: T.3.3
E166  Model hyperparameters (depth, leaves, regularization) were tuned for a different feature-set size and may need co-tuning when the feature count changes substantially.
     how: Compare the feature count at which hyperparameters were last tuned with the current feature count; a large change suggests co-tuning is needed.
     used at: T.3.3
E167  The expert chose to increase regularization instead of ablating suspect feature blocks, despite ablation being the more direct diagnostic step.
     how: Review whether the chosen action (regularization increase) addresses the root concern or merely masks it, compared to directly ablating the suspect features.
     used at: T.3.3
E168  The newly chosen model architecture or checkpoint fails to load or instantiate correctly, preventing any evaluation.
     how: Attempt to load the model and run a forward pass; check for crashes or errors during weight-loading or construction.
     used at: T.4
E169  The second-order (hessian) approximation in the custom objective is a key component whose formulation materially affects optimization quality and score.
     how: Compare scores between analytic-hessian and constant-hessian variants; check whether hessian choice correlates with meaningful performance differences.
     used at: T.4
E170  A constant-hessian (ones) baseline for the custom objective is known to be stable and competitive.
     how: Check whether using a constant hessian as a baseline has been tested and whether it matches or exceeds the current custom objective performance.
     used at: T.4.2
E171  The model architecture flag (e.g., multihead) does not match the checkpoints being loaded, causing a weight/architecture mismatch.
     how: Verify that runtime architecture flags are consistent with the saved checkpoint architecture before running inference.
     used at: T.5
E172  A single model with richer internal pooling/attention could replace the diversity currently achieved by combining multiple simpler models.
     how: Check whether an untested single-model architecture with advanced pooling could match or exceed the current ensemble's diversity benefit.
     used at: T.5
E173  A specific current ensemble member is suspected of degrading overall performance based on isolation scores or prior blend evidence.
     how: Compare each member's standalone and marginal contribution to identify members that hurt the blend.
     used at: T.5
E174  Input preprocessing parameters (e.g., crop offsets, temporal windows) should be co-varied with ensemble member changes, as they have shown score impact in prior edits.
     how: Review whether preprocessing settings were tuned for the old ensemble composition and may need adjustment for the new one.
     used at: T.5
E175  Flip TTA was previously disabled or removed and can now be re-enabled to test its current effect.
     how: Check version history to see if flip TTA was previously active, then disabled, and whether conditions have changed enough to warrant re-enabling.
     used at: T.5.3
E176  The marginal gain from the proposed TTA variation has not yet been measured for the current model/ensemble configuration.
     how: Check leaderboard history and ablation logs to see if the specific TTA variation has been scored with the current model setup.
     used at: T.5.3
E177  The proposed TTA variation was previously tried and caused a score regression.
     how: Review submission history to see if this TTA approach was tested before and whether it hurt performance.
     used at: T.5.3
E178  TTA effectiveness varies across checkpoint versions or ensemble configurations, requiring re-evaluation rather than assuming prior results hold.
     how: Compare TTA ablation results across different checkpoints or ensemble versions to see if the effect is consistent.
     used at: T.5.3
E179  Disabling a currently-enabled TTA is a valid ablation to isolate its contribution to the current setup.
     how: Check whether TTA is currently active and whether removing it would constitute a clean ablation experiment.
     used at: T.5.3
E180  Prediction entropy varies enough across samples to warrant conditioning TTA behavior on uncertainty.
     how: Measure per-sample prediction entropy across inference passes to see if adaptive TTA (e.g., more passes for uncertain samples) would help.
     used at: T.5.3
E181  A parameter controls the number of deterministic augmented views averaged at inference time.
     how: Inspect the inference code for a parameter (e.g., hack_count) that sets how many augmented views are averaged.
     used at: T.5.3
E182  The proposed TTA technique is a standard approach used in strong public solutions for this competition.
     how: Review public notebooks and top solutions to see if the TTA variation is commonly used.
     used at: T.5.3
E183  TTA's variance-reduction benefit depends on the current ensemble size — fewer models make TTA more valuable, more models may make it redundant.
     how: Assess whether the current ensemble diversity already provides sufficient variance reduction, diminishing TTA's marginal benefit.
     used at: T.5.3
E184  The submission pipeline or scoring may clip or transform predictions in a way that interacts with prediction scale.
     how: Check whether scaling (e.g., *100) causes clipping, rounding, or other transformations that produce a large unexpected score change.
     used at: T.6
E185  The evaluation metric is invariant to monotonic transformations of predictions, so scale changes should not affect the score.
     how: Verify whether the metric (e.g., AUC) is rank-based and therefore unaffected by monotonic rescaling of predictions.
     used at: T.6
E186  The OptimizedRounder is producing inconsistent or potentially overfitted thresholds, making a simpler baseline comparison worthwhile.
     how: Compare OptimizedRounder thresholds across folds/experiments and test whether naive rounding yields comparable or better results.
     used at: T.6
E187  Complex distribution-matching post-processing may be masking or amplifying errors in the upstream loss function.
     how: Evaluate whether removing or simplifying the post-processing reveals a hidden error in the custom loss, by comparing raw vs. post-processed scores.
     used at: T.6
E188  A previously tried threshold-based binning method (e.g., pd.cut) performed worse than an earlier rounding approach.
     how: Review past experiment logs to confirm that the binning approach degraded performance relative to simpler rounding.
     used at: T.6
E189  The prediction array dtype is incompatible with DataFrame construction or CSV serialization, causing format errors rather than a calibration issue.
     how: Inspect the dtype of the prediction array and test whether it causes errors during DataFrame creation or CSV writing.
     used at: T.6
E190  The post-processing code contains a typo or bug that prevents it from executing correctly.
     how: Review the post-processing code (e.g., cut_values) for typos or syntax errors that cause silent failures or exceptions.
     used at: T.6
E191  A zero-variance or otherwise stable reference sample exists that can anchor the bias correction.
     how: Check whether any training example has standard_error==0 or near-zero variance, providing a reliable reference point for calibrating the correction.
     used at: T.6.2
E192  The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set.
     how: Assess whether the mean-shift or distributional correction derived from training data is likely to generalize, considering test set size and noise.
     used at: T.6.2
E193  Raw model outputs may exceed the valid target range or hit exact boundaries.
     how: Inspect whether continuous predictions fall outside the expected domain (e.g., [0,1]) or land on exact boundary values that could distort calibration.
     used at: T.6.2
E194  Releasing or deleting completed intermediate objects causes downstream errors or was already attempted without resolving OOM.
     how: Check whether prior attempts to free memory (del, gc.collect) either failed to reduce peak memory or introduced runtime errors due to premature deletion of still-referenced objects.
     used at: T.7.1
E195  Precomputed artifacts (embeddings, cached features) are available that can replace expensive in-process computation and its associated memory footprint.
     how: Check whether saved embeddings, feature caches, or lighter checkpoint variants exist that can be loaded instead of recomputing large intermediate tensors during the failing stage.
     used at: T.7.1
E196  Duplicated or redundant code paths create unnecessary copies of large intermediate arrays that inflate peak memory.
     how: Inspect the failing stage for duplicated computation blocks or redundant variable assignments that hold multiple copies of the same large data structure simultaneously.
     used at: T.7.1