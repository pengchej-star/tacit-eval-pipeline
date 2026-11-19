# evidence/registry.md — one definition per check, shared across nodes

E01  The current pipeline fails, produces implausible predictions, or regressed sharply after an integration change.
     how: Inspect runtime logs, prediction summaries, and the first changed stage relative to the working baseline.
     used at: T
E02  There is no trustworthy baseline or the observed gain cannot be distinguished from confounding or variability.
     how: Review scored baselines, fold provenance, version diffs, and no-change reruns.
     used at: T
E03  Training coverage, label quality, source mix, or outcome encoding is a documented limitation.
     how: Audit sample populations, annotation quality, unused data, and target-construction code.
     used at: T
E04  Input inspection reveals lost content, unsuitable transforms, or missing predictive features.
     how: Compare raw observations with exact model inputs and existing feature ablations.
     used at: T
E05  Single-model validation or training logs expose a capacity, architecture, checkpoint, or optimization limitation.
     how: Inspect learning curves, checkpoint comparisons, and model-specific residuals.
     used at: T
E06  Several valid prediction sources exist and their held-out errors are not identical.
     how: Align out-of-fold arrays and compare residual correlations and existing blend ablations.
     used at: T
E07  Valid base predictions remain but the metric exposes an inference or calibration opportunity.
     how: Inspect target granularity, probability reliability, valid input symmetries, and post-processing history.
     used at: T
E08  Resource limits or repeated computation prevent complete, reproducible experiments.
     how: Inspect memory, timing, stage-completion, and reproducibility logs.
     used at: T
E09  A checkpoint or feature-pipeline change preceded the first large regression.
     how: Compare the last working and failing configuration manifests and their intermediate sample outputs.
     used at: T.1
E10  All components run, but combining their outputs causes the regression.
     how: Compare standalone predictions with the final blend and inspect accumulation and output ranges.
     used at: T.1
E11  The run errors or fails to create a valid complete output file.
     how: Inspect execution logs and the final artifact against the task’s required schema.
     used at: T.1
E12  A valid file contains nearly random scores despite strong stored validation results.
     how: Compare a small labeled replay with archived predictions and inspect weight-loading and preprocessing reports.
     used at: T.1
E13  Strict loading reports missing keys or incompatible tensor dimensions.
     how: Load the checkpoint strictly and compare its keys, tokenizer length, and configured hidden dimensions with the reconstructed model.
     used at: T.1.1
E14  The same raw example produces different training and inference features.
     how: Run both preprocessors on saved examples and compare token IDs, normalization, shapes, and feature values.
     used at: T.1.1
E15  Sample keys or ordered feature names disagree across arrays being combined.
     how: Compare unique row IDs and ordered column manifests before the merge or prediction call.
     used at: T.1.1
E16  A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
     how: Trace the first few examples and configuration flags through each stage and compare against its documented input contract.
     used at: T.1.1
E17  A hand-calculated blend disagrees with the implemented blend.
     how: Compute the weighted result for a few rows using explicit numeric arrays and compare divisors, terms, and weight totals.
     used at: T.1.2
E18  Output axes, activation, or loss derivatives disagree with the target definition.
     how: Inspect a forward pass and compare its shape, activation, gradient, and Hessian against a simple reference calculation.
     used at: T.1.2
E19  The number of accumulated predictions is smaller than the enabled member count.
     how: Log each executed model and fold, count appended arrays, and trace the array written to disk.
     used at: T.1.2
E20  Predictions are constant or unchanged after changes that should affect them.
     how: Measure per-column variance and inspect raw outputs and loaded sample IDs before and after each stage.
     used at: T.1.2
E21  One member orders risk or target values in the opposite direction.
     how: Compare metric definitions and held-out target correlations for that member and the existing blend.
     used at: T.1.2
E22  The first failure is an import error or unresolved artifact path.
     how: Read the earliest traceback, list mounted artifacts, and inspect the requested package symbol and version.
     used at: T.1.3
E23  The first failure names unsupported hardware or mismatched tensor devices.
     how: Inspect device availability and the model and input device attributes at the failing operation.
     used at: T.1.3
E24  Inference finishes but the required prediction file is absent, incomplete, or from debug mode.
     how: Inspect the final output file, row count, columns, write path, and production flags.
     used at: T.1.3
E25  The first failure is an API, variable, or configuration error on a small batch.
     how: Reproduce the traceback on a minimal batch and inspect the first failing call’s arguments and types.
     used at: T.1.3
E26  Some ensemble outputs are missing and a verified prediction cache exists for exactly those samples.
     how: Check failure logs, cached model versions, sample-key coverage, and cached array statistics.
     used at: T.1.3
E27  An error handler substitutes zeros or placeholders for failed predictions.
     how: Read exception handlers and compare the substituted arrays with expected component distributions.
     used at: T.1.3
E28  No complete pipeline has produced a scored prediction file.
     how: Check experiment records for a successful full run and saved baseline predictions.
     used at: T.2
E29  Leakage, in-sample meta-features, or local-to-external disagreement is documented.
     how: Inspect feature provenance, fold exclusions, and paired validation and submission results.
     used at: T.2
E30  The split fails to preserve the task’s grouping boundary or relevant population distribution.
     how: Compare fold IDs and population histograms with how future examples are expected to arrive.
     used at: T.2
E31  A score movement cannot be attributed to a specific change or exceeds no-change variability only slightly.
     how: Compare version diffs and repeated-run score ranges.
     used at: T.2
E32  A training feature uses held-out labels or predictions made on its own training rows.
     how: Trace target-derived features and compare row IDs with the fitting data for every contributing model.
     used at: T.2.2
E33  Stacking members use incompatible folds or cannot establish exclusion of each predicted training row.
     how: Compare saved split manifests and fold IDs for every out-of-fold prediction column.
     used at: T.2.2
E34  Local model rankings disagree with earlier external results or the public evaluation set is tiny.
     how: Tabulate paired local and external scores with evaluation-set sizes and inspect differences relative to local variability.
     used at: T.2.2
E35  Repeated entities or target columns enter supposedly unsupervised feature construction.
     how: Inspect selected columns and feature-fitting row provenance before evaluating the pipeline.
     used at: T.2.2
E36  Examples are independent but random folds have markedly different target frequencies.
     how: Compare per-fold target histograms and inspect identifiers for repeated entities or overlapping observations.
     used at: T.2.3
E37  Related examples share an entity or source that must be unseen at evaluation.
     how: Inspect entity/source IDs and the task’s test-set construction for cross-row dependence.
     used at: T.2.3
E38  Feature clusters reveal related examples but no usable group metadata exists.
     how: Inspect target-free embedding or topic clusters and audit available metadata for a real grouping key.
     used at: T.2.3
E39  The current fold count leaves very small or unstable validation sets.
     how: Count validation rows and events per fold and inspect the spread of fold metrics and threshold fits.
     used at: T.2.3
E40  A known subgroup resembles the test population and is poorly represented in the current folds.
     how: Compare subgroup counts and feature or label distributions across training, held-out folds, and available test metadata.
     used at: T.2.3
E41  The proposed subgroup fold augmentation places the same IDs in training and validation.
     how: Intersect train and validation IDs for every fold; score the proposal only on an additional disjoint holdout.
     used at: T.2.3
E42  Several functional changes were made between the last two scored versions.
     how: Read the version diff and identify independently toggleable modifications with a saved baseline.
     used at: T.2.4
E43  The current configuration has a repeatable large regression against a reproducible saved baseline.
     how: Replay the two configurations with pinned artifacts and compare the gap with historical repeatability.
     used at: T.2.4
E44  Identical code has produced materially different predictions or scores.
     how: Compare no-change run logs, checkpoint hashes, prediction checksums, and recorded scores.
     used at: T.2.4
E45  A rewrite was intended to preserve model behavior exactly.
     how: Inspect the diff for only infrastructure changes and locate archived predictions for identical inputs.
     used at: T.2.4
E46  There is no competitive operating point and the proposed changes must be compatible as a package.
     how: Inspect baseline performance and dependencies such as jointly changed input dimensions and required model heads.
     used at: T.2.4
E47  Several valid probes of the current lever have failed to exceed the observed variability.
     how: Plot recent tested values and scores against the saved best and repeat-run range.
     used at: T.2.4
E48  Existing training rows contain suspected label errors, duplicates, imbalance, or identifiable source shift.
     how: Audit row keys, label confidence, subgroup counts, and source-wise distributions.
     used at: T.3
E49  Compatible auxiliary labeled or unlabeled examples are available but unused.
     how: Inspect available datasets and compare their input and label schemas with the current training set.
     used at: T.3
E50  The present target ignores censoring, metric-relevant groups, or a reversible offset.
     how: Compare the target-construction code with outcome semantics and training-fold target statistics.
     used at: T.3
E51  Large out-of-fold residuals coincide with independently suspected label errors.
     how: Inspect residual-ranked examples alongside raw labels and annotation-quality evidence.
     used at: T.3.1
E52  An identifiable source or low-confidence subset differs from the expected test population.
     how: Compare source-wise features, labels, annotation confidence, and available test metadata.
     used at: T.3.1
E53  Training includes duplicated observations or overlapping windows from the same event.
     how: Count repeated sample keys and overlap in event/time intervals.
     used at: T.3.1
E54  A relevant subgroup is scarce and repeated or interpolated training examples remain semantically valid.
     how: Inspect subgroup counts, within-class neighbors, and the task’s expected label distribution.
     used at: T.3.1
E55  Dropping the mismatched subgroup would remove a substantial amount of otherwise useful labeled data.
     how: Count the rows removed by the proposed filter and compare subgroup coverage before and after filtering.
     used at: T.3.1
E56  The configuration is selected and a development-only holdout still excludes training rows.
     how: Inspect the final-fit flag and split code against the frozen model-selection record.
     used at: T.3.1
E57  Additional labeled examples have compatible targets and observable quality indicators.
     how: Inspect the auxiliary schema, label definitions, annotation confidence, and representative examples.
     used at: T.3.2
E58  Unlabeled examples exist and the teacher has credible independent validation performance.
     how: Inspect unlabeled input compatibility, teacher holdout metrics, and confidence distributions.
     used at: T.3.2
E59  The extra labeled source has a documented distribution shift.
     how: Compare source-wise feature and target distributions with the original holdout.
     used at: T.3.2
E60  Outcomes include both event times and censoring indicators.
     how: Inspect target columns and confirm that censored times cannot be treated as observed event times.
     used at: T.3.3
E61  The metric evaluates named groups separately and group survival distributions differ.
     how: Read the metric formula and plot training-fold survival estimates and sample counts by group.
     used at: T.3.3
E62  Continuous regression targets have fold-dependent offsets and are not censored outcomes.
     how: Compare training-fold target means and model residual means and inspect the target schema.
     used at: T.3.3
E63  Some groups have too few events to estimate their own survival curves reliably.
     how: Count uncensored events per group and inspect uncertainty or step instability in the estimated curves.
     used at: T.3.3
E64  Missing values, category mappings, or numeric scales are inconsistent with the selected learner.
     how: Inspect the model-input matrix and fitted preprocessing objects.
     used at: T.4
