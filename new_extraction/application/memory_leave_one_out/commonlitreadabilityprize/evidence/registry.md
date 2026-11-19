# evidence/registry.md — one definition per check, shared across nodes

E01  Predictions or new features no longer match the original sample identifiers or column order.
     how: Compare identifier sequences, join cardinalities and feature names before and after the changed transformation.
     used at: T.1.1
E02  The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
     how: Compare stored architecture parameters, vocabulary sizes and transform settings with the active constructor; inspect missing and unexpected weight keys.
     used at: T.1.1
E03  Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member.
     how: Trace array shapes, variances, accumulator counts and the final output variable on a small batch.
     used at: T.1.1
E04  A traceback identifies an import, callback signature, dataframe operation or device mismatch.
     how: Read the first failing traceback and inspect the arguments, installed module path, tensor devices and object types.
     used at: T.1.1
E05  No end-to-end run has yet produced a verified prediction file.
     how: Inspect run logs and verify whether a tiny input batch completes loading, transformation, prediction and output writing.
     used at: T.1.1
E06  Peak memory is reached while several models or intermediate matrices coexist.
     how: Inspect allocation logs and object lifetimes at the failed stage; measure peak memory on a representative batch.
     used at: T.1.2
E07  Repeated trials recompute identical upstream features or predictions.
     how: Compare stage timings and configuration hashes across recent runs to identify unchanged expensive stages.
     used at: T.1.2
E08  The current trial needs pipeline feedback before a full fold and estimator budget is justified.
     how: Check whether the trial changes code wiring or searches a parameter and whether reduced runs preserve a useful validation signal.
     used at: T.1.2
E09  Manual toggles, duplicated code or obsolete dependencies have caused integration errors.
     how: Compare recent tracebacks and diffs with the active configuration paths and repeated model-loading blocks.
     used at: T.1.2
E10  A final artifact is being generated with development-only fold or sample limits still enabled.
     how: Inspect effective run configuration and compare expected sample, fold and member counts with execution logs.
     used at: T.1.2
E11  The active pipeline crashes, produces invalid outputs or fails prediction parity against the working version.
     how: Run a small representative batch and compare shapes, identifiers, value ranges and saved outputs with the preserved baseline.
     used at: T.1
E12  Verified predictions are correct but measured runtime or peak memory prevents planned experiments.
     how: Check parity results alongside stage timing and memory logs.
     used at: T.1
E13  The last scored version changed several plausible causes of the score movement.
     how: Read the version diff and list changed data, model and prediction settings.
     used at: T.2.1
E14  The observed improvement is comparable to variation among unchanged reruns.
     how: Compare its delta with recorded baseline rerun range or paired-seed variation.
     used at: T.2.1
E15  A verified regression is much larger than prior gains from the proposed small adjustment.
     how: Compare the current score loss with repeated baseline results and the historical size of calibration or weight-tuning gains.
     used at: T.2.1
E16  A controlled sweep has a consistent improving direction and has not bracketed its optimum.
     how: Read the parameter-value and held-out-score table with other settings and seeds fixed.
     used at: T.2.1
E17  Recent controlled perturbations on both sides fail to improve beyond measured noise.
     how: Inspect the last sweep and repeated baseline results, including the effective blend weight of the component being tuned.
     used at: T.2.1
E18  A stable working configuration is unavailable for controlled comparisons.
     how: Check saved configurations, checkpoints and prediction artifacts for a reproducible baseline.
     used at: T.2.1
E19  Multiple rows share a subject, entity, topic or near-duplicate source that can leak across folds.
     how: Count repeated group identifiers and inspect overlap or clustering of similar examples across current folds.
     used at: T.2.2.1
E20  Rows are independent enough to split and rare labels are absent or highly uneven in current folds.
     how: Inspect group overlap and per-fold label counts or binned target distributions.
     used at: T.2.2.1
E21  A recognizable training population has a different distribution from the intended test population.
     how: Compare source metadata, label histograms and available test covariates by population.
     used at: T.2.2.1
E22  Current validation estimates fluctuate because each holdout has few informative examples.
     how: Compare fold sizes, target coverage and fold-score dispersion across existing runs.
     used at: T.2.2.1
E23  The same labeled sample appears in both training and validation for a fold.
     how: Intersect stable sample identifiers in each fold and trace special-subset insertion code.
     used at: T.2.2.1
E24  Reproducing a recorded overlapping-fold experiment is required and a separate untouched holdout exists.
     how: Confirm the experimental purpose, overlapping sample list and a disjoint holdout never used for model or threshold fitting.
     used at: T.2.2.1
E25  Model choices are frozen and independent validation has already selected the configuration.
     how: Check the experiment record and ensure final fitting will not be evaluated on its own training rows.
     used at: T.2.2.1
E26  Early stopping or further hyperparameter selection still relies on the reserved holdout.
     how: Inspect the training callbacks and remaining experiment plan.
     used at: T.2.2.1
E27  Current folds leak related rows or poorly represent the target population.
     how: Inspect identifier overlap and per-fold population and label distributions.
     used at: T.2.2
E28  Training selects checkpoints using a different objective direction or output convention from the task metric.
     how: Compare task scoring code with the evaluation callback, output activation and early-stopping configuration.
     used at: T.2.2
E29  The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better.
     how: Compare saved metric curves and the independent scores of checkpoints selected by each criterion.
     used at: T.2.2
E30  The data unit, temporal structure and missingness have not been established.
     how: Check whether a data profile reports entity history lengths, ordering, dtypes and missing-value rates.
     used at: T.2
E31  Existing scores come from a known-valid split but the cause or reproducibility of a change is unclear.
     how: Review split-integrity checks, version diffs and repeated-run scores.
     used at: T.2
E32  Reported validation gains disagree systematically with independent evaluations or the intended metric.
     how: Compare the checkpoint ranking across validation and independent scores, then inspect split membership and metric definitions.
     used at: T.2
E33  The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary.
     how: Inspect rows per entity and compare current features with history statistics, recent windows and changes.
     used at: T.3.1
E34  Known relationships or metadata have predictive meaning absent from the current columns.
     how: Inspect available fields and prior residual slices for ratios, interactions or category-conditioned differences.
     used at: T.3.1
E35  Document quality depends on length, organization or language statistics not exposed by current representations.
     how: Compare target and residual distributions against paragraph counts, sentence lengths, readability and error rates.
     used at: T.3.1
E36  Useful text variation is lexical or topical and the current vocabulary filters discard it.
     how: Inspect token frequencies, vocabulary coverage and prior n-gram or topic-model ablations.
     used at: T.3.1
E37  A pretrained encoder is available and existing lexical features miss semantic similarity.
     how: Inspect sample errors, available encoder outputs and previous dense-feature ablations.
     used at: T.3.1
E38  A related predictor has valid out-of-fold predictions aligned to the current training rows.
     how: Verify held-out provenance, row identifiers and corresponding test predictions for the candidate model.
     used at: T.3.1
