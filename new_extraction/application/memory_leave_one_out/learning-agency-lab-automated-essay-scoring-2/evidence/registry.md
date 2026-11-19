# evidence/registry.md — one definition per check, shared across nodes

E01  Current scores cannot distinguish model changes because splits, metrics, or experiments are unreliable.
     how: Inspect split overlap, scoring code, version diffs, and repeated-run score variation.
     used at: T
E02  Predictions fail basic validity or do not match the trained pipeline.
     how: Inspect loading diagnostics, input/output IDs, prediction ranges, and train/inference configurations.
     used at: T
E03  Correct runs are blocked by memory, session limits, or repeated expensive work.
     how: Use runtime logs and memory profiles to locate the limiting stage.
     used at: T
E04  Available task-relevant information is absent, distorted, or diluted in current inputs.
     how: Compare raw data with feature tensors and existing feature or modality ablations.
     used at: T
E05  Label quality, data coverage, censoring, or sample weighting limits the training signal.
     how: Inspect label distributions, event indicators, data provenance, and quality-stratified errors.
     used at: T
E06  Learning curves or controlled single-model experiments implicate capacity, objective, or optimization.
     how: Inspect train/validation curves and model-family or head comparisons.
     used at: T
E07  Correct aligned predictions from multiple sources show potentially complementary errors.
     how: Inspect OOF provenance, standalone scores, residual correlations, and current blend ablations.
     used at: T
E08  Valid base predictions retain an observable calibration, granularity, or inference-view mismatch.
     how: Inspect held-out calibration, target support, domain symmetries, and current post-processing ablations.
     used at: T
E09  Related rows cross folds or fold target distributions are visibly skewed.
     how: Inspect split IDs and per-fold target summaries.
     used at: T.1
E10  The reported evaluation callback is incorrect, unstable, or a measured runtime bottleneck.
     how: Compare metric code, curves, and profiler output with the task’s scoring definition.
     used at: T.1
E11  Multiple edits or stochastic reruns make the latest score movement ambiguous.
     how: Review version diffs and repeated baseline scores.
     used at: T.1
E12  Several candidate configurations can be scored on an existing representative holdout.
     how: Inspect stored validation predictions, labels, and split provenance; verify candidates used the same rows.
     used at: T.1.1
E13  Fold target distributions differ substantially despite independent observations.
     how: Tabulate class proportions or target-bin histograms by fold and compare with the full labeled sample.
     used at: T.1.1
E14  Several rows or overlapping windows belong to the same prediction entity.
     how: Count repeated entity IDs and intersect IDs or window intervals across the current train and validation partitions.
     used at: T.1.1
E15  A proposed stacker lacks held-out predictions aligned to common row and fold identifiers.
     how: Join each base model’s prediction file to saved fold indices and check that no row was predicted by a model trained on it.
     used at: T.1.1
E16  Local and public scores have ranked existing checkpoints differently.
     how: Compare the paired local/external score table and public sample size; distinguish ranking reversals from repeated-run variation.
     used at: T.1.1
E17  The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons.
     how: Compare the configured evaluation callback with the task formula and recorded task scores along training.
     used at: T.1.2
E18  The task metric fluctuates sharply between nearby iterations while a smooth proxy tracks generalization better.
     how: Inspect validation curves and prior stopping-point comparisons on identical folds.
     used at: T.1.2
E19  Callback values or shapes disagree with an independent calculation.
     how: Evaluate a small labeled prediction vector through both code paths and inspect the framework callback arguments.
     used at: T.1.2
E20  Metric computation dominates repeated training or blending evaluations.
     how: Read profiler timings for the callback and compare its output against the existing reference implementation.
     used at: T.1.2
E21  No complete pipeline has yet produced a scored prediction file.
     how: Inspect run artifacts and the experiment log for a successful end-to-end scored baseline.
     used at: T.1.3
E22  The last score change followed several simultaneous functional edits.
     how: Diff the last two scored versions and list changed inputs, checkpoints, training settings, and blend formulas.
     used at: T.1.3
E23  Existing unchanged runs vary by as much as the candidate gain.
     how: Compare repeated scores and prediction files for an identical configuration, including pinned artifacts.
     used at: T.1.3
E24  A reproducible parameter trend exists but the optimum has not been bracketed.
     how: Inspect the trial table for consistently improving values and whether values on both sides have been evaluated.
     used at: T.1.3
E25  The latest configuration is substantially worse than a reproducible saved baseline.
     how: Compare the regression with measured run variation and locate the exact saved configuration and artifacts.
     used at: T.1.3
E26  Several recent settings failed to improve beyond the measured noise floor.
     how: Read the recent sweep table, including failed probes, and compare its range with unchanged-run variation.
     used at: T.1.3
E27  The first baseline is far below existing scored alternatives and several compatible missing components are already evidenced.
     how: Compare available baseline scores and code paths for missing domain preprocessing, suitable models, or averaging; record the loss of attribution before bundling.
     used at: T.1.3
E28  Failures begin at import, checkpoint resolution, or state loading.
     how: Read the earliest error and loading diagnostics.
     used at: T.2
E29  The model runs but rows, features, or executed branches do not match the intended pipeline.
     how: Inspect IDs, stage shapes, and per-model prediction counts.
     used at: T.2
E30  Prediction scale, direction, finiteness, or blending arithmetic is invalid.
     how: Inspect numeric summaries and manually recompute representative outputs.
     used at: T.2
E31  No usable final output exists or accumulated patches obstruct basic execution.
     how: Inspect the first failure and final artifact schema.
     used at: T.2
E32  A configured artifact is missing or its resolved path differs from the saved artifact.
     how: List available files and compare full resolved paths, including filename punctuation and cleanup commands.
     used at: T.2.1
E33  Imports fail or resolve to a different library copy than the checkpoint requires.
     how: Inspect import exceptions, module file locations, local package versions, and path ordering.
     used at: T.2.1
E34  Checkpoint keys, tensor shapes, tokenizer vocabulary, or head dimensions disagree with the constructed model.
     how: Compare the saved configuration and state dictionary with the instantiated model under strict loading.
     used at: T.2.1
E35  Loading appears successful but predictions resemble an untrained or constant model.
     how: Inspect loaded parameter statistics, missing-key reports, evaluation mode, and predictions on a small known labeled sample.
     used at: T.2.1
E36  Outputs are constant across substantial edits or some configured members never produce predictions.
     how: Trace loop entry counts, array accumulation, input row IDs, and the exact variable written to disk.
     used at: T.2.2
E37  A new feature branch receives implausible shapes or values.
     how: Print small tensor slices, axis meanings, and statistics before and after each new transform.
     used at: T.2.2
E38  Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
     how: Compare saved training configuration, feature order, scaler/encoder artifacts, and inference call order.
     used at: T.2.2
E39  Test categories include unseen levels or the inference code fits a new encoder.
     how: Compare category sets and inspect calls to fit, fit_transform, and transform.
     used at: T.2.2
E40  A preprocessing or target-building step consumes identifiers or labels unavailable at prediction time.
     how: Trace input dependencies against the test schema and audit fitting boundaries inside each fold.
     used at: T.2.2
E41  A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence.
     how: Locate reference predictions and compare both implementations on the same ordered sample.
     used at: T.2.2
E42  Prediction units or monotonic direction disagree with the labels or other members.
     how: Check target scaling and inverse-link code, and compare standalone held-out score direction with a trusted member.
     used at: T.2.3
E43  Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.
     how: Recompute a few rows by hand and compare active member counts, weights, types, and array shapes.
     used at: T.2.3
E44  Inputs or intermediate network outputs contain non-finite values.
     how: Run finite-value checks stage by stage on a small failing batch.
     used at: T.2.3
E45  The called method or argument belongs to a different API wrapper than the instantiated object.
     how: Inspect object types and local function signatures at the failing call.
     used at: T.2.3
E46  The pipeline fails before completing even one sample or model.
     how: Read the first traceback and try the same path on one batch with minimal training.
     used at: T.2.4
E47  Inference finishes but the expected prediction file is absent or malformed.
     how: Read the final artifact and compare its path, row IDs, columns, and numeric values with the required template.
     used at: T.2.4
E48  Some ensemble output files are missing or fallback arrays are placeholders.
     how: Inspect each member file, its provenance and row alignment, and logs identifying which fallback path executed.
     used at: T.2.4
E49  Repeated patches leave duplicated transformations or hidden dependencies that prevent reliable fixes.
     how: Trace the current stages and compare duplicate code paths and their outputs.
     used at: T.2.4
E50  Runs fail or slow sharply at a reproducible memory peak.
     how: Inspect memory profiles and failure traces.
     used at: T.3
E51  Repeated loading, extraction, or full training dominates otherwise working experiments.
     how: Compare stage timings across recent runs.
     used at: T.3
E52  Device support or API limitations block a required operation.
     how: Inspect runtime exceptions and available local interfaces.
     used at: T.3
E53  The raw table or engineered feature table exceeds memory before model inference starts.
     how: Compare dataframe sizes and profiler memory peaks during loading and aggregation.
     used at: T.3.1
