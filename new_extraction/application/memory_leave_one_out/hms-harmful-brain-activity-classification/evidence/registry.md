# evidence/registry.md — one definition per check, shared across nodes

E01  Execution fails during import, file access or device initialization.
     how: Read the first traceback and inspect available files, installed packages and tensor devices.
     used at: T.1
E02  The loaded checkpoint disagrees with the model architecture or vocabulary.
     how: Compare saved configuration, weight keys and shapes, tokenizer vocabulary and missing or unexpected load keys.
     used at: T.1
E03  The selected checkpoint files are missing, ambiguous or different from the intended run.
     how: List artifact directories and compare resolved filenames and fold identifiers with the run manifest.
     used at: T.1
E04  Rows or feature columns can be reordered or mismatched across pipeline stages.
     how: Compare identifier uniqueness, merge cardinality, row order, feature names and column order at each boundary.
     used at: T.1
E05  Inference encodings or missing-value treatment differ from those used in training.
     how: Compare persisted encoders, category maps, required input fields and NaN counts before model input.
     used at: T.1
E06  The ensemble output cannot be reproduced from its intended component arrays and weights.
     how: Recompute a few rows by hand and inspect array types, shapes, normalization, fold loops and final output references.
     used at: T.1
E07  Evaluation callbacks fail or disagree with independently computed values.
     how: Inspect callback arguments and validation-set names, compare a small known example, and numerically check custom derivatives.
     used at: T.1
E08  The output file is missing, constant, stale or produced from the wrong input data.
     how: Read the generated file and verify IDs, columns, row count, variation and equality with the final prediction array.
     used at: T.1
E09  Several stages are unverified and the first faulty transformation is unknown.
     how: Run a tiny representative batch and inspect shapes, values and exceptions after each transformation.
     used at: T.1
E10  A code or artifact refactor was intended to preserve predictions but may have changed them.
     how: Run both versions on the same fixed sample and compare intermediate and final arrays with suitable numeric tolerance.
     used at: T.1
E11  Several independently adjustable factors changed together.
     how: Inspect version diffs and identify factors that can be toggled without changing other inputs.
     used at: T.2.2
E12  A recent modification caused a substantial regression relative to a reproducible saved baseline.
     how: Compare scores and output diagnostics against the saved configuration, checkpoint and feature artifacts.
     used at: T.2.2
E13  The preferred setting has reversed when another tightly coupled setting changed.
     how: Compare earlier paired trials and identify the interacting settings and their feasible combinations.
     used at: T.2.2
E14  Target imbalance or sparse target ranges leave random folds unrepresentative.
     how: Tabulate labels or continuous-target bins in each fold and check minimum stratum sizes.
     used at: T.2.4
E15  Rows share entities or topics whose information would cross an ordinary random split.
     how: Inspect entity overlap and topic or feature-cluster membership across proposed folds.
     used at: T.2.4
E16  A known training subgroup differs from the expected test population.
     how: Compare subgroup features and target frequencies, then assert no row overlaps between fit and validation.
     used at: T.2.4
E17  A large holdout materially reduces training data and its estimates no longer change model selection.
     how: Inspect learning curves and score uncertainty at different holdout sizes while retaining independent evaluation.
     used at: T.2.4
E18  Local validation and external evaluation rank the same candidate models differently.
     how: Collect paired candidate scores, split definitions and evaluation sizes and assess consistency across folds.
     used at: T.2.4
E19  The proposed split places the same row or entity in both training and validation.
     how: Intersect training and validation row identifiers and entity identifiers in each proposed fold.
     used at: T.2.4
E20  No valid end-to-end prediction and evaluation result exists yet.
     how: Check the run ledger for a reproducible prediction file, metric implementation and baseline score.
     used at: T.2
E21  Several edits changed together or a regression has no clear cause.
     how: Compare the configurations and artifacts used by the last good and current runs.
     used at: T.2
E22  Reported gains are small relative to suspected stochastic or evaluation-set variation.
     how: Inspect repeated predictions, random seeds, evaluation size and the distribution of unchanged-run scores.
     used at: T.2