E39  The proposed prediction feature was generated by fitting on the same rows it predicts.
     how: Trace model fit indices and prediction indices for every candidate feature row.
     used at: T.3.1
E40  Many current features have weak or unstable importance and the model overfits.
     how: Compare importance ranks across folds, train-validation gaps and previous cutoff experiments.
     used at: T.3.2
E41  A fixed cap or stale selection file excludes newly useful feature families.
     how: Compare current column names and importance ranks with the cached selection list and selected-feature counts.
     used at: T.3.2
E42  A particular added feature group coincides with a regression or contributes only redundant signal.
     how: Inspect the feature diff, previous group ablations and residual correlations while model settings are fixed.
     used at: T.3.2
E43  Feature ranking was computed using the same holdout that is used to report the selected model score.
     how: Trace selection-fit indices and final evaluation indices.
     used at: T.3.2
E44  Whitespace, spelling changes or text cropping differ from the trained tokenizer inputs.
     how: Compare token IDs and retained spans for identical examples under training and inference preprocessing.
     used at: T.3.3
E45  Small visual details are lost at the current image resize and compatible higher-resolution inference is available.
     how: Inspect resized samples, training resolution metadata and a prior resolution-only comparison.
     used at: T.3.3
E46  Input scale, channel order or reshape differs from the checkpoint training pipeline.
     how: Compare numerical summaries and rendered inputs from training and inference for the same raw example.
     used at: T.3.3
E47  The current time-frequency transform blurs transient events or narrow spectral patterns.
     how: Inspect spectrograms and FFT window, hop and dynamic-range settings alongside training metadata.
     used at: T.3.3
E48  Raw signals show fixed-frequency interference or extreme amplitude artifacts.
     how: Inspect power spectra and amplitude histograms before preprocessing.
     used at: T.3.3
E49  The labeled event occupies only part of the available time or image extent.
     how: Compare annotation windows and representative crops with the model input region.
     used at: T.3.3
E50  An available channel or modality captures structure not present in the active input.
     how: Inspect input schemas, channel coverage and earlier modality ablations or per-modality errors.
     used at: T.3.3
E51  Existing checkpoints were trained with different transforms from the proposed inference change.
     how: Compare the candidate transform settings with each checkpoint manifest.
     used at: T.3.3
E52  The active estimator supports NaNs and prior imputation erased useful missingness patterns.
     how: Inspect estimator support and compare missingness-conditioned validation errors with and without filling.
     used at: T.3.4
E53  The active neural or other estimator fails on NaNs or unseen categorical values.
     how: Run a small batch containing those cases and inspect finite-output checks and encoder behavior.
     used at: T.3.4
E54  Scaling, rounding or sparse-column filtering has no demonstrated benefit for the active tree model.
     how: Read isolated preprocessing ablations and compare retained signal and validation scores.
     used at: T.3.4
E55  A localized training subset has unreliable labels, duplicates or a distribution unlike the test population.
     how: Inspect annotator agreement, repeated IDs, out-of-fold residuals and source-conditioned distributions.
     used at: T.3.5
E56  Additional labeled examples have compatible labels and usable input formats.
     how: Audit label definitions, source overlap, shape compatibility and source-specific validation results.
     used at: T.3.5
E57  Unlabeled examples are available and a validated teacher produces sufficiently confident predictions.
     how: Inspect teacher calibration and pseudo-label confidence and coverage by class on held-out labeled examples.
     used at: T.3.5
E58  The target metric exposes errors concentrated in an underrepresented class or population.
     how: Compare class counts and per-class or per-population held-out errors with the metric weighting.
     used at: T.3.5
E59  Minority examples admit meaningful interpolation and earlier synthetic-data tests improved held-out results.
     how: Inspect feature neighborhoods and synthetic examples, and read matched augmented-versus-original trials.
     used at: T.3.5
E60  Stricter filtering would remove most examples of a valid target class or population.
     how: Tabulate retained counts and target distributions under the proposed filters.
     used at: T.3.5
E61  Errors concentrate on structure present in raw data but absent from the current features.
     how: Inspect residual examples against current feature definitions and raw history, text or metadata.
     used at: T.3
E62  The feature matrix is large or recently expanded and selection artifacts may be stale.
     how: Compare feature schemas, selection lists and recent feature-group ablations.
     used at: T.3
E63  A fixed trained model receives text, images or signals whose representation can be checked against training.
     how: Inspect preprocessing code, checkpoint metadata and paired rendered or tokenized examples.
     used at: T.3
E64  Missing values, unseen categories or unnecessary scaling dominate preprocessing failures or ablation results.
     how: Inspect missingness profiles, encoder coverage and model-specific finite-output checks.
     used at: T.3
E65  The limiting evidence concerns label quality, class coverage or availability of more examples.
     how: Review label agreement, population counts and available labeled or unlabeled sources.
     used at: T.3
E66  Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
     how: Inspect target definitions, censoring indicators, group outcome distributions and existing transforms.
     used at: T.4
E67  The loss and output activation optimize a different target structure from the task metric.
     how: Compare training objective, output ranges and task scoring, and inspect custom gradient and Hessian calculations.
     used at: T.4
E68  Training and validation performance are both weak at the current tree depth or leaf count.
     how: Read learning curves and capacity-only sweeps on the same feature set.
     used at: T.4
E69  Training improves while validation degrades as model complexity or feature count grows.
     how: Compare train-validation curves and depth, penalty and subsampling ablations.
     used at: T.4
E70  Training stops while validation is still improving or a lower learning rate has not been given enough rounds.
     how: Inspect learning-rate schedules, best-iteration positions and stopping patience relative to the training limit.
     used at: T.4
E71  The dataset is limited and label-preserving transformations represent variation expected at test time.
     how: Inspect transformed examples, label semantics and augmentation-only validation trials.
     used at: T.4
E72  Repeated augmentation-strength changes have already failed to improve the fixed baseline.
     how: Read controlled transform-probability and magnitude sweeps and compare with repeated-run variation.
     used at: T.4
E73  A strong backbone is followed by only a minimal pooled linear head.
     how: Inspect the model graph and previous attention or hidden-layer ablations.
     used at: T.5.3
E74  Separate heads or extra normalization layers underperform a simpler shared head.
     how: Compare controlled head experiments with matching weights and inspect train-validation gaps.
     used at: T.5.3
E75  Multiple modality embeddings are available but their current combination discards distinct information.
     how: Inspect embedding shapes and the fusion operator, and review addition-versus-concatenation ablations.
     used at: T.5.3
E76  The proposed head differs from the saved weights and no matching retrained checkpoint is available.
     how: Compare layer names and tensor shapes with the checkpoint state.
     used at: T.5.3
E77  The current model underfits and a trained larger variant is available with compatible inputs.
     how: Compare train and validation learning curves and available checkpoint manifests.
     used at: T.5.2