E65  Text truncation, cleaning, or omitted context is visible in tokenized examples.
     how: Compare raw text and encoded sequences, including masks and discarded spans.
     used at: T.4
E66  Useful feature sources are absent or an expanded feature set has become noisy.
     how: Inspect feature manifests, feature-group ablations, and representative residual errors.
     used at: T.4
E67  Raw signals can support an untested domain-valid filter or representation.
     how: Inspect traces, power spectra, spectral images, and the current transform configuration.
     used at: T.4
E68  The current resize, crop, or time window discards relevant information.
     how: Visualize the exact model input against the original observation and label scope.
     used at: T.4
E69  A selected learner receives NaN or infinite values it cannot handle natively.
     how: Measure finite-value coverage at the learner input and inspect the learner’s configured missing-value handling.
     used at: T.4.1
E70  Test categories are unseen or encoded differently from training categories.
     how: Compare category vocabularies and inspect fitted encoder artifacts and transform calls.
     used at: T.4.1
E71  Input scales differ markedly across features or from the pretrained backbone’s expected distribution.
     how: Plot feature ranges and compare current normalization with the training configuration.
     used at: T.4.1
E72  All downstream learners are trees and standardization adds no demonstrated signal.
     how: Inspect the model list and existing scaled versus unscaled validation results.
     used at: T.4.1
E73  Cleaning removes punctuation, spelling, or structure that may carry target information.
     how: Inspect paired raw and cleaned texts and the task’s label definition.
     used at: T.4.2
E74  Manual padding, special tokens, or masks differ from the training tokenizer.
     how: Compare token IDs, vocabulary, attention masks, and padding on a few saved examples.
     used at: T.4.2
E75  A meaningful fraction of inputs loses potentially relevant content to truncation.
     how: Measure token-length quantiles and inspect the discarded spans of long labeled examples.
     used at: T.4.2
E76  Distinct text fields or task metadata are available but omitted from the encoded context.
     how: Inspect input schema, representative examples, and whether matching training checkpoints can be produced.
     used at: T.4.2
E77  The model is fixed and no checkpoint was trained for the proposed new prompt or vocabulary.
     how: Compare the planned input format with training metadata and available checkpoints.
     used at: T.4.2
E78  Word order fragments or corpus-frequency filters are missing from the current text representation.
     how: Inspect vectorizer n-gram ranges, vocabulary statistics, and document-frequency settings.
     used at: T.4.3
E79  The current representation lacks semantic information available from a compatible pretrained encoder.
     how: Inspect feature sources and labeled examples with similar meaning but different surface wording.
     used at: T.4.3
E80  A domain interaction or structural statistic is plausible and not explicitly represented.
     how: Inspect raw fields, error examples, and the existing feature list for the proposed interaction.
     used at: T.4.3
E81  Structured metadata is present at both training and inference and varies with residual errors.
     how: Verify metadata availability and compare held-out residuals across its categories.
     used at: T.4.3
E82  Recent feature additions increased dimension without a reliable validation gain.
     how: Compare feature manifests and held-out scores before and after each added group.
     used at: T.4.3
E83  The saved feature-selection list predates the current feature matrix.
     how: Compare the selection artifact’s column names and provenance with the current feature schema.
     used at: T.4.3
E84  The current time-frequency representation obscures short events or narrow frequency structure.
     how: Inspect raw traces and spectrograms alongside FFT, window, hop, and sampling settings.
     used at: T.4.4
E85  Raw traces show a known interference frequency or substantial out-of-band energy.
     how: Inspect power spectra and the current filter response on representative recordings.
     used at: T.4.4
E86  Rare amplitude spikes dominate the signal range.
     how: Plot signal quantiles and clipped versus unclipped traces around suspected artifacts.
     used at: T.4.4
E87  Available sensors or meaningful channel differences are absent from the current input.
     how: Compare the raw sensor schema and domain-valid channel operations with the model’s channel manifest.
     used at: T.4.4
E88  A scalar spectral image is being mapped to channels arbitrarily for an image backbone.
     how: Inspect rendered inputs and the channel mapping expected by the pretrained image model.
     used at: T.4.4
E89  Raw multichannel sequences are being reshaped into an image with an untested spatial layout.
     how: Inspect the reshape code and plot how time and channels map onto both image axes.
     used at: T.4.4
E90  Only fixed checkpoints are available and the proposed front end differs from their training pipeline.
     how: Compare the proposed transform configuration against each checkpoint’s recorded preprocessing.
     used at: T.4.4
E91  Relevant small structures disappear at the current resize resolution.
     how: Compare original and resized examples and inspect the checkpoint’s training image dimensions.
     used at: T.4.5
E92  Spatial borders contain irrelevant regions or the current crop removes useful content.
     how: Overlay crop boundaries on representative images or spectral inputs.
     used at: T.4.5
E93  Labels describe a short interval but the model consumes a much longer or misaligned window.
     how: Compare annotated time spans, sampling rate, and the actual extracted input windows.
     used at: T.4.5
E94  Neighboring time windows contain plausible predictive context that is currently discarded.
     how: Inspect adjacent windows and prior center-only versus context-enabled results.
     used at: T.4.5
E95  Compatible saved variants exist and current inference can compare them without retraining.
     how: Inspect checkpoint metadata and confirm a fixed valid inference path.
     used at: T.5
E96  Current architecture or pretraining has plateaued across credible training trials.
     how: Review standalone validation results across completed runs and available alternative learners.
     used at: T.5
E97  The backbone is useful but pooling, head structure, or modality fusion is restrictive.
     how: Inspect the model graph and error or branch-ablation evidence.
     used at: T.5
E98  Training logs expose optimization, loss, regularization, or implementation shortcomings.
     how: Inspect learning curves, objective definitions, and fold-training artifacts.
     used at: T.5
E99  Several compatible runs differ in training procedure or seed and have not been compared consistently.
     how: List checkpoint manifests and paired scores under identical inference settings.
     used at: T.5.1
E100  Final-epoch and best-validation snapshots differ and late training may overfit.
     how: Compare epoch learning curves and the available stopping-selection criteria.
     used at: T.5.1
E101  Several nearby snapshots from the same parameterization are available.
     how: Inspect architecture identity and training trajectory continuity for the saved weight states.
     used at: T.5.1
E102  The candidate snapshots come from different architectures or unrelated initializations.
     how: Compare architecture keys, shapes, initialization records, and training-run provenance.
     used at: T.5.1
E103  Repeated variants of the same algorithm have plateaued on the same feature matrix.
     how: Review controlled algorithm trials and their validation errors with fixed inputs.
     used at: T.5.2
E104  A compatible backbone pretrained on more relevant data or with a different objective is available.
     how: Inspect checkpoint metadata, domain coverage, and input compatibility.
     used at: T.5.2
E105  Learning curves indicate underfitting or overfitting that tracks model size.
     how: Compare training and validation curves for existing sizes and their parameter counts.
     used at: T.5.2
E106  Labeled data are small and fine-tuning is unstable while useful pretrained embeddings are available.
     how: Inspect seed-to-seed fine-tuning variation, dataset size, and frozen embedding quality on labeled examples.
     used at: T.5.2
E107  Nearby training examples in embedding space tend to share targets.
     how: Inspect leakage-free nearest-neighbor label agreement on held-out examples.
     used at: T.5.2
E108  A larger model alone has repeatedly failed to improve independent validation.
     how: Compare size-controlled runs with matching preprocessing and training effort.
     used at: T.5.2
E109  The backbone is strong but the head is minimal or labels may need distinct attention.
     how: Inspect model graph and label-wise residual patterns for a pooled linear or shared head.
     used at: T.5.3
E110  The model discards useful token or layer information in a fixed pooling step.
     how: Inspect hidden-state extraction and pooling code and examples where salient content is diluted.
     used at: T.5.3
E111  A useful modality is available but absent, or an existing branch has uncertain value.
     how: Inspect input availability, branch configuration, and previous modality ablations.
     used at: T.5.3
E112  Equal-sized branch embeddings are averaged even though their information may be distinct.
     how: Inspect the fusion tensor operation and branch-specific features or ablation results.
     used at: T.5.3
E113  The proposed head differs from all available checkpoints and retraining is unavailable.
     how: Compare parameter names and dimensions with saved checkpoints and available training execution.
     used at: T.5.3
E114  Learning curves reveal unstable convergence or an unsuitable stopping point.
     how: Inspect losses, learning-rate history, and the selected epoch.
     used at: T.5.4
E115  The current loss or output semantics do not match the target or evaluation metric.
     how: Compare training objective and activation code with the task’s target and metric definitions.
     used at: T.5.4
E116  Training error falls while held-out error worsens.
     how: Compare training and validation curves under the current data split.
     used at: T.5.4
E117  A tree learner’s depth, leaf count, or penalties constrain the observed fit.
     how: Inspect fitted tree sizes, train/validation gap, and prior nearby hyperparameter trials.
     used at: T.5.4
E118  A weak component lacks consistent folds, proper batching, or saved per-fold models.
     how: Audit its training loop against the split manifest and produced checkpoint files.
     used at: T.5.4
E119  Training loss diverges, oscillates, or falls too slowly at the current learning rate.
     how: Plot loss and gradient behavior against the logged learning rate.
     used at: T.5.4.1
E120  Progress stalls or deteriorates at a specific schedule transition.
     how: Overlay validation loss and learning-rate history across epochs.
     used at: T.5.4.1
E121  A controlled optimizer alternative is available after reasonable rate and schedule trials.
     how: Review optimizer configuration and completed trials with comparable budgets.
     used at: T.5.4.1
E122  Validation is still improving at the final epoch or worsens well before it.
     how: Inspect the full training and validation learning curves.
     used at: T.5.4.1
E123  The stopping callback monitors training data, the wrong metric direction, or the wrong validation set.
     how: Read evaluation-set order, callback metric name, maximize/minimize flag, and saved best iteration.
     used at: T.5.4.1
E124  Targets are probability distributions and the evaluation uses distributional divergence.
     how: Read the metric formula and verify normalized target distributions.
     used at: T.5.4.2
E125  Outputs are independent labels or bounded independent targets rather than mutually exclusive classes.
     how: Inspect label co-occurrence and the current activation and loss pairing.
     used at: T.5.4.2
E126  The metric rewards pair ordering while training uses only pointwise errors.
     how: Compare the metric definition with the current objective and held-out pairwise errors.
     used at: T.5.4.2
E127  Labels occupy an ordered finite scale.
     how: Inspect unique labels, ordering semantics, and the penalty for distant mistakes.
     used at: T.5.4.2
E128  A custom differentiable objective is already used and its constants or derivatives are unverified.
     how: Read the objective code and compare gradients and Hessians with numerical derivatives.
     used at: T.5.4.2
E129  A meaningful auxiliary classification target can be derived without extra unavailable labels.
     how: Inspect target bins or related outputs and confirm adequate training examples per auxiliary class.
     used at: T.5.4.2
E130  A high-capacity head overfits while the pretrained representation remains useful.
     how: Compare head training and validation curves and inspect the current dropout configuration.
     used at: T.5.4.3