E54  Memory grows between sequential model runs because completed objects remain live.
     how: Inspect memory after each model and references to model objects and intermediate arrays.
     used at: T.3.1
E55  Memory failure occurs in a single forward pass and grows with batch size.
     how: Inspect the traceback and peak accelerator memory for progressively smaller batches.
     used at: T.3.1
E56  Model tensors dominate memory and the current pipeline uses full precision.
     how: Inspect tensor dtypes and allocations and any prior paired precision results.
     used at: T.3.1
E57  A full training run is currently needed just to test code wiring or screen a parameter.
     how: Measure run time and inspect whether fold, seed, and iteration counts can be reduced coherently.
     used at: T.3.2
E58  The expensive upstream outputs are unchanged across downstream experiments.
     how: Compare artifact hashes and configurations for repeated feature extraction or base-model inference.
     used at: T.3.2
E59  A session cannot finish all folds but completed fold checkpoints can be reused.
     how: Compare per-fold run time with the session limit and inspect persisted fold manifests.
     used at: T.3.2
E60  Repeated ranking or subgroup post-processing dominates the inference-adjustment search.
     how: Inspect stage timings and compare current rank outputs on tied and grouped predictions with a small exact reference.
     used at: T.3.2
E61  Variant changes require repeated manual edits that have caused configuration drift.
     how: Inspect duplicate constants, path lists, and flags across the notebook.
     used at: T.3.2
E62  The configured accelerator or dataframe backend does not support a required operation.
     how: Inspect the device error, available hardware, and a minimal local backend probe.
     used at: T.3.3
E63  The current wrapper cannot expose the needed custom metric or iteration control.
     how: Inspect the installed wrapper signature and the native training interface used by existing code.
     used at: T.3.3
E64  The estimator wrapper already supports the required stopping and probability outputs.
     how: Inspect its local interface and compare it with the extra dataset and prediction-conversion code currently maintained.
     used at: T.3.3
E65  Repeated rows are collapsed into a limited summary or their structure is still unknown.
     how: Inspect entity histories and the current tabular feature specification.
     used at: T.4
E66  Many engineered inputs are redundant, sparse, or implicated in prior regressions.
     how: Review importance stability, missingness, and feature-group ablation results.
     used at: T.4
E67  Missingness or stored numerical precision conflicts with estimator assumptions.
     how: Inspect actual dtypes, NaNs, and active model capabilities.
     used at: T.4
E68  Text truncation, formatting, or omitted metadata plausibly limits the encoder.
     how: Inspect tokenized samples and the text/metadata schema.
     used at: T.4
E69  Spatial or spectral preprocessing removes relevant structure or mismatches trained inputs.
     how: Inspect transformed examples and saved extraction settings.
     used at: T.4
E70  Several aligned modalities or channels exist and their use or fusion remains unresolved.
     how: Inspect available inputs, branch outputs, and existing modality ablations.
     used at: T.4
E71  The number and ordering of records per prediction entity are not yet established.
     how: Inspect entity counts, sorted timestamps, feature prefixes, and missingness summaries.
     used at: T.4.1
E72  No working entity-level feature baseline exists.
     how: Inspect the feature table and training inputs for duplicate prediction IDs and missing aggregation logic.
     used at: T.4.1
E73  Only the last observation or one central statistic is currently retained.
     how: Compare the aggregation specification with within-entity variation and existing importance plots.
     used at: T.4.1
E74  Full-history aggregates obscure behavior near the prediction time.
     how: Compare recent and full-history distributions, history lengths, and the label time horizon.
     used at: T.4.1
E75  Entities have ordered histories whose recent changes are not represented.
     how: Inspect sequence lengths, time ordering, and whether current aggregates discard direction of change.
     used at: T.4.1
E76  Domain-related columns have a meaningful ratio or deviation not present in the features.
     how: Inspect column definitions and the existing derived-feature list, then review prior interaction ablations.
     used at: T.4.1
E77  Timestamps vary meaningfully across entities and have been discarded from the feature table.
     how: Compare timestamp ranges and target patterns with the current aggregation outputs.
     used at: T.4.1
E78  A wide feature table has stable cross-fold importance estimates.
     how: Compare rankings across fitted folds and inspect whether low-ranked columns dominate feature count.
     used at: T.4.2
E79  A particular added feature family coincided with a regression or is error-prone.
     how: Review feature-version diffs, prior group ablations, and implementation failures.
     used at: T.4.2
E80  Some columns are almost entirely missing.
     how: Compute column missingness on train and validation and inspect the model’s use of those columns.
     used at: T.4.2
E81  The classifier consumes a truncated backbone embedding and full-dimensional checkpoints are available.
     how: Inspect pooled tensor width, head parameter count, and compatible checkpoint configurations.
     used at: T.4.2
E82  The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes.
     how: Inspect estimator capabilities, aggregation-generated NaNs, and prior preprocessing ablations.
     used at: T.4.3
E83  At least one active model rejects missing values or lacks native handling.
     how: Inspect estimator input checks and the finite-value fraction of its actual feature matrix.
     used at: T.4.3
E84  Low-precision storage creates spurious fine-scale differences relative to meaningful measurement resolution.
     how: Compare raw and stored values, unique-value spacing, and dtype conversion code.
     used at: T.4.3
E85  Relevant text lies outside the retained token range or is diluted by unrelated spans.
     how: Inspect token-length distributions, truncation examples, and task-relevant span locations.
     used at: T.4.4
E86  Custom normalization changes text beyond the tokenizer’s training assumptions.
     how: Compare before/after examples and existing cleaning ablations.
     used at: T.4.4
E87  Distinct text fields are flattened together despite different roles in the target.
     how: Inspect input schema, encoding templates, and available checkpoints for separate or paired streams.
     used at: T.4.4
E88  Structured metadata or surface statistics vary with targets but are absent from the model.
     how: Inspect train-only metadata summaries, target associations, and the current input signature.
     used at: T.4.4
E89  Useful fine detail is lost at the current resize and compatible higher-resolution weights exist.
     how: Inspect downsampled examples, checkpoint training sizes, and prior resolution probes.
     used at: T.4.5
E90  The current temporal or spatial window misses the labeled region or includes irrelevant context.
     how: Compare timestamp or crop bounds with label scope, sequence lengths, and current retained content.
     used at: T.4.5
E91  Time-frequency bins are too coarse for the event durations or frequency structure of interest.
     how: Inspect spectrograms, transform parameters, sampling rate, and matched checkpoint settings.
     used at: T.4.5
E92  Input intensity statistics differ from the training preprocessing or target-domain distribution.
     how: Compare per-channel statistics and saved normalization code with inference tensors.
     used at: T.4.5
E93  Known interference frequencies or an unsuitable passband remain in the signal.
     how: Inspect spectra, filter response, sampling rate, and documented signal bandwidth.
     used at: T.4.5
E94  A few extreme values dominate the raw or spectral dynamic range.
     how: Inspect value quantiles and plots before and after current clipping.
     used at: T.4.5
E95  A natural-image backbone receives scalar spectral images and a color encoding has not been tested.
     how: Inspect input channels, pretraining expectations, and any compatible color-encoded checkpoints.
     used at: T.4.5
E96  An arbitrary signal-to-image factorization creates implausible local neighborhoods.
     how: Trace the reshape dimensions and visualize adjacent image positions against original time and channel indices.
     used at: T.4.5
E97  Useful channels are available in the same signal but excluded from the current tensor.
     how: Compare raw channels and derived-channel definitions with model input indices.
     used at: T.4.6
E98  A different modality or representation carries information the current branch cannot see.
     how: Inspect paired samples, existing standalone modality scores, and available compatible training paths.
     used at: T.4.6
E99  An existing branch adds substantial complexity and its incremental benefit is unverified or negative.
     how: Inspect previous branch ablations and branch-specific outputs on the same rows.
     used at: T.4.6
E100  Equal-width branch embeddings are averaged before classification, potentially discarding distinct information.
     how: Inspect fusion code, feature dimensions, and compatible heads for concatenation and averaging.
     used at: T.4.6
E101  Data quantity, label quality, duplication, or imbalance is the observed limitation.
     how: Inspect learning curves, sample provenance, counts, and quality-stratified errors.
     used at: T.5
E102  Censoring or evaluation-group fairness is not represented appropriately by the current target.
     how: Inspect outcome schema, target construction, and per-group scores.
     used at: T.5
E103  Training overfits despite plausible label-preserving input perturbations being available.
     how: Inspect train/validation gaps and examples of domain-compatible transforms.
     used at: T.5
E104  A substantial labeled holdout remains unused after the configuration has already been selected.
     how: Inspect split sizes, stopping strategy, and the independently saved validation evidence.
     used at: T.5.1
E105  Additional labeled examples exist with compatible targets and adaptable input shapes.
     how: Inspect their provenance, label definitions, distribution, and previous inclusion experiments.
     used at: T.5.1
E106  Unlabeled examples and a pseudo-labeling procedure already improved another comparable member.
     how: Review available pseudo-label artifacts, confidence diagnostics, and labeled-only versus pseudo-labeled validation results.
     used at: T.5.1