E78  Larger variants fail to beat the established smaller model under matched evaluation.
     how: Read standalone checkpoint scores with fixed preprocessing, thresholds and fold count.
     used at: T.5.2
E79  The current pretraining domain or architecture misses structure visible in persistent errors.
     how: Inspect error cases and compare available domain-pretrained, convolutional, transformer or signal-model candidates.
     used at: T.5.2
E80  The input is a small or unconventional pseudo-image and larger backbones previously added no signal.
     how: Inspect input dimensions and controlled backbone-size ablations.
     used at: T.5.2
E81  Several compatible training runs or stages exist but have not been compared with one fixed inference path.
     how: List saved checkpoints and their validation, stage and configuration metadata.
     used at: T.5
E82  Checkpoint-only tuning has stalled and available architectures or pretraining sources offer a different representation.
     how: Compare recent checkpoint trials and inspect the compatible candidate backbone inventory.
     used at: T.5
E83  Backbone features are strong but pooling, output heads or modality fusion remain minimal or poorly validated.
     how: Inspect the model graph and component-level ablations.
     used at: T.5
E84  Tabular features are stable and a different boosting method or interface offers the required optimization controls.
     how: Inspect current library constraints, callback needs and previous same-feature framework trials.
     used at: T.5
E85  A newer checkpoint has worse independent validation despite being from a later training stage.
     how: Compare stage-specific held-out scores under identical inference settings.
     used at: T.5
E86  Existing members make highly correlated errors and a reasonable candidate differs in inputs, targets or architecture.
     how: Compare aligned held-out residual correlations and candidate standalone scores.
     used at: T.6.1
E87  A member removal improves held-out performance or the full blend fails to beat its best component.
     how: Read leave-one-out and single-member ablations at fixed aggregation settings.
     used at: T.6.1
E88  Additional compatible folds or seeds are available and prior additions reduce prediction variance.
     how: Inspect checkpoint provenance, fold coverage and the marginal score curve as repeats were added.
     used at: T.6.1
E89  Increasing repeat count has repeatedly failed while different model families have complementary errors.
     how: Compare repeat-count sweeps and residual correlations across families.
     used at: T.6.1
E90  A component or upstream preprocessing changed since the current subset was chosen.
     how: Compare current manifests with the versions used for the last member ablation.
     used at: T.6.1
E91  The metric depends on ordering and members use incompatible output scales or target transforms.
     how: Read the metric and plot per-member score distributions and rank correlations on aligned validation rows.
     used at: T.6.2.1
E92  Raw magnitudes carry useful information and rank conversion has repeatedly failed under the current configuration.
     how: Compare raw and rank averages on the same saved predictions with unchanged weights.
     used at: T.6.2.1
E93  The task scores probability distributions and logits are available before normalization.
     how: Inspect loss expectations, saved tensor semantics and row sums after each candidate aggregation.
     used at: T.6.2.1
E94  The upstream model changed after the last raw-versus-rank comparison.
     how: Compare checkpoint and preprocessing manifests with those of the previous comparison.
     used at: T.6.2.1
E95  Members differ substantially in quality and a small contribution from a complementary weaker member helps.
     how: Read standalone, equal-blend and small-weight trials on the same validation predictions.
     used at: T.6.2.2
E96  Tuned weights fail to beat equal averaging beyond repeated-evaluation uncertainty.
     how: Compare coefficient sweeps with the uniform baseline using repeated seeds or an independent holdout.
     used at: T.6.2.2
E97  A member was upgraded or its prediction scale changed after weights were selected.
     how: Compare component manifests and prediction distributions with the last coefficient-fitting run.
     used at: T.6.2.2
E98  Only a small public score sample supports highly specific member or class weights.
     how: Inspect the provenance and number of independent examples used for coefficient selection.
     used at: T.6.2.2
E99  Member output scales or probability conventions differ.
     how: Inspect raw output ranges, activation placement and target-transform definitions.
     used at: T.6.2
E100  Members are already aligned to a common convention but their contributions are poorly balanced.
     how: Compare per-member quality, current weights and fixed-domain coefficient trials.
     used at: T.6.2
E101  Cross-fitted base predictions are available with enough held-out data to fit and validate a meta-learner.
     how: Check OOF provenance and split sizes, then inspect prior linear-stack versus fixed-blend results.
     used at: T.6.2
E102  Meta-learner fitting reused in-sample base predictions or its gains vanish on independent data.
     how: Trace base-fit, meta-fit and final-evaluation row indices and compare the resulting scores.
     used at: T.6.2
E103  Flips, mirrored channels or alternate crops preserve the task label and were compatible with training.
     how: Inspect domain semantics, transformed examples and the checkpoint augmentation recipe.
     used at: T.6.3
E104  A transform exchanges meaningful frequency, time or channel positions without a valid symmetry.
     how: Compare transformed input axes and channel semantics with the labeling rule.
     used at: T.6.3
E105  Controlled TTA trials show no reliable gain for this checkpoint or ensemble.
     how: Compare identity-only and transformed-view predictions under identical seeds and aggregation.
     used at: T.6.3
E106  Current errors vary by crop or orientation and averaging available valid views helped prior trials.
     how: Inspect per-view held-out errors and the matched averaging ablation.
     used at: T.6.3
E107  The pool lacks independent predictions or includes demonstrably harmful members.
     how: Inspect per-member scores, residual correlations and leave-one-out ablations.
     used at: T.6
E108  The member pool is stable but output conventions or coefficient choices have not been validated.
     how: Compare saved prediction distributions and previous combination-rule experiments.
     used at: T.6
E109  Valid alternate input views are available for the same trained checkpoints.
     how: Inspect transform semantics, checkpoint metadata and matched TTA trial results.
     used at: T.6
E110  Inference budget cannot accommodate further model or view passes but saved predictions are available.
     how: Compare measured pass times with the remaining budget and inspect saved prediction artifacts.
     used at: T.6
E111  Targets occupy discrete ordered levels and the metric is sensitive to class boundaries or ties.
     how: Inspect the training target histogram and compute the metric on a saved prediction sample under rounding and continuous output.
     used at: T.7.2
E112  Threshold fitting improves tuning folds but loses to simple rounding on independent folds.
     how: Compare fitted cutpoints with fixed rounding on an untouched calibration-evaluation split.
     used at: T.7.2
E113  The metric is unchanged by strictly monotone rescaling and no discretization gain has been established.
     how: Read the scoring implementation and compare rankings before and after the proposed rescaling.
     used at: T.7.2
E114  A new checkpoint or blend has shifted the prediction distribution since thresholds were fitted.
     how: Compare output histograms and threshold-crossing counts with the original calibration predictions.
     used at: T.7.2
E115  Discretization collapses an output column to a constant or introduces harmful ties.
     how: Count unique outputs and inspect per-column rank variance under the candidate boundaries.
     used at: T.7.2