E131  Small visual intensity or geometric changes preserve the label.
     how: Inspect domain examples and the task’s orientation and appearance semantics.
     used at: T.5.4.3
E132  Spectral inputs contain locally redundant regions and masking preserves the event label.
     how: Inspect time-frequency plots and event duration relative to proposed mask widths.
     used at: T.5.4.3
E133  Labels are soft distributions and linear mixtures of examples are a plausible training perturbation.
     how: Inspect target semantics and a small set of mixed inputs with their mixed labels.
     used at: T.5.4.3
E134  The task relies on exact orientation or a small localized event.
     how: Inspect annotations and event extent against the proposed transform or mask.
     used at: T.5.4.3
E135  Members have not been ablated or unused complementary checkpoints exist.
     how: Inspect membership history, per-member metrics, and available candidate predictions.
     used at: T.6
E136  The member set is stable but its averaging or stacking rule has not been compared.
     how: Inspect the combination formula and prior controlled aggregation trials.
     used at: T.6
E137  Member outputs differ in scale, calibration, or activation semantics.
     how: Plot component score distributions and read their output definitions.
     used at: T.6
E138  The stacker input schema is stale or a new out-of-fold feature source is available.
     how: Compare the fitted stacker’s columns with cached base predictions and auxiliary feature manifests.
     used at: T.6
E139  A blend optimizer is the dominant iteration cost and its gains plateau as trials increase.
     how: Inspect optimizer trial histories, independent validation scores, and wall-clock logs.
     used at: T.6
E140  The ensemble has not been compared with its strongest single member.
     how: Inspect saved standalone and blend validation results under identical evaluation.
     used at: T.6.1
E141  A recent member addition regressed or several members appear redundant.
     how: Compare prior leave-one-out results, standalone quality, and residual correlations.
     used at: T.6.1
E142  Current members share highly correlated errors and an unused prediction source is available.
     how: Inspect residual correlations and candidate input, target, or model-family metadata.
     used at: T.6.1
E143  Multiple folds or independent seed checkpoints exist and single-run predictions are unstable.
     how: Inspect checkpoint manifests and held-out variation across runs.
     used at: T.6.1
E144  The current blend consistently beats every tested single model by more than evaluation variability.
     how: Compare repeated or cross-validated standalone and blend metrics.
     used at: T.6.1
E145  Current members use similar algorithms and have strongly correlated held-out residuals.
     how: Compare model-family metadata and pairwise out-of-fold residual correlations.
     used at: T.6.1.3
E146  Available modalities or feature representations are not covered by current members.
     how: Compare the ensemble’s input manifests with available signal, text, or feature views.
     used at: T.6.1.3
E147  The backbone is fixed but differently trained pooling or head variants are available.
     how: Inspect compatible head checkpoints and their held-out prediction correlations.
     used at: T.6.1.3
E148  The outcome admits distinct valid target encodings with different residual patterns.
     how: Inspect target definitions and available out-of-fold predictions from each transformation.
     used at: T.6.1.3
E149  A candidate’s held-out errors are almost identical to those of an existing member.
     how: Align out-of-fold rows and compare residual correlation and candidate-only corrected errors.
     used at: T.6.1.3
E150  All required fold checkpoints are compatible and currently only some are used.
     how: Compare the fold manifest, saved checkpoints, and enabled inference indices.
     used at: T.6.1.4
E151  Independent training seeds produce materially different held-out predictions.
     how: Compare fixed-split checkpoints trained with different seeds on the same validation rows.
     used at: T.6.1.4
E152  Some fold checkpoints are missing or consistently weak on credible validation.
     how: Inspect artifact availability and per-fold quality evidence without selecting on tiny leaderboard differences.
     used at: T.6.1.4
E153  Only repeated deterministic forward passes are available, not independently trained runs.
     how: Inspect checkpoint hashes, training seeds, and evaluation-mode outputs.
     used at: T.6.1.4
E154  A small set of prediction sources can be compared with fixed global coefficients.
     how: Inspect the member count, score distributions, and available held-out prediction matrix.
     used at: T.6.2
E155  One model family has many more checkpoints than another.
     how: Count members by architecture, training run, and target representation and inspect their current total influence.
     used at: T.6.2
E156  Different members are reliably stronger on identifiable classes or sample subsets.
     how: Compare subgroup or per-class held-out errors with subgroup sample sizes.
     used at: T.6.2
E157  Leakage-free out-of-fold predictions are available for training a low-capacity meta-model.
     how: Verify row-level exclusions, shared fold manifests, and a separate evaluation split for the stacker.
     used at: T.6.2
E158  Meta-model fits or conditional weights overfit a small validation set in earlier trials.
     how: Compare fitted-combiner training and held-out results with the uniform average.
     used at: T.6.2
E159  Members have comparable held-out quality and weight tweaks have not generalized.
     how: Compare per-member metrics and earlier uniform versus tuned blend results.
     used at: T.6.2.1
E160  Members differ consistently in quality and aligned held-out predictions are available.
     how: Compare member metrics over folds and verify cached out-of-fold rows.
     used at: T.6.2.1
E161  Residual covariance suggests that subtracting a correlated source could correct systematic error.
     how: Inspect the held-out residual covariance and a disjoint-validation signed linear fit.
     used at: T.6.2.1
E162  The dataset is small and fitted coefficients vary sharply across folds.
     how: Compare coefficient estimates and blend scores across disjoint validation folds.
     used at: T.6.2.1
E163  The metric depends on ordering and member score scales or calibration differ.
     how: Read the metric formula and plot each member’s aligned held-out score distribution.
     used at: T.6.3
E164  A fitted linear combiner receives predictors with very different variance or heavy tails.
     how: Compare out-of-fold score means, variances, quantiles, and extreme values.
     used at: T.6.3
E165  Bounded component probabilities are highly concentrated before averaging.
     how: Plot per-member probability histograms and inspect errors among low-probability cases.
     used at: T.6.3
E166  Models expose both logits and probabilities and the metric evaluates distributions.
     how: Inspect the output activation location and the metric’s normalization requirements.
     used at: T.6.3
E167  Absolute magnitudes are required by a downstream additive correction.
     how: Trace the correction formula and its expected input scale.
     used at: T.6.3
E168  Valid alternate input views or stochastic model outputs are available.
     how: Inspect transform semantics, model modes, and prior single-pass predictions.
     used at: T.7
E169  The target is discrete or the metric treats ties and ordinal errors specially.
     how: Inspect target values and the scoring implementation.
     used at: T.7
E170  The metric needs calibrated probabilities and held-out calibration is imperfect.
     how: Read the metric and inspect reliability plots, row sums, and probability loss.
     used at: T.7
E171  Residual bias is localized to a reliable reference, auxiliary signal, or metadata rule.
     how: Inspect out-of-fold residuals conditioned on the proposed correction input.
     used at: T.7
E172  Existing post-processing was tuned before a model or ensemble change.
     how: Compare the post-processing artifact provenance with the current prediction configuration.
     used at: T.7
E173  There are known label-preserving flips, sensor permutations, crops, or views.
     how: Inspect domain symmetry, label scope, and representative transformed inputs.
     used at: T.7.1
E174  Dropout is intentionally active and repeated passes produce different outputs.
     how: Inspect module modes and compare repeated forward-pass arrays for the same input.
     used at: T.7.1
E175  The model is in evaluation mode and repeated passes are numerically identical.
     how: Inspect training/evaluation flags and maximum difference between repeated predictions.
     used at: T.7.1
E176  A proposed transform changes event orientation, timing, or clinically meaningful location.
     how: Compare transformed examples with the label definition and relevant annotations.
     used at: T.7.1
E177  Targets occupy a finite ordered set and continuous outputs need a discrete mapping.
     how: Inspect unique labels, submission constraints, and the metric’s treatment of ordered mistakes.
     used at: T.7.2
E178  The expected test label proportions are credibly stable relative to training.
     how: Compare available source/time label histograms and the task’s test sampling description.
     used at: T.7.2
E179  Large identifiable subgroups have different held-out calibration curves.
     how: Plot score-to-label curves and counts by subgroup, including errors in any inferred group labels.
     used at: T.7.2
E180  Outputs contain exact ties whose treatment differs across the metric or ranking implementation.
     how: Count ties and run the metric on a small tied example to inspect its actual convention.
     used at: T.7.2
E181  Subgroup assignment is noisy or each subgroup has few calibration examples.
     how: Inspect subgroup classifier errors and held-out calibration sample counts.
     used at: T.7.2
E182  Training and expected test label frequencies differ.
     how: Compare known source-specific label distributions and test source composition.
     used at: T.7.2
E183  Logits are consistently too sharp or too flat on held-out examples.
     how: Inspect reliability plots and held-out probability loss against confidence.
     used at: T.7.3
E184  Specific classes have stable prediction-mass errors after normalization.
     how: Compare average predicted and observed class distributions across validation folds.
     used at: T.7.3
E185  Predictions violate the required range or do not sum to one for a distributional task.
     how: Inspect final output minima, maxima, row sums, and submission requirements.
     used at: T.7.3
E186  The metric only uses within-column rank and no later blend or rounding depends on magnitude.
     how: Read the metric implementation and trace remaining post-processing operations.
     used at: T.7.3
E187  Residuals show a stable additive offset or target scaling was not inverted.
     how: Compare held-out residual means across folds and inspect training target transformations.
     used at: T.7.4
E188  A validated auxiliary classifier identifies cases where the base continuous model is biased.
     how: Compare base residuals by auxiliary confidence or class on out-of-fold examples.
     used at: T.7.4
E189  A metadata rule predicts an affected target with high precision on held-out examples.
     how: Count held-out rule matches and errors and verify the metadata exists at inference.
     used at: T.7.4
E190  The proposed correction uses true test labels or metadata unavailable at inference.
     how: Trace the correction’s inputs and compare them with the test schema.
     used at: T.7.4
E191  The full run exceeds memory capacity or repeatedly fails on large batches.
     how: Inspect memory traces and out-of-memory logs.
     used at: T.8
E192  Runtime is dominated by repeated preprocessing, incomplete-stage restarts, or a profiled slow operation.
     how: Inspect stage timings and repeated computation logs.
     used at: T.8
E193  Identical inputs and artifacts produce different predictions because stochastic execution remains uncontrolled.
     how: Compare repeated arrays and inspect seeds, data-loader workers, model modes, and transform randomness.
     used at: T.8
E194  Memory remains allocated after one model finishes and grows across stages.
     how: Inspect accelerator and host memory at model-load, post-prediction, and stage-exit boundaries.
     used at: T.8.1
E195  The first forward pass fails at the current batch size.
     how: Run progressively smaller batches and inspect peak allocation and the failing tensor shape.
     used at: T.8.1
E196  Parameters or activations dominate memory and supported reduced precision is available.
     how: Inspect tensor dtypes, parameter size, hardware capability, and any prior precision comparisons.
     used at: T.8.1
E197  Predictions or probability metrics shift materially in prior reduced-precision trials.
     how: Compare identical-example predictions and held-out metrics from full and reduced precision.
     used at: T.8.1
E198  Expensive features or base predictions are recomputed unchanged during downstream sweeps.
     how: Profile repeated runs and compare upstream configuration and artifact hashes.
     used at: T.8.2