E107  Training examples contain duplicated windows, flagged outliers, or measurable label-quality variation.
     how: Inspect overlap IDs, out-of-fold residuals, annotator counts, and retained sample counts under proposed filters.
     used at: T.5.1
E108  Class imbalance or subgroup error patterns suggest the current sample weighting is unsuitable.
     how: Compare class counts and per-class held-out errors with the metric’s weighting and earlier weight sweeps.
     used at: T.5.1
E109  The outcome is censored and ordinary regression targets do not express the observed event information.
     how: Inspect event indicators, observation times, censoring rates, and current target-building code.
     used at: T.5.2
E110  The metric scores predefined groups and their outcome distributions differ substantially.
     how: Read the metric grouping definition and compare training-only event and censoring distributions by group.
     used at: T.5.2
E111  Some groups have too few observed events for stable group-specific transforms.
     how: Count events and inspect transform stability across training folds within each group.
     used at: T.5.2
E112  Image intensity varies naturally but strong augmentation has previously distorted useful structure.
     how: Inspect image distributions and augmentation examples alongside prior magnitude sweeps.
     used at: T.5.3
E113  The model sees spectrograms and should tolerate missing local time-frequency evidence.
     how: Inspect signal events and candidate masks to confirm they do not systematically erase the full target interval.
     used at: T.5.3
E114  Labels are soft distributions and the existing training code already supports weighted example mixing.
     how: Inspect label normalization and mixup weights and compare previous mixed versus unmixed training results.
     used at: T.5.3
E115  The current predictor’s inductive bias or pretraining domain appears unsuitable.
     how: Compare standalone errors, data modality, and available alternative predictors.
     used at: T.6
E116  The backbone is useful but pooling or the output head is limiting.
     how: Review architecture and head-only ablation results.
     used at: T.6
E117  A tree model’s capacity, regularization, or round budget is implicated by learning curves.
     how: Inspect tree fit and validation traces.
     used at: T.6
E118  Neural optimization or objective mismatch is visible in training diagnostics.
     how: Inspect optimizer, loss, activation, and rate traces.
     used at: T.6
E119  The available trained states differ more than recent architecture changes or stopping is poorly configured.
     how: Review checkpoint scores, training curves, and component-training audits.
     used at: T.6
E120  The current family has plateaued despite useful features and controlled tuning.
     how: Review the single-model tuning history and whether an alternative family offers a different treatment of the data.
     used at: T.6.1
E121  A domain-relevant or structurally different pretrained backbone is available.
     how: Inspect its training domain, expected inputs, and existing standalone validation evidence.
     used at: T.6.1
E122  Capacity appears limiting or a smaller model may meet the same quality target.
     how: Compare train/validation errors, resource use, and available size-matched checkpoints.
     used at: T.6.1
E123  Pretrained embeddings are available but end-to-end fine-tuning is noisy or expensive.
     how: Inspect cached representation quality, sample count, and variance across fine-tuning runs.
     used at: T.6.1
E124  Similar labeled examples exist and a leakage-free retrieval index can be built for each validation fold.
     how: Inspect nearest-neighbor examples and verify that the query’s label and validation rows are excluded from its index.
     used at: T.6.1
E125  The tuned standard tree booster still appears to overfit and a dropout-based variant is supported.
     how: Inspect train/validation curves and prior booster comparisons, including whether early stopping works for the variant.
     used at: T.6.1
E126  The backbone is strong but its current head is only a minimal projection.
     how: Inspect architecture definitions and the plateau under backbone-fixed experiments.
     used at: T.6.2
E127  A complex multi-head or normalization design has regressed or overfit.
     how: Compare train/validation behavior and head ablations with matching checkpoints.
     used at: T.6.2
E128  Useful token or hidden-layer information is discarded by the current pooling.
     how: Inspect pooling code, available hidden states, sequence structure, and earlier pooling comparisons.
     used at: T.6.2
E129  The main regression target has a meaningful discrete or auxiliary structure that can be learned jointly.
     how: Inspect target support and previous auxiliary-task validation results; verify sufficient labels for both tasks.
     used at: T.6.2
E130  Training fit is poor under shallow trees or prior depth changes show a clear capacity effect.
     how: Inspect train/validation curves, depth and leaf settings, and completed capacity probes.
     used at: T.6.3
E131  Training improves while validation stagnates under the current tree capacity.
     how: Compare curves and prior penalties or minimum-leaf settings on the same feature set.
     used at: T.6.3
E132  Every tree sees all rows and columns and the model overfits after feature selection.
     how: Inspect bagging and feature-fraction settings and the held-out gap.
     used at: T.6.3
E133  Lower learning rates reach the round cap or trigger stopping before sustained convergence.
     how: Inspect best iteration, learning rate, round budget, and metric progression near stopping.
     used at: T.6.3
E134  Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
     how: Compare standalone and ensemble validation curves across saved iteration checkpoints.
     used at: T.6.3
E135  Training is unstable or converges too slowly under the current fine-tuning rate.
     how: Inspect loss curves, gradient behavior, rate settings, and previous rate trials.
     used at: T.6.4
E136  Convergence stalls around the current decay schedule’s transitions.
     how: Plot learning rate and validation metric over steps and compare with earlier schedules.
     used at: T.6.4
E137  The current optimizer has reproducible convergence limitations after learning-rate tuning.
     how: Inspect optimization traces and prior controlled rate sweeps before comparing another optimizer.
     used at: T.6.4
E138  The pretrained backbone fits training data well but the added head overfits.
     how: Inspect train/validation gaps and the head’s current dropout and capacity.
     used at: T.6.4
E139  The output activation or training loss imposes assumptions inconsistent with the labels or task metric.
     how: Compare mutually exclusive versus independent targets, distributional labels, or pairwise ranking requirements with the current head and loss.
     used at: T.6.4
E140  The metric is still improving at the training cap or extra epochs have started to overfit.
     how: Inspect held-out learning curves and saved adjacent-epoch checkpoints.
     used at: T.6.5
E141  Stopping occurs during noisy short plateaus, especially with a reduced learning rate.
     how: Inspect the patience window, curve fluctuations, and later improvements in longer runs.
     used at: T.6.5
E142  Several compatible trained states already exist with different validation results.
     how: Inspect checkpoint metadata, stage provenance, and fixed-pipeline scores.
     used at: T.6.5
E143  Several late states of one compatible architecture are available and individual weights remain noisy.
     how: Inspect training continuity, parameter keys, and validation behavior of those states.
     used at: T.6.5
E144  A weak ensemble component lacks the fold discipline or tuning used by the stronger components.
     how: Audit its split indices, saved OOF predictions, data loading, and training configuration.
     used at: T.6.5
E145  The value of specific active or candidate members is uncertain.
     how: Inspect addition, replacement, and leave-one-out results.
     used at: T.7
E146  Current members have highly correlated errors and additional independent prediction sources are available.
     how: Compare residual correlations with available architectures, representations, folds, and seeds.
     used at: T.7
E147  Membership is stable but existing weights ignore quality differences or group sizes.
     how: Inspect effective coefficients, member scores, and previous weighting comparisons.
     used at: T.7
E148  Member output scales or activation order are inconsistent with the intended metric and blend.
     how: Inspect score distributions, links, and the aggregation formula.
     used at: T.7
E149  Aligned OOF predictions support a learned combiner and its capacity or features remain unresolved.
     how: Inspect OOF provenance and meta-model validation results.
     used at: T.7
E150  A compatible unused candidate has reasonable standalone predictions and potentially different residual errors.
     how: Inspect aligned candidate predictions, standalone scores, residual correlations, and earlier inclusion trials.
     used at: T.7.1
E151  A stronger or different candidate is available for a known weak or redundant slot.
     how: Compare the current slot and replacement on the same held-out rows and inspect their correlations with the rest of the blend.
     used at: T.7.1
E152  An active member has repeatedly worsened the fixed blend or seems redundant.
     how: Read leave-one-out results and per-member residual correlations using unchanged weights or renormalized baselines.
     used at: T.7.1
E153  No same-split comparison establishes that the ensemble beats its strongest member.
     how: Inspect saved standalone and ensemble scores on identical examples.
     used at: T.7.1
E154  The current regression followed removal of members that previously had positive ablation evidence.
     how: Compare member manifests before and after the regression and locate their validated prediction files.
     used at: T.7.1
E155  Most active members share one architecture or algorithm and their residuals are highly correlated.
     how: Inspect the member manifest and held-out residual correlation matrix.
     used at: T.7.2
E156  An available modality, feature set, or preprocessing variant is absent from current members.
     how: Compare training representations and standalone validation results for the alternate path.
     used at: T.7.2
E157  Different valid outcome transforms produce complementary residuals for the same task.
     how: Inspect OOF predictions from existing transformed-target models and verify target-direction alignment.
     used at: T.7.2
E158  Training seeds produce substantial variance while architecture and fold setup remain fixed.
     how: Compare saved independent-seed predictions and same-split score distributions.
     used at: T.7.2