E23  The existing validation split is absent, unstable or disagrees with the target evaluation.
     how: Compare fold label distributions, repeated entities and local-versus-held-out model rankings.
     used at: T.2
E24  One numeric parameter remains uncertain and reliable local scores can distinguish its settings.
     how: Inspect prior sweep values, validation scores and noise estimates to identify an untested bracket.
     used at: T.2
E25  Repeated nearby trials have failed to improve the best verified result.
     how: Review the trial ledger for marginal gains, regression frequency and unchanged-run variation.
     used at: T.2
E26  The unit of prediction and structure of repeated raw records are not yet understood.
     how: Inspect schema, entity counts, time ordering, missingness and representative grouped records.
     used at: T.2
E27  Several observations belong to one prediction entity and only a small summary is currently used.
     how: Inspect records per entity, ordering and existing aggregate columns.
     used at: T.3.1
E28  Order and recency contain variation that full-history summaries conceal.
     how: Plot ordered entity histories and compare last values, historical means and recent windows.
     used at: T.3.1
E29  Related columns or metadata imply a signal not expressed in the present features.
     how: Inspect domain definitions, joint feature distributions and residuals by the proposed interaction.
     used at: T.3.1
E30  Text structure or error patterns vary with the target beyond the current representation.
     how: Inspect labeled texts, residuals and existing length, spelling, sentence and readability features.
     used at: T.3.1
E31  Lexical frequency or local word patterns are absent or poorly covered by current features.
     how: Inspect vectorizer vocabulary, n-gram coverage, document frequencies and decomposition dimensions.
     used at: T.3.1
E32  Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
     how: Inspect source provenance and dimensions and review embedding-source ablations on held-out data.
     used at: T.3.1
E33  Another model or related labeled source provides predictive information absent from current inputs.
     how: Inspect auxiliary labels, fold provenance, identifier joins and whether every training prediction excludes its own label.
     used at: T.3.1
E34  Distinct text roles or observed metadata are lost by the current input encoding.
     how: Inspect tokenized examples, field boundaries and metadata availability at both training and inference.
     used at: T.3.1
E35  A cleaning or tokenization rule changes information relevant to the target or checkpoint.
     how: Compare raw and transformed examples, tokenizer outputs and the saved training preprocessing.
     used at: T.3.1
E36  Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
     how: Inspect missing-value patterns, learner support, preprocessing artifacts and ablation scores.
     used at: T.3.1
E37  The inference image size differs from training or may discard task-relevant detail.
     how: Read checkpoint preprocessing metadata and inspect resized examples and previous resolution trials.
     used at: T.3.1
E38  Image input statistics differ from the checkpoint’s training preprocessing.
     how: Compare channel order and pixel statistics before and after preprocessing with the saved recipe.
     used at: T.3.1
E39  A meaningful fraction of task-relevant text is truncated.
     how: Measure token-length distribution and inspect the portions removed by current truncation.
     used at: T.3.1
E40  Many low-ranked features remain and their contribution is uncertain.
     how: Inspect fold-aggregated importance and compare validation scores for smaller and larger retained sets.
     used at: T.3.2
E41  A specific feature family is redundant, noisy or previously harmful.
     how: Review group-level ablations, missingness, cardinality and correlations with existing features.
     used at: T.3.2
E42  Available importance methods disagree about which features to retain.
     how: Compare fold-stable rankings and validation scores of equally sized selected subsets.
     used at: T.3.2
E43  A saved feature list was built for a different feature schema.
     how: Compare selected column names and artifact metadata with the current engineered columns.
     used at: T.3.2
E44  A known subset has unreliable labels or differs from the intended test population.
     how: Inspect out-of-fold residuals, label audits and subgroup feature/label distributions.
     used at: T.3.3
E45  Rare classes or target-like subgroups have insufficient influence on fitting.
     how: Tabulate class and subgroup frequencies and inspect metric contributions and current sampling weights.
     used at: T.3.3
E46  A sparse subgroup has too few examples and plausible interpolation neighbors exist.
     how: Inspect subgroup sample sizes and neighbor distances, and verify augmentation excludes validation rows.
     used at: T.3.3