E116  The current output is already valid and additional random perturbations only reorder close predictions.
     how: Inspect the task metric and compare deterministic outputs with prior noise-injection trials.
     used at: T.7.2
E117  Outputs have the wrong direction, link function, range or calibration for the required predictions.
     how: Read submission semantics and inspect score signs, ranges, probability sums and calibration plots.
     used at: T.7
E118  The required labels are discrete or the rank metric is affected by the target tie structure.
     how: Inspect label support, the scoring implementation and current rounding behavior.
     used at: T.7
E119  A known subgroup or metadata rule explains systematic residuals beyond the current model.
     how: Compare group-conditioned errors and the reliability of the proposed indicator on held-out rows.
     used at: T.7
E120  The proposed subgroup correction uses information unavailable or differently defined at inference.
     how: Compare training and test schemas and trace how each correction indicator is produced.
     used at: T.7
E121  The proposed transform is strictly monotone on a single output and evaluation only uses ordering.
     how: Check the mathematical transform and compare prediction ranks before and after it.
     used at: T.7
E122  The pipeline crashes or fails output, alignment or checkpoint-consistency checks.
     how: Inspect the first failing log entry and a tiny end-to-end run including the saved prediction file.
     used at: T
E123  Current score differences are confounded, noisy or based on an unrepresentative validation split.
     how: Compare version diffs, unchanged reruns, fold membership and independent scores.
     used at: T
E124  Error analysis points to missing information, label problems or input representation mismatch.
     how: Inspect residual examples with raw data, feature schemas, annotation quality and preprocessing metadata.
     used at: T
E125  Learning curves show undertraining, overfitting or an objective mismatch with usable current inputs.
     how: Inspect train-validation curves, stopping points and the relationship between loss and task scoring.
     used at: T
E126  The current model has plateaued and compatible alternative checkpoints or architectures are available.
     how: Review controlled recent trials and the manifest of trained candidate models.
     used at: T
E127  Multiple valid predictors or valid alternate input views have complementary errors.
     how: Compare aligned held-out predictions, residual correlations and per-view errors.
     used at: T
E128  Predictions are valid but their scale, discretization or subgroup bias mismatches the scoring requirements.
     how: Inspect task scoring, label support, calibration plots and subgroup residuals.
     used at: T
E129  Measured runtime or peak memory prevents completing planned validation experiments.
     how: Read stage timings and memory logs from a representative run.
     used at: T
E130  The current parameter search has too few data points to identify the optimum.
     how: Check whether the sweep covers enough values to bracket or converge on the best setting.
     used at: T.2
E131  The pipeline has an unresolved code bug (e.g., missing column, signature mismatch, wrong variable reference) that prevents producing a valid submission.
     how: Attempt an end-to-end run and check whether it completes without error and produces a submittable output file.
     used at: T.2
E132  Each successive addition to the ensemble has yielded improvement, suggesting the search space is not yet saturated.
     how: Review the score trajectory across recent additions to see if gains are still consistently positive.
     used at: T.2
E133  The baseline is far enough from competitive that bundling multiple known-good changes is more efficient than sequential ablation.
     how: Compare current score to competitive threshold and estimate time cost of individual ablations.
     used at: T.2
E134  OOF predictions from the current fold count are too noisy for reliable threshold or weight optimization.
     how: Estimate variance of OOF scores across folds and check whether increasing folds would meaningfully reduce it.
     used at: T.2
E135  Recent tuning iterations have yielded diminishing or oscillating returns, suggesting the current search direction is exhausted.
     how: Plot score changes over recent tuning edits and check for a plateau or oscillation pattern.
     used at: T.2
E136  The current CV configuration makes each experimental iteration too slow to test planned improvements in the available time.
     how: Estimate wall-clock time per experiment and compare to the number of experiments remaining.
     used at: T.2
E137  Trained model variants or saved artifacts are available but have not yet been tested in the current ensemble.
     how: Check the saved-models directory for untested checkpoints or model variants.
     used at: T.2
E138  Inference-time transforms (resolution, normalization, augmentation) differ from those used during training, causing a train/eval mismatch.
     how: Compare the preprocessing and augmentation pipeline applied at inference time against the one used during training for the checkpoint being evaluated.
     used at: T.2.2
E139  The model's blend weight is small enough that individual overfitting has negligible impact on the ensemble prediction.
     how: Check the model's weight in the final ensemble and estimate the maximum score shift from that component overfitting.
     used at: T.2.2
E140  The task metric is too expensive to compute, limiting the number of evaluation trials or CV folds that can be run.
     how: Measure wall-clock time per metric evaluation and compare against the budget needed for the planned number of Optuna trials or CV folds.
     used at: T.2.2
E141  Changing the train/validation split ratio (e.g., 80/20 vs 85/15) has produced a measurable score change in prior experiments.
     how: Compare leaderboard or CV scores across experiments that differed only in split ratio.
     used at: T.2.2.1
E142  Reducing fold count frees compute budget for additional hyperparameter experiments during active tuning.
     how: Estimate wall-clock savings from fewer folds and compare against the cost of planned hyperparameter sweeps.
     used at: T.2.2.1
E143  A previous experiment with a different fold count achieved a better leaderboard score than the current fold count.
     how: Compare LB scores across submissions that differed primarily in the number of CV folds.
     used at: T.2.2.1
E144  Reducing fold count would meaningfully reduce training time while keeping enough folds for stable OOF estimates.
     how: Estimate per-fold training time and check whether the remaining fold count still yields acceptably low variance in OOF metrics.
     used at: T.2.2.1
E145  Reducing holdout/validation size gives more training data, which may improve score when the dataset is small or the model is a minor blend component.
     how: Check dataset size and whether the model is a small-weight blend component where marginal training data matters more than validation precision.
     used at: T.2.2.1
E146  The stratification target used for splitting is a noisy or unreliable proxy for the actual label distribution used in scoring.
     how: Compare the stratification column's values against the scoring-metric labels to assess alignment and noise.
     used at: T.2.2.1
E147  The current clustering input for group-based splitting does not capture topic or text similarity as well as text-based representations (e.g., TF-IDF, embeddings).
     how: Compare cluster coherence or downstream CV-LB correlation when using engineered numeric features vs. text-based representations for group assignment.
     used at: T.2.2.1
E148  The clustering fit and predict steps use mismatched inputs, causing incorrect group assignments for the CV splitter.
     how: Inspect the code to verify that kmeans.fit() and kmeans.predict() receive identically-structured feature matrices.
     used at: T.2.2.1
E149  Topic-based or cluster-based grouping produced CV estimates that did not correlate well with LB or showed problematic fold-score dispersion.
     how: Compare CV-LB rank correlation and per-fold score variance under group-based splitting vs. random/stratified splitting.
     used at: T.2.2.1
E150  An external dataset with actual topic or group labels is available and could replace inferred clusters for group-based splitting.
     how: Check available Kaggle input datasets or external sources for pre-labeled topic/group annotations.
     used at: T.2.2.1