E159  Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
     how: Inspect fold coverage, checkpoint provenance, and the marginal-gain table.
     used at: T.7.2
E160  One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
     how: Check checkpoint metadata and fixed-pipeline full-versus-subset scores across held-out samples.
     used at: T.7.2
E161  Members have comparable quality and tuned weights have not reliably improved the simple average.
     how: Compare uniform and tuned blend scores across the same held-out samples or repeated evaluations.
     used at: T.7.3
E162  Component quality differs reproducibly or a member’s predictions have changed since weights were tuned.
     how: Inspect standalone scores, OOF residuals, and artifact versions relative to the saved weight configuration.
     used at: T.7.3
E163  A candidate’s residual contribution appears negatively correlated with the remaining blend’s error.
     how: Compute conditional residual associations and inspect prior small signed-weight probes on held-out data.
     used at: T.7.3
E164  Model families contain unequal numbers of folds or variants.
     how: Count members per group and expand the current formula into effective per-family weights.
     used at: T.7.3
E165  Current weights depend on statistics of a very small or varying inference sample.
     how: Inspect weight-generation code and the sample count and variability used to estimate adaptive coefficients.
     used at: T.7.3
E166  Different components consistently win on different classes with adequate validation examples.
     how: Compare per-class held-out errors and sample counts across folds.
     used at: T.7.3
E167  Useful score magnitudes or calibrated additive corrections are already validated.
     how: Inspect raw-versus-rank comparisons and whether downstream adjustments rely on absolute scale.
     used at: T.7.4
E168  The metric is rank-based and member score distributions differ in calibration or scale.
     how: Read the metric definition and plot per-member prediction distributions and held-out raw/rank blend results.
     used at: T.7.4
E169  Stacking or weighted blending mixes columns with different scales or outlier-heavy outputs.
     how: Inspect OOF column quantiles and scaler fitting code; compare spread and outliers across members.
     used at: T.7.4
E170  Overconfident member probabilities cluster near the boundaries and their magnitude dominates the blend.
     how: Inspect probability histograms and existing held-out power-transform comparisons.
     used at: T.7.4
E171  Compatible pre-softmax logits are available and the task scores categorical probability distributions.
     how: Inspect saved logits, class ordering, and the distributional metric before comparing combination order.
     used at: T.7.4
E172  Current inputs to an arithmetic average are unnormalized outputs although the blend is intended to average distributions.
     how: Inspect each member’s output activation and row sums before averaging.
     used at: T.7.4
E173  A fixed blend has plateaued and enough aligned held-out base predictions exist to fit a small combiner.
     how: Inspect OOF coverage, row alignment, sample count relative to member count, and fixed-blend scores.
     used at: T.7.5
E174  The current stacker’s model class underfits or a complex stacker overfits the available meta-data.
     how: Compare training and held-out meta-model errors and prior family ablations.
     used at: T.7.5
E175  The current meta-learner’s best setting lies at a search boundary or coefficients are unstable.
     how: Inspect search history, convergence warnings, and coefficient variation across folds.
     used at: T.7.5
E176  Useful new OOF outputs or embeddings exist, or the current meta-feature schema contains weak redundant columns.
     how: Inspect feature provenance, alignment, correlations, and previous meta-feature ablations.
     used at: T.7.5
E177  Validated symmetries or unintended stochastic inference could explain residual variance.
     how: Inspect transforms, evaluation mode, and repeated prediction files.
     used at: T.8
E178  Prediction bias, scale, or probability mass conflicts with the output requirements or validation labels.
     how: Inspect residuals, calibration plots, ranges, and row sums.
     used at: T.8
E179  Discrete target support or degenerate ties affect the ranking metric.
     how: Inspect target levels and raw/post-processed prediction uniqueness.
     used at: T.8
E180  Auxiliary predictions or reliable metadata support a targeted correction.
     how: Inspect held-out conditional errors and correction ablations.
     used at: T.8
E181  The task has label-preserving transformations represented by the trained model.
     how: Inspect domain symmetries, training augmentations, and prior transformed-view validation results.
     used at: T.8.1
E182  A small noisy task may benefit from stochastic head averaging and dropout can be activated deliberately.
     how: Inspect model mode and verify that repeated dropout-enabled passes actually vary while other layers remain appropriate for inference.
     used at: T.8.1
E183  Repeated inference changes scores unexpectedly or dropout settings are being tuned while inactive.
     how: Compare identical-run predictions and inspect evaluation mode, random transforms, seeds, and dynamic batching.
     used at: T.8.1
E184  Held-out regression residuals show a stable offset or a reliable reference example exposes one.
     how: Inspect signed residual means across folds and reference-example prediction error.
     used at: T.8.2
E185  A component’s bounded activation compresses its contribution to a heterogeneous blend.
     how: Inspect pre-activation distributions and held-out blended performance across existing temperature settings.
     used at: T.8.2
E186  Class probability mass is systematically biased on a representative validation set.
     how: Compare predicted and observed class distributions and per-class calibration diagnostics.
     used at: T.8.2
E187  The task requires bounded values or row-normalized probabilities and current outputs violate that contract.
     how: Read the output requirements and compute ranges and row sums after every activation.
     used at: T.8.2
E188  Only ordering is scored and added scaling or clipping has no validated benefit.
     how: Inspect the metric’s invariances and compare rank order before and after current transforms, including ties.
     used at: T.8.2
E189  Targets occupy a small set of repeated levels while model outputs are fully continuous.
     how: Inspect unique target values and their frequencies by output column and the metric’s treatment of tied ranks.
     used at: T.8.3
E190  Existing binning collapses one or more prediction columns to a constant.
     how: Count distinct values and variance per column after binning and compare with the raw outputs.
     used at: T.8.3
E191  Exact prediction ties are common and their treatment can change the scored ordering.
     how: Inspect tied-value counts and the metric implementation, then check existing tie-preserving and tie-breaking comparisons.
     used at: T.8.3
E192  An auxiliary classifier or head gives held-out information not captured by the main prediction.
     how: Inspect its confidence, error correlation, and previously tested correction magnitudes on aligned rows.
     used at: T.8.4
E193  A prediction-time metadata condition almost determines a particular target in training and held-out examples.
     how: Cross-tabulate the condition and target by split and inspect exceptions and distribution shift.
     used at: T.8.4
E194  The current post-processing was tuned for older checkpoints or its contribution is unverified.
     how: Compare artifact versions and fixed-model correction-on versus correction-off results.
     used at: T.8.4
E195  External model weights or artifacts loaded at inference time can differ between runs despite identical code.
     how: Check whether the inference notebook references externally attached or mutable model weights that are not version-locked, causing non-reproducible predictions.
     used at: T.1
E196  The current exploration direction has consistently degraded scores across multiple recent attempts.
     how: Review the score history for the current line of experiments and determine whether repeated attempts have all resulted in regressions.
     used at: T.1
E197  A required pipeline step is disabled or skipped, preventing a valid evaluation or submission from being produced.
     how: Inspect the pipeline configuration to see if any essential step (e.g., ensembler, postprocessing) is currently disabled.
     used at: T.1
E198  Per-fold predictions and fold indices are not saved to disk, preventing offline verification of validation scores.
     how: Check whether the pipeline writes out per-fold predictions and corresponding sample indices so that scores can be independently recomputed.
     used at: T.1
E199  A global initialization call silently overrides a parameter used during inference, causing hidden inconsistency.
     how: Trace initialization routines (e.g., mt.init()) to see if they silently reset or override parameters such as batch size that affect evaluation results.
     used at: T.1
E200  No valid submission file has been produced, so external (leaderboard) scoring feedback is unavailable for comparison.
     how: Verify whether a submission file was successfully generated and submitted so that external scoring can corroborate local CV results.
     used at: T.1
E201  The public test set is too small for single-checkpoint swaps to produce meaningful score differences.
     how: Check the size of the public test set and assess whether score differences from individual checkpoint changes are within noise range.
     used at: T.1.1
E202  The expert lacks local cross-validation infrastructure to rank checkpoints without relying on the noisy public leaderboard.
     how: Determine whether a local CV pipeline exists that can score and rank candidate checkpoints independently of public LB submissions.
     used at: T.1.1
E203  Multiple recent versions have not been submitted to the leaderboard, making submission budget conservation relevant.
     how: Check whether there is a backlog of unsubmitted versions and whether the remaining submission budget is limited.
     used at: T.1.1
E204  A config mapping variant names to checkpoint versions exists or can be trivially added so switching between composite models is a one-line change.
     how: Inspect the codebase for a dictionary or configuration structure that maps variant names to checkpoint paths, enabling easy swaps.
     used at: T.1.1
E205  Early-stopping patience (early_stopping_rounds) is too short for the noise level of the current selection metric, risking premature stopping before the true best iteration.
     how: Compare the noise / variance of the selection metric across consecutive iterations to the current early_stopping_rounds setting; if metric fluctuations span more iterations than the patience window, the best checkpoint may be missed.
     used at: T.1.2