E199  Completed folds or training stages are repeated because a session cannot finish all work.
     how: Inspect checkpoint completeness and stage-level runtime logs.
     used at: T.8.2
E200  Adding or removing models requires edits in several inconsistent code locations.
     how: Search model IDs, paths, and flags and compare their values across the pipeline.
     used at: T.8.2
E201  Profiling identifies a slow metric, transform, or excessive sequence padding.
     how: Measure per-stage runtime and padding ratios on representative batches.
     used at: T.8.2
E202  The cached intermediate’s preprocessing or row schema no longer matches the current experiment.
     how: Compare cache manifests and row/column keys with the requested configuration.
     used at: T.8.2
E203  The variable written to the submission file differs from the variable holding the actual predictions.
     how: Compare the variable name in the CSV-writing step to the variable that accumulates model predictions.
     used at: T.1
E204  A hardcoded preprocessing parameter (e.g., image size, sequence length) does not match what the loaded model expects.
     how: Check that inference-time preprocessing constants match the training configuration of each checkpoint.
     used at: T.1
E205  The model wrapper class has an attribute-name mismatch between __init__ and forward(), causing a silent error or crash.
     how: Verify that every submodule assigned in __init__ is referenced by the same attribute name in forward().
     used at: T.1
E206  Debug output was added to inspect loaded checkpoint contents, indicating a suspected weight-loading mismatch.
     how: Check logs for diagnostic print statements about checkpoint state_dict keys or shapes.
     used at: T.1
E207  model.eval() was not called before inference, leaving dropout and batch-norm in training mode.
     how: Verify that model.eval() is called after loading weights and before generating predictions.
     used at: T.1
E208  Inference-time configuration (pooling, preprocessing params, batch size, text normalization) does not match the training-time configuration of the loaded checkpoint.
     how: Compare inference hyperparameters and preprocessing steps against the training config that produced each checkpoint.
     used at: T.1
E209  Required model checkpoint or pretrained weight files are missing or their paths are stale/incorrect.
     how: Verify that every referenced checkpoint path exists on disk and points to the intended artifact.
     used at: T.1
E210  A control-flow statement (continue/break/return) in the model loop prevents some models from executing or contributing predictions.
     how: Trace the inference loop to confirm every model iteration reaches the prediction-accumulation step.
     used at: T.1
E211  A required runtime flag or mode variable is not set correctly, causing inference to run in an unintended mode.
     how: Check that all mode flags (e.g., hack_infer, TEST_MODE) are set to their intended inference-time values.
     used at: T.1
E212  The custom objective function's gradient or Hessian computation is mathematically incorrect or uses a placeholder value.
     how: Review the custom loss function's first and second derivatives for correctness against the intended formula.
     used at: T.1
E213  The prediction call is scoped incorrectly relative to where its required inputs are prepared, causing it to use stale data or skip folds.
     how: Check that the prediction statement and its input-preparation block share the same loop/conditional scope for every fold.
     used at: T.1
E214  A leftover debug or fallback code block still exists that could overwrite or corrupt the final submission output.
     how: Search for any interim submission writes or fallback blocks that could execute alongside the main output logic.
     used at: T.1
E215  A duplicate model instantiation creates a redundant object that wastes memory or shadows the intended model.
     how: Check that each model class is instantiated exactly once and the correct instance is used for inference.
     used at: T.1
E216  A variable name mismatch causes the aggregation/stacking array to reference a different array than the one populated by the prediction calls.
     how: Compare the variable names assigned in each model's predict call with the variable names read in the ensemble aggregation step; flag any that do not match.
     used at: T.1.2
E217  A variable reference points to the wrong object (e.g., wrong model, wrong directory, wrong column set), causing a component to silently duplicate or substitute another.
     how: Trace each variable passed into ensemble/stacking/submission calls back to its assignment and verify it refers to the intended distinct object.
     used at: T.1.2
E218  A code block for one of the intended ensemble or pipeline components is commented out, disabled, or otherwise not executed.
     how: Check whether every intended model/component has an active (uncommented, reachable) prediction block that contributes to the final output.
     used at: T.1.2
E219  An accumulation statement (append, +=, etc.) is at the wrong indentation level relative to its loop, so only the last iteration's result is captured.
     how: Verify that statements accumulating per-iteration results (e.g., preds.append) are indented inside the loop body, not outside it.
     used at: T.1.2
E220  Duplicate column aliases or keys in the feature/prediction pipeline silently overwrite earlier computed values.
     how: List all column names or dictionary keys produced during aggregation and check for duplicates that would cause silent overwrites.
     used at: T.1.2
E221  The input construction code uses an incorrect concatenation or formatting operation, producing malformed model inputs.
     how: Inspect how raw fields are combined into model input strings/tensors and verify the operation produces the intended structure (e.g., element-wise Series concat vs list concat).
     used at: T.1.2
E222  The tokenizer configuration (e.g., do_lower_case, vocab) is inconsistent with the loaded model checkpoint, producing wrong token IDs.
     how: Compare the tokenizer settings against the model checkpoint's expected tokenizer configuration and verify token IDs match expected values on sample inputs.
     used at: T.1.2
E223  The data-loading code reads the wrong file or uses a hardcoded row count that does not match the actual test set.
     how: Verify the file path in the read call points to the intended test file and that any hardcoded row counts match the actual file length.
     used at: T.1.2
E224  A guard condition or code path prevents the submission file from actually being written to disk.
     how: Trace the submission write call and confirm it is reached unconditionally (no if-guard, no early return) and the file appears on disk with the correct row count.
     used at: T.1.2
E225  The fold-averaging divisor is applied inside the per-fold loop instead of once after all folds, causing incorrect scaling of predictions.
     how: Check whether the division by n_folds (or equivalent normalization) occurs once after the loop completes, not inside each iteration.
     used at: T.1.2
E226  The model loading paths point to wrong experiment directories or files, causing incorrect or failed model loads.
     how: Verify each model load path resolves to the intended checkpoint file and that the loaded weights correspond to the expected experiment.
     used at: T.1.2
E227  An unnecessary or environment-incompatible package-install cell exists that may cause failures in the runtime environment.
     how: Check whether a conda/pip install cell is redundant or conflicts with the platform's pre-installed packages.
     used at: T.1.3
E228  The edit is an empty-diff re-run (no code change) rather than an actual fix, used to check whether the failure was transient.
     how: Compare the diff between the current and previous version; if empty, the expert is re-running unchanged code.
     used at: T.1.3
E229  The failure is caused by a trivial syntax or string-escaping error introduced during manual editing.
     how: Inspect the traceback for SyntaxError, typo in string literals, or malformed expressions introduced in the latest edit.
     used at: T.1.3
E230  This is a follow-up fix iteration for the same root-cause error that a previous version already attempted to fix.
     how: Check whether a prior version addressed the same error and the current edit is a second (or later) attempt at the same fix.
     used at: T.1.3
E231  Previously removed feature groups need to be re-added individually to isolate which one causes the pipeline failure.
     how: Check whether the fix strategy is incremental re-introduction of removed components to bisect the error source.
     used at: T.1.3
E232  The source or destination directories are mounted as read-only, preventing file write/copy operations.
     how: Check whether the failing operation attempts to write to a read-only mounted path (e.g., /kaggle/input/).
     used at: T.1.3
E233  The notebook runs out of disk space or memory during inference because previously-loaded models or data are not cleaned up.
     how: Check runtime logs for disk-full or OOM errors and whether intermediate artifacts are deleted between model runs.
     used at: T.1.3
E234  Available model checkpoints or fold outputs have not been tested in the current ensemble or evaluation.
     how: Check whether untested checkpoint files from different folds or CV runs exist that could change ensemble composition.
     used at: T.2
E235  A rewritten or refactored pipeline has not been verified to reproduce the previous pipeline's outputs before trusting new scores.
     how: Compare outputs of the new pipeline against the old pipeline on the same data to confirm functional equivalence.
     used at: T.2
E236  Validation predictions for specific data subsets may have been computed with incorrect preprocessing or augmentation settings, making OOF scores unreliable for those subsets.
     how: Audit augmentation and preprocessing flags applied during OOF prediction for each data subset or variant.
     used at: T.2
E237  The pipeline depends on external cached artifacts that may not be reproducible or may differ from freshly computed results.
     how: Check whether cached files (embeddings, features, etc.) were generated under the same conditions as the current pipeline expects.
     used at: T.2
E238  The number of CV folds is too low for stable OOF-based threshold optimization or metric estimation.
     how: Assess whether OOF prediction noise from the current fold count materially affects threshold tuning or QWK estimation.
     used at: T.2
E239  Post-processing or formatting edits have not been externally validated to confirm the submission file is still correctly structured.
     how: Check whether the submission file format (columns, row count, value ranges) has been verified after recent post-processing changes.
     used at: T.2
E240  Inference-time transforms (e.g., resize, normalization, augmentation) differ from training-time transforms, causing a distribution mismatch that inflates or deflates validation metrics.
     how: Compare the full preprocessing and augmentation pipeline applied during training versus inference and flag any discrepancies.
     used at: T.2.2
E241  The practitioner lacks a proper offline validation setup and is using indirect proxies (filenames, LB submissions) to rank models.
     how: Check whether a local CV or held-out evaluation procedure exists and is being used as the primary model-selection signal.
     used at: T.2.2
E242  Early-exit or runtime guards truncate training or evaluation, producing incomplete CV scores that misrepresent true model quality.
     how: Verify that all training folds and evaluation steps run to completion without being short-circuited by runtime or resource guards.
     used at: T.2.2
E243  The target labels are soft/distributional rather than hard classes, making standard stratification on a consensus label potentially inappropriate.
     how: Check whether the labels used for stratification are hard consensus labels derived from soft vote distributions, which may misrepresent the true label structure.
     used at: T.2.3
E244  The feature matrix passed to the clustering/splitting step includes non-feature columns (e.g., IDs, targets) that should be excluded.
     how: Inspect the dataframe or array passed to KMeans.fit or the CV splitter for columns like essay_id, score, or other metadata that are not valid features.
     used at: T.2.3
E245  The KMeans clustering call receives invalid input (non-numeric data or mismatched matrices between fit and predict).
     how: Check that KMeans.fit and KMeans.predict receive the same numeric feature matrix without string columns or shape mismatches.
     used at: T.2.3
E246  Materializing the clustering input as a dense array exceeds available memory.
     how: Check whether the sparse-to-dense conversion (e.g., toarray()) for the clustering input fits within the runtime memory budget.
     used at: T.2.3
E247  The feature representation used for KMeans clustering may not capture the semantic similarity (e.g., topic) needed for valid group construction.
     how: Compare whether TF-IDF vectors, engineered features, or another representation better reflects the grouping structure required for generalization.
     used at: T.2.3
E248  The CV splitter or related variables referenced in the loop are not yet instantiated, causing a runtime error.
     how: Verify that the splitter object (e.g., sgkf) and any required accumulator variables are defined before the CV loop executes.
     used at: T.2.3
E249  The current edit references variables or dataframes that do not exist in the notebook scope, causing a runtime error.
     how: Check that all variable names (e.g., 'train', dataframe references) used in the split/read calls are defined and aligned in the current notebook scope.
     used at: T.2.3