E47  Training images exhibit nuisance variation that valid augmentation could reproduce.
     how: Inspect augmented examples, domain label invariances and train-versus-validation learning curves.
     used at: T.3.3
E48  Raw data contains structure not represented by current features.
     how: Compare source records with the feature schema and model input examples.
     used at: T.3
E49  The feature set is large, changed recently or contains suspected unhelpful groups.
     how: Inspect feature counts, importance stability, ablation scores and saved selection provenance.
     used at: T.3
E50  Label quality, imbalance or limited coverage constrains the current learner.
     how: Inspect residuals, label frequencies and subgroup distributions.
     used at: T.3
E51  Available backbones differ in capacity or domain pretraining relevant to the task.
     how: Inspect pretrained model provenance, capacity, memory needs and controlled standalone scores.
     used at: T.4.1
E52  The tuned current tree method has plateaued and another boosting implementation is available.
     how: Review baseline curves and each candidate’s objective, missing-value and early-stopping support.
     used at: T.4.1
E53  A minimal or poorly matched prediction head limits an otherwise useful representation.
     how: Inspect the head, pooling and target structure together with head ablations and checkpoint compatibility.
     used at: T.4.1
E54  The present output activation or label formulation mismatches the target structure.
     how: Inspect target support, independence, ordering, metric penalties and the current loss/activation pair.
     used at: T.4.1
E55  A generative model could score the text but its output reliability is unverified.
     how: Inspect generated scores on labeled held-out examples for format validity, range and target agreement.
     used at: T.4.1
E56  Outcomes contain censoring or the metric evaluates risk ranking within known subgroups.
     how: Inspect event indicators, observed durations, censoring rates and per-group metric definitions.
     used at: T.4.2
E57  Target centering differs across folds or from the inference output scale.
     how: Inspect fold target means, transform fitting scope and inverse-transform code.
     used at: T.4.2
E58  The current loss optimizes a surrogate that poorly tracks the held-out metric.
     how: Compare loss and metric trajectories and inspect candidate gradients, Hessians and target semantics.
     used at: T.4.2
E59  The best epoch or iteration under the current stopping metric is not best under the target metric.
     how: Recompute both metrics over saved validation predictions along the training trajectory.
     used at: T.4.2
E60  The current API obscures required probability output or evaluation controls.
     how: Inspect method signatures, prediction semantics and callback support on a minimal fit.
     used at: T.4.2
E61  Training fit or the train-validation gap suggests an inappropriate tree capacity.
     how: Compare curves and past depth/leaf sweeps with feature count and sample size.
     used at: T.4.3
E62  The fitted model overfits or current regularization suppresses useful signal.
     how: Inspect learning curves and controlled penalty, subsampling or dropout sweeps.
     used at: T.4.3
E63  Training is unstable or stops before a lower-rate run can converge.
     how: Inspect per-iteration curves, learning rates, stopping points and maximum iteration caps.
     used at: T.4.3
E64  Validation improvement continues at the cap or has already reversed before the selected checkpoint.
     how: Plot validation performance against epochs or rounds and inspect best-iteration and patience logs.
     used at: T.4.3
E65  Convergence behavior suggests the current optimization schedule is a bottleneck.
     how: Inspect learning-rate history, loss oscillation and comparable optimizer runs.
     used at: T.4.3
E66  An ensemble member lacks reproducible fold-trained models or unbiased validation predictions.
     how: Inspect training splits, per-fold checkpoint saves and OOF coverage with no self-prediction.
     used at: T.4.3
E67  Compatible snapshots occupy nearby useful solutions and individual predictions vary.
     how: Check identical parameter schemas and snapshot validation behavior along the training trajectory.
     used at: T.4.3
E68  The existing formulation has plateaued and a materially different candidate is available.
     how: Review same-input comparisons and candidate architecture or training metadata.
     used at: T.4
E69  The current training signal differs from what evaluation rewards.
     how: Read target construction, loss and evaluation implementations and compare their validation behavior.
     used at: T.4