E206  Recent code changes or refactors have not yet been verified to produce valid end-to-end predictions.
     how: Check whether the latest pipeline version has been executed and its output validated or submitted.
     used at: T.2
E207  Inference-time preprocessing or feature extraction parameters differ from those used during model training.
     how: Compare spectrogram settings, normalization, scaling, transforms, and input derivation steps between inference code and the training configuration of the loaded checkpoint.
     used at: T.2
E208  Model must be constructed inside the TPU/distributed strategy scope for checkpoint loading to work correctly.
     how: Check whether the framework requires model construction within a specific device/strategy scope that load_model() alone does not satisfy.
     used at: T.2.1
E209  Loading fails or produces incorrect results due to a GPU/CPU device mismatch between the saving and loading environments.
     how: Check whether torch.load (or equivalent) needs an explicit map_location argument because the checkpoint was saved on a different device type.
     used at: T.2.1
E210  The source/input directories are read-only, so in-place file operations (mv, rename, write) on them will fail.
     how: Check whether the loading code attempts destructive or write operations on a read-only mounted filesystem.
     used at: T.2.1
E211  A duplicate or conflicting model instantiation exists that overwrites or shadows the correctly loaded model.
     how: Check whether the code creates multiple model objects and whether a later instantiation replaces the one with properly loaded weights.
     used at: T.2.1
E212  The forward-pass wiring applies an operation (activation, residual, etc.) to the wrong intermediate variable.
     how: Trace the forward method and verify each operation's input variable matches the intended tensor from the computation graph.
     used at: T.2.2
E213  The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa).
     how: Check that each stage's input variable name points to the correctly transformed (or untransformed) data object.
     used at: T.2.2
E214  A data filtering condition uses an inverted comparison operator (== instead of != or vice versa), selecting the wrong subset of rows.
     how: Inspect the filter predicate and verify the comparison operator matches the intended inclusion/exclusion logic.
     used at: T.2.2
E215  A redundant or unintended aggregation step (e.g., unweighted mean) overwrites the intended weighted blend of predictions.
     how: Search the inference script for any additional np.mean or averaging call that runs after the weighted blend is computed.
     used at: T.2.2
E216  The inference code contains a duplicated or residual preprocessing/transform step that was not present during training.
     how: Diff the inference preprocessing pipeline against the training pipeline to find steps that appear an extra time or are leftover from old code.
     used at: T.2.2
E217  Function default arguments or internal references use variable names that were renamed in a prior refactor, causing NameError or silent misuse.
     how: Search for function signatures and body references that use old variable names no longer defined in the current scope.
     used at: T.2.2
E218  The loaded data file is actually the wrong split (e.g., training set loaded instead of test set), detectable by unexpected row count or content.
     how: Compare the loaded file's row count and content against the expected test-set size and schema.
     used at: T.2.2
E219  A guard condition or code path prevents the final submission file from being written to disk.
     how: Trace the code path that writes the submission CSV and check whether any conditional or early return blocks execution.
     used at: T.2.2
E220  An indentation or scoping bug causes a critical statement (e.g., predict call) to execute outside its intended conditional or loop block.
     how: Review recent diffs for indentation changes that move statements in or out of if/for/while blocks.
     used at: T.2.2
E221  Model or artifact file paths reference an outdated directory that no longer matches the current environment's pretrained-model location.
     how: List the file paths used to load model weights and verify each resolves to an existing file in the current environment.
     used at: T.2.2
E222  After reordering or sorting rows, the submission predictions are no longer aligned to the expected ID ordering.
     how: Check whether the final submission dataframe's ID column matches the required ordering after any sort or merge operations.
     used at: T.2.2
E223  The prediction API call used at inference time does not match the model object's actual method signature or name.
     how: Inspect the model class definition and verify the method name and arguments used in the inference call exist and are correct.
     used at: T.2.2
E224  A stacking feature or ensemble member produces outputs with a different row count than the main prediction dataframe.
     how: Compare the shape (number of rows) of each member's prediction array or stacking feature column against the target dataframe; a mismatch causes misaligned or truncated predictions.
     used at: T.2.3
E225  A proposed change (e.g., higher resolution, larger model) significantly increases compute cost, making a full end-to-end run risky without a quick sanity check first.
     how: Compare estimated resource usage of the proposed configuration against available compute budget and time limits.
     used at: T.2.4
E226  Debug/development mode flags or reduced hyperparameters are still active, preventing a production-quality full run.
     how: Check for DEBUG flags, reduced n_estimators, truncated epochs, or other dev-time shortcuts that need to be reverted for a valid run.
     used at: T.2.4
E227  A feature (e.g., TTA, ensembling) was deliberately disabled for debugging and now needs to be re-enabled and validated.
     how: Review which pipeline components were turned off during debugging and confirm they have been restored and tested.
     used at: T.2.4
E228  Some augmentation or TTA variants are producing incorrect or harmful predictions that degrade the final aggregated output.
     how: Inspect individual TTA/augmentation variant outputs for anomalies or compare per-variant scores to identify harmful contributions.
     used at: T.2.4
E229  The current pipeline runs end-to-end but produces a significantly worse score than a prior known-good version, indicating a quality regression.
     how: Compare the current submission score against the best previously achieved score to confirm the pipeline has not regressed.
     used at: T.2.4
E230  Adding or switching a model/component requires editing scattered code locations rather than a single configuration entry.
     how: Check whether adding a new model or variant requires changes in multiple code locations vs. a single config addition.
     used at: T.3
E231  Duplicated inline logic across feature groups or pipeline stages requires multiple manual edits for a single conceptual change.
     how: Check whether a single logical change (e.g., adding an aggregation) requires edits in more than one code block.
     used at: T.3
E232  A deleted or freed object is still referenced later in the pipeline, preventing actual memory reclamation.
     how: Trace all references to the deleted object downstream of the deletion point; if any code path accesses it afterward, the memory is never truly freed.
     used at: T.3.1
E233  Peak memory is driven by the number of sequential inference passes (e.g., seed replicas) kept simultaneously in memory.
     how: Check whether reducing the number of sequential model runs (seed replicas) lowers the observed peak GPU memory, indicating that concurrent allocations across runs contribute to the peak.
     used at: T.3.1
E234  Duplicate DataFrame copies (e.g., X_train/X_test/y_train/y_test) are created in a loop instead of using index-based slicing into a single master DataFrame, roughly doubling memory usage.
     how: Inspect the cross-validation or processing loop to see whether new DataFrame copies are allocated rather than using views or index-based slicing on the original DataFrame.
     used at: T.3.1
E235  The competition-specific evaluation metric is already integrated into the training callback, so fast debug runs produce metric-aligned feedback without a separate evaluation step.
     how: Check whether the custom eval metric (e.g., lgb_amex_metric) is wired into the training callback, eliminating the need for a separate post-hoc evaluation pass.
     used at: T.3.2
E236  A reduced fold count was used as a temporary speed compromise for a slower algorithm and should be restored now that a faster algorithm is in use.
     how: Check whether the current fold count was reduced to accommodate a slower boosting method (e.g., dart) and whether switching to a faster method (e.g., gbdt) allows restoring the full fold count without excessive runtime.
     used at: T.3.2
E237  A faster file format (e.g., Feather) is available and would reduce repeated I/O time compared to the current data format.
     how: Check whether the current data loading format (e.g., Parquet, CSV) is a bottleneck and whether switching to a faster serialization format would meaningfully reduce per-iteration I/O time.
     used at: T.3.2
E238  Stage-2 parameters (LR, epochs, callbacks) need to be tuned independently from stage-1, requiring a decoupled iteration cycle.
     how: Check whether the pipeline has separable stages whose hyperparameters can be swept independently, avoiding full end-to-end reruns for downstream-only changes.
     used at: T.3.2
E239  Memory is not being reclaimed between heavy stages, causing accumulation that could force restarts or OOM failures during iteration.
     how: Check whether intermediate objects are freed (gc.collect, del, etc.) between pipeline stages, and whether memory accumulation is forcing unnecessary restarts that slow the cycle.
     used at: T.3.2
E240  A bug in the feature extraction code (e.g., invalid API call, wrong variable reference, or faulty transformation logic) produces incorrect or erroneous feature values.
     how: Review the feature engineering code for API misuse, variable mix-ups, or logic errors that would produce incorrect computed features.
     used at: T.4
E241  Domain-informed feature interactions or derived variables (e.g., clinical variable cross-products, matching scores) are not yet explicitly represented as input features.
     how: Check whether known domain-relevant interactions or composite variables have been engineered and included in the feature set.
     used at: T.4
E242  A recently introduced preprocessing or cleaning step caused a score regression, indicating it is harmful and should be reverted or revised.
     how: Compare scores before and after the recent preprocessing change to determine if it caused a regression.
     used at: T.4
E243  A candidate aggregation is mathematically redundant with existing aggregations already in the feature set.
     how: Check whether the proposed aggregation (e.g., sum = mean × count, var = std², etc.) is already implicitly or explicitly captured by current features, making it uninformative for tree-based models.
     used at: T.4.1