E250  The target variable y and the group labels passed to StratifiedGroupKFold.split are derived from different or misaligned dataframes.
     how: Verify that y and groups arrays are aligned row-for-row with the same dataframe and have matching lengths.
     used at: T.2.3
E251  Real topic/prompt labels are available as external metadata that could replace unsupervised cluster-based groups.
     how: Check whether a supplementary file with ground-truth topic or prompt labels exists and can be joined to the training data.
     used at: T.2.3
E252  The target variable passed to StratifiedGroupKFold is float-valued rather than integer/discrete, which will cause an error or degenerate stratification.
     how: Check the dtype of y passed to StratifiedGroupKFold.split and confirm it contains discrete class labels.
     used at: T.2.3
E253  The validation design change is bundled with other modifications (e.g., hyperparameters, GPU config, callbacks), preventing isolated evaluation of its effect.
     how: Check whether the edit changes only the split/fold logic or also modifies model hyperparameters, hardware config, or other pipeline components simultaneously.
     used at: T.2.3
E254  A nested CV scheme (outer × inner folds) could produce more robust OOF estimates than a flat scheme.
     how: Evaluate whether a nested CV design is appropriate given the dataset size, computational budget, and whether it has been tried before.
     used at: T.2.3
E255  The feature-selection artifacts (e.g., saved feature lists) match the current CV fold count and splitting setup.
     how: Verify that any pre-computed feature-selection file corresponds to the same number of folds and split strategy currently in use.
     used at: T.2.3
E256  Early-stopping patience is calibrated relative to the training set size implied by the fold count, avoiding premature stopping.
     how: Check whether the early-stopping patience and max boosting rounds are appropriate given the smaller training sets that result from higher fold counts.
     used at: T.2.3
E257  The effect of adding extra data is confounded with other simultaneous changes (e.g., checkpoint, stage config), so its isolated contribution is unknown.
     how: Compare changelogs between versions to see whether the extra-data addition was the sole change or bundled with other modifications.
     used at: T.3
E258  Auxiliary data could be isolated into a separate early training stage to prevent it from contaminating later fine-tuning stages.
     how: Review the multi-stage training pipeline to determine whether extra data is mixed into all stages or can be confined to an initial pre-training stage.
     used at: T.3
E259  A development holdout is currently active, withholding a significant fraction of labeled rows from the final training fit.
     how: Check whether a dev/validation split is still reserving labeled data that could be folded back into training for the final submission model.
     used at: T.3
E260  A previous version implementing this change was not submitted/scored, so a re-run is needed to obtain the leaderboard score.
     how: Check submission history to see whether the relevant prior version received a leaderboard score.
     used at: T.3.1
E261  The current baseline already achieves a competitive score, so this change is an incremental experiment rather than a fix for a known problem.
     how: Compare the current best leaderboard score against the expected gain from the proposed change.
     used at: T.3.1
E262  Reliable offline (CV) validation is unavailable, so leaderboard submissions are required to evaluate each variant.
     how: Check whether a trustworthy local cross-validation metric exists that correlates with leaderboard performance.
     used at: T.3.1
E263  Previous experiments showed that the best known score used all data without the proposed filtering, so the filtering may not help.
     how: Review historical scores comparing filtered vs. unfiltered training sets.
     used at: T.3.1
E264  The change is explicitly framed as a reversible experiment with a plan to revert if it worsens the score.
     how: Check whether the expert stated an intent to revert if the change does not improve performance.
     used at: T.3.1
E265  A previous attempt at the same type of change (data selection/filtering) caused a measurable score regression.
     how: Review leaderboard history for prior versions that applied similar data selection logic and check whether they regressed.
     used at: T.3.1
E266  Bundling complementary training improvements with the data selection change may compensate for any individual weakness.
     how: Check whether multiple orthogonal improvements are being applied together in this version.
     used at: T.3.1
E267  The previously implemented logic needs a verification run to confirm it executes correctly before further changes.
     how: Check whether the prior version ran to completion without errors and produced expected outputs.
     used at: T.3.1
E268  The previous edit used the wrong variable/flag for the intended subgroup selection, and this run is a single-variable fix to isolate the correct effect.
     how: Compare the code diff to confirm only the subgroup key was changed.
     used at: T.3.1
E269  An alternative approach to the same problem (e.g., sample weighting via loss) was already tried and did not yield improvement.
     how: Check experiment history for prior attempts addressing the same imbalance via a different mechanism.
     used at: T.3.1
E270  Removing the augmentation/filtering code simplifies the pipeline and eliminates a confounding factor when tuning other components.
     how: Check whether the code being removed is an independent module whose removal reduces confounds.
     used at: T.3.1
E271  The evaluation metric rewards calibrated ordinal predictions rather than balanced class accuracy, making synthetic oversampling likely counterproductive.
     how: Check whether the evaluation metric (e.g., QWK) penalizes the distributional shift introduced by oversampling.
     used at: T.3.1
E272  The proposed mechanism (e.g., scale_pos_weight) is designed for a different task type and may be ignored or misapplied in the current objective.
     how: Check whether the parameter or technique is compatible with the model's objective function.
     used at: T.3.1
E273  A pre-computed artifact (e.g., outlier list) already exists and is ready to be loaded for this change.
     how: Verify that the required pre-computed file exists in the current environment.
     used at: T.3.1
E274  The pseudo-labeled model's standalone score is competitive with the component it would replace in the ensemble.
     how: Compare the pseudo-labeled model's standalone leaderboard score against the ensemble baseline or the member it would replace.
     used at: T.3.2
E275  Previous attempts to include extra data in training consistently failed to beat the best score without extra data.
     how: Review the history of prior versions that integrated extra data and compare their scores against the best no-extra-data score.
     used at: T.3.2
E276  Extra-data feature arrays have compatible shapes with the primary training data (or a padding/truncation strategy is in place).
     how: Compare the .npy array shapes of extra data against primary training data and verify alignment or preprocessing steps.
     used at: T.3.2
E277  A clean scored comparison exists between the with-extra-data and without-extra-data configurations (no confounding changes).
     how: Check whether a version that differs only in the inclusion of extra data has been scored on the leaderboard.
     used at: T.3.2
E278  The extra-data pipeline was previously added and then removed, providing an A/B comparison history.
     how: Review version history for natural add/remove cycles of extra data and their associated scores.
     used at: T.3.2
E279  Previous versions that included extra data did not simultaneously change other variables (e.g., checkpoints), so the extra-data effect is unconfounded.
     how: Inspect changelogs of prior extra-data versions to determine whether other variables were changed simultaneously.
     used at: T.3.2
E280  Pseudo-labeling has consistently improved other architectures/members in this pipeline.
     how: Review standalone scores of other ensemble members before and after pseudo-label training.
     used at: T.3.2
E281  Pseudo-labeling has already been applied to this specific model and improved its standalone score.
     how: Check whether this specific model was previously trained with pseudo-labels and compare its before/after standalone scores.
     used at: T.3.2
E282  Multiple target transformations exist but have not been individually evaluated on the leaderboard to determine which is best.
     how: List all target variants currently trained and check whether each has a solo leaderboard submission isolating its contribution.
     used at: T.3.3
E283  A candidate monotonic target transform would produce predictions not already represented by existing transforms in the ensemble.
     how: Compare the rank-order and distribution of the proposed transform's outputs against those of all current target transforms to verify it adds non-redundant signal.
     used at: T.3.3
E284  A recently tested representation change caused a regression and should be reverted.
     how: Compare scores before and after the representation change to confirm the regression.
     used at: T.4
E285  A recent change to the number or selection of input channels has not been isolated from other simultaneous changes.
     how: Check whether the channel change was introduced alongside other modifications and whether its individual effect has been measured.
     used at: T.4
E286  A recently added NER-based preprocessing step has shown inconsistent effects and its net contribution is unclear.
     how: Compare scores across checkpoints with and without NER preprocessing to determine whether it reliably helps.
     used at: T.4
E287  The encoding transform produces an output with mismatched row counts between train and test sets.
     how: Compare the number of rows in the encoded output array against the expected number of samples in the test set.
     used at: T.4.1
E288  A previous implementation of this text-input modification had a code bug that prevented proper evaluation of the idea.
     how: Review version history and logs for errors (wrong function calls, incorrect axis parameters, data-flow issues) in prior attempts at the same preprocessing change.
     used at: T.4.2
E289  The modified text is used as an additional feature alongside the raw text rather than replacing it, preserving the original signal.
     how: Check whether the pipeline concatenates or augments features from both raw and processed text, versus substituting one for the other.
     used at: T.4.2
E290  A previous version without this text cleaning scored higher than the version with it, suggesting the preprocessing hurts performance.
     how: Compare validation/leaderboard scores between the version that introduced the cleaning and the immediately prior version without it.
     used at: T.4.2
E291  The text preprocessing applied at inference differs from what was used during training of the loaded checkpoint, creating a train/inference mismatch.
     how: Compare the preprocessing flags and pipeline used when the checkpoint was trained against the current inference-time preprocessing configuration.
     used at: T.4.2
E292  The text-input modification has only been tested with one checkpoint and its effect may be checkpoint-dependent.
     how: Check whether the preprocessing change has been evaluated across multiple model checkpoints or only with a single one.
     used at: T.4.2
E293  The pretrained encoder's subword tokenization already handles misspellings and special characters, making explicit text cleaning redundant.
     how: Assess whether the encoder's tokenizer (e.g., BPE, WordPiece) naturally decomposes unusual tokens in a way that already captures the signal the cleaning targets.
     used at: T.4.2
E294  Strong public solutions or top-scoring approaches use a different spectrogram rendering or resolution strategy than the current pipeline.
     how: Review top public notebooks, competition discussion, and leaderboard solutions to see if a different front-end representation (e.g., multi-resolution spectrograms, colormap-rendered RGB) is consistently used by high scorers.
     used at: T.4.4
E295  The time-index or sampling-rate calculation used in spectrogram window extraction contains a numerical error.
     how: Audit the code that converts time offsets to sample indices, checking that the sampling rate multiplier matches the actual data rate after any resampling steps.
     used at: T.4.4
E296  The proposed front-end change was previously bundled with other modifications and has never been ablated in isolation.
     how: Check the experiment log to see whether the spectrogram or front-end change in question was introduced alongside other changes, making its individual contribution unknown.
     used at: T.4.4
E297  The best-scoring configuration used a higher sampling rate or wider filter band than what is currently proposed.
     how: Compare the sampling rate and filter-range parameters of the current proposal against those of the historically best-scoring version in the experiment log.
     used at: T.4.4
E298  The most recent front-end changes have not yet been scored, so the immediate next step is a scoring run rather than a new front-end experiment.
     how: Check whether the last set of front-end modifications has been submitted and scored; if not, a submission is needed before introducing further changes.
     used at: T.4.4
E299  The current GPU spectrogram library has been a recurring source of bugs and instability.
     how: Review the commit/version history for bug fixes related to the GPU spectrogram library (e.g., cupy/cusignal) and count how many iterations were needed to stabilize it.
     used at: T.4.4