E70  Learning curves show that current fitting settings are inadequate.
     how: Inspect loss, validation metric, selected iterations and training resource logs.
     used at: T.4
E71  The ensemble’s errors are shared across similar members and a distinct candidate is available.
     how: Compare aligned OOF residual correlations and held-out gains from small-weight candidate inclusion.
     used at: T.5.1
E72  Existing models share an architecture but alternative training or feature recipes yield different errors.
     how: Inspect recipe provenance and residual correlation of predictions from the alternative variants.
     used at: T.5.1
E73  Some available members may add noise or redundancy despite acceptable standalone scores.
     how: Compute single-member and leave-one-member-out metrics on aligned held-out predictions.
     used at: T.5.1
E74  Removing or disabling previously validated members caused a regression.
     how: Compare the current member manifest and outputs with the last verified ensemble.
     used at: T.5.1
E75  Several compatible trained checkpoints differ in seed, recipe or training stage.
     how: Inspect artifact metadata and evaluate each through identical preprocessing and aggregation.
     used at: T.5.1
E76  Fold quality or training-regime mismatch may make some available checkpoints harmful.
     how: Inspect per-fold scores, training provenance and independent inclusion/exclusion results.
     used at: T.5.1
E77  A candidate improves standalone score but adds no gain in prior fixed-weight inclusion tests.
     how: Compare candidate standalone and incremental ensemble scores on the same disjoint evaluation rows.
     used at: T.5.1
E78  Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
     how: Inspect checkpoint coverage, per-fold prediction differences and incremental averaging scores.
     used at: T.5.2
E79  Predictions vary across trained seeds beyond the expected evaluation noise.
     how: Compare aligned predictions and scores from seed-specific checkpoints and incremental averages.
     used at: T.5.2
E80  The task is invariant to candidate transformations and predictions vary across those views.
     how: Inspect transformed examples, domain invariances and paired held-out predictions with and without TTA.
     used at: T.5.2
E81  Dropout is active or intentionally proposed at inference and creates nontrivial prediction variance.
     how: Check model train/eval flags and compare repeated forward passes on identical inputs.
     used at: T.5.2
E82  Several stopping-rule or training-stage snapshots have complementary errors.
     how: Inspect checkpoint provenance and held-out predictions from best and final training snapshots.
     used at: T.5.2
E83  Members have similar quality or optimized combinations have unstable held-out gains.
     how: Compare member scores and equal versus tuned combination performance across held-out folds.
     used at: T.5.3
E84  Members differ in useful contribution and held-out predictions support weight comparisons.
     how: Evaluate a coarse weight grid, residual correlation and stability of the best region across folds.
     used at: T.5.3
E85  A candidate is anti-correlated with residual error after accounting for stronger members.
     how: Fit or evaluate bounded signed weights on OOF predictions and confirm improvement on separate folds.
     used at: T.5.3
E86  Member scales differ or raw versus rank aggregation has changed preference across configurations.
     how: Plot member score distributions and compare both aggregation methods on identical held-out predictions.
     used at: T.5.3
E87  Member scales or outliers distort their intended relative contributions.
     how: Inspect per-member quantiles and outliers; fit candidate scalers on OOF data and apply them unchanged.
     used at: T.5.3
E88  Families have unequal numbers of checkpoints that would otherwise determine their influence.
     how: Count members per family and inspect the effective weights under flat versus grouped averaging.
     used at: T.5.3
E89  Enough OOF examples exist to learn stable complementary relationships among base outputs.
     how: Audit OOF provenance, meta-feature count, held-out stacker gains and regularization sensitivity.
     used at: T.5.3
E90  The available meta-features contain in-sample predictions or have unverifiable fold provenance.
     how: Trace every training meta-feature to a base-model fold and assert that its row was excluded during fitting.
     used at: T.5.3
E91  The current set may omit complementary signal or include harmful members.
     how: Review candidate residual correlations and fixed-blend inclusion ablations.
     used at: T.5
E92  A single predictor is unstable and repeatable alternatives are available.
     how: Inspect variability across folds, seeds and valid input transformations.
     used at: T.5