E151  Setting n_splits close to the number of distinct groups/topics allows each fold to hold out one or a few complete groups, approximating leave-one-group-out CV.
     how: Count distinct groups/topics and compare against the chosen n_splits to see if near-LOGO CV is feasible.
     used at: T.2.2.1
E152  Sample weighting was already attempted and did not improve CV/LB, motivating a fold-structure change instead.
     how: Review recent experiment logs for sample-weighting results and confirm they did not yield improvement.
     used at: T.2.2.1
E153  A nested CV scheme (outer × inner folds) could produce more robust OOF estimates than a flat scheme with the same total number of models.
     how: Compare OOF estimate variance and CV-LB correlation between nested and flat CV designs.
     used at: T.2.2.1
E154  Inner fold indices in the nested CV are not correctly mapped back to original dataset indices, causing data misalignment.
     how: Trace the index mapping from inner-fold splits back to the original DataFrame and verify correctness.
     used at: T.2.2.1
E155  The current CV splitting operates on a subset rather than the full dataset, potentially excluding useful training rows.
     how: Compare the number of rows entering the CV splitter against the total available labeled rows.
     used at: T.2.2.1
E156  Recently added engineered features have not improved the score, suggesting a different feature source or transformation type is needed.
     how: Check whether the last several feature additions failed to improve validation/LB scores, indicating diminishing returns from the current feature engineering direction.
     used at: T.3
E157  A previously promising feature variant was replaced or removed before being confirmed on the leaderboard.
     how: Check version history for a feature change that showed improvement but was superseded without a submission to lock in the gain.
     used at: T.3
E158  Pretrained checkpoints for an additional modality or model are available and compatible with the current inference pipeline.
     how: Check whether trained model files for an unused modality or architecture exist and can be loaded without modification.
     used at: T.3
E159  A second data modality has been developed and produces valid predictions that can be blended with the primary modality.
     how: Check whether a separate modality pipeline already generates well-formed predictions ready for ensembling.
     used at: T.3
E160  Multi-resolution or multi-window variants of the same modality are known to be effective but have not all been tried.
     how: Check competition discussion, public solutions, or literature for evidence that varying resolution/window parameters of the input yields complementary views.
     used at: T.3
E161  Input preprocessing parameters were changed simultaneously and their individual effects are unknown.
     how: Check whether multiple preprocessing hyperparameters were altered in the same version without ablation.
     used at: T.3
E162  Overlapping or duplicate observation windows from the same source are present in the training set, causing redundancy.
     how: Check whether the training data contains near-duplicate rows from the same recording or document that inflate effective sample count without adding information.
     used at: T.3
E163  A recently added input modality or feature source did not improve or worsened the score.
     how: Check whether the most recent modality/feature addition led to a score regression or no improvement on validation/LB.
     used at: T.3
E164  A new input modality or feature source was added in the prior version but has not yet been scored.
     how: Check whether the last version introduced a new input but no submission or validation score was recorded for it.
     used at: T.3
E165  A specific model or modality previously demonstrated a score improvement when added to the ensemble.
     how: Check version history for evidence that including a particular model/modality in the ensemble yielded a measurable gain.
     used at: T.3
E166  A previous attempt to add a modality or feature source failed due to preprocessing bugs rather than inherent lack of value.
     how: Check whether a prior modality/feature addition that hurt the score had known preprocessing errors that could explain the failure.
     used at: T.3
E167  Multiple feature sources were added simultaneously and need to be tested individually to isolate their contributions.
     how: Check whether the last version combined multiple new features without individual ablation submissions.
     used at: T.3
E168  A stacked prediction feature is fitted on the same rows it predicts, creating target leakage.
     how: Check whether any meta-feature (e.g., SVR/NN OOF predictions) is computed using in-sample fitting rather than proper out-of-fold or held-out fitting.
     used at: T.3
E169  The unsupervised feature extractor is fit on a mixed population that biases representations toward the non-target subpopulation.
     how: Check whether TF-IDF, embeddings, or similar unsupervised features are fit on a dataset where the target subpopulation is a minority, skewing learned representations.
     used at: T.3
E170  Predictions from a trained model are available but not yet used as features in the downstream learner.
     how: Check whether a trained model (e.g., transformer, NN) has produced predictions that could serve as meta-features but are not yet included in the feature set.
     used at: T.3
E171  An alternative pretrained model or module may produce richer or better-aligned features than the one currently used.
     how: Check whether a different transformer or pretrained module is available that could replace or supplement the current feature source.
     used at: T.3
E172  The expert is incrementally stepping through feature-selection cutoff values without a systematic grid search or recorded comparison of validation scores.
     how: Check whether the expert has a comparison table or grid of validation scores at each tried ratio, or is blindly stepping one value at a time.
     used at: T.3.2
E173  Validation or leaderboard scores have been monotonically improving as the feature retention ratio increases, suggesting further expansion may still help.
     how: Review the score trajectory across recent feature-ratio experiments to see if the trend is still improving.
     used at: T.3.2
E174  The previous feature-set change was not submitted to the leaderboard, so there is no external evidence of its effect.
     how: Check whether the last feature-set modification has a corresponding leaderboard submission for comparison.
     used at: T.3.2
E175  The feature targeted for ablation is known to be important from external solutions or domain knowledge, making it a meaningful diagnostic probe.
     how: Check external references or domain knowledge for whether the candidate feature is expected to carry strong signal.
     used at: T.3.2
E176  A feature-engineering function contains a coding bug that corrupts its output.
     how: Inspect the code of the feature-generation function for logical or indexing errors.
     used at: T.3.2
E177  The expert plans to use leaderboard feedback to iteratively restore pruned features rather than trusting the importance ranking alone.
     how: Check whether the expert's stated plan includes a restore-on-regression loop after aggressive pruning.
     used at: T.3.2
E178  Previous feature-count experiments show a non-monotonic relationship between count and score, and the current cutoff direction is informed by that evidence.
     how: Review the score history across different feature counts to determine whether the optimum has been bracketed.
     used at: T.3.2
E179  Features being considered for expansion are highly correlated with existing features, adding redundancy rather than new signal.
     how: Check pairwise correlations or VIF among the candidate and existing features.
     used at: T.3.2
E180  Model capacity hyperparameters (depth, leaves) are being changed simultaneously with the feature count, confounding their individual effects.
     how: Check whether the current edit changes both model capacity and feature-set size at the same time.
     used at: T.3.2
E181  A prior version using a specific precomputed feature-selection file achieved the best known score.
     how: Check the version history to see which feature-selection configuration produced the highest score.
     used at: T.3.2
E182  The expert is adjusting model capacity hyperparameters (e.g., max_depth) as a proxy for feature-set complexity rather than directly changing the feature cutoff.
     how: Check whether the code change modifies a model hyperparameter rather than the feature selection threshold.
     used at: T.3.2