E300  A previously tested time-frequency factorization (resolution/shape) yielded a competitive score and should be considered before trying untested alternatives.
     how: Look up the experiment log for earlier spectrogram shape/factorization settings and their corresponding scores to see if a known-good configuration exists.
     used at: T.4.4
E301  The current bandpass filter implementation may introduce excessive ringing, latency, or computational cost compared to a simpler alternative.
     how: Inspect the filter type (FIR vs IIR), order, and edge behavior of the current preprocessing filter; compare runtime and impulse response against a lower-order alternative.
     used at: T.4.4
E302  The resolution-vs-score curve from prior experiments provides a clear signal (trend or peak) to guide the next resolution choice.
     how: Review scores from previously tested resolutions and check whether the trend suggests further gains, a plateau, or a non-monotonic peak.
     used at: T.4.5
E303  The proposed inference resolution differs from the checkpoint's training resolution, risking distribution shift.
     how: Compare the inference resolution being set against the resolution the pretrained/finetuned checkpoint was trained at.
     used at: T.4.5
E304  The score change from the last resolution/crop change is within run-to-run variance, so the effect is uncertain.
     how: Compare the magnitude of the score change to the observed variance across NOOP or repeated runs.
     used at: T.4.5
E305  The actual code edit changes a different parameter than the intended input-extent parameter, confounding the experiment.
     how: Inspect the diff to verify that only the intended input-extent parameter (resolution, crop, window) was changed.
     used at: T.4.5
E306  The proposed resolution change causes GPU memory issues requiring infrastructure workarounds.
     how: Check whether the new resolution fits within single-GPU memory or requires batch-size reduction / multi-GPU inference.
     used at: T.4.5
E307  Prior crop or offset experiments indicate a particular spatial crop value scores better than the current setting.
     how: Review scores from previously tested crop percentages and offsets to identify the best-performing configuration.
     used at: T.4.5
E308  The inference-time crop center or offset does not match the crop alignment used during training.
     how: Compare the crop offset parameter at inference to the default or documented crop alignment used during checkpoint training.
     used at: T.4.5
E309  Prior temporal-window parameter changes show the score is sensitive to the temporal extent, justifying further incremental tuning.
     how: Check whether previous changes to the temporal window length or alignment produced meaningful score differences.
     used at: T.4.5
E310  There is an input preprocessing mismatch (e.g., image resize, decoding size) between what the model expects and what the inference pipeline provides.
     how: Compare the model's expected input dimensions with the actual dimensions produced by the data loading/decoding pipeline.
     used at: T.5
E311  The candidate checkpoint/model shows poor standalone performance, suggesting fold-averaging or multi-seed aggregation is needed before judging it.
     how: Check standalone validation scores of individual folds or seeds versus the aggregated result.
     used at: T.5
E312  The candidate model group's standalone score is known and underperforms the best baseline, so improvement via checkpoint or config changes is plausible.
     how: Compare the standalone leaderboard score of the model group against the best known baseline.
     used at: T.5
E313  The upstream training pipeline may have produced new or updated checkpoint artifacts since the last inference run.
     how: Check whether the training pipeline has completed new runs or produced updated checkpoint files since the last inference submission.
     used at: T.5
E314  The previous modification reduced backbone or architectural diversity relative to the best-scoring configuration.
     how: Compare the set of backbones/architectures in the current version versus the best-scoring prior version.
     used at: T.5
E315  Prior experiments with a different pipeline showed that scaling up the backbone size improved performance, suggesting the same scaling direction for the current pipeline.
     how: Review historical results comparing smaller vs. larger backbone variants in prior or parallel pipelines.
     used at: T.5
E316  Adding a model trained with a different loss function or training objective would increase ensemble diversity beyond current members.
     how: Inventory the loss functions used by all current ensemble members and check whether an alternative-loss checkpoint is available.
     used at: T.5
E317  Public top solutions or winning notebooks for this competition commonly use a specific backbone/architecture that differs from the current one.
     how: Review public kernels, discussion forums, and winning solution write-ups to identify commonly used backbones.
     used at: T.5.2
E318  A trained variant of a different capacity within the same backbone family has a checkpoint available and can be evaluated standalone.
     how: Check whether a smaller or larger variant checkpoint exists and can be loaded into the current pipeline for standalone evaluation.
     used at: T.5.2
E319  The code path for the alternative model contains a bug that must be fixed before any valid comparison can be made.
     how: Attempt to run the alternative model's inference path and check for runtime errors or incorrect outputs.
     used at: T.5.2
E320  The alternative checkpoint's leaderboard score is already known from a previous submission.
     how: Check submission history to see if this exact checkpoint was previously scored.
     used at: T.5.2
E321  The alternative model or embedding can run within the inference time and resource budget.
     how: Estimate or benchmark the alternative model's inference time and memory usage against competition constraints.
     used at: T.5.2
E322  The alternative predictor has undergone significantly fewer training/tuning iterations than the current one, so a fair comparison requires acknowledging the maturity gap.
     how: Compare the number of training iterations, hyperparameter sweeps, and checkpoint versions between the current and alternative models.
     used at: T.5.2
E323  A newer version of the same checkpoint set is available and may contain improved training results.
     how: Check the checkpoint repository or versioning system for updated checkpoint files.
     used at: T.5.2
E324  The proposed change is only a checkpoint swap within the same architecture, not an actual model family or capacity change.
     how: Inspect the edit diff to determine whether the architecture definition changed or only the checkpoint path.
     used at: T.5.2
E325  The alternative backbone was introduced in a recent version but has not yet been scored on the leaderboard.
     how: Check submission history to confirm whether the version containing the backbone swap has received a leaderboard score.
     used at: T.5.2
E326  A larger or different variant within a known model family is available in standard libraries and compatible with the current input pipeline without major restructuring.
     how: Check whether the alternative model can be loaded from standard libraries and accepts the same input format.
     used at: T.5.2
E327  The alternative predictor was previously a proven ensemble member that contributed positively to the score.
     how: Review past submission logs and ablation results to confirm the alternative model's historical contribution.
     used at: T.5.2
E328  A structurally different model family (e.g., 1D CNN/RNN on raw signals vs. 2D CNN on spectrograms, or GBDT vs. linear) is known from public solutions to complement the current approach.
     how: Review public solutions and literature to identify model families that provide complementary signal to the current architecture.
     used at: T.5.2
E329  Changing internal components (e.g., activation functions, attention heads) within the existing architecture constitutes a meaningful variant worth testing before switching model families entirely.
     how: Identify whether smaller architectural modifications have been explored before committing to a full model family switch.
     used at: T.5.2
E330  The alternative predictor variant was already tested and scored worse than the current model.
     how: Check submission history for prior scores of the proposed alternative.
     used at: T.5.2
E331  A variant of the current model augmented with a different inference mechanism (e.g., KNN) has pretrained checkpoints available and can be swapped in with minimal code changes.
     how: Verify that the augmented variant's checkpoints exist and the code path to load them is straightforward.
     used at: T.5.2
E332  A known competitive alternative framework/algorithm with different regularization or tree-building strategies is available for the same feature matrix.
     how: Identify whether alternative GBDT or ML frameworks (XGBoost, CatBoost, etc.) are available and offer meaningfully different inductive biases.
     used at: T.5.2
E333  The previous poor performance of the alternative predictor may have been caused by suboptimal thresholds, config, or bugs rather than inherent model inadequacy.
     how: Review whether the prior poor result had known confounds such as wrong thresholds, config errors, or implementation bugs.
     used at: T.5.2
E334  A training technique (e.g., seed averaging, fold ensembling) that improved the current model has not yet been applied to the alternative model.
     how: Check whether the alternative model's checkpoints include the same ensembling/averaging techniques used for the current best.
     used at: T.5.2
E335  The inference config specifies a model size/architecture that does not match the checkpoint's training architecture.
     how: Compare the model architecture specified in the inference config against the architecture used to train the loaded checkpoint.
     used at: T.5.2
E336  A previous head or pooling modification produced a meaningful score change, providing evidence about the value of further head modifications.
     how: Check whether prior head/pooling changes (e.g., SSE block, attention pooling) led to score gains or regressions.
     used at: T.5.3
E337  An earlier head/block variant has not been re-tested since the rest of the architecture evolved and its checkpoints still exist.
     how: Check whether a previously replaced block still has valid checkpoints and the surrounding architecture has changed enough to warrant re-evaluation.
     used at: T.5.3
E338  A smaller or initial variant of the proposed modification has already been scored and can serve as a reference baseline.
     how: Check whether a reduced-capacity or earlier version of the new component has a known score.
     used at: T.5.3
E339  Reinitializing the last few transformer layers is a known small-data fine-tuning technique not yet applied in the current pipeline.
     how: Check whether layer reinitialization has been tried and whether the dataset size justifies it.
     used at: T.5.3
E340  A normalization layer (e.g., BatchNorm) in the prediction head is the likely cause of a score regression and should be removed or replaced.
     how: Check whether adding BatchNorm or similar normalization to the head coincided with a score drop.
     used at: T.5.3
E341  A layer defined in the prediction head is never actually applied to the tensor, making it a no-op bug.
     how: Trace the forward pass to verify every defined layer is actually called on the data.
     used at: T.5.3
E342  An auxiliary output head (e.g., binning/classification head) has been tested and its effect on the score is uncertain or negative.
     how: Compare leaderboard or validation scores with the auxiliary head active (num_bins>1) versus regression-only (num_bins=1).
     used at: T.5.4
E343  A recent code or config change has not yet been scored, so a rerun is needed before drawing conclusions.
     how: Check whether the latest edit has a corresponding completed submission or validation score.
     used at: T.5.4
E344  A recent hyperparameter change was too large a jump and should be reverted before trying another axis.
     how: Review the magnitude of the last hyperparameter change relative to prior values and whether it caused a score regression.
     used at: T.5.4
E345  Recent regularization parameter sweeps indicate the optimum lies at or below the current value.
     how: Examine the score trajectory across recent reg_alpha or reg_lambda values to identify the direction of improvement.
     used at: T.5.4
E346  The custom objective's tunable constants have shown score sensitivity in recent trials and the current values may not be optimal.
     how: Review score changes across recent trials where the objective's scalar parameters (e.g., a, b) were varied.
     used at: T.5.4
E347  Several consecutive hyperparameter sweeps have failed to exceed the best score, suggesting diminishing returns from this lever.
     how: Count the number of recent parameter changes that did not improve the best known score.
     used at: T.5.4
E348  Multiple hyperparameter axes are being changed simultaneously without isolating each effect.
     how: Check whether the last edit changed more than one hyperparameter at a time without intermediate validation.
     used at: T.5.4
E349  The number of boosting iterations or training epochs needs adjustment because ensemble members require fewer iterations than a standalone model.
     how: Compare the optimal iteration count for a single model versus each member in the current ensemble setup.
     used at: T.5.4
E350  The optimizer choice was recently changed and caused a score regression.
     how: Compare the score before and after the optimizer switch in the most recent edit history.
     used at: T.5.4
E351  A recent loss function change has altered gradient dynamics, requiring a proportional learning rate adjustment.
     how: Check whether the loss function was recently changed and whether the new gradient magnitudes justify re-tuning the learning rate.
     used at: T.5.4.1