E93  Valid model outputs differ in quality, scale or complementary error.
     how: Inspect member prediction distributions, residual correlations and available OOF sample size.
     used at: T.5
E94  The metric depends on order and proposed transformations only erase or perturb useful ordering.
     how: Inspect metric semantics and compare raw outputs with transformed ranks and held-out scores.
     used at: T.6.1
E95  Labels occupy known ordered levels and learned thresholds are not reliably better.
     how: Inspect allowed labels and compare fixed versus fitted thresholds on independent held-out predictions.
     used at: T.6.1
E96  Continuous outputs carry signal but fixed cutpoints systematically misallocate ordinal labels.
     how: Inspect OOF score distributions by label and independent gains from ordered threshold optimization.
     used at: T.6.1
E97  Target-level frequencies are stable enough that a reference distribution may improve mapping.
     how: Compare training and representative validation label frequencies and hold out samples for evaluating the map.
     used at: T.6.1
E98  Residual distributions differ reproducibly across groups available at inference.
     how: Plot groupwise residuals, counts and independently scored global versus group-specific mappings.
     used at: T.6.1
E99  Previously optimized cutpoints fail to improve a separate held-out set.
     how: Apply saved cutpoints unchanged to an independent labeled split and compare with fixed rounding.
     used at: T.6.1
E100  The target has a restricted range or a small ordered set of values.
     how: Inspect label frequencies and the metric’s response to ties and discretization.
     used at: T.6
E101  Predictions have an inverted convention or a reproducible additive bias.
     how: Inspect target/output conventions and plot held-out residual means, including a fixed reference when available.
     used at: T.6
E102  Prediction ranges mismatch the required support or the calibration distribution.
     how: Compare output quantiles with allowed values and training/OOF prediction distributions.
     used at: T.6
E103  Component confidence distributions are mismatched and their nonlinear combination changes ordering.
     how: Plot calibration and quantiles of component probabilities and compare transformed blends on held-out rows.
     used at: T.6
E104  An auxiliary classifier or observable rule predicts a specific systematic residual.
     how: Measure the rule’s held-out precision and residual effect, checking output columns and correction masks.
     used at: T.6
E105  Post-processing was tuned before an upstream change or its contribution is unknown.
     how: Compare transformed and raw versions of identical stored predictions on the same held-out rows.
     used at: T.6
E106  Full runs are too expensive to locate errors or screen candidate settings.
     how: Measure stage runtimes and inspect debug flags, fold coverage and restored production settings.
     used at: T.7
E107  The full dataset or feature matrix exceeds available memory.
     how: Measure peak table size and group sizes, then verify complete-entity chunking and output coverage.
     used at: T.7
E108  Peak memory rises across successive model or feature stages.
     how: Profile live objects and device memory, and trace downstream references before releasing objects.
     used at: T.7
E109  Inference fails at large batches or padding dominates sequence computation.
     how: Inspect batch peak memory and sequence lengths and compare identifier-aligned outputs after rebatching.
     used at: T.7
E110  Model inference dominates memory and supported lower precision may reduce its footprint.
     how: Compare full and reduced-precision predictions and held-out metrics on a representative batch.
     used at: T.7
E111  Most run time recomputes artifacts unchanged by the current experiment.
     how: Profile stages and compare feature/model configuration hashes with saved artifact metadata.
     used at: T.7
E112  Multiple variants share fragile duplicated code or overwrite each other’s artifacts.
     how: Trace configuration dispatch, per-model preprocessing, filenames and stage dependencies.
     used at: T.7
E113  The required fold training cannot finish within one session but completed checkpoints can be persisted.
     how: Compare per-fold runtime with session limits and inspect a manifest of successfully saved folds.
     used at: T.7
E114  Repeated metric computation dominates search time rather than model fitting.
     how: Profile evaluation calls and compare the optimized and reference metric on fixed arrays including edge cases.
     used at: T.7
E115  The current run fails or its predictions violate an expected invariant.
     how: Inspect errors, output shapes, row identifiers, prediction ranges and a known-good run.
     used at: T