E183  Missingness is concentrated in specific columns with extreme NA rates that differ substantially from the rest of the feature set.
     how: Compute per-column missing-value rates and check whether any columns have NA rates that are outliers relative to the overall distribution of missingness across features.
     used at: T.3.4
E184  The oversampling or rebalancing is applied only to an unsupervised preprocessing step, not to the supervised label or fold structure.
     how: Check whether the training-population change affects the supervised objective or only an auxiliary unsupervised component (e.g., TF-IDF fitting).
     used at: T.3.5
E185  A smaller backbone variant is available and could serve as a useful baseline or ensemble complement.
     how: Check whether a trained smaller-backbone checkpoint exists and whether it could add diversity to an ensemble or serve as a diagnostic baseline.
     used at: T.5.2
E186  The alternative backbone has undergone significantly fewer training/tuning iterations than the current backbone.
     how: Compare the number of training iterations or checkpoint refinements between the current and candidate backbones to assess maturity.
     used at: T.5.2
E187  Recent checkpoint swaps within the current backbone have shown score degradation.
     how: Review the score trajectory of recent checkpoint versions within the same backbone to detect a worsening trend.
     used at: T.5.2
E188  The proposed change is only a minor checkpoint version bump within the same architecture, not a true capacity or family change.
     how: Inspect the edit to determine whether it actually changes backbone scale/family or merely swaps a checkpoint version within the same architecture.
     used at: T.5.2
E189  A previously successful backbone variant has not been re-evaluated after recent pipeline changes.
     how: Check whether pipeline changes (transforms, preprocessing, postprocessing) have occurred since the last evaluation of a previously strong backbone variant.
     used at: T.5.2
E190  An intermediate-sized backbone variant exists that has not yet been evaluated, despite smaller and larger variants having been tried.
     how: List all available backbone size variants in the family and check whether any intermediate sizes remain untested.
     used at: T.5.2
E191  The candidate backbone is directly available in the framework's model zoo and compatible with the current input pipeline without major refactoring.
     how: Verify that the candidate backbone can be loaded from the standard library and accepts the current input shape/format without pipeline changes.
     used at: T.5.2
E192  A previous backbone comparison used a different library/implementation, so the result may reflect implementation mismatch rather than true capacity difference.
     how: Check whether prior backbone comparisons used the same model library (e.g., timm vs torchvision) to rule out implementation confounds.
     used at: T.5.2
E193  The larger backbone requires batch size reduction or other memory accommodations to fit within hardware constraints.
     how: Estimate GPU memory usage for the larger backbone and check whether batch size or other settings must be adjusted to avoid OOM.
     used at: T.5.2
E194  The larger backbone's poor score may be attributable to stale or miscalibrated postprocessing (e.g., thresholds, ensemble weights) rather than inferior representation.
     how: Check whether postprocessing parameters (rounding thresholds, ensemble weights) were re-optimized after switching backbone scale.
     used at: T.5.2
E195  An alternative training-hyperparameter checkpoint of the candidate backbone is available and has not yet been tested.
     how: Check whether multiple checkpoints trained with different hyperparameters (learning rate, schedule, etc.) exist for the candidate backbone.
     used at: T.5.2
E196  Previous large-backbone trials used fewer ensemble members (folds/seeds) than the best smaller-backbone submission, confounding the comparison.
     how: Compare the number of ensemble members (folds, seeds) used in the large-backbone trial versus the best smaller-backbone submission.
     used at: T.5.2
E197  A different training strategy (e.g., intermediate pretraining, different fine-tuning recipe) for the larger backbone might close the gap with the smaller model.
     how: Check whether alternative training strategies (ITPT, different fine-tuning schedules) have been tried for the larger backbone.
     used at: T.5.2
E198  A hybrid variant (e.g., large backbone with reduced hidden dimension) is available that might combine large-model pretraining benefits with smaller-model stability.
     how: Check whether reduced-dimension or distilled variants of the larger backbone exist and are available.
     used at: T.5.2
E199  A previously high-scoring backbone/config combination motivates reverting to or re-evaluating that configuration.
     how: Check the leaderboard history for a prior backbone/config that achieved a strong score and has not been revisited.
     used at: T.5.2
E200  Historical results showed that scaling up the backbone consistently improved scores, so a reversal of that pattern in the current pipeline suggests a bug or confound.
     how: Compare the backbone-scaling trend in the current pipeline against the established trend from prior pipeline versions.
     used at: T.5.2
E201  The pipeline's consistent underperformance across all backbone sizes suggests a code or configuration bug rather than a backbone selection problem.
     how: Check whether all backbone sizes underperform expectations uniformly, which would indicate a pipeline-level issue rather than a backbone-specific one.
     used at: T.5.2
E202  An alternative attention/head block design is available but has not yet been tested as a replacement for the current head.
     how: List the head block variants considered or previously used and check whether each has been evaluated under the current architecture and training setup.
     used at: T.5.3
E203  The current head's capacity (e.g., channel widths or layer sizes) may be too small to capture the required patterns.
     how: Compare the head's parameter count and channel dimensions against the complexity of the task and check whether increasing capacity has been tried.
     used at: T.5.3
E204  A previous configuration with the same head parameters was already tested and its score is known, making a rerun redundant.
     how: Check the experiment log for prior runs that used the identical head configuration and note their scores.
     used at: T.5.3
E205  The fusion head approach was only tested in a confounded setting (alongside other changes), so its standalone effect on performance is unknown.
     how: Review experiment history to determine whether the fusion head was ever evaluated in isolation without concurrent changes to other components.
     used at: T.5.3
E206  Adding more fold checkpoints to the ensemble/fusion head is expected to improve robustness based on prior evidence.
     how: Check whether previous experiments showed consistent improvement when additional fold models were added to the ensemble.
     used at: T.5.3
E207  A layer in the head (e.g., BatchNormalization) is defined but never applied to the tensor, making it a no-op.
     how: Trace the forward pass of the head and verify every defined layer is actually called on the input tensor.
     used at: T.5.3
E208  A code bug (e.g., shape mismatch, wrong variable, broken loop, path error) prevents the ensemble pipeline from executing correctly or producing valid blended predictions.
     how: Inspect the ensemble/inference code for runtime errors, shape mismatches, incorrect variable references, or broken control flow that prevent correct prediction aggregation.
     used at: T.6
E209  Additional trained checkpoints, model variants, or pretrained artifacts are available but have not yet been included in the ensemble pool.
     how: Check input directories, dataset artifacts, and training outputs for model files or saved predictions not currently loaded by the ensemble script.
     used at: T.6
E210  The pipeline uses only a single random seed for cross-validation, so multi-seed averaging is a straightforward variance-reduction opportunity.
     how: Check whether the CV loop is run with a single seed and whether repeating it with different seeds and averaging is feasible within the inference budget.
     used at: T.6