E352  The current learning rate falls outside the commonly recommended range for the model architecture being fine-tuned.
     how: Compare the current learning rate against published recommended ranges for the specific pretrained model (e.g., BERT: 2e-5 to 5e-5).
     used at: T.5.4.1
E353  The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
     how: Verify that the next change isolates a single variable so its effect can be attributed clearly.
     used at: T.5.4.1
E354  The most recent LR change has not yet been evaluated, so the current sweep direction should continue before reversing.
     how: Check whether the last learning rate trial was scored; if not, continuing the sweep is justified before changing strategy.
     used at: T.5.4.1
E355  Multiple learning rate trials spanning a wide range have been completed, enabling a bracket-and-bisect refinement strategy.
     how: Review the set of LR values already tried and their outcomes to determine if a narrowing search (bisection) is now possible.
     used at: T.5.4.1
E356  A previously tried hyperparameter value is worth revisiting because other model changes (e.g., regularization) have since altered the optimization landscape.
     how: Check whether intervening changes to the model or pipeline justify re-evaluating a previously tested learning rate.
     used at: T.5.4.1
E357  Newly added randomly-initialized parameters require more total gradient steps than the current training duration provides.
     how: Check whether new layers or heads were added to the model and whether the current epoch/step count is sufficient for those parameters to converge.
     used at: T.5.4.1
E358  Previous stronger augmentation experiments (rotation, color jitter, contrast, saturation) degraded or failed to improve scores compared to the mild baseline.
     how: Review experiment logs to see if augmentation additions beyond the minimal baseline caused score drops or no improvement.
     used at: T.5.4.3
E359  Two-sample mixup is already implemented and functional in the current training pipeline.
     how: Inspect the training code to confirm whether mixup is already active and producing valid mixed samples.
     used at: T.5.4.3
E360  NaN values exist in the input data (spectrograms or EEG) that could corrupt mixed or masked samples.
     how: Check input tensors for NaN values before augmentation or mixing steps.
     used at: T.5.4.3
E361  Spectrogram blackout/masking augmentation code was previously scaffolded or introduced but has not yet been scored.
     how: Check version history for commented-out or unscored spectrogram masking code that can be activated and evaluated.
     used at: T.5.4.3
E362  Previous spectrogram masking augmentation attempts have not clearly improved the score, warranting re-runs or parameter iteration.
     how: Review leaderboard scores for versions with spectrogram masking and assess whether results are inconclusive or clearly negative.
     used at: T.5.4.3
E363  MixUp-style augmentation was previously tried and did not sufficiently address overfitting.
     how: Check experiment logs for prior mixup results and whether overfitting persisted afterward.
     used at: T.5.4.3
E364  A recent dropout increase yielded a measurable score improvement, suggesting further fine-grained tuning around the current dropout value is warranted.
     how: Compare leaderboard scores before and after the most recent dropout change to confirm a positive trend.
     used at: T.5.4.3
E365  The current edit removes multi-seed or multi-fold averaging to establish a single-checkpoint baseline before re-adding ensemble members.
     how: Check whether the code change strips averaging to isolate a baseline.
     used at: T.6.1.4
E366  Restricting to a specific sub-checkpoint path has been tested before and showed measurable score changes.
     how: Review submission history for experiments that restricted checkpoint subsets and note whether scores changed.
     used at: T.6.1.4
E367  Adding the next fold/seed checkpoint yielded a gain above the noise threshold established by no-change reruns.
     how: Compare the LB delta from adding the checkpoint against the noise floor from identical reruns.
     used at: T.6.1.4
E368  A specific model family's folds have produced the best score so far, suggesting more folds of that family could further improve the blend.
     how: Check submission history for which model family achieved the top score and whether more folds are available.
     used at: T.6.1.4
E369  Updated or retrained checkpoint variants are available for the same folds and may produce better predictions than the originals.
     how: Check the experiment directory for newer checkpoint versions (e.g., 'pt2') covering the same folds.
     used at: T.6.1.4
E370  A single-fold weighted combination might outperform uniform multi-fold averaging when fold-specific signal strength varies.
     how: Check whether per-fold performance varies enough that weighting or selection could beat uniform averaging.
     used at: T.6.1.4
E371  Adding more fold checkpoints to the average previously improved the score in similar configurations.
     how: Review submission history for monotonic improvement when fold count increased.
     used at: T.6.1.4
E372  LB score variability from no-change reruns is large enough to obscure small ensemble membership differences.
     how: Compare the noise floor from identical reruns against the expected delta from adding/removing a checkpoint.
     used at: T.6.1.4
E373  Runtime budget is insufficient to run all desired ensemble members at current per-sample processing cost.
     how: Estimate total inference time for all candidate checkpoints and compare against the submission time limit.
     used at: T.6.1.4
E374  A smaller model variant achieved the best leaderboard score among tested model sizes, suggesting the averaging dimension should prioritize that variant.
     how: Compare LB scores across model sizes to identify which variant benefits most from fold averaging.
     used at: T.6.1.4
E375  An OOF-based scaler is available or can be constructed to align averaged checkpoint predictions with the target distribution.
     how: Check whether out-of-fold predictions exist that could calibrate the ensemble output.
     used at: T.6.1.4
E376  No single-fold prediction has been submitted to the leaderboard to establish a baseline for measuring the ensemble's contribution.
     how: Check submission history for a single-checkpoint baseline submission.
     used at: T.6.1.4
E377  No per-fold validation diagnostics are available to guide which folds to include or remove.
     how: Check whether per-fold OOF or validation metrics exist for the candidate checkpoints.
     used at: T.6.1.4
E378  Full-data (non-fold) model checkpoints exist alongside fold-specific checkpoints and have not yet been evaluated.
     how: Check the experiment directory for full-data trained checkpoints distinct from fold-specific ones.
     used at: T.6.1.4
E379  A complementary fold-weight subset may recover performance lost by a previous fold-weight experiment.
     how: Check whether the inverse of a previously tested fold-weight mask has been tried.
     used at: T.6.1.4
E380  The two strongest individual checkpoints have not yet been tested together as a pair.
     how: Identify the top-performing individual checkpoints and check whether their combination has been submitted.
     used at: T.6.1.4
E381  The multi-member ensemble scored below the best single checkpoint, indicating weaker members add noise.
     how: Compare the ensemble LB score against the best single-checkpoint LB score.
     used at: T.6.1.4
E382  The score has not yet dropped when increasing the repeat/fold count, so the stopping criterion (revert on first drop) has not been triggered.
     how: Review the sequence of scores as repeat count increased and check for any regression.
     used at: T.6.1.4
E383  Diminishing or negative returns were observed when repeat count exceeded a moderate threshold in earlier experiments.
     how: Review historical repeat-count sweep results for the inflection point where gains stopped or reversed.
     used at: T.6.1.4
E384  Cross-model diversity already reduces variance, so fewer per-model repeats may suffice compared to a single-model configuration.
     how: Check whether the ensemble includes multiple model architectures and whether per-model repeat count can be reduced.
     used at: T.6.1.4
E385  The previous combination rule has not been scored on the leaderboard, so there is no feedback on whether it is correct.
     how: Check submission history for whether the current blend configuration has received a public LB score.
     used at: T.6.2
E386  New or improved base-model predictions are available that were not used when the current meta-learner was trained.
     how: Compare the set of base-model outputs used to train the current stacker against newly available prediction files.
     used at: T.6.2
E387  The stacking layer's contribution is confounded with other simultaneous changes (e.g., checkpoint swaps), making it hard to attribute score differences.
     how: Check whether the stacker change was the only variable altered between the two compared submissions.
     used at: T.6.2
E388  A simpler combination rule (e.g., weighted blend or simple average) already performs near the best observed score, so a more complex combiner may not be justified.
     how: Compare the best score achieved by simple blending against the best score from learned stacking.
     used at: T.6.2
E389  A specific combination strategy (e.g., per-fold blending, hierarchical grouping) has not yet been tried.
     how: Review the list of combination strategies attempted so far and identify untried alternatives.
     used at: T.6.2
E390  Manual weight tuning has been tried extensively without consistent improvement, motivating a switch to a learned combination rule.
     how: Review history of manual weight adjustments and whether they yielded stable gains.
     used at: T.6.2
E391  An alternative meta-learner type (e.g., kernel ridge, random forest, SVR) is available as a fitted artifact but has not been tried in the current pipeline.
     how: Check which meta-learner types have saved model files and which have actually been evaluated.
     used at: T.6.2
E392  The public leaderboard evaluation set is too small for reliable comparison of combination rules.
     how: Check the number of evaluation rows on the public LB relative to the variance of the metric.
     used at: T.6.2
E393  The current combination weights were calibrated for a different set of members and are stale after adding or removing prediction sources.
     how: Check whether the member set has changed since the current weights were last tuned.
     used at: T.6.2
E394  The meta-learner's key hyperparameters were set without tuning evidence and may not be optimal.
     how: Check whether the current meta-learner hyperparameters were chosen via systematic search or set manually.
     used at: T.6.2
E395  Backward elimination of base-model columns improves the meta-learner's OOF score, suggesting some inputs are redundant or harmful.
     how: Run leave-one-out or backward elimination on the stacker's input columns and check if OOF score improves.
     used at: T.6.2
E396  L1 (Lasso) vs L2 (Ridge) regularization in the meta-learner trades off sparsity (dropping weak members) against retaining all members for diversity.
     how: Compare the number of base models against the risk of dropping useful correlated predictions under L1.
     used at: T.6.2
E397  Mixed-precision or numerical-format changes at inference time have a known or suspected effect on output fidelity.
     how: Check whether AMP/autocast or other precision settings were toggled and whether their score impact has been measured.
     used at: T.7
E398  Stochastic noise introduced during inference (e.g., random augmentations, dropout left on) is degrading a rank-based or deterministic metric.
     how: Compare deterministic vs. stochastic inference pipelines and check whether the metric is invariant to added noise.
     used at: T.7
E399  An additive or multiplicative offset is applied to predictions whose provenance or isolated effect has not been verified.
     how: Trace the origin of the offset and run an ablation with it removed to measure its standalone contribution.
     used at: T.7
E400  The threshold or calibration optimization is computed on a validation set whose label distribution does not match the expected test distribution.
     how: Compare label distributions between the validation set used for threshold tuning and the target test set.
     used at: T.7
E401  A recently introduced auxiliary-signal weight has not been swept or optimized.
     how: Check whether the weight for the new signal was set heuristically and whether a grid search has been run.
     used at: T.7
E402  Per-column post-processing or discretization steps have been added or removed without a clear ablation showing their individual contribution.
     how: Review the history of per-column transforms and compare scores with and without each one.
     used at: T.7
E403  The degenerate-column detection guard has a logic bug or is too strict/lenient, causing incorrect overwrites or missed near-constant columns.
     how: Inspect the guard condition for edge cases (e.g., near-constant columns, binning collapse) and test with synthetic degenerate inputs.
     used at: T.7