E116  A score change cannot yet be attributed to a reproducible intervention.
     how: Inspect experiment diffs, repeated-run scores and validation-versus-held-out rankings.
     used at: T
E117  The current inputs discard useful structure or contain demonstrated noise.
     how: Inspect raw examples, feature provenance, ablation results and train/test distributions.
     used at: T
E118  Valid inputs and evaluation still expose underfitting, overfitting or objective mismatch.
     how: Inspect learning curves, residuals, model capacity and target/metric definitions.
     used at: T
E119  Several valid predictors are available or a predictor has measurable variance.
     how: Inspect aligned held-out predictions, individual scores and residual correlations.
     used at: T
E120  Valid raw predictions violate target structure or show a correctable held-out bias.
     how: Compare raw outputs with target distributions, subgroup residuals and submission requirements.
     used at: T
E121  Runtime, memory or repeated computation prevents completing informative experiments.
     how: Inspect stage timings, peak memory, run logs and existing cached artifacts.
     used at: T
E122  There remain untested checkpoints from available training runs that could further calibrate the CV-to-LB relationship.
     how: Check whether additional checkpoints (from the same or different training runs) exist that have not yet been submitted to LB, and whose submission could help map the CV-to-LB relationship.
     used at: T.2.4
E123  Inference-time data transforms differ from training-time transforms, causing a systematic mismatch between CV and LB performance.
     how: Compare the preprocessing/augmentation pipeline applied during training with the one applied at inference time; check for discrepancies that would make CV non-representative of LB.
     used at: T.2.4
E124  Alternative holdout sizes have not been tested and could yield a better bias-variance trade-off for validation.
     how: List the holdout fractions already tried and check whether plausible alternatives remain untested.
     used at: T.2.4
E125  A previous validation-scheme change was confounded by simultaneous hyperparameter changes, so the effect of the scheme change alone is unknown.
     how: Check whether the last time the validation split was changed, other parameters also changed in the same experiment, preventing isolation of the split effect.
     used at: T.2.4
E126  The clustering or grouping algorithm used to construct validation folds receives the intended feature inputs (not metadata or wrong columns).
     how: Inspect the code to verify that the fit and predict calls for the grouping method (e.g., KMeans) receive the correct numeric feature matrix.
     used at: T.2.4
E127  The features used to derive synthetic groups (e.g., KMeans clusters) may not capture the semantic similarity that drives the real distribution shift.
     how: Compare the features fed into the clustering algorithm with representations (e.g., TF-IDF, embeddings) that better reflect the domain-relevant similarity structure.
     used at: T.2.4
E128  The number of distinct groups (topics/entities) is known and informs the feasible number of CV splits for grouped cross-validation.
     how: Count the distinct group labels and verify that n_splits does not exceed the number of groups and is chosen to give meaningful fold sizes.
     used at: T.2.4
E129  External or previously loaded topic/group metadata is available and could serve as a natural grouping variable for grouped CV.
     how: Check whether topic or entity metadata has been loaded or is accessible, and whether it has been considered as the grouping variable for the validation split.
     used at: T.2.4
E130  The fold-construction code operates on the full dataset rather than an unintended subset.
     how: Verify that the split/indexing logic applies to all rows of the training data, not a filtered or partial dataframe from a prior step.
     used at: T.2.4
E131  No local validation mechanism currently exists, so changes can only be evaluated via leaderboard submission.
     how: Check whether a local holdout or CV loop is implemented; if not, every change requires a submission to get feedback.
     used at: T.2.4
E132  The holdout set is being (re-)enabled specifically for tuning a new model architecture rather than for final evaluation.
     how: Determine whether the purpose of the current holdout is hyperparameter/architecture search (where repeated use is expected) versus final unbiased evaluation.
     used at: T.2.4
E133  A previous train/validation split ratio change did not improve the score, suggesting the current ratio should be reverted or kept.
     how: Check version history for whether a recent split-ratio edit improved or degraded the metric.
     used at: T.3.3