E211  Prior experiments with negative or alternative ensemble weights revealed the direction of a member's correlation, informing the combination rule.
     how: Review logs of past weight-search experiments (e.g., negative-weight trials) to determine whether auxiliary signals are positively or negatively correlated with the target.
     used at: T.6
E212  Multiple fold checkpoints from cross-validation are available but only a subset is being loaded or averaged during inference.
     how: Compare the number of fold checkpoint files on disk with the loop bounds or explicit fold list in the inference script.
     used at: T.6
E213  Run-to-run variance is large enough that single submissions cannot reliably distinguish between ensemble configurations or checkpoint quality.
     how: Compare the magnitude of observed score fluctuations across repeated identical submissions to the score differences between candidate configurations.
     used at: T.6
E214  Historical experiments show a monotonic improvement trend when adding more ensemble members, suggesting further expansion is beneficial.
     how: Review the score trajectory across prior versions as the member count increased (e.g., 1→2→6→20 models).
     used at: T.6
E215  Simplifying a noisy ensemble member (e.g., reducing its internal variant count) may improve its contribution to the overall blend.
     how: Check whether any member is itself a complex sub-ensemble whose internal variants may be adding noise rather than signal.
     used at: T.6
E216  Previous ensemble composition and combination-rule changes have already been explored and are yielding diminishing returns.
     how: Review the version history of pool membership and weighting experiments to assess whether recent changes produced meaningful score improvements.
     used at: T.6
E217  Pseudo-labeled checkpoint variants for the same architecture improved scores in prior experiments, suggesting similar variants should be tried.
     how: Check training logs or prior submissions for evidence that pseudo-label-trained checkpoints outperformed their non-pseudo counterparts.
     used at: T.6
E218  The averaging domain (raw vs rank vs other transform) is the untested variable in the current combination rule.
     how: Check whether the current experiment is specifically varying the averaging domain (e.g., raw mean vs rank-averaging).
     used at: T.6.2
E219  The most recent raw-vs-rank comparison favoured raw averaging.
     how: Review the last experiment that compared raw and rank averaging and note which performed better.
     used at: T.6.2
E220  Previous fine-grained weight or hyperparameter tuning failed to improve over a simpler default, suggesting reverting to simpler settings.
     how: Check whether the last weight-tuning or HP-tuning run improved over the simpler baseline.
     used at: T.6.2
E221  The competition metric is non-linear or rank-based, making analytical weight selection unreliable and requiring empirical search.
     how: Determine whether the target metric is non-linear/rank-based and thus incompatible with closed-form optimal weights.
     used at: T.6.2
E222  The averaging or stacking step references incorrect column prefixes, causing wrong model-group predictions to be used.
     how: Verify that column name prefixes in the blend/meta-learner code match the actual model-group naming convention.
     used at: T.6.2
E223  Previous averaging-domain experiments showed only marginal differences, suggesting a nonlinear transformation (e.g., sigmoid) is worth trying.
     how: Check whether prior raw-vs-rank comparisons yielded negligible differences, motivating exploration of alternative transforms.
     used at: T.6.2
E224  The meta-learner's hyperparameters have not yet been tuned with automated search over an appropriate range.
     how: Check whether an automated HP search (e.g., Optuna) has been run for the current meta-learner and whether the search range was adequate.
     used at: T.6.2
E225  A hierarchical or per-target-group meta-learner approach has not yet been fully tried and validated.
     how: Check whether a per-group-then-blend or hierarchical stacking strategy has been attempted and submitted.
     used at: T.6.2
E226  Switching from L2 (Ridge) to L1 (Lasso) regularization in the meta-learner may improve sparsity by zeroing out unhelpful base models.
     how: Check whether L1 regularization has been tried for the meta-learner and whether it improved sparsity or performance.
     used at: T.6.2
E227  The Lasso (L1) meta-learner caused a large regression compared to Ridge, so reverting to Ridge is warranted.
     how: Compare the Lasso meta-learner's OOF/LB score against the Ridge baseline to see if Lasso regressed.
     used at: T.6.2
E228  Greedy feature (model) elimination on OOF data has not yet been tried with the current expanded model pool.
     how: Check whether a greedy forward/backward model selection pass has been run on the latest set of base models.
     used at: T.6.2
E229  The constrained weighted blend (positive weights, sum-to-one) underperformed the prior Ridge meta-learner.
     how: Compare the constrained blend's OOF/LB score against the Ridge stacking baseline.
     used at: T.6.2
E230  The final submission post-processing (e.g., rankdata) contradicts the intended raw-space blending, potentially negating its benefit.
     how: Check whether a downstream rank transform is applied after a raw-space blend, making the raw-space choice moot.
     used at: T.6.2
E231  A conditional offset or correction on a subset of rows (e.g., boosting predictions for specific indices) could improve the blend beyond global weight changes.
     how: Check whether row-level or group-level additive/multiplicative corrections have been considered for the blend.
     used at: T.6.2
E232  The observed score difference between raw and rank averaging is negligibly small (e.g. <0.001), favoring the simpler default.
     how: Compare the magnitude of the raw-vs-rank score delta from the most recent valid experiment.
     used at: T.6.2.1
E233  Historically, the stronger or better-calibrated ensemble members have performed better under raw averaging than rank averaging.
     how: Review per-model ablation logs to see whether top-performing members' contributions are better preserved in raw space.
     used at: T.6.2.1
E234  The last raw-versus-rank comparison is confounded by an unrelated change (member subset, untuned weights, or a code bug), making the result unreliable.
     how: Check whether any variable other than the averaging domain changed between the comparison runs.
     used at: T.6.2.1
E235  Rank-space averaging has consistently produced the best leaderboard scores across recent iterations.
     how: Review the last several submission versions and confirm whether rank-space was used in all top-scoring entries.
     used at: T.6.2.1
E236  The inference resolution differs from the training resolution, and matching or varying resolution is expected to meaningfully affect predictions.
     how: Compare the resolution used at training time with the resolution set for inference; check if resolution mismatch is known to help or hurt.
     used at: T.6.3
E237  Different inference resolutions on the same checkpoint produce meaningfully different predictions that could benefit from multi-resolution averaging.
     how: Run the same checkpoint at two or more resolutions and measure prediction divergence or complementary error patterns.
     used at: T.6.3
E238  Single-model inference scores substantially worse than the multi-model ensemble, leaving room for TTA to close the gap.
     how: Compare single-model score to ensemble score; if the gap is large, TTA may provide complementary diversity similar to adding models.
     used at: T.6.3
E239  The proposed TTA transform is a known effective technique in strong public solutions or established baselines for this task.
     how: Review top public solutions and competition discussions to see if the specific TTA transform is commonly used and beneficial.
     used at: T.6.3
E240  The preprocessing pipeline has changed substantially since the last TTA trial, requiring re-evaluation of TTA effectiveness.
     how: Check whether data preprocessing (spectrograms, normalization, cropping) has changed since the last TTA experiment; if so, prior TTA results may not transfer.
     used at: T.6.3