E404  Separate prediction columns (e.g., event indicator and time-to-event) are available and could be combined or post-processed jointly.
     how: Check whether the pipeline produces multiple output columns and whether the metric expects a joint or composite prediction.
     used at: T.7
E405  The marginal gain of each TTA variant has not been measured in isolation against a no-TTA baseline.
     how: Check whether a clean no-TTA baseline submission exists so the isolated effect of each TTA pass can be quantified.
     used at: T.7.1
E406  Stochastic augmentation TTA has been shown to regress performance compared to deterministic TTA in prior experiments.
     how: Review experiment history for score regressions when switching from deterministic to stochastic TTA.
     used at: T.7.1
E407  Different input resolutions produce sufficiently diverse predictions to benefit from averaging.
     how: Compare prediction variance across resolution variants to confirm they contribute complementary information.
     used at: T.7.1
E408  The seed strategy for stochastic TTA passes produces meaningfully diverse outputs rather than near-duplicate predictions.
     how: Check whether different seed spacings or seed values yield measurably different stochastic outputs.
     used at: T.7.1
E409  The inference code actually performs multiple forward passes and averages them when dropout-based stochastic TTA is enabled.
     how: Verify that the inference loop runs multiple passes and aggregates results rather than running a single noisy pass.
     used at: T.7.1
E410  Previous experiments changing the same TTA parameter produced no score change, suggesting this change will also have no effect.
     how: Review prior experiment logs for identical or near-identical parameter changes and their measured outcomes.
     used at: T.7.1
E411  A prior attempt to increase the number of inference passes was tried but never submitted, so its effect remains unknown.
     how: Check experiment history for untested pass-count changes that lack validation scores.
     used at: T.7.1
E412  TTA effect is inconsistent across checkpoint versions or ensemble compositions, so its benefit must be re-validated when the model changes.
     how: Compare TTA on/off scores across different checkpoint or ensemble versions to see if the effect is stable.
     used at: T.7.1
E413  TTA is currently disabled (or enabled) in the latest submission, so toggling it is a direct A/B test.
     how: Check the TTA flag state in the most recent submission to confirm the toggle direction.
     used at: T.7.1
E414  Raw prediction entropy or variance should be inspected before deciding whether stochastic averaging can reduce uncertainty.
     how: Examine per-sample prediction entropy or softmax variance from single-pass inference.
     used at: T.7.1
E415  An entropy-based or uncertainty-based TTA variant did not improve over the deterministic baseline in a recent experiment.
     how: Check the score of the entropy/uncertainty TTA run against the deterministic baseline.
     used at: T.7.1
E416  The additional inference passes fit within the submission time limit.
     how: Estimate total inference time with the proposed number of TTA passes and compare to the allowed time budget.
     used at: T.7.1
E417  The TTA implementation averages logits before softmax rather than averaging softmax probabilities (or vice versa).
     how: Inspect the TTA code to determine whether aggregation happens in logit space or probability space.
     used at: T.7.1
E418  Previous flip TTA attempts produced inconsistent results (sometimes helping, sometimes hurting) across different configurations.
     how: Review experiment history for flip TTA score deltas under varying preprocessing or ensemble setups.
     used at: T.7.1
E419  Concatenating original and augmented inputs in the batch dimension is more efficient than separate forward passes for TTA.
     how: Check whether the TTA implementation batches augmented views together or runs them as separate forward passes.
     used at: T.7.1
E420  The TTA code correctly accumulates and averages predictions from all intended views or passes.
     how: Inspect the inference loop to verify that all TTA outputs are properly aggregated (not just the last one).
     used at: T.7.1
E421  Multi-view TTA (e.g., left/center/right crops) produced no measurable improvement over single-view inference.
     how: Compare the most recent multi-view TTA submission score against the single-view baseline.
     used at: T.7.1
E422  The TTA toggle is confounded with other simultaneous code changes, preventing a clean A/B comparison.
     how: Review the diff to check whether the TTA change is the only modification or if unrelated changes are bundled.
     used at: T.7.1
E423  The per-class multipliers were tuned on a different checkpoint version than the one currently in use.
     how: Check whether the calibration parameters (e.g., per-class multipliers) were derived from the same model checkpoint that is currently being used for inference.
     used at: T.7.3
E424  Recent submissions show that per-class multipliers worsened the score, suggesting they should be disabled.
     how: Compare leaderboard scores of recent submissions with and without per-class multipliers to determine if they are currently helping or hurting.
     used at: T.7.3
E425  The logit scaling is applied inside the model's forward pass during training, altering gradient flow and training dynamics rather than only adjusting inference-time outputs.
     how: Inspect whether the calibration transformation is applied at inference time only or also during training, which would change its effect from post-hoc calibration to a training-time modification.
     used at: T.7.3
E426  The test set size is small enough that applying bias corrections estimated from training data risks overfitting to training distribution statistics.
     how: Compare the number of test examples to the degrees of freedom introduced by the correction; assess whether the correction's variance exceeds its bias-reduction benefit.
     used at: T.7.4
E427  The proposed correction's effect is confounded with other pipeline issues (e.g., bookkeeping bugs), so an isolated A/B test is needed before attributing improvement to the correction itself.
     how: Check whether the correction was tested in isolation or whether its measured effect could be explained by co-occurring pipeline changes or bugs.
     used at: T.7.4
E428  The correction magnitude or weight is a first guess that has not been systematically swept or validated.
     how: Check whether the chosen correction magnitude was selected via a systematic search (e.g., CV sweep) or is an unvalidated initial estimate.
     used at: T.7.4
E429  The detection method used to flag cases for correction may miss relevant instances that appear in alternative fields or signals.
     how: Check whether the metadata or content field used for detection covers all locations where the relevant signal can appear.
     used at: T.7.4
E430  The evaluation metric is relatively insensitive to the exact correction magnitude, indicating diminishing returns from further fine-tuning.
     how: Examine whether a sweep of correction values shows a flat or near-flat metric response, suggesting the exact value matters little.
     used at: T.7.4
E431  The base model outputs have changed since the correction weight was last optimized, so previously suboptimal correction values may now be optimal.
     how: Check whether the underlying model predictions have been updated since the correction parameters were last tuned, invalidating prior parameter choices.
     used at: T.7.4
E432  The correction method preserves the relative ordering of non-flagged samples rather than distorting their ranks.
     how: Verify that the correction (e.g., rank manipulation or additive offset) does not inadvertently change the relative ordering of samples that were not targeted for correction.
     used at: T.7.4
E433  A variable deletion or comment-out removes a definition still referenced downstream, causing a runtime error.
     how: Trace variable definitions and deletions; check whether any deleted/commented variable is used later in the pipeline.
     used at: T.8
E434  Dead code, redundant assignments, or unused imports have accumulated, creating maintenance overhead and risk of stale-reference errors.
     how: Scan for duplicate assignments, unreachable branches, and unused imports that could mask bugs or slow debugging.
     used at: T.8
E435  A recent configuration change broke execution, and the pipeline has not yet been verified to run end-to-end successfully.
     how: Check whether the last submission or run failed, indicating the current pipeline state is broken.
     used at: T.8
E436  Debug-mode or stress-test data is too small to exercise the pipeline realistically, so bottlenecks or failures only surface in full runs.
     how: Compare debug data size and diversity against production data to see if the test is representative.
     used at: T.8
E437  Model is in eval mode, so batch normalization uses fixed running stats, making predictions independent of batch size.
     how: Check whether the model is set to eval mode and whether any layers (e.g., batch norm) would cause batch-size-dependent behavior.
     used at: T.8.1
E438  The object being deleted is still referenced downstream in the pipeline, causing a runtime error.
     how: Trace variable references after each `del` statement to confirm the deleted object is not used later.
     used at: T.8.1
E439  Reducing the number of inference replicas (e.g., seeds) is an acceptable trade-off to fit within memory while still producing a valid submission.
     how: Evaluate whether fewer seeds/replicas still yield acceptable prediction quality and fit within resource limits.
     used at: T.8.1
E440  Repeated inference passes (e.g., hack_count) multiply effective memory usage, requiring a smaller per-pass batch size.
     how: Check whether the pipeline runs multiple inference passes that accumulate memory, and whether per-pass batch size must be reduced accordingly.
     used at: T.8.1
E441  The replacement model has a smaller memory footprint than the model it replaces, allowing a larger batch size.
     how: Compare the parameter count and activation memory of the new model versus the old model.
     used at: T.8.1
E442  The edit changes multiple variables simultaneously (e.g., precision and blend weights), confounding the effect of the resource reduction.
     how: Check whether the proposed change modifies only the resource-reduction parameter or also alters other pipeline settings.
     used at: T.8.1
E443  GPU usage is contributing to memory pressure or compatibility issues that could be avoided by forcing CPU inference.
     how: Determine whether GPU memory is the bottleneck and whether switching to CPU would resolve the issue within time limits.
     used at: T.8.1
E444  A duplicated code block loads the model or computes outputs twice, wasting memory.
     how: Inspect the pipeline for redundant model loading or duplicate computation blocks that could be consolidated.
     used at: T.8.1
E445  The runtime error at a specific batch size is not purely OOM but a batch-size-dependent shape or computation issue.
     how: Check error messages to distinguish between OOM errors and shape/computation errors that depend on batch size.
     used at: T.8.1
E446  The pipeline contains training-only code paths (fold splitting, augmentations, OOF evaluation) that never execute during inference and can be safely removed.
     how: Inspect the codebase for training-specific logic that is dead code during inference and verify removal does not affect test predictions.
     used at: T.8.2
E447  A reduced or single-fold test run revealed a latent bug (e.g., indexing error) that would crash or produce wrong results in the full pipeline.
     how: Run a quick single-fold or subset execution and check for crashes or incorrect outputs that indicate hidden bugs.
     used at: T.8.2
E448  Pre-trained model artifacts, cached predictions, or checkpoints from prior runs exist and are ready to be loaded, avoiding retraining or recomputation.
     how: Check whether saved model weights, logits, or intermediate predictions from previous sessions are available and loadable.
     used at: T.8.2
E449  The pipeline does not persist intermediate artifacts (e.g., logits) as reusable outputs, requiring redundant re-execution to obtain them.
     how: Check whether key intermediate results are written to disk in a reusable format or must be regenerated each time.
     used at: T.8.2
E450  The caching or deduplication change is bundled with other unrelated changes, making it impossible to attribute any score difference to the specific optimization.
     how: Check whether the iteration-reduction change is isolated in its own commit/version or confounded with other modifications.
     used at: T.8.2
E451  The test set size can be detected at runtime to skip unnecessary computation on trivially small public test sets while still running fully on the private test set.
     how: Check whether the public test set is known to be very small and whether an early-exit based on row count is safe for the private submission.
     used at: T.8.2
E452  Memory is not freed between heavy pipeline stages, causing accumulation that could crash or slow subsequent stages.
     how: Profile memory usage across stages and check whether large objects (models, tensors, dataframes) are explicitly deleted or garbage-collected between stages.
     used at: T.8.2
E453  The pipeline lacks a debug/test mode with independent stage gates, forcing all stages to run even when only one is being tested or debugged.
     how: Check whether individual pipeline stages can be selectively enabled/disabled via flags without code changes.
     used at: T.8.2