E244  Previously added aggregations or derived features caused score regression or no improvement and should be reverted.
     how: Review submission history to check whether recently added aggregation statistics or derived features degraded or failed to improve the score compared to the prior baseline.
     used at: T.4.1
E245  A previously added date/time encoding variant has not yet been validated via submission.
     how: Check whether the date encoding approach from a prior version was actually submitted and scored, or remains unvalidated.
     used at: T.4.1
E246  A previous feature engineering attempt caused pipeline bugs or inconsistencies that prevented successful submission.
     how: Check whether prior attempts at the proposed feature type failed due to implementation errors (variable mismatches, column ordering, train/test inconsistencies) rather than being genuinely uninformative.
     used at: T.4.1
E247  Multiple prior date-feature encoding variants have all failed to improve over the baseline without date features.
     how: Review submission history for all attempted S_2/date encoding strategies (days-since-max, scaled mean, global max subtraction, per-customer merge) and check whether any improved over the date-excluded baseline.
     used at: T.4.1
E248  An aggregation type applied to one column group (numeric or categorical) has not yet been applied to the other relevant column group.
     how: Check whether aggregations like 'first' or 'last' are applied consistently across both numeric and categorical feature sets.
     used at: T.4.1
E249  A proposed derived feature (ratio, log, etc.) is prone to numerical instability (division by near-zero, overflow) compared to simpler alternatives.
     how: Check whether the derived feature involves division or other operations that produce unstable values when denominators are near zero.
     used at: T.4.1
E250  Interaction/derived features should be computed on aggregated customer-level columns rather than raw row-level columns before aggregation.
     how: Check whether computing interactions on pre-aggregated row-level data vs. post-aggregated customer-level data yields more informative features.
     used at: T.4.1
E251  Prior interaction/derived feature experiments have consistently failed to improve over the current best baseline score.
     how: Review submission history to check whether interaction-style features (lag, ratio, differences between columns) have ever produced a score improvement.
     used at: T.4.1
E252  The proposed aggregation change reverses a recent edit, re-adding features that were just removed.
     how: Check whether the proposed addition was recently removed in a prior edit, indicating oscillation rather than progress.
     used at: T.4.1
E253  A recently added feature has not been validated via submission, so its individual impact is unknown.
     how: Check whether the most recently added feature or feature group was submitted and scored individually.
     used at: T.4.1
E254  Recent-window aggregation features are already computed and available for use in downstream interaction features.
     how: Check whether tail/window-based aggregation columns already exist in the feature table and can be reused for interaction features.
     used at: T.4.1
E255  A prior window-size configuration scored better than the current one, motivating reverting to the earlier setting.
     how: Compare submission scores across different window sizes (e.g., tail-3 vs tail-6) to determine which performed better.
     used at: T.4.1
E256  An alternative data format (e.g., precomputed .npy arrays) preserves raw sequence structure enabling different aggregation strategies than the current pipeline.
     how: Check whether precomputed data files retain per-entity sequence information that the current parquet-based aggregation pipeline discards.
     used at: T.4.1
E257  Public high-scoring solutions use a broader set of standard per-customer aggregations than the current feature pipeline.
     how: Compare the current aggregation set against known high-scoring public solutions to identify missing standard aggregations (e.g., mean/std/min/max/last for numeric, count/last/nunique for categorical).
     used at: T.4.1
E258  The validation metric has not yet peaked or declined as the retention fraction increases, so further expansion is warranted.
     how: Check whether the monotonic sweep of retention ratio has shown a plateau or decline; if not, the next step should be tried.
     used at: T.4.2
E259  The previous aggressive feature cut (low retention ratio) may have removed useful features, as indicated by no improvement or regression in validation.
     how: Compare validation scores before and after the aggressive cut to see if it caused a regression.
     used at: T.4.2
E260  The expert has already tried this exact retention ratio in a previous version, making this a repeated rather than novel experiment.
     how: Check version history for whether the same top_ratio value was previously tested.
     used at: T.4.2
E261  No leaderboard scores have been submitted for recent versions, so the expert lacks external validation to confirm the current feature-selection ratio is optimal.
     how: Check whether any recent versions have been submitted to the leaderboard for external feedback.
     used at: T.4.2
E262  A recent pipeline or hyperparameter change (e.g., eval metric switch, regularization update) may have shifted the optimal feature-selection ratio, motivating a re-sweep.
     how: Check whether model hyperparameters or the evaluation metric changed since the last feature-selection sweep.
     used at: T.4.2
E263  The expert is incrementally stepping through feature-selection ratios without a systematic grid search or recorded validation scores for comparison.
     how: Check whether validation scores from each retention-ratio step have been logged and compared.
     used at: T.4.2
E264  A submitted leaderboard score from a recent retention-ratio step provides a concrete baseline for comparison.
     how: Check whether a LB score exists from a nearby sweep step to serve as a reference point.
     used at: T.4.2
E265  A recent feature-exclusion experiment was not submitted to the leaderboard, suggesting local validation showed no improvement or a regression.
     how: Check whether the feature-exclusion variant was submitted; if not, infer that local validation was unfavorable.
     used at: T.4.2
E266  Feature_fraction and bagging_fraction are set to 1.0 (no subsampling), leaving room for regularization via subsampling as an alternative to hard feature removal.
     how: Check current LightGBM subsampling parameters to see if implicit feature noise reduction is already active.
     used at: T.4.2
E267  The edit changes multiple hyperparameters simultaneously alongside the feature-selection change, confounding diagnosis of what helped.
     how: Check whether the diff modifies only the feature-selection parameter or also other hyperparameters in the same commit.
     used at: T.4.2
E268  The existing preprocessing code contains an implementation bug that prevents it from executing correctly and must be fixed before evaluating the preprocessing strategy.
     how: Review the current preprocessing code for runtime errors (e.g., incorrect column deletion syntax) that make the intended transformation non-functional.
     used at: T.4.3
E269  The pretrained checkpoint was trained on single-sequence input, so switching to paired encoding at inference creates a train/inference mismatch.
     how: Check whether the checkpoint's original training used single-text or paired-text input and whether the current inference setup matches.
     used at: T.4.4
E270  The resolution-score curve from prior probes is non-monotonic or has an identified peak region, guiding the next resolution to test.
     how: Review scored submissions at different resolutions and check whether the trend is monotonic or shows a peak.
     used at: T.4.5
E271  Run-to-run variance at the current setting is large enough that the expected gain from the encoding change may not be distinguishable.
     how: Compare the magnitude of the expected improvement to the observed run-to-run score variance.
     used at: T.4.5
E272  A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated.
     how: Check whether prior runs that modified this encoding setting also changed the backbone, ensemble, or other variables simultaneously.
     used at: T.4.5
E273  Missing or NaN values in the signal or spectrogram need explicit handling before normalization and model input.
     how: Inspect the raw signal or computed spectrogram for NaN/Inf entries that would corrupt downstream normalization or inference.
     used at: T.4.5
E274  A branch's standalone score is substantially worse than the other branch, indicating it still needs improvement before ensembling.
     how: Run each branch in isolation and compare leaderboard scores to determine if one branch is dragging down the ensemble.
     used at: T.4.6
E275  The signal extraction indexing uses an incorrect sampling rate or offset, causing misaligned input segments.
     how: Verify that the window/segment extraction code uses the correct sampling rate multiplier and offset so that extracted segments correspond to the intended time intervals.
     used at: T.4.6
E276  The backbone capacity is insufficient for the number of input channels or modality complexity, requiring a larger model variant.
     how: Check whether the backbone architecture (e.g., EfficientNet-B0 vs B2) is appropriately sized for the input dimensionality after a modality change.
     used at: T.4.6
E277  A previous attempt to increase input channels worsened the score, suggesting adding more channels may not help.
     how: Review prior experiment logs where channel count was increased and check whether the score degraded.
     used at: T.4.6
E278  Removing or disabling a branch leaves unguarded code paths that break or produce incorrect inputs when that branch is absent.
     how: Inspect the data assembly and forward-pass code for references to the removed branch that are not properly conditioned on its presence.
     used at: T.4.6
E279  A full-modality baseline score exists to compare the ablation against.
     how: Confirm that a valid leaderboard or validation score from the full-modality configuration is available as a reference point before running ablations.
     used at: T.4.6
E280  A prior ablation removing one branch showed degradation compared to the full-modality baseline, confirming that branch's contribution.
     how: Review previous ablation results to see if removing any single branch caused a score drop relative to the full pipeline.
     used at: T.4.6
E281  The pretrained weights were trained with a specific fusion method, so changing the fusion strategy at inference creates a train/inference mismatch.
     how: Check whether the fusion mechanism (e.g., averaging vs concatenation) used at inference matches what was used during training of the loaded weights.
     used at: T.4.6
E282  NaN or corrupted values in inputs/targets are causing training instability (e.g., NaN losses or corrupted mixed samples).
     how: Inspect training logs and intermediate tensors for NaN propagation during data mixing or augmentation steps.
     used at: T.5