E241  The TTA change is being combined with another inference change in the same submission, confounding the comparison.
     how: Check whether the current commit changes only TTA settings or also modifies other inference components (e.g., enabling/disabling branches, changing models).
     used at: T.6.3
E242  The TTA configuration was previously coded but never submitted for leaderboard scoring, so a clean submission is needed to measure its effect.
     how: Check submission history to see if the current TTA setting has already been scored on the leaderboard or only run locally/not submitted.
     used at: T.6.3
E243  The current base model is substantially stronger than the model on which TTA was previously tested, so prior TTA results may not generalize.
     how: Compare the base model checkpoint used in the last TTA trial to the current one; if the model has improved significantly, TTA benefit may differ.
     used at: T.6.3
E244  The required TTA input tensors are already computed and cached during preprocessing, so enabling TTA adds only forward-pass cost.
     how: Check whether the transformed views needed for TTA are already available in the preprocessing pipeline or require additional data loading/transformation.
     used at: T.6.3
E245  A concave (power < 1) transform applied before averaging changes how model disagreements are resolved, altering the blend beyond a simple monotone rescaling of the final output.
     how: Check whether the proposed transform is applied before an aggregation step (e.g., averaging), which means it is not a simple monotone post-hoc rescaling but changes the effective weighting of confident vs. uncertain predictions.
     used at: T.7
E246  The proposed transform was introduced alongside other changes and its isolated effect on the evaluation metric has not been measured.
     how: Review the submission history to determine whether the transform's effect was confounded with other simultaneous changes.
     used at: T.7
E247  A concave power transform (exponent < 1) was previously tested and showed a positive effect on the evaluation score.
     how: Check prior experiment logs for evidence that this specific transform improved the score.
     used at: T.7
E248  Per-class multipliers have shown mixed or negative results in prior experiments, suggesting they may not consistently help.
     how: Review prior experiment logs for the effect of per-class multipliers across different model versions.
     used at: T.7
E249  Per-class multipliers consistently improved the leaderboard score across prior versions.
     how: Review prior experiment logs for consistent positive effect of per-class multipliers.
     used at: T.7
E250  Different inference scripts implement different post-processing or rounding logic that could produce different final predictions.
     how: Compare the post-processing code paths in the two inference scripts for differences in rounding, aggregation, or ordinal conversion.
     used at: T.7
E251  The MinMaxScaler normalization step added in a recent version degraded the evaluation score compared to the version without it.
     how: Compare leaderboard scores before and after the introduction of MinMaxScaler normalization.
     used at: T.7
E252  The post-processing pipeline interacts with the training loss function in a way that masks or amplifies training errors.
     how: Analyze whether the distribution-mapping post-processing and the custom loss function have conflicting assumptions about the output distribution.
     used at: T.7
E253  A previous change in the discretization method (e.g., rounding vs. threshold binning) coincided with a score change.
     how: Check submission history for score changes that coincided with switching the discretization/binning method.
     used at: T.7
E254  A previous variant of the subgroup/domain correction rule scored higher than the current variant, providing a clear revert target.
     how: Compare leaderboard scores across variants of the domain-specific correction rule.
     used at: T.7
E255  Combining a noisy auxiliary classifier output with the primary continuous score degrades predictions compared to using the continuous score alone.
     how: Compare evaluation scores with and without the auxiliary classifier component in the final prediction.
     used at: T.7
E256  The ensemble combination method is sensitive to the relative scale of input predictions (e.g., due to negative weights or linear combination).
     how: Check whether the ensemble optimizer uses a scale-sensitive combination method and whether input predictions are on comparable scales.
     used at: T.7
E257  Some model variants have outlier-heavy prediction distributions that would benefit from robust scaling (e.g., median/IQR) rather than mean/std-based scaling.
     how: Inspect the prediction distributions of the models being combined for heavy tails or outliers.
     used at: T.7
E258  The expert is searching nearby values of an additive/multiplicative correction parameter to optimize it.
     how: Check whether prior experiments tested alternative values of the correction parameter.
     used at: T.7
E259  An additive offset applied to one component creates inconsistent scales when averaged with rank-transformed components.
     how: Check whether all components being averaged are on the same scale (e.g., all proper ranks) or whether an offset has broken scale consistency.
     used at: T.7
E260  Applying the correction in final prediction space (after ensemble averaging) rather than in individual model space avoids distorting the ensemble's rank structure for unaffected samples.
     how: Check whether the correction is applied before or after ensemble aggregation and whether it affects the ranking of non-targeted samples.
     used at: T.7
E261  Simple/naive rounding has not yet been tested as a baseline to quantify the value added by optimized thresholds.
     how: Check whether a plain .round() baseline has been evaluated; if not, the comparison needed to justify optimized boundaries is missing.
     used at: T.7.2
E262  A distribution-matching (quantile/cumulative-count) discretization is available as an alternative to per-sample threshold optimization.
     how: Check whether sorting predictions and assigning discrete scores to match the known training-label cumulative distribution has been considered or tested.
     used at: T.7.2
E263  The threshold-fitting population has a different label distribution than the test set, biasing the fitted thresholds.
     how: Check whether the data used to optimize thresholds (e.g., full training set, specific subgroups, or different corpora) matches the test-set distribution.
     used at: T.7.2
E264  An intermediate normalization or rescaling step before discretization alters the distribution fed into the boundary logic and may degrade rank-based scoring.
     how: Check whether any normalization (e.g., dividing by max+1) is applied between raw predictions and the discretization step, and whether it changes rankings or metric outcomes.
     used at: T.7.2
E265  The current post-processing configuration has not been validated end-to-end with the current ensemble via a submitted or held-out score.
     how: Check whether the exact post-processing pipeline paired with the current model/ensemble has been scored on an independent evaluation (submission or held-out set).
     used at: T.7.2
E266  The specific replacement values or boundary positions in the current threshold mapping could be further refined to improve the metric.
     how: Check whether the chosen threshold values and replacement constants have been systematically varied or whether only a single setting was tried.
     used at: T.7.2
E267  The training-label distribution for a target column is heavily skewed, making certain threshold placements more plausible than others.
     how: Inspect the label frequency distribution per column to see if extreme skew justifies asymmetric or unusual threshold placement.
     used at: T.7.2
E268  A different discretization algorithm (e.g., gap-merging, KBinsDiscretizer, Nelder-Mead) may be more appropriate than the currently chosen method.
     how: Check whether alternative discretization strategies have been compared and whether the current method is the best fit for the data characteristics.
     used at: T.7.2
E269  Applying the conversion globally to all columns performed worse than applying it to a curated subset, so column selection matters.
     how: Check whether the set of columns receiving ordinal conversion has been ablated and whether a curated list outperforms a blanket application.
     used at: T.7.2