E134  Previous attempts to add stronger augmentation degraded performance compared to the mild-augmentation baseline.
     how: Compare leaderboard/validation scores of versions with stronger augmentation vs. the mild-augmentation baseline.
     used at: T.3.3
E135  The upward sweep of class/positive-class weights has been completed and showed degradation at high values, motivating exploration in a different direction.
     how: Review the sequence of class-weight experiments and their scores to determine whether the upward sweep is exhausted.
     used at: T.3.3
E136  The expert is currently sweeping class weights below 1.0 and has not yet found the optimum in that region.
     how: Check the version history for below-1.0 weight experiments and whether a clear optimum has emerged.
     used at: T.3.3
E137  The competition metric is ranking-based or ordinal, so class reweighting may be invariant or harmful because it affects calibration rather than score ordering.
     how: Examine the competition metric definition and determine whether it depends on score ordering vs. calibrated probabilities.
     used at: T.3.3
E138  Previous attempts to adjust loss-function constants alone did not yield consistent improvements.
     how: Review version history for loss-constant tuning experiments and their score trajectories.
     used at: T.3.3
E139  The best leaderboard score was achieved without augmentation, and all augmented versions scored lower.
     how: Compare the top leaderboard score from non-augmented versions against all augmented versions.
     used at: T.3.3
E140  The scale_pos_weight parameter is applicable and correctly interpreted under the current objective (e.g., regression, not just binary classification).
     how: Check the model objective type and verify that scale_pos_weight has the intended effect for that objective.
     used at: T.3.3
E141  The prediction method (e.g., predict vs predict_proba) is mismatched with the model API or evaluation requirements.
     how: Check whether the code calls the correct prediction method for the model object type and whether the output format (probabilities vs class labels) matches what the evaluation metric expects.
     used at: T.4
E142  A previously underperforming candidate may have failed due to ancillary settings (ensemble weights, checkpoint selection, pipeline bugs) rather than inherent model weakness.
     how: Review whether the larger or alternative model's poor results can be attributed to surrounding configuration issues rather than the model itself, warranting a re-evaluation with corrected settings.
     used at: T.4
E143  The custom objective's parameters vary across folds or subgroups, causing inconsistent loss landscapes that destabilize training.
     how: Check whether loss function parameters (e.g., target shifts, mean/variance) are computed per-fold and whether this variation introduces instability compared to a fixed global parameterization.
     used at: T.4
E144  A structural pipeline change (e.g., stratification, new features) has shifted the optimal value of a fitting hyperparameter that was previously tuned.
     how: Check whether a recent structural change to the pipeline invalidates previously tuned hyperparameters, requiring re-optimization of fitting settings.
     used at: T.4
E145  A known best value for the target-transform parameter exists from prior experiments and can serve as the baseline for further sweeps.
     how: Review submission history to identify the parameter value that produced the best held-out or LB score.
     used at: T.4.2
E146  The training sample distribution does not match the test distribution, and resampling or reweighting could better align the target.
     how: Compare the class/subgroup proportions in training data versus the expected test distribution.
     used at: T.4.2
E147  Ensemble weighting or blending interacts with the target centering change, so isolation is needed to attribute the effect.
     how: Check whether the ensemble aggregation method confounds measurement of a target-transform change.
     used at: T.4.2
E148  Subgroup-specific baseline distributions differ materially, so a global target transform distorts within-group rankings.
     how: Compare the baseline outcome distributions across known subgroups (e.g., demographic strata) to assess whether a single global transform is appropriate.
     used at: T.4.2
E149  The target-transform parameter (e.g., COLLAPSE) directly controls the censoring-aware transform and small changes produce measurable metric differences.
     how: Verify that the parameter under consideration feeds directly into the target transform and review prior experiments for sensitivity evidence.
     used at: T.4.2
E150  The existing ensemble already includes a model using the proposed target transform, so adding another would be redundant rather than diversifying.
     how: Inventory the target transforms already used across ensemble members to check for duplication.
     used at: T.4.2
E151  The current boosting mode (e.g., DART) makes early-stopping callbacks unreliable, requiring manual iteration tuning.
     how: Check whether the boosting mode (e.g., DART) invalidates the early-stopping mechanism, forcing manual round/iteration selection.
     used at: T.4.3