E283  The competition metric is rank-based or otherwise insensitive to the class-weight direction being explored.
     how: Check whether the target metric (e.g., Gini, capture-at-k%) is rank-based and therefore unlikely to benefit from the proposed reweighting direction.
     used at: T.5.1
E284  Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended.
     how: Compare leaderboard or validation scores before and after recent data-filtering changes to see if the filter helped or hurt.
     used at: T.5.1
E285  The group-conditioning implementation correctly identifies and matches group labels in the data (e.g., no mismatch between string labels and encoded values).
     how: Verify that the code used to condition target construction on evaluation groups actually matches rows for each group, rather than silently matching zero rows due to label-type mismatches.
     used at: T.5.2
E286  Geometric transforms (e.g., rotation) have not been previously tried and are now being introduced into the augmentation pipeline.
     how: Check the augmentation history to see whether geometric transforms like rotation were already attempted or are genuinely new.
     used at: T.5.3
E287  The proposed augmentation code was already scaffolded or commented out in a prior version and only needs to be activated, not written from scratch.
     how: Inspect previous code versions to see if the augmentation logic already exists in commented-out or disabled form.
     used at: T.5.3
E288  The previous augmentation run did not clearly improve over the non-augmented baseline, so a re-run is needed to distinguish signal from variance.
     how: Compare leaderboard scores of the augmented and non-augmented runs and assess whether the difference exceeds expected run-to-run variance.
     used at: T.5.3
E289  Multiple hyperparameters were changed simultaneously, preventing attribution of validation changes to individual parameters.
     how: Review the edit history and check whether recent changes bundled multiple hyperparameter modifications in a single iteration.
     used at: T.6
E290  A recently introduced boosting variant (e.g., DART) is conflicting with existing training infrastructure (early stopping, checkpointing) or not clearly improving scores.
     how: Check training logs and submission history for the new boosting variant to see if it caused errors, required bug fixes, or failed to improve over the baseline.
     used at: T.6
E291  The candidate backbone or model family was previously tested and underperformed, so switching back requires a clear rationale for why results would differ now.
     how: Check experiment logs for prior runs with the same backbone/family and note whether conditions (preprocessing, hyperparameters, inference setup) have materially changed.
     used at: T.6.1
E292  A structurally different model family (e.g., 1D CNN/RNN on raw signals) is a known strong complementary approach in top solutions for this task.
     how: Review public top solutions and competition write-ups to confirm that a distinct model family (different input representation or architecture class) is a proven strong component.
     used at: T.6.1
E293  The alternative predictor family has been tested in only a few configurations and has not yet matched the current best, leaving uncertainty about whether further tuning could close the gap.
     how: Count how many configurations of the alternative family have been evaluated and compare their best score to the incumbent; assess whether the search has been thorough enough to rule out the alternative.
     used at: T.6.1
E294  An alternative attention/block design is architecturally motivated to capture information (e.g., spatial) that the current block does not.
     how: Compare the architectural inductive biases of candidate blocks (e.g., SpatialAttentionBlock vs SSEBlock) and assess whether the alternative captures relevant structure the current one misses.
     used at: T.6.2
E295  The proposed head modification bundles multiple changes rather than isolating a single component's contribution.
     how: Inspect the edit diff and count how many independent changes (hidden layers, dropout, flags, pooling, etc.) are introduced simultaneously.
     used at: T.6.2
E296  A previously tested head component was evaluated under a substantially different architecture context, so its performance in the current setup is unknown.
     how: Check whether the candidate head component was last benchmarked with a different backbone, pooling, or training regime than the current one.
     used at: T.6.2
E297  A previously used head configuration (e.g., channel sizes, layer counts) is a known baseline that can be reverted to for comparison.
     how: Review experiment history for earlier head configurations and their recorded performance to identify reversion candidates.
     used at: T.6.2
E298  The checkpoint being loaded was trained with an architecture that matches (or mismatches) the head design being evaluated.
     how: Compare the architecture used to produce the checkpoint weights against the architecture defined in the current code to check compatibility.
     used at: T.6.2
E299  The current head contains a wiring bug where a layer is instantiated but never applied to the tensor flow.
     how: Trace the forward pass in the head code and verify that every instantiated layer is actually called on the appropriate input tensor.
     used at: T.6.2
E300  A recent change to the loss function or architecture invalidates previously tuned hyperparameters, requiring re-tuning of LR and regularization.
     how: Check whether the loss function, output head, or other structural component was changed after the last round of hyperparameter tuning, making old HP values unreliable.
     used at: T.6.4
E301  A previous optimization trial was confounded by a bug or misconfiguration, so its results cannot be used as valid evidence.
     how: Review logs and code for earlier trials to determine whether any implementation error (e.g., code typo, disconnected layer, wrong activation) invalidated the observed outcome.
     used at: T.6.4
E302  A recent score anomaly suggests a code or shape bug rather than a genuine model quality result.
     how: Check whether a catastrophic score drop or anomalous result is explained by a code bug (shape mismatch, missing args, variable name error) rather than a real configuration change.
     used at: T.7
E303  A previously contributing member was disabled or removed and could be re-added to the ensemble.
     how: Check version history for members that contributed to the best-scoring ensemble but were subsequently removed or disabled.
     used at: T.7
E304  The most recent member additions worsened the score compared to the prior best, suggesting those additions were not beneficial.
     how: Compare the score before and after the latest member additions to determine if they helped or hurt.
     used at: T.7
E305  Manual weight tuning has stagnated or regressed, indicating the current blending approach has saturated.
     how: Review recent weight-tuning iterations for diminishing returns or score regression.
     used at: T.7
E306  The fold count configuration does not match the number of available checkpoint files.
     how: Compare the configured fold count against the actual number of checkpoint files in the directory.
     used at: T.7
E307  The best known score was achieved with a specific subset of members, and reverting to that configuration is a viable baseline.
     how: Identify which exact member set and weights produced the historical best score.
     used at: T.7
E308  Automatic checkpoint discovery (e.g., glob) loads all fold checkpoints indiscriminately, including potentially weak folds that harm the average.
     how: Check whether the checkpoint loading mechanism filters by quality or loads everything found.
     used at: T.7
E309  Adding new backbone models has consistently improved the leaderboard score in recent iterations.
     how: Review the score trajectory across recent versions where new models were added.
     used at: T.7
E310  Multiple members were changed simultaneously, making it impossible to attribute the score change to any single member.
     how: Check whether recent edits changed multiple ensemble members or weights at once, confounding attribution.
     used at: T.7
E311  Post-processing steps interact with the ensemble configuration and their independent effect is unclear.
     how: Check whether post-processing (thresholding, entropy adjustment, etc.) was tuned jointly or independently from the ensemble composition.
     used at: T.7
E312  Run-to-run variance or platform noise is large enough that single-submission score comparisons are unreliable.
     how: Check whether repeated identical submissions produce meaningfully different scores, undermining single-run comparisons.
     used at: T.7
E313  Runtime budget is insufficient to run the full ensemble, requiring member reduction or per-sample cost savings.
     how: Check whether the current ensemble exceeds the submission time limit.
     used at: T.7
E314  Recent preprocessing or feature changes may have invalidated previously tuned ensemble weights or member selections.
     how: Check whether upstream preprocessing changes occurred since the last ensemble tuning.
     used at: T.7
E315  The current pipeline uses only a single model or checkpoint, making multi-fold averaging unnecessary or potentially harmful.
     how: Check whether the pipeline has enough distinct models/folds to benefit from ensembling.
     used at: T.7
E316  Rank conversion was already tried in a prior version and its effect size is known.
     how: Check version history for previous rank-conversion experiments and their measured deltas.
     used at: T.7.4
E317  Rank conversion has not yet been tested with the current model/ensemble configuration.
     how: Check whether the current combination of model architecture, folds, resolution, and head has been scored with rank averaging enabled.
     used at: T.7.4
E318  The model head or architecture changed since the last rank-vs-raw comparison, so the previous winner may no longer hold.
     how: Compare the current model configuration against the configuration used in the most recent rank-vs-raw test.
     used at: T.7.4
E319  A nonlinear power transform (e.g., sqrt) has already been tried and its effect is known.
     how: Check version history for power-transform experiments and their LB/CV deltas.
     used at: T.7.4
E320  The ensemble composition or model architecture has changed since the last domain-transform experiment, so its effect may differ now.
     how: Check whether any ensemble members, weights, or model components changed after the last power/rank/sigmoid transform test.
     used at: T.7.4
E321  Simple weight tuning of the arithmetic blend has already been tried and yielded only marginal improvement.
     how: Review prior weight-tuning experiments and their score deltas to confirm diminishing returns in the current domain.
     used at: T.7.4
E322  An alternative blend strategy (e.g., sigmoid, logit-space) was implemented but never scored on the leaderboard.
     how: Check submission history to see if the alternative blend strategy version was actually submitted and scored.
     used at: T.7.4
E323  With only one model source, rank averaging is a no-op or potentially harmful compared to raw predictions.
     how: Count the number of distinct model sources contributing to the blend; if only one, rank transformation has no calibration-alignment benefit.
     used at: T.7.4
E324  A rank or normalization transform is still applied in the submission/inference code despite the blending stage being changed to operate on raw outputs.
     how: Inspect the full prediction pipeline from blend output to submission file for residual rank/normalization transforms.
     used at: T.7.4
E325  A bug in the blending code was corrupting predictions, making previous domain-comparison results unreliable.
     how: Review recent bug fixes and determine whether any affected the prediction values used in prior rank-vs-raw comparisons.
     used at: T.7.4
E326  The current pipeline state is uncertain due to multiple recent NOOP or rollback versions, making it unclear which stacking configuration is active.
     how: Review version history (e.g., v28-v32) to determine whether the current stacking stage is actually enabled and which configuration is live.
     used at: T.7.5
E327  Pre-trained meta-learner artifacts (e.g., serialized ridge/kernel-ridge ensemblers) are available and compatible with the current fold prediction pipeline.
     how: Check whether saved joblib/pickle meta-learner files exist and whether their expected input schema matches the current base-model outputs.
     used at: T.7.5
E328  The meta-learner was trained on a different feature set than what is currently being fed at inference time, creating a train/inference mismatch.
     how: Compare the feature columns used when the meta-learner was fitted (e.g., with/without binned features) against the columns provided at inference time.
     used at: T.7.5
E329  The meta-learner has been retrained on the current feature set (including any newly added base models), so train/inference features are aligned.
     how: Verify that the meta-learner was re-fitted after the most recent change to the base-model feature set.
     used at: T.7.5
E330  A predict call for one of the base fold models is missing a required argument, causing that member's predictions to be invalid.
     how: Inspect inference code for each base model fold to ensure all required arguments (e.g., test_values) are passed correctly.
     used at: T.7.5
E331  Multiple diverse pre-trained meta-learner families (linear, kernel, tree-based) are available, enabling comparison or blending across stacker types.
     how: Inventory saved meta-learner artifacts and check which model families (ridge, SVR, XGB, etc.) have been fitted and serialized.
     used at: T.7.5
E332  Blending two or more different meta-learner families (e.g., Ridge + SVR) may be more robust than relying on a single meta-learner, given observed sensitivity to meta-learner choice.
     how: Compare CV/LB variance of individual meta-learners vs. a blend of two or more meta-learner predictions.
     used at: T.7.5
E333  The meta-training set is small enough that complex meta-learners (e.g., tree-based) risk overfitting the stacking layer.
     how: Check the number of meta-training rows relative to the complexity of the candidate meta-learner.
     used at: T.7.5
E334  The current stacking/averaging code has known bugs in column selection or accumulation that prevent a valid comparison of learned stacking vs. averaging.
     how: Audit the ensemble code for column-indexing errors, off-by-one bugs, or incorrect accumulation logic.
     used at: T.7.5
E335  Test-time augmentation (e.g., multi-view or flip TTA) showed negligible or no improvement in recent submissions.
     how: Compare submission scores with and without TTA; if the difference is negligible, TTA is not addressing a residual problem and may be removed or replaced.
     used at: T.8
E336  TTA (e.g., horizontal flip) has shown limited or diminishing marginal gain on recent checkpoints/ensemble compositions, suggesting limited remaining headroom.
     how: Review scored submission history to see if TTA gains have been small, inconsistent, or declining as the ensemble evolved.
     used at: T.8.1
E337  Dropping TTA to save compute is worthwhile because the freed budget can be redirected to multi-model ensembling with a larger expected gain.
     how: Compare the compute cost of TTA versus adding another model to the ensemble and estimate the marginal score impact of each.
     used at: T.8.1
E338  TTA has not yet been tested in combination with the current fold-averaging / ensemble setup, so its marginal value is unknown.
     how: Check submission logs to see whether TTA was evaluated on the current ensemble/fold configuration or only on earlier versions.
     used at: T.8.1
E339  Multi-resolution inference has been tested and the different resolutions produce meaningfully different predictions worth blending.
     how: Run the same model at multiple input resolutions and measure prediction diversity (e.g., correlation, disagreement rate).
     used at: T.8.1
E340  The loaded checkpoint weights are compatible with the modified model architecture (layer names, output dimensions).
     how: Verify that the checkpoint's state_dict keys and tensor shapes match the current model definition before running inference.
     used at: T.8.1
E341  Single-model inference scores substantially worse than multi-model ensemble, leaving room for TTA or additional inference views to close the gap.
     how: Compare the best single-model score to the current ensemble score to estimate the headroom available.
     used at: T.8.1
E342  The additional inference passes from TTA remain within the submission time/compute budget.
     how: Estimate total inference time with TTA enabled and confirm it fits within the allowed submission window.
     used at: T.8.1
E343  The averaging of TTA views is done at the correct stage (logits vs. probabilities) for optimal calibration.
     how: Inspect the inference code to determine whether softmax is applied before or after averaging across TTA views, and test both.
     used at: T.8.1
E344  The inference code path for the target model branch is enabled and correctly wired to apply the intended TTA transforms.
     how: Inspect the inference script to confirm the relevant model branch is not commented out or bypassed before adding TTA.
     used at: T.8.1
E345  The TTA change is isolated from other simultaneous modifications so its effect can be attributed cleanly.
     how: Review the diff between the current and previous version to ensure only TTA-related changes are present.
     used at: T.8.1
E346  TTA benefit depends on base model strength; weaker models may not benefit while stronger ones might.
     how: Compare TTA impact across models of different quality levels in the submission history.
     used at: T.8.1
E347  Pre-computed multi-crop tensors (e.g., left/center/right) are available at inference time but not all are being passed through the model.
     how: Check the data pipeline to see if additional crop views are already saved and could be used for TTA without extra preprocessing.
     used at: T.8.1
E348  The TTA code change has not yet been submitted for scoring, so its actual effect is unverified.
     how: Check whether a scored submission exists for the version containing the TTA modification.
     used at: T.8.1
E349  A previous calibration change (e.g., scaling multiplier) was associated with a score change, suggesting reverting or re-testing that specific setting is warranted.
     how: Compare scores before and after the specific calibration change to determine if reverting improves performance.
     used at: T.8.2
E350  Previous implementations of the calibration correction had implementation bugs (e.g., device mismatch, tokenization placement) that may have masked its true benefit.
     how: Review prior code changes for implementation errors that could have confounded the calibration correction's effect.
     used at: T.8.2
E351  Per-class or per-component multipliers have not been individually ablated to confirm each one contributes positively.
     how: Check whether each per-class multiplier has been tested in isolation (enabled vs. disabled) on a validation set.
     used at: T.8.2
E352  The calibration parameters were tuned on a different model checkpoint than the one currently in use, so they should be re-validated before applying.
     how: Check whether the current calibration settings were optimized for the current checkpoint or an earlier one.
     used at: T.8.2
E353  The output array has a dtype that causes silent data corruption or errors during serialization (e.g., non-float64 in DataFrame/CSV construction).
     how: Inspect the dtype of the prediction array before it is written to the submission file.
     used at: T.8.2
E354  A recently added or modified calibration step has not yet been submitted or validated, so its effect on the score is unknown.
     how: Check whether the latest calibration change has been evaluated via submission or held-out validation.
     used at: T.8.2
E355  Base model predictions produce meaningful, non-degenerate orderings that would benefit from discretization rather than being harmed by it.
     how: Check whether the continuous model outputs have sufficient variance and meaningful rank structure such that discretizing them would improve alignment with discrete targets rather than destroying useful signal.
     used at: T.8.3
E356  Alternative discretization methods (e.g., epsilon-based gap merging, per-column adaptive strategies) have not yet been explored beyond the current approach.
     how: Review whether the current binning/quantization strategy is the only one tried, and whether per-column epsilon merging or other adaptive approaches could better match target granularity.
     used at: T.8.3
E357  The per-column epsilon or bin-width parameters can be further refined to better match each target's actual discrete level spacing.
     how: Compare the current epsilon/bin-width values against the observed spacing between discrete target levels for each column and check for mismatches.
     used at: T.8.3
E358  The implementation contains a bug where edge cases (e.g., empty arrays, off-by-one errors) cause incorrect or degenerate overwrites.
     how: Inspect the binning/post-processing code for edge-case bugs such as empty-set handling, wrong comparison operators, or unassigned return values.
     used at: T.8.3
E359  The hard-coded column list for post-processing may be misaligned with the actual set of target columns.
     how: Compare the hard-coded column list against the dynamically determined target columns to check for missing or extraneous entries.
     used at: T.8.3
E360  Some threshold conditions have gaps or overlapping ranges that leave certain prediction values unassigned or ambiguously mapped.
     how: Enumerate all threshold boundaries and verify that every possible prediction value falls into exactly one bin with no gaps or overlaps.
     used at: T.8.3
E361  A content-based heuristic (e.g., phonetic matching) has been tested and found to degrade performance compared to the simpler metadata-based rule.
     how: Compare leaderboard scores between the content-based heuristic and the metadata-based rule to see if the content approach hurt performance.
     used at: T.8.4