E152  GPU acceleration is available and would meaningfully speed up training iterations.
     how: Check whether a GPU device is available and whether switching to GPU-based training would provide a significant speedup for the current model.
     used at: T.4.3
E153  GPU training caused instability or errors requiring fallback to CPU.
     how: Check whether GPU-based training produced errors or numerical instability that necessitate reverting to CPU training.
     used at: T.4.3
E154  Missing-value handling was toggled off or commented out and re-enabling it may improve training stability.
     how: Check whether missing-value imputation code is currently disabled and whether re-enabling it changes training behavior.
     used at: T.4.3
E155  The training loop currently lacks early-stopping and iteration-logging callbacks.
     how: Check whether the training loop has early-stopping and logging callbacks configured; if absent, convergence cannot be monitored.
     used at: T.4.3
E156  Multiple hyperparameters are being changed simultaneously without isolating individual effects.
     how: Check whether more than one hyperparameter was changed between consecutive runs, preventing attribution of score changes to a single factor.
     used at: T.4.3
E157  The models share a single generic parameter dictionary rather than having model-specific tuned configurations.
     how: Check whether all models in the pipeline use the same hyperparameter dictionary, preventing per-model tuning.
     used at: T.4.3
E158  Reducing per-model training cost frees compute budget for downstream search (e.g., blend-weight optimization).
     how: Check whether lowering per-model iteration count would free enough compute to meaningfully expand a downstream hyperparameter or blending search.
     used at: T.4.3
E159  A previous combination attempt failed due to a configuration mismatch or bug, so the result may not reflect the true potential of that combination.
     how: Review logs/code of the prior attempt to identify whether a mismatch (e.g., wrong flags, incompatible checkpoints) invalidated the earlier result.
     used at: T.5
E160  No reliable local validation metric is available, so blend/weight selection must rely on leaderboard feedback.
     how: Check whether a trustworthy OOF or holdout evaluation pipeline exists for comparing blend variants locally.
     used at: T.5
E161  The blending/ensemble code has a bug (e.g., variable name error, wrong file reference, denominator mismatch) that causes the output to not reflect the intended combination.
     how: Audit the combination code for variable name reuse, weight/member count mismatches, and incorrect file references.
     used at: T.5
E162  Weight-only tuning of the current blend has plateaued, suggesting a structural change (add/remove member or change method) is needed.
     how: Check recent iteration history to see if weight adjustments have stopped yielding score improvements.
     used at: T.5
E163  A previously tried combination method (e.g., adaptive blending, stacking) did not improve over the simpler baseline approach.
     how: Compare scores of the alternative combination method against the simpler fixed-weight or averaging baseline.
     used at: T.5
E164  The existing blend weights were calibrated for a different set of members and are now stale.
     how: Check whether the current weight values were optimized for the current member set or an earlier one.
     used at: T.5
E165  Hierarchical or grouped blending (e.g., averaging within model families first) could better balance contributions from unequally-sized groups.
     how: Check whether the current flat combination over-represents a model family that contributes many members.
     used at: T.5
E166  The current combination method (e.g., rank-averaging) cannot down-weight a weaker member, requiring removal instead of reweighting.
     how: Check whether the combination method supports per-member weighting or only equal contribution.
     used at: T.5
E167  The evaluation metric is rank-based, so rank-preserving transforms (e.g., min-max scaling) cannot change the score for a single model.
     how: Check whether the target metric depends only on ranks, making monotonic transforms of individual predictions irrelevant.
     used at: T.6
E168  Published top solutions or domain knowledge indicate specific post-processing techniques (e.g., discretization, host-based masking) that are known to be effective.
     how: Review public kernels, top-solution write-ups, or domain conventions for established post-processing patterns applicable to this task.
     used at: T.6
E169  The current post-processing code contains a bug (typo, wrong operator, or missing branch) that prevents it from executing correctly.
     how: Inspect the post-processing code for syntax errors, typos, or logic mistakes that would produce incorrect or no output.
     used at: T.6