import json,re,collections
from pathlib import Path
P=Path(__file__).parent
rows=[]
with (P.parent/'episode_items.jsonl').open() as source:
 for line in source:
  e=json.loads(line)
  for k,item in enumerate(e['items'],1):
   rows.append(dict(idx=len(rows),id=f"{e['ep_id']}#{k}",**item))
# Compact taxonomy specification: keys are internal authoring labels, not output IDs.
branches=[]; leaves={}; decisions={}
def branch(key,name,question,desc):
 n=dict(key=key,name=name,decision=question,description=desc,children=[],source='data');branches.append(n);return n
def choice(parent,key,name,question,desc,opts):
 n=dict(key=key,name=name,decision=question,description=desc,children=[],source='data');parent['children'].append(n);decisions[key]=n
 for k,title,description in opts:
  l=dict(key=k,name=title,description=description,source='data',children=[],items=[]);n['children'].append(l);leaves[k]=l
 return n
b=branch('evidence','Improve the evidence for choosing changes','Which uncertainty should I resolve before another performance change?','Choose the next measurement or comparison when existing scores cannot reliably guide improvement.')
choice(b,'split','Choose a validation design','Which split design should I test for this data?', 'Select the split constraint that best represents the intended unseen examples.',[
 ('stratify','Preserve target proportions','Use stratified folds, binning a continuous target when needed, to stabilize target distributions.'),
 ('group','Hold related examples together','Use entity, source, topic, or defensible inferred groups to keep related examples out of opposing folds.'),
 ('subgroup_split','Probe subgroup allocation','Compare subgroup allocation schemes with a separate disjoint evaluation set; overlapping train and validation rows in the source trajectories do not provide an unbiased score.'),
 ('holdout','Change holdout allocation','Compare holdout fractions or cross-validation against full-data fitting while preserving an independent selection signal.')])
choice(b,'measure','Choose a trustworthy comparison','Which measurement would resolve the uncertainty in the apparent gain?', 'Distinguish score noise, misleading validation, confounded edits, and incorrect metric computation.',[
 ('repeat','Measure repeat-run variability','Repeat an unchanged configuration with pinned artifacts and compare score distributions rather than single best runs.'),
 ('local','Check local and external score agreement','Compare local validation with earlier external evaluations and use local selection when leaderboard resolution or sample size is inadequate.'),
 ('isolate','Isolate one change','Compare configurations differing in one meaningful factor, or use a small factorial comparison for an interaction.'),
 ('metric','Align the evaluation callback','Implement and verify the task metric and its optimization direction in validation and early stopping.'),
 ('eda','Inspect data structure','Inspect entity counts, ordering, feature types, missingness, and target distributions before selecting a representation.')])
choice(b,'recovery','Choose a response to an unsuccessful search','Should I restore, narrow, or redirect the current experiment?', 'Use the size and attribution of regressions to choose the next experiment.',[
 ('restore','Restore the proven configuration','Recover the exact known-good configuration before reintroducing changes separately.'),
 ('pivot','Move to a different improvement lever','Stop a saturated local sweep and test a qualitatively different source of signal or modeling change.'),
 ('bracket','Narrow the parameter search','Bracket a promising continuous parameter range and refine it with controlled local comparisons.'),
 ('baseline','Establish a working baseline','Build and evaluate a minimal end-to-end solution before adding further complexity.')])
b=branch('repair','Repair incorrect or mismatched predictions','Which failure mechanism should I investigate first?','Choose a correctness repair when predictions, scores, or execution contradict the intended pipeline.')
choice(b,'compat','Restore model and input compatibility','Which training-to-inference contract is broken?', 'Match artifacts and transformations to the configuration that produced the learned weights.',[
 ('load_weights','Match architecture and weights','Reconstruct the trained architecture and inspect strict checkpoint loading, tensor dimensions, and missing or prefixed state keys.'),
 ('preprocess_match','Match input preprocessing','Restore the training-time resolution, filtering, normalization, feature extraction, and input format at inference.'),
 ('token_match','Match tokenizer and vocabulary','Use the training tokenizer, special-token definitions, vocabulary size, and token-index logic with the checkpoint.'),
 ('feature_match','Match feature schema and encoders','Reuse fitted encoders and the exact feature names, ordering, and dimensions expected by the downstream model.')])
choice(b,'flow','Locate a data-flow defect','Where should I check for lost or corrupted signal?', 'Trace data and predictions through the stage most consistent with the observed failure.',[
 ('align','Restore row and identifier alignment','Join auxiliary features and prediction files by explicit identifiers and reverse any sorting before output.'),
 ('coverage','Restore missing model contributions','Verify every intended fold, branch, and model executes and contributes the intended prediction array.'),
 ('arithmetic','Correct aggregation arithmetic','Check numeric array types, axes, divisors, group normalization, weights, and shapes in ensemble calculations.'),
 ('signal','Trace inputs and prediction signal','Inspect small examples, stage outputs, variance, and data sources to locate placeholders, constant predictions, or wrong inputs.'),
 ('finite','Repair invalid numerical values','Check inputs and intermediate tensors for NaNs or infinities and apply model-appropriate handling.'),
 ('objective_bug','Correct the custom objective implementation','Audit custom-loss gradients, Hessians, shapes, and callback inputs before attributing a score collapse to modeling.')])
choice(b,'runtime','Resolve the first execution failure','What dependency failure prevents the intended computation?', 'Repair the concrete failing contract before running a full experiment.',[
 ('paths','Resolve artifact paths','List available artifacts and fix checkpoint, configuration, and preprocessing paths before loading.'),
 ('dependencies','Resolve package compatibility','Correct imports, offline dependencies, versions, and module search paths to load the intended implementation.'),
 ('device','Match computation devices','Align model and tensor devices or use a supported CPU backend before re-enabling acceleration.'),
 ('api','Repair syntax or API contracts','Use a minimal failing example to correct variable scope, parameter names, dataframe semantics, or function signatures.'),
 ('output','Write the intended submission','Validate output columns, row count, final prediction variable, filename, and file-writing execution.')])
b=branch('inputs','Change the information presented to the model','Which input representation should I change next?','Choose a concrete feature or preprocessing experiment based on missing signal or excess noise.')
choice(b,'tabular','Represent repeated or structured records','Which structured feature construction should I test?', 'Choose a representation that captures the kind of information missing from the current features.',[
 ('aggregate','Add entity-level summary statistics','Aggregate repeated records with controlled additions of location, spread, extrema, counts, or last values.'),
 ('lag','Add temporal changes or recent windows','Compute lags, first-to-last changes, or recent-window statistics to represent temporal dynamics.'),
 ('interaction','Add domain interactions','Construct semantically justified differences, ratios, products, or composite features and test their marginal value.'),
 ('numeric','Change numeric precision or scaling','Compare rounding, precision, or scaling choices without changing the underlying observations.'),
 ('missing','Change missing-value handling','Compare native missing-value support with explicit model-appropriate imputation.'),
 ('metadata','Add structured metadata','Encode relevant source, category, time, or other available metadata as features.')])
choice(b,'text','Represent text for the model','Which text representation should I test next?', 'Select the representation whose information is absent or poorly captured in the current pipeline.',[
 ('text_clean','Change text normalization','Compare minimal tokenizer-compatible processing with domain-specific cleaning, cropping, or spelling normalization.'),
 ('prompt','Change text input structure','Test metadata prompts, paired inputs, separate text streams, or explicit formatting with matching training support.'),
 ('sparse','Tune sparse n-gram features','Compare word and character n-grams, frequency cutoffs, and vocabulary ranges.'),
 ('linguistic','Add linguistic or structural statistics','Extract text counts, readability, syntax, sentiment, or section and sentence summaries as candidate features.'),
 ('embedding','Add pretrained dense representations','Extract pooled pretrained embeddings or low-dimensional semantic representations and validate their added signal.'),
 ('retrieval','Add similarity or auxiliary-task features','Use training-neighbor labels or predictions from related-data models as carefully aligned auxiliary features.')])
choice(b,'signal_input','Represent images and signals','Which spatial or signal representation should I test?', 'Choose a representation change that addresses lost detail, unwanted variation, or missing channels.',[
 ('resolution','Sweep input resolution','Compare nearby input resolutions with compatible checkpoints while holding other model settings fixed.'),
 ('spectral','Change time-frequency resolution','Compare spectral transforms, window sizes, hop lengths, or frequency bands using compatible training and inference.'),
 ('crop','Change the observed window','Test spatial crops or temporal context windows against the label scope and training configuration.'),
 ('filter','Change signal filtering or clipping','Compare justified filtering, noise suppression, clipping, or sampling settings and validate their consistency with training.'),
 ('normalize','Change input normalization','Compare channel or instance normalization and dynamic-range transforms using training-supported settings.'),
 ('reshape','Change channel layout or rendering','Test added channels, pseudo-image shapes, or color representations while preserving sample and channel identity.')])
choice(b,'selection','Control the feature set','Which feature-set reduction or refresh should I perform?', 'Choose how to remove noise or repair stale selection without silently excluding new useful features.',[
 ('ablate_features','Ablate a feature family','Remove or restore one candidate feature group and measure its incremental contribution.'),
 ('importance','Estimate feature relevance','Aggregate importance estimates across folds or compare importance methods before choosing a subset.'),
 ('cutoff','Tune the retained feature count','Sweep feature-selection thresholds or count limits against held-out performance.'),
 ('refresh','Recompute feature selection','Regenerate and version the selected feature list whenever the candidate feature space changes.'),
 ('compact','Reduce dense representation dimensions','Prune embedding sources or dimensions when expanded dense features introduce noise or exceed resources.')])
b=branch('data','Change training examples or targets','Which data or target intervention should I test?','Choose a change to supervision or sample exposure based on noise, imbalance, censoring, or distribution shift.')
choice(b,'population','Choose training examples','Which change to the training population is justified?', 'Compare data additions, removals, and reweighting according to their likely relevance to unseen examples.',[
 ('filter_data','Filter or deduplicate training data','Test removing noisy, redundant, overlapping, or distribution-mismatched samples against an unchanged validation set.'),
 ('external','Add labeled auxiliary data','Integrate relevant external labeled examples and compare joint versus staged use.'),
 ('pseudo','Use pseudo-labeled examples','Evaluate models trained with unlabeled-data pseudo-labels against supervised counterparts.'),
 ('resample','Reweight or resample subpopulations','Change class or source exposure through appropriate sample weights or resampling.'),
 ('synthetic','Interpolate training examples','Test synthetic within-class neighbors or mixup-style feature interpolation and ablate it if harmful.')])
choice(b,'target','Choose a target formulation','Which supervision representation should I test?', 'Select a target formulation that reflects censoring, ordering, or group-specific evaluation.',[
 ('survival','Transform censored outcomes','Compare regression-friendly survival probabilities, hazards, or rank-based targets with consistent risk direction.'),
 ('group_target','Construct targets within evaluation groups','Estimate target transforms separately within the groups used by the evaluation criterion.'),
 ('target_scale','Tune target centering or transformation strength','Sweep target offsets, nonlinear strength parameters, or centering conventions while preserving inverse transforms.'),
 ('ordinal','Use ordinal or classification supervision','Compare regression with ordinal cumulative outputs or multiclass supervision for discrete ordered labels.')])
choice(b,'augment','Choose training augmentation','Which augmentation should I test against the unaugmented baseline?', 'Choose perturbations consistent with label invariances and observed overfitting.',[
 ('image_aug','Use mild image perturbations','Compare controlled brightness, contrast, or geometric augmentation strengths and remove harmful additions.'),
 ('mask_aug','Mask signal regions','Test random time-frequency masking to reduce reliance on particular signal regions.'),
 ('mixup','Mix labeled examples','Compare standard and multi-example mixup with label mixing appropriate to the task.')])
b=branch('fit','Change the learned model','Which model-fitting change is the most plausible next intervention?','Choose an architecture, objective, or optimization experiment based on observed fit limitations.')
choice(b,'family','Choose a model family or initialization','Which replacement model should I test as a standalone candidate?', 'Compare alternatives while preserving data, validation, and inference correctness.',[
 ('backbone','Change pretrained backbone or capacity','Compare backbone families or sizes with their matching tokenizer, head dimensions, and trained checkpoints.'),
 ('domain_pretrain','Use domain-adapted pretraining','Test pretrained weights adapted to the task domain against a general-pretraining baseline.'),
 ('tree_family','Change tree learner or boosting variant','Compare tree libraries, standard versus dropout boosting, or equivalent model implementations on the same features.'),
 ('modality_model','Fit a model for a different representation','Build a standalone model suited to raw signals, spectral inputs, fixed embeddings, or another complementary representation.')])
choice(b,'architecture','Change the prediction architecture','Which architectural component should I alter?', 'Target the representational bottleneck while retaining compatibility between learned weights and inference code.',[
 ('head','Change head capacity or attention','Compare shared versus separate heads, hidden layers, and attention blocks on a fixed backbone.'),
 ('pool','Change pooling or representation normalization','Compare sequence or hidden-layer pooling and normalization before the prediction layer.'),
 ('aux_head','Add auxiliary supervision','Train a parallel classification or summary head and compare its effect on the main prediction.'),
 ('fusion','Change feature-level modality fusion','Compare separate input branches, concatenation, and averaging using a correspondingly trained prediction head.'),
 ('dropout','Change training-time dropout','Tune head dropout or multisample dropout to control variance during fitting.')])
choice(b,'tree_fit','Tune a tree learner','Which tree-fitting constraint should I adjust?', 'Choose the parameter family indicated by underfitting, overfitting, or incomplete optimization.',[
 ('capacity','Tune tree depth and leaves','Sweep depth and leaf limits to balance representational capacity and generalization.'),
 ('tree_reg','Tune penalties and subsampling','Compare leaf penalties and row or column sampling while fixing other capacity settings.'),
 ('boost_budget','Coordinate boosting rate and rounds','Adjust learning rate together with sufficient boosting rounds and verify convergence.'),
 ('early','Change stopping patience or criterion','Compare stopping patience, monitored validation sets, and fixed-round training using observed learning curves.'),
 ('defaults','Reset uncertain tree parameters','Compare an extensively hand-tuned configuration with a controlled library-default baseline.')])
choice(b,'neural_fit','Tune neural optimization or loss','Which training change should I test?', 'Use convergence and objective mismatch to choose an optimization intervention.',[
 ('learning','Tune learning rate','Bracket the fine-tuning learning rate while checking convergence and instability.'),
 ('schedule','Change optimizer or learning-rate schedule','Compare optimizer or decay schedule choices under a matched training budget.'),
 ('epochs','Change training duration or stages','Compare epoch budgets, staged fine-tuning, or batch size using held-out learning behavior.'),
 ('loss','Change the training objective','Compare metric-aligned losses or custom objective shapes against the standard objective.'),
 ('train_structure','Make component training cross-validated','Train and persist a component on consistent folds with valid held-out predictions and data loaders.')])
b=branch('pool_models','Change the prediction pool','How should I change which trained predictors contribute?','Choose a candidate addition, replacement, reduction, or repetition before tuning the blend.')
choice(b,'diversity','Choose the source of ensemble diversity','What kind of additional predictor should I test?', 'Add one source whose errors may complement the current pool and verify its marginal contribution.',[
 ('diverse','Add a different model family','Add predictions from a distinct architecture or algorithm family and test them alongside the intact baseline.'),
 ('representation_diverse','Add an alternative input representation','Add a model trained with a different modality, preprocessing, feature set, or input window.'),
 ('target_diverse','Add an alternative supervision recipe','Add models trained with different target transformations or complementary training recipes.'),
 ('folds','Average more fold or snapshot predictions','Compare incremental fold or checkpoint averaging with the current single or smaller predictor pool.'),
 ('seeds','Average independently seeded models','Train or load independent seed checkpoints and measure the marginal value of additional runs.'),
 ('swa','Average checkpoint weights','Test stochastic weight averaging of compatible checkpoints before inference.')])
choice(b,'members','Choose ensemble membership','Which membership experiment should I run next?', 'Use standalone and marginal evidence to decide whether to add, remove, replace, or restore predictors.',[
 ('candidate','Measure a candidate in isolation','Evaluate a candidate alone with its correct inference pipeline before interpreting its blend contribution.'),
 ('add_member','Test one additional member','Add a candidate to the unchanged baseline and retain it only if its marginal contribution is supported.'),
 ('prune','Remove a harmful or redundant member','Perform controlled leave-one-out or subset ablations and retain the smaller pool when it improves held-out performance.'),
 ('replace_member','Replace one fixed ensemble slot','Swap one component checkpoint or model while holding other members and blend settings fixed.'),
 ('restore_members','Restore complementary members','Reassemble previously beneficial predictors after an isolation test or excessive pruning.'),
 ('retest_members','Retest membership after upstream changes','Re-evaluate prior inclusions and exclusions when other components or aggregation rules change.')])
choice(b,'checkpoint','Select a trained artifact','Which checkpoint comparison should I perform?', 'Choose checkpoint candidates according to available training runs, stages, and validation evidence.',[
 ('checkpoint_sweep','Compare trained runs or folds','Evaluate candidate checkpoint artifacts one at a time under a fixed compatible inference pipeline.'),
 ('checkpoint_stage','Compare training stages or stopping rules','Compare final, best-validation, clean-subset, or multi-stage snapshots rather than assuming the latest is best.'),
 ('checkpoint_regime','Compare full-data and fold-trained weights','Compare full-data, fold-only, and mixed checkpoint pools using independent evaluation.')])
b=branch('outputs','Change prediction combination or output mapping','Which operation on valid predictions should I change?','Choose a blend or post-processing intervention that matches the task metric and prediction semantics.')
choice(b,'combine','Choose a combination rule','Which rule should I compare against the current aggregation?', 'Select an aggregation trial based on score scales, calibration, and available out-of-fold training data.',[
 ('rank','Compare rank and raw-score averaging','Test per-model rank normalization against raw averaging under the current ranking metric and model configuration.'),
 ('probability','Compare probability and logit aggregation','Compare averaging normalized probabilities with averaging logits followed by the required output activation.'),
 ('hierarchy','Group before averaging','Average homogeneous folds or model families first, then combine groups to control their effective contribution.'),
 ('stack','Fit a regularized prediction stacker','Train a simple meta-learner on aligned out-of-fold predictions and compare it against direct averaging.'),
 ('stack_type','Change the meta-learner','Compare linear, kernel, Bayesian, or tree meta-learners with controlled regularization and held-out evaluation.'),
 ('power','Try a nonlinear probability blend','Compare a power transform or power mean with arithmetic averaging on unchanged component predictions.')])
choice(b,'weights_rule','Choose how to weight predictors','Which weighting strategy should I use as the next comparison?', 'Choose weight constraints and search scope according to evidence about component quality and validation stability.',[
 ('weights','Tune nonuniform blend weights','Optimize or sweep relative weights on fixed aligned predictions and compare with equal weighting.'),
 ('uniform','Use a uniform-weight baseline','Restore or establish equal weights when quality differences or tuned-weight gains are not reliable.'),
 ('negative','Allow signed blend coefficients','Test negative coefficients when correlated errors may benefit from subtraction and the output semantics permit it.'),
 ('adaptive','Compare conditional and global weights','Test per-class or sample-dependent weighting against a fixed global blend.'),
 ('reweight','Retune after component changes','Re-optimize weights after changing model quality, member count, normalization, or augmentation.'),
 ('scale_blend','Normalize component scales','Compare raw, standardized, or robustly scaled component predictions before fitting blend weights.')])
choice(b,'stack_inputs','Choose meta-model inputs','Which stacking feature change should I test?', 'Choose an input modification while preserving the out-of-fold training and test schema.',[
 ('oof','Generate valid out-of-fold meta-features','Build aligned held-out base predictions with shared fold indices before fitting a downstream learner.'),
 ('stack_expand','Add auxiliary stacking features','Test extra base outputs, embeddings, or auxiliary head predictions and retrain the meta-learner on the expanded schema.'),
 ('stack_prune','Select a smaller meta-feature set','Compare curated subsets of base predictions or auxiliary features against the full stack.')])
choice(b,'discretize','Map continuous scores to discrete labels','Which discretization rule should I compare?', 'Choose a mapping compatible with the target levels, metric, and calibration sample.',[
 ('threshold','Optimize ordinal cutpoints','Fit ordered cutpoints on held-out predictions, retuning them after model changes.'),
 ('round','Use simple clip-and-round','Compare simple rounding and clipping against learned cutpoints to detect calibration overfitting.'),
 ('quantile','Match empirical target frequencies','Compare quantile or distribution-based label mapping with per-example thresholding.'),
 ('bin','Merge or threshold near-equal scores','Test per-target binning or thresholding for quasi-discrete labels with explicit tie handling.'),
 ('group_cut','Compare group-specific cutpoints','Use observable or independently predicted subgroups to compare separate calibration with a global mapping.'),
 ('degenerate','Handle degenerate bins and ties','Check constant output columns and tie behavior, restoring continuous outputs where binning destroys useful order.')])
choice(b,'calibrate','Correct output semantics or bias','Which output correction should I test or repair?', 'Distinguish invalid output conventions from residual bias in otherwise valid predictions.',[
 ('link','Restore prediction units and activation','Apply the correct inverse target scaling, sigmoid, softmax, label offset, or probability normalization.'),
 ('direction','Align risk-score direction','Check whether larger scores mean greater risk and reverse inconsistent component signs before blending.'),
 ('temperature','Rescale probabilities or logits','Compare temperature or per-class scaling with unmodified probabilities and renormalize as required.'),
 ('offset','Correct systematic prediction bias','Test a held-out mean shift, reference-example correction, or small additive offset.'),
 ('rule','Apply auxiliary or metadata corrections','Test confidence-gated classifier or high-precision metadata corrections on the relevant output subset.'),
 ('post_ablate','Ablate an existing output transform','Toggle the current post-processing step without changing the model to verify it still helps.')])
choice(b,'tta','Choose inference-time averaging','Which repeated-view inference strategy should I test?', 'Select only transformations compatible with the task and evaluate their incremental contribution.',[
 ('geometric_tta','Average deterministic symmetry views','Compare original predictions with fixed flips or domain-specific channel symmetries.'),
 ('crop_tta','Average windows or resolutions','Average predictions across valid temporal crops or spatial resolutions.'),
 ('stochastic_tta','Compare stochastic forward-pass averaging','Test random transformations or active-dropout averaging against deterministic inference.'),
 ('deterministic','Disable unintended stochastic inference','Use evaluation mode and controlled randomness, checking whether repeated passes actually differ.')])
b=branch('execution','Make useful experiments feasible','Which execution change removes the current bottleneck?','Choose a resource or engineering intervention that enables valid evaluation or full-strength inference.')
choice(b,'memory','Control peak resource use','Which resource intervention fits the observed bottleneck?', 'Use measured memory or throughput behavior to choose a concrete implementation change.',[
 ('chunk','Stream complete entities or prediction batches','Partition large data by safe boundaries and concatenate validated predictions without loading everything at once.'),
 ('release','Release sequential model state','Free models and intermediate arrays after their last use before loading the next component.'),
 ('downcast','Reduce stored feature precision','Downcast intermediate feature matrices where their ranges and precision permit it.'),
 ('batch','Tune inference batch size','Reduce batches to resolve memory failures or increase them for throughput while checking output invariance.'),
 ('precision','Compare inference precision','Test half or mixed precision against full precision with unchanged model and inputs.'),
 ('accelerate','Optimize expensive computation','Replace bottleneck operations with verified vectorized, compiled, or suitable backend implementations.')])
choice(b,'iteration','Shorten experiment turnaround','What can I reduce or reuse without invalidating the experiment?', 'Choose between cheaper trial execution and reusing unchanged computation.',[
 ('debug','Run a reduced end-to-end smoke test','Use a small data slice, fold count, or training budget to verify correctness before a full run.'),
 ('cache','Cache expensive reusable artifacts','Persist features, embeddings, predictions, or fitted preprocessing so downstream trials reuse unchanged work.'),
 ('resume','Resume only unfinished training','Save fold or stage artifacts and run only missing work across sessions.'),
 ('production','Restore full production execution','Verify debug guards, fold limits, and training shortcuts are disabled when generating the final evaluated prediction.')])
choice(b,'structure','Make pipeline changes reproducible','Which code-organization change addresses the observed fragility?', 'Choose an explicit reproducibility intervention and verify it preserves intended outputs.',[
 ('modular','Parameterize and separate model pipelines','Use explicit configurations and reusable or model-specific inference components to prevent integration drift.'),
 ('refactor','Verify a cleanup or inference-only refactor','Remove obsolete code incrementally and compare predictions with a saved reference.'),
 ('pin','Pin configurations and artifacts','Record exact settings, checkpoint manifests, seeds, and selected weights to reproduce a result.'),
 ('fallback','Make missing-component behavior explicit','Detect missing prediction artifacts and validate any fallback or reduced ensemble rather than silently emitting placeholders.')])
# Explicit item placement is maintained separately for auditability.
assign={}
def put(key,s):
 for part in s.split():
  if '-' in part:
   a,z=map(int,part.split('-')); ids=range(a,z+1)
  else: ids=[int(part)]
  for i in ids:
   if i in assign: raise ValueError(('duplicate assignment',i,assign[i],key))
   assign[i]=key
# Items 0–196: grouped tabular modeling and initial image experiments.
put('rank','0 3 8 10 12 14 16 18 20')
put('resolution','1 4 15 17')
put('head','2 9 11 13')
put('restore','5 7 89 174 176 190')
put('isolate','6 32 54 76 82 86 92 95 97 143 151 169 196')
put('domain_pretrain','19')
put('weights','21 24 109 144 177')
put('negative','22')
put('metric','23 47 49 58 104 107 127 145 152 153 159 172 188')
put('pivot','25 30 33 64 65 91')
put('api','26 68 80 84 99 111 160 168 194')
put('holdout','27 29 161')
put('capacity','28 31 56 79 142 179 184')
put('repeat','34 55 149')
put('debug','35 39 41 59 66 74 101 118 141 155 156 191 193')
put('link','36 100')
put('chunk','37 102 116 128 163')
put('resample','38 103 183 195')
put('cutoff','40 44 46 48 132 187')
put('tree_reg','42 43 50 57')
put('bracket','45')
put('boost_budget','51 53 93 113 140 146')
put('ablate_features','52 62 75 77 119 121 126 133 137 175 186')
put('loss','60')
put('tree_family','61 94 96 131 180 192')
put('early','63 120 148')
put('aggregate','67 69 110 150 170 185')
put('metadata','70')
put('missing','71 167 173')
put('lag','72 81 85 87')
put('numeric','73 105 171')
put('interaction','78 83 90 134')
put('accelerate','88')
put('stack','98 106 108')
put('defaults','112 114')
put('importance','115 166 189')
put('folds','117 129 135 139 181')
put('local','122 147')
put('downcast','123')
put('baseline','124 158 165 178')
put('modular','125')
put('seeds','130 136')
put('cache','138')
put('eda','154')
put('refactor','157 162')
put('signal','164')
put('group','182')
# Items 197–423: text ensembles, pooling, and checkpoint experiments.
put('weights','197 214 215 225 228 234 254 259 264 268 298 300 304 309 327 345 346 349 351 354 357 370 375 377 381 391 422')
put('local','198 202 253 255 277')
put('crop','199')
put('pivot','200 222 247 287 319 363')
put('checkpoint_sweep','201 359 366 408 415')
put('folds','203 216 237 239 310 360 405 419')
put('replace_member','204 207 224 263 288 294 307 374')
put('candidate','205 227 242 243 258 275 348 350 365 367 368 369 399 407')
put('uniform','206 290 313 317')
put('stack','208 210 211 213 217 230 232 246 261 385')
put('hierarchy','209 226 241 273 318')
put('repeat','212 305')
put('stack_expand','218 248 252 322 326 332 388')
put('target_diverse','219 221')
put('arithmetic','220 235 240 244 251 295 330 331 334 355')
put('modular','223 387')
put('release','229 231 233 269 383')
put('diverse','236 280 281 286 289 292 364 382 398')
put('add_member','238 279 293 297 303 312 314 316 329 372 384')
put('prune','249 278 284 296 306 333 339 356 390')
put('add_member','250 325 338')
put('rule','256')
put('api','257 267 271 315 353')
put('restore_members','260 272 344 352 371')
put('restore','262 285')
put('isolate','265 291 343 406 410 414 417 420')
put('retrieval','266')
put('stack_type','270 320 323 389')
put('weights','274')
put('pool','276 386 392 396 418')
put('refactor','282 340')
put('swa','283')
put('offset','299 416')
put('weights','301')
# Architecture-checkpoint repair rather than blend weights for this homonymous label.
assign[301]='load_weights'
put('weights','302')
assign[302]='load_weights'
put('pin','308')
put('token_match','311')
put('cache','321 335')
put('feature_match','324')
put('align','328')
put('stratify','336')
put('debug','337')
put('backbone','342')
put('weights','341')
assign[341]='load_weights'
put('coverage','347')
put('dropout','358')
put('stochastic_tta','361 376 409')
put('adaptive','362')
put('deterministic','373 378 380')
put('seeds','379 393 401 412')
put('signal','394 400')
put('stack_prune','395')
put('text_clean','397')
put('precision','402')
put('weights','403')
assign[403]='load_weights'
put('retest_members','404')
put('aux_head','411 421')
put('prompt','413')
put('rank','423')
# Items 424–628: survival modeling and heterogeneous stacking.
put('modular','424 430 440')
put('train_structure','425 470 517 620 621')
put('group_target','426 455')
put('weights','427 436 501 504 505 552 567')
put('isolate','428 439 448 528 561 577 578 623')
put('restore','429 449 461 493 502 539 614')
put('temperature','431 458')
put('reweight','432 497 530')
put('schedule','433 460')
put('stack_expand','434 600 616')
put('filter_data','435 462')
put('replace_member','437 464 553 603 625')
put('pivot','438 478 508 509 554 557 568')
put('refactor','441 520 602')
put('feature_match','442 452 456 522 534 559')
put('signal','443 480 485 592')
put('direction','444 537 549 551')
put('deterministic','445 513')
put('seeds','446 447 453 454 459 463')
put('target_scale','450 457')
put('diverse','451 468 481 486 487 525 541 545 558 560 564 581 585 593 606')
put('restore_members','465 533 613')
put('negative','466 610')
put('target_diverse','467 484 494 514 526 542 574 588 611')
put('cache','469 628')
put('scale_blend','471 472 475')
put('bracket','473')
put('pin','474')
put('checkpoint_regime','476')
put('tree_family','477 479')
put('output','482')
put('weights','483 488 489')
put('survival','490 524 573')
put('rule','491 495 503 506 550 556 571')
put('post_ablate','492')
put('boost_budget','496 583 587')
put('ablate_features','498 535')
put('folds','499 584')
put('device','500 569')
put('arithmetic','507 579 607')
put('stack_prune','510 516 618')
put('repeat','511')
put('representation_diverse','512 594 619')
put('release','515 601')
put('oof','518 591')
put('accelerate','519 622')
put('add_member','521 527 536 543 562 575 576 596 624')
put('baseline','523 566 582')
put('coverage','529 544 547')
put('candidate','531 532')
put('rank','538 540 570 572 595 605')
put('loss','546')
put('missing','548')
put('retest_members','555')
put('objective_bug','563')
put('finite','565')
put('prune','580')
put('numeric','589')
put('feature_match','590')
put('stack_type','597 599 604 612 615 617 626 627')
put('stack','598 609')
put('epochs','608')
# Items 629–799: output mapping, text tuning, early signal ensembles.
put('batch','629 696')
put('signal','630 675 718 720 722 723')
put('feature_match','631 632')
put('restore','633 635 703 729 772 797')
put('isolate','634 637 654 658 662 664 701 742 746 757 777 788')
put('threshold','636 639')
put('post_ablate','638 663 680 682 733')
put('weights','640 706 734 771 775 776')
put('output','641')
put('paths','642 646 650 689 730 743 748')
put('checkpoint_sweep','643 645 651 655 714 745 795')
put('rank','644 647 649 659')
put('prune','648 677 709 768 790 792')
put('text_clean','652 656 657 702')
put('backbone','653 799')
put('bin','660 665 710 739 740 741')
put('degenerate','661 667 673 731')
put('folds','666 688 700 713 721 747 763')
put('debug','668 669')
put('cache','670')
put('api','671 691 705 755')
put('fallback','672 676 678')
put('production','674')
put('quantile','679 719 725')
put('diverse','681 767 780')
put('prompt','683')
put('epochs','684 708')
put('dropout','685 762')
put('resume','686 690')
put('ablate_features','687 778')
put('pivot','692 759')
put('retrieval','693 697')
put('modular','694 764 779')
put('uniform','695 711')
put('release','698')
put('holdout','699')
put('align','704')
put('linguistic','707')
put('representation_diverse','712')
put('link','715 717 754')
put('baseline','716 766')
put('checkpoint_stage','726')
put('offset','727')
put('aux_head','728')
put('checkpoint_sweep','732')
put('rule','735 736 737 738')
put('debug','744')
put('learning','749 751 756 758 760 761')
put('token_match','750')
put('metadata','752')
put('pool','753')
put('seeds','765')
put('probability','769')
put('cache','770')
put('dependencies','773')
put('target_diverse','774')
put('fusion','781 785 798')
put('crop_tta','782')
put('repeat','783')
put('refactor','784 789 794')
put('signal','786 787')
put('add_member','791')
put('crop_tta','793')
put('candidate','796')
# Items 800–1095: noisy checkpoint comparisons and signal pipelines.
put('prune','800 806 807 808 814 816 827 861 862 863 867 869 870 942 943 945 952 953 955 1029 1063')
put('weights','801 815 888 928 936 1028 1031 1062 1070 1071 1073 1074 1075 1083 1084 1090 1091')
put('link','802 1042')
put('production','803')
put('repeat','804 811 820 821 823 829 834 839 840 843 849 850 851 853 854 855 856 857 859 864 871 872 875 882 885 1025')
put('folds','805 818 822 826 833 841 847 848 858 868 876 879 886 887 964 1022')
put('deterministic','809 865')
put('restore_members','810 832 954')
put('preprocess_match','812 825 891 903 926 1038 1044 1046 1057 1087')
put('ablate_features','813 993 996 1003 1005')
put('candidate','817 835 852 880 881 922 923 927 937 941 958 1026 1033 1034 1036 1048 1052 1056 1066 1067 1069 1078 1079 1082')
put('retest_members','819 956')
put('spectral','824 965 1000 1009')
put('stochastic_tta','828 838')
put('isolate','830 836 837 895 918 969 970 974 976 981 989 1018 1040 1051 1061 1065')
put('pin','831 842 845 878 1081')
put('pivot','844 902 909 972 982 1011 1085')
put('probability','846')
put('diverse','860 920 921 924 932 1030 1047 1050 1055 1058 1059')
put('baseline','866 983')
put('refactor','873 910 911 938 944 995 1076')
put('precision','874')
put('batch','877')
put('checkpoint_sweep','883 889 892 898 913 915 949 985 1015 1020 1060')
put('add_member','884')
put('backbone','890 899 906 917 919 968 1024')
put('geometric_tta','893 1049 1053')
put('temperature','894 896 897')
put('normalize','900 967 1089')
put('restore','901 934 963 977 978 984 998 1072')
put('modality_model','904 1039 1086')
put('load_weights','905 907 908 1064')
put('representation_diverse','912 925 940 946 957')
put('adaptive','914')
put('preprocess_match','916')
put('coverage','929 933 935 939 947 1027 1088')
put('crop','930')
put('reweight','931 1094')
put('pseudo','948 1032 1035')
put('signal','950 951 973 1019')
put('fusion','959 992 1017')
put('filter','960 975')
put('reshape','961 966 971 1054')
put('api','962 1077')
put('mixup','979')
put('loss','980')
put('filter_data','986 988 991 1001 1002 1093')
put('resume','987')
put('checkpoint_stage','990 1012 1016 1041 1043')
put('pool','994')
put('debug','997')
put('group','999')
put('head','1004')
put('accelerate','1006')
put('external','1007 1008 1013 1014')
put('mask_aug','1010')
put('paths','1021')
put('replace_member','1023 1092 1095')
put('modular','1037')
put('retrieval','1045')
put('baseline','1068')
put('local','1080')
# Items 1096–1327: ordinal text tasks and high-dimensional feature pipelines.
put('prompt','1096 1179 1190')
put('debug','1097 1105 1144 1146 1157 1216 1288 1318 1326')
put('prune','1098 1100 1136')
put('isolate','1099 1101 1113 1119 1122 1128 1194 1200 1224 1227 1234 1239 1241 1246 1258 1260 1269 1279 1289 1296 1297')
put('folds','1102 1114 1139 1153 1155 1162 1302 1303')
put('modular','1103 1107 1116 1166 1193 1197 1198 1210 1281')
put('device','1104 1185')
put('load_weights','1106 1127 1145 1177 1180 1181 1192')
put('threshold','1108 1109 1115 1118 1124 1129 1130 1142 1167 1187 1196 1212 1231 1253 1254 1264 1293')
put('arithmetic','1110 1126 1389')
put('token_match','1111 1120 1121 1172')
put('backbone','1112 1123 1133 1134 1141 1189')
put('refactor','1117 1158 1159 1184')
put('ordinal','1125 1160 1168')
put('checkpoint_sweep','1131 1147 1164 1174')
put('seeds','1132')
put('checkpoint_stage','1135 1170 1182')
put('domain_pretrain','1137')
put('weights','1138 1156 1304 1309')
put('pivot','1140 1149 1183 1236 1240 1298 1312 1323')
put('quantile','1143')
put('group_cut','1148 1150')
put('align','1151')
put('batch','1152')
put('restore_members','1154')
put('link','1161')
put('candidate','1163')
put('api','1165 1206 1213 1267')
put('preprocess_match','1169 1175')
put('precision','1171')
put('restore','1173 1176 1188 1226 1228 1271 1274 1315')
put('checkpoint_regime','1178')
put('offset','1186')
put('feature_match','1191 1287 1300')
put('text_clean','1195')
put('add_member','1199')
put('prune','1201')
put('stratify','1202')
put('cutoff','1203 1218 1229 1242 1252 1286 1295')
put('linguistic','1204 1217 1219 1221 1244 1249 1311')
put('output','1205')
put('tree_family','1207 1275 1319')
put('metric','1208 1327')
put('oof','1209 1223 1266 1273')
put('cache','1211 1232 1276 1325')
put('embedding','1214 1251 1285 1316 1317 1320 1324')
put('sparse','1215 1250')
put('repeat','1220')
put('refresh','1222 1235 1262 1282')
put('synthetic','1225 1299 1301')
put('loss','1230 1291 1292 1308')
put('diverse','1233')
put('capacity','1237 1283 1322')
put('bracket','1238')
put('refactor','1243')
put('ablate_features','1245 1257 1261 1277 1313')
put('objective_bug','1247')
put('round','1248 1306')
put('subgroup_split','1255 1256 1259 1284 1314')
put('importance','1263')
put('resample','1265 1268')
put('pin','1270')
put('filter_data','1272')
put('release','1278 1280')
put('compact','1290')
put('group','1294')
put('production','1305')
put('metadata','1307')
put('target_scale','1310')
put('dependencies','1321')
# Items 1328–1500: feature selection, engineering, and image inference.
put('modular','1328 1331 1343 1465')
put('importance','1329 1332')
put('ablate_features','1330 1334 1369 1377 1399 1404 1414')
put('capacity','1333 1419 1422 1452')
put('candidate','1335 1388 1390 1411 1498')
put('folds','1336 1380 1429 1446 1450 1462 1474 1485')
put('oof','1337 1416 1417')
put('refresh','1338 1364')
put('signal','1339 1351 1353 1361 1463')
put('isolate','1340 1342 1362 1365 1381 1400 1412 1415 1418 1447 1453 1479')
put('tree_reg','1341 1358 1372 1430 1445')
put('early','1344 1359')
put('cache','1345 1402 1427 1442')
put('paths','1346 1356 1408 1471')
put('feature_match','1347 1386')
put('align','1348 1350 1439')
put('debug','1349 1394 1396 1398 1421 1481')
put('stack_prune','1352')
put('resample','1354 1355')
put('post_ablate','1357')
put('text_clean','1360')
put('round','1363')
put('weights','1366 1420 1423 1434 1443 1448 1475 1488')
put('restore','1367 1440')
put('embedding','1368 1370 1374 1378 1383 1384')
put('release','1371 1373 1482 1486')
put('device','1375 1433')
put('linguistic','1376 1392 1425')
put('api','1379 1405 1428 1455 1483')
put('retrieval','1382 1395 1413')
put('compact','1385 1391 1397')
put('boost_budget','1387')
put('downcast','1393')
put('offset','1401')
put('group','1403 1407 1410')
put('stratify','1406')
put('sparse','1409')
put('pivot','1424 1431 1435 1457 1493 1496')
put('debug','1426')
put('diverse','1432')
put('signal','1436')
put('prune','1437')
put('reweight','1438 1492')
put('replace_member','1441 1444')
put('bracket','1449')
put('output','1451')
put('refactor','1454')
put('local','1456 1459 1467')
put('head','1458')
put('preprocess_match','1460')
put('normalize','1461')
put('load_weights','1464')
put('checkpoint_sweep','1466 1494')
put('backbone','1468')
put('resolution','1469')
put('geometric_tta','1470 1472 1477 1490 1491')
put('batch','1473')
put('uniform','1476')
put('stochastic_tta','1478')
put('crop_tta','1480')
put('power','1484 1489')
put('rank','1487 1500')
put('restore_members','1495')
put('debug','1497')
put('dependencies','1499')
# Items 1501–1673: image/signal refinements and final ensemble experiments.
put('candidate','1501 1529 1576 1610 1615 1621 1670')
put('weights','1502 1503 1504 1609 1626 1629 1652 1661 1663 1672 1673')
put('diverse','1505 1593 1658 1666')
put('dependencies','1506 1508')
put('power','1507')
put('load_weights','1509 1527 1533 1537 1540 1594 1601')
put('deterministic','1510 1521')
put('link','1511 1516')
put('signal','1512 1530 1577 1669')
put('resolution','1513 1524 1525 1526 1532 1539 1542 1544')
put('batch','1514 1592 1618 1668')
put('normalize','1515 1520 1665')
put('isolate','1517 1519 1549 1563 1570 1581 1583 1598 1605 1606 1612 1619 1624 1628 1630 1631 1638 1640 1643 1645 1648 1650 1651 1657')
put('folds','1518 1554')
put('preprocess_match','1522 1584 1604 1613 1662 1664')
put('checkpoint_sweep','1523 1557')
put('output','1528')
put('repeat','1531 1534 1536 1538 1541 1543 1545 1548 1572 1580 1588 1596 1600 1627 1632 1634 1654')
put('dropout','1535')
put('refactor','1546 1555')
put('image_aug','1547 1551')
put('pivot','1550')
put('loss','1552')
put('learning','1553')
put('geometric_tta','1556 1568 1587 1589 1591 1599')
put('representation_diverse','1558 1565 1566 1571 1575 1656 1660')
put('coverage','1559')
put('add_member','1560 1646 1647')
put('pin','1561')
put('spectral','1562 1585 1586 1590')
put('probability','1564')
put('prune','1567 1582 1597 1620 1644')
put('crop','1569 1595 1603 1608 1614 1637')
put('cache','1573')
put('filter','1574 1611 1649 1655 1667')
put('backbone','1578 1625 1653')
put('restore_members','1579 1607 1659')
put('retest_members','1602')
put('fusion','1616 1633 1636 1639')
put('uniform','1617')
put('reshape','1622 1623 1671')
put('replace_member','1635 1641 1642')
put('restore_members','245')
put('interaction','586')
put('candidate','724')
# Targeted semantic review corrections.
assign[80]='pin'
assign[153]='api'
assign[267]='dependencies'
assign[461]='restore'
assign[649]='rank'
assign[759]='pivot'
assign[1040]='baseline'
assign[1361]='debug'
# Preserve the minority bundled-change strategy as a distinct experimental choice.
node=dict(key='bundle',name='Test a coordinated bundle',description='Compare a jointly changed configuration with a saved baseline when the changes are coupled, then ablate the bundle before attributing its gain.',source='data',children=[],items=[])
decisions['recovery']['children'].append(node);leaves['bundle']=node
for i in [461,582,1040,1598]: assign[i]='bundle'
assign[563]='coverage'
assign[1305]='debug'
assign[1389]='coverage'
# Report authoring gaps before materializing the final artifacts.
missing=set(range(len(rows)))-assign.keys()
if missing:
 for i in sorted(missing): print('UNPLACED',i,rows[i]['general']['goal'])
 raise SystemExit('Complete explicit placements first')
for i,k in assign.items():
 if k not in leaves: raise ValueError(('unknown leaf',i,k))
 leaves[k]['items'].append(rows[i]['id'])
for k,l in leaves.items():
 if not l['items']: print('EMPTY',k)

# Checks describe observations available before selecting the next child action.
checks={}
def C(key,statement,how,**pushes):
 checks.setdefault(key,[]).append(dict(check=statement,how=how,pushes=pushes))
C('root','The current predictions fail a schema, signal, or compatibility check.','Inspect the latest traceback, sample predictions, output dimensions, and artifact loading logs.',repair=1,outputs=-.7,pool_models=-.6)
C('root','The claimed gain is no larger than variation in prior unchanged runs.','Compare recent score deltas with the range or standard deviation of repeated runs using identical artifacts.',evidence=1,fit=-.4,outputs=-.4)
C('root','Errors concentrate where the existing input representation loses available information.','Inspect residuals by history length, text section, image detail, or signal window and compare with the raw inputs.',inputs=.9)
C('root','A known noisy or shifted subgroup dominates the training errors.','Break down held-out errors and label distributions by data source, label confidence, or entity subgroup.',data=.9)
C('root','Learning curves show underfitting, overfitting, or unstable optimization despite correct inputs.','Compare training and held-out loss curves with the model capacity, loss, and optimizer configuration.',fit=.9)
C('root','Available candidate predictors make complementary held-out errors.','Align existing out-of-fold predictions and inspect residual correlations and candidate blend scores.',pool_models=.9,outputs=.5)
C('root','Valid cached predictions exist and output mapping or blending is not yet compared on held-out data.','Inspect prediction artifacts and the experiment log for missing aggregation or calibration baselines.',outputs=.9)
C('root','Resource failures prevent the intended full pipeline or meaningful trials from completing.','Locate out-of-memory errors, time-limit exits, and stages dominating the runtime profile.',execution=1)
# Top-level routing decisions.
C('evidence','Related records, source shifts, or unstable target proportions undermine the present split.','Inspect fold assignments against entity IDs, data sources, timestamps, and per-fold label histograms.',split=.9)
C('evidence','Recent comparisons are confounded, noisy, or use a questionable metric.','Read the edit diffs, repeat-run scores, metric implementation, and validation-to-external score pairs.',measure=1)
C('evidence','Several recent trials failed to beat a reproducible baseline.','Compare the trial ledger with the last saved best configuration, including the size and consistency of regressions.',recovery=.9)
C('repair','A new artifact or representation was introduced immediately before the failure.','Compare the last working artifact manifest, model definition, and preprocessing configuration with the failing run.',compat=1)
C('repair','Execution completes but outputs are constant, implausible, or omit configured components.','Inspect intermediate prediction statistics and execution counts for each fold and model.',flow=1,runtime=-.4)
C('repair','A traceback or absent output file identifies an execution dependency failure.','Read the first exception and confirm whether the required final file exists.',runtime=1)
C('inputs','Examples contain repeated structured observations that the current features collapse inadequately.','Compare raw entity histories with the columns supplied to the model.',tabular=.9)
C('inputs','Free text is the principal input and residuals vary with language or document structure.','Inspect representative errors alongside text lengths, sections, vocabulary coverage, and existing feature families.',text=.9)
C('inputs','Image or signal preprocessing discards potentially label-relevant detail.','Compare raw examples and rendered model inputs with the task label scope and preprocessing parameters.',signal_input=.9)
C('inputs','An expanded or stale feature set is associated with worse validation or schema drift.','Compare feature manifests and held-out scores before and after feature additions.',selection=1)
C('data','Sample quality, class proportions, or source coverage differ from the intended test population.','Inspect label confidence, duplicate IDs, source frequencies, and task-described test sampling.',population=.9)
C('data','The label definition includes censoring, ordinal levels, or group-specific ranking.','Read the target columns and evaluation formula and inspect the current constructed targets.',target=1)
C('data','A neural model overfits and the input admits label-preserving perturbations.','Compare train/validation curves and inspect whether candidate transformations preserve the annotated event or image finding.',augment=.9)
C('fit','A correctly implemented backbone or learner has plateaued across local tuning.','Review controlled trials on the current family and available compatible pretrained or alternative learner candidates.',family=.8)
C('fit','A minimal head or fusion rule discards useful backbone or branch information.','Inspect model forward code and branch dimensions and compare errors with representation ablations.',architecture=.9)
C('fit','The active learner is a tree model with capacity or convergence problems.','Read the learner configuration and tree training/validation curves.',tree_fit=1,neural_fit=-.7)
C('fit','The active component is neural and its optimization or loss is suspect.','Inspect neural training curves, gradient stability, epochs, scheduler, and objective definition.',neural_fit=1,tree_fit=-.7)
C('pool_models','Existing members mostly share the same architecture, features, targets, or training randomness.','Compare the member manifest and out-of-fold residual correlations.',diversity=.9)
C('pool_models','There are untested, weak, or recently changed members in the current pool.','Review individual scores, marginal ablations, and member changes since the last weight search.',members=.9)
C('pool_models','Several compatible saved runs or training-stage artifacts are available.','List checkpoint metadata and their held-out metrics without loading them into the final blend.',checkpoint=.9)
C('outputs','Prediction scales or the aggregation domain differ across members.','Inspect raw score ranges, probability sums, activations, and the current blending expression.',combine=.9)
C('outputs','The same valid prediction pool has only an arbitrary weight allocation.','Compare current weights with component quality and previous equal-weight or optimized-blend results.',weights_rule=.9)
C('outputs','A downstream learner uses base predictions or embeddings as input features.','Inspect the meta-feature manifest and whether valid out-of-fold training inputs exist.',stack_inputs=.9)
C('outputs','The task requires discrete ordered outputs or labels occupy a few repeated levels.','Inspect the target value histogram and official output and metric specification.',discretize=1)
C('outputs','Prediction units, probability calibration, or subgroup residual bias need correction.','Compare output ranges and per-class or per-group residual plots with the task target definition.',calibrate=.9)
C('outputs','The input has valid alternate views that the current inference uses only once.','Inspect training transformations and domain symmetries or available context windows.',tta=.8)
C('execution','Peak memory or per-batch throughput is the limiting resource.','Inspect allocation failures and stage-level memory and runtime logs.',memory=1)
C('execution','Repeated trials recompute unchanged work or fail late after expensive training.','Profile the trial cycle and identify reusable artifacts or the smallest execution that reproduces the issue.',iteration=.9)
C('execution','Hard-coded paths, duplicated model code, or unrecorded settings cause configuration drift.','Compare code paths and artifact manifests across recently inconsistent runs.',structure=.9)
# Evidence and validation.
C('split','Target classes or target bins are unevenly distributed across the current folds.','Count labels or fixed target bins per fold and compare their frequencies.',stratify=.9)
C('split','Multiple rows share an entity, source, or topic that should be unseen at evaluation.','Check identifiers and the task test-population definition, then count group overlap between train and validation.',group=1,stratify=-.4)
C('split','A recognizable source subgroup differs from the evaluation population.','Compare source-specific label and feature distributions with known test metadata.',subgroup_split=.8)
C('split','The proposed subgroup allocation places the same row in training and validation.','Intersect train and validation row IDs for every fold, including injected subgroup rows.',subgroup_split=-1,group=.8)
C('split','A large fixed holdout substantially reduces fitting data after model choices are settled.','Inspect training versus holdout counts and whether the holdout still controls early stopping or selection.',holdout=.9)
C('measure','Unchanged runs vary by as much as the proposed improvement.','Inspect repeated scores and prediction differences with fixed input and checkpoint hashes.',repeat=1)
C('measure','The public evaluation is tiny or disagrees with local model rankings.','Use task-provided evaluation sizes and earlier paired local/external scores to assess resolution and ranking agreement.',local=1)
C('measure','The compared versions changed multiple independent settings.','Read version diffs for changes to checkpoints, features, seeds, and output transforms.',isolate=1)
C('measure','Early stopping monitors a proxy, wrong dataset, or wrong metric direction.','Inspect callback arguments and recompute the task metric on saved validation labels and predictions.',metric=1)
C('measure','The prediction unit or ordering of raw observations is not yet established.','Inspect table keys, sample histories, timestamps, missingness summaries, and target joins.',eda=1)
C('recovery','A reproducible regression followed a change and the prior working configuration is available.','Compare the regression with repeat-run variability and inspect the saved baseline manifest.',restore=1,bundle=-.6)
C('recovery','Several trials along the same lever show no reliable improvement.','Read the trial ledger and compare best recent deltas with measured noise.',pivot=1,bracket=-.6)
C('recovery','Nearby tested parameter values bracket an improving region.','Plot existing parameter-score pairs with noise estimates and identify a local interval worth refining.',bracket=.9,pivot=-.4)
C('recovery','No complete pipeline has produced a valid measured prediction.','Check execution logs and output artifacts for an end-to-end baseline.',baseline=1)
C('recovery','The candidate changes are coupled and a saved baseline permits later ablation.','Identify dependencies such as rate with training duration, or a new modality with its required model, and verify the baseline artifacts.',bundle=.6)
# Correctness repairs.
C('compat','Checkpoint keys or tensor dimensions disagree with the reconstructed model.','Use strict loading diagnostics and compare hidden sizes, head shapes, and state-dict prefixes.',load_weights=1)
C('compat','Inference transforms differ from those recorded for the training checkpoint.','Diff resizing, filters, normalization, cropping, and feature-extraction configurations.',preprocess_match=1)
C('compat','Vocabulary, special tokens, or token positions differ from training.','Compare tokenizer files, vocabulary length, special-token IDs, and any token-position extraction code.',token_match=1)
C('compat','A downstream model receives different columns, encodings, or dimensions from those used in fitting.','Compare ordered feature manifests, fitted encoder metadata, and the current matrix shape.',feature_match=1)
C('flow','Data or predictions were sorted, concatenated, or joined without an explicit identifier mapping.','Compare ID sequences across every input frame and prediction vector.',align=1)
C('flow','Configured model or fold counts exceed the number of accumulated predictions.','Inspect loop counters, skip flags, accumulation indentation, and the final component manifest.',coverage=1)
C('flow','The blend magnitude or shape changes unexpectedly with member count.','Evaluate the arithmetic on a tiny known numeric array and inspect axes, divisors, and weight totals.',arithmetic=1)
C('flow','Model or stage outputs are constant, placeholders, or derived from the wrong dataset.','Inspect prediction variance, first examples, data IDs, and references passed between stages.',signal=1)
C('flow','Inputs, losses, or intermediate activations contain nonfinite values.','Count NaNs and infinities at each boundary and identify the earliest occurrence.',finite=1)
C('flow','A custom objective edit preceded divergence or a catastrophic score loss.','Compare analytical gradients and Hessians with numerical derivatives on a tiny sample and inspect return shapes.',objective_bug=1)
C('runtime','The error is a missing file or a read-only source path.','List mounted files, resolve the configured path, and inspect the failing file operation.',paths=1)
C('runtime','The failure is an import, missing symbol, or incompatible package version.','Inspect the import traceback, module file locations, and bundled package versions.',dependencies=1)
C('runtime','The error names an unsupported accelerator or mismatched tensor devices.','Inspect model and tensor device fields and installed backend support.',device=1)
C('runtime','The first failure names an undefined variable, invalid keyword, type, or method.','Reduce the failing call to a small example and compare it with the local function signature and object types.',api=1)
C('runtime','The computation completes but the expected prediction file is absent or invalid.','Inspect output directory, writer execution, filename, columns, IDs, row count, and final prediction variable.',output=1)
# Input representations and feature selection.
C('tabular','There are multiple observations per entity but the model sees only a latest row or a narrow summary.','Compare entity record counts with the current aggregation feature list.',aggregate=.9)
C('tabular','Recent changes or temporal order are not represented by full-history summaries.','Inspect sorted histories and held-out errors for entities with changing trajectories.',lag=.9)
C('tabular','Related measurements have interpretable differences, ratios, or interactions absent from the feature set.','Read column definitions and inspect candidate interaction distributions for valid denominators and plausible units.',interaction=.8)
C('tabular','Stored precision, scaling, or noisy decimals are unsuitable for the learner.','Inspect dtypes, unique-value counts, quantization, and the learner preprocessing requirements.',numeric=.8)
C('tabular','Aggregations create missing values or model families differ in native NaN support.','Count missing values after aggregation and inspect the configured learner input requirements.',missing=1)
C('tabular','Available metadata has plausible target signal and is absent from the model.','Compare held-out residuals by available source, category, or time fields and confirm those fields exist at inference.',metadata=.8)
C('text','Cleaning may remove meaningful punctuation, spelling, or pretrained-tokenizer cues.','Compare raw and normalized examples and inspect the checkpoint training preprocessing.',text_clean=.9)
C('text','Distinct text segments or known metadata are currently flattened without structure.','Inspect input construction and tokenized examples against the task fields.',prompt=.9)
C('text','The sparse representation omits common n-grams or has a large rare-token tail.','Inspect vocabulary coverage, document frequencies, n-gram ranges, and matrix sparsity.',sparse=.9)
C('text','Text quality or document organization is relevant but absent from current features.','Inspect target definitions and errors by readability, sentence length, sections, or linguistic patterns.',linguistic=.8)
C('text','Current features capture counts but lack semantic information.','Inspect existing feature families and available pretrained encoders, including embedding dimensions and memory requirements.',embedding=.9)
C('text','Labeled neighbors or related-task labeled data are available without using evaluation labels.','Inspect available training corpora, nearest-neighbor quality on held-out examples, and auxiliary-data provenance.',retrieval=.8)
C('signal_input','Resizing removes label-relevant detail and compatible resolution checkpoints exist.','Inspect raw and resized samples plus checkpoint input-shape metadata.',resolution=.9)
C('signal_input','Time-frequency detail is unresolved at the current transform settings.','Inspect spectrograms alongside sampling rate, FFT window, hop length, and event duration.',spectral=.9)
C('signal_input','The current crop misses the labeled interval or includes mostly irrelevant context.','Compare crop boundaries and window duration with annotations and training extraction code.',crop=.9)
C('signal_input','Raw signals contain known interference, extreme amplitudes, or irrelevant frequency content.','Inspect signal traces, amplitude quantiles, power spectra, and filter settings.',filter=.9)
C('signal_input','Input scale or channel statistics differ from the pretrained model expectations.','Compare input mean, spread, and dynamic range with the checkpoint preprocessing record.',normalize=.9)
C('signal_input','Channel layout or pseudo-image shape obscures available signal structure.','Inspect tensor dimensions and rendered samples for channel identity, aspect ratio, and useful additional derived channels.',reshape=.8)
C('selection','A newly added feature family coincided with worse held-out performance.','Compare the feature manifest and controlled validation scores before and after the addition.',ablate_features=1)
C('selection','No stable relevance ranking exists for the current wide feature space.','Inspect fold-level importance artifacts and their stability across folds or attribution methods.',importance=.9)
C('selection','A ranking exists but its retention threshold is arbitrary or stale.','Read selected counts, cap settings, and previous feature-count validation sweeps.',cutoff=1)
C('selection','Features were added or renamed after the saved selection file was generated.','Compare feature-generation versions and names with the saved selection manifest.',refresh=1,cutoff=-.3)
C('selection','Expanded embeddings raise dimensionality sharply and validation has not improved.','Compare embedding dimensions, source count, resource usage, and held-out scores before and after expansion.',compact=.9)
# Data and supervision.
C('population','Duplicates, overlapping windows, unreliable labels, or mismatched sources are identifiable.','Inspect entity/window overlap, label confidence, source metadata, and out-of-fold residual outliers.',filter_data=.9)
C('population','Additional labeled data with compatible input and label definitions exists.','Compare auxiliary-source label semantics, coverage, quality, and distribution with the current training data.',external=.9)
C('population','Unlabeled examples and a validated teacher or pseudo-labeled checkpoint are available.','Inspect teacher confidence on held-out data and the pseudo-label generation recipe.',pseudo=.8)
C('population','A class or test-representative subgroup is underexposed during training.','Compare sample frequencies and per-group errors with the task metric and expected test distribution.',resample=.9)
C('population','A minority group is small and within-class interpolation is meaningful in the feature space.','Inspect class-specific neighbor distances, feature types, and prior oversampling results.',synthetic=.6)
C('population','Previous synthetic oversampling hurt the same held-out metric.','Read controlled augmentation-on/off results under the present feature and validation setup.',synthetic=-1,resample=.3)
C('target','Targets contain event times and censoring indicators rather than fully observed outcomes.','Inspect target schema and the censoring fraction.',survival=1)
C('target','The evaluation separately scores predefined groups with different survival or target distributions.','Read the metric formula and compare target distributions by its grouping variable.',group_target=1)
C('target','A scalar target transform or centering convention changed or remains untuned.','Inspect target-construction code, inverse transforms, and prior transform-parameter comparisons.',target_scale=.8)
C('target','Labels are ordered discrete levels but the current model is plain regression.','Inspect unique target values and the penalty for neighboring versus distant mistakes.',ordinal=.9)
C('augment','Small image brightness or geometric changes preserve the target semantics.','Inspect domain examples and the training transform code for valid invariances.',image_aug=.8)
C('augment','The model relies on narrow time-frequency patches that may be absent at inference.','Inspect spectrograms, occlusion sensitivity, or error cases with missing signal regions.',mask_aug=.8)
C('augment','Targets can be meaningfully mixed and current training overfits individual examples.','Inspect soft-label semantics, training/validation divergence, and existing mixup settings.',mixup=.8)
# Learned model choices.
C('family','A compatible alternative pretrained backbone or size is available.','Inspect artifact metadata, required tokenizer or input shape, and existing controlled backbone comparisons.',backbone=.8)
C('family','Available pretraining data is substantially closer to the task domain than the current initialization.','Read checkpoint provenance and compare it with task inputs.',domain_pretrain=.9)
C('family','The features are tabular or fixed vectors and the current tree implementation has plateaued.','Inspect the feature matrix and recent depth, rate, and regularization trials.',tree_family=.8)
C('family','A meaningful input representation is not served well by the current architecture.','Compare raw signal, spectral image, or fixed embedding structure with the current model input and available alternatives.',modality_model=.9)
C('architecture','The backbone feeds a minimal, inappropriate shared, or oversized head.','Inspect the head layers, per-target parameter sharing, and training/validation behavior.',head=.9)
C('architecture','Only one hidden layer or pooling statistic is used despite variable-length or multi-layer information.','Read the forward pass and inspect the tensors discarded before the output layer.',pool=.9)
C('architecture','An auxiliary target or discretized version of the main target is available.','Inspect label derivability from training targets and whether independent validation can assess the main-task effect.',aux_head=.8)
C('architecture','Multiple informative branches are merged by a lossy or untested rule.','Inspect branch ablations, equal-dimension averaging, concatenation dimensions, and corresponding checkpoint training.',fusion=.9)
C('architecture','The head overfits or varies markedly across seeds.','Inspect train/validation gaps, seed-specific scores, and current dropout configuration.',dropout=.9)
C('tree_fit','Trees appear capacity-limited or increased capacity has begun to overfit.','Compare training and validation curves across existing depth and leaf-count settings.',capacity=.9)
C('tree_fit','Training error improves while validation worsens with the current feature set.','Inspect learning curves and row/column sampling and penalty settings.',tree_reg=.9)
C('tree_fit','Learning rate changed without a corresponding convergence budget.','Compare rate, maximum rounds, selected iteration, and whether validation was still improving at the cap.',boost_budget=1)
C('tree_fit','Stopping occurs before convergence, on the wrong set, or with excessive patience.','Inspect the monitored dataset/metric and training logs around the selected iteration.',early=1)
C('tree_fit','Many manually set parameters lack isolated evidence of benefit.','Review the parameter history against default values and controlled comparisons.',defaults=.9)
C('neural_fit','Training is unstable or converges poorly at the current learning rate.','Inspect batch losses, gradients, warm-up behavior, and earlier rate trials.',learning=1)
C('neural_fit','The training loss stalls at a schedule transition or under the current optimizer.','Inspect the learning-rate trace, optimizer state, and loss curve around transitions.',schedule=.9)
C('neural_fit','Training ends while validation improves or continues well beyond its best epoch.','Inspect epoch-level validation curves and stage-specific checkpoint metrics.',epochs=.9)
C('neural_fit','The training loss poorly represents the ranking, distribution, or ordinal evaluation objective.','Compare the mathematical training objective with the evaluation formula and prior loss ablations.',loss=.9)
C('neural_fit','A component lacks consistent fold training or reproducible held-out predictions.','Compare its train/validation indices, preprocessing scope, saved checkpoints, and data-loader logic with other components.',train_structure=1)
# Prediction pool.
C('diversity','Current members share a family and their held-out errors are highly correlated.','Inspect architecture metadata and an aligned out-of-fold residual correlation matrix.',diverse=.9)
C('diversity','A relevant modality, feature set, or preprocessing view is not represented.','Compare member input manifests with available raw data and known representation ablations.',representation_diverse=.9)
C('diversity','Alternative valid target transforms or training recipes yield different held-out errors.','Compare candidate recipe metadata and aligned out-of-fold predictions.',target_diverse=.9)
C('diversity','Compatible unused fold or snapshot predictions are already available.','Inspect checkpoint manifests, fold identities, and the current average membership.',folds=.9)
C('diversity','Training seeds produce materially different held-out predictions.','Compare existing independent seed runs and verify inference repeats alone are not identical.',seeds=.9)
C('diversity','Compatible checkpoints from one weight-space trajectory are saved.','Check architecture identity, training trajectory, and availability of snapshots suitable for weight averaging.',swa=.8)
C('members','The candidate has not yet produced verified standalone predictions.','Inspect candidate inference logs, prediction statistics, and any standalone held-out score.',candidate=1,add_member=-.5)
C('members','A functioning candidate has plausible complementary errors but no marginal-blend result.','Compare aligned out-of-fold residuals and confirm it has not yet been tested alongside the intact baseline.',add_member=.9)
C('members','A member is weak, redundant, or associated with a regression.','Inspect prior leave-one-out results, component errors, and when it entered the pool.',prune=.9)
C('members','A new compatible checkpoint can replace a specific weaker slot.','Compare the slot and candidate training recipes and existing standalone quality evidence.',replace_member=.9)
C('members','Removing formerly useful members caused a reproducible regression.','Compare the saved successful member manifest with the current reduced pool and its scores.',restore_members=1)
C('members','Other model components or aggregation rules changed since the last membership test.','Diff component artifacts and aggregation settings against the last ablation record.',retest_members=1)
C('checkpoint','Several runs or fold checkpoints have matching architecture and preprocessing.','Inspect checkpoint metadata and their local validation scores.',checkpoint_sweep=.9)
C('checkpoint','Artifacts differ mainly by training stage or stopping criterion.','Read checkpoint epoch, stage, and selection-metric metadata.',checkpoint_stage=1)
C('checkpoint','Both full-data-trained and fold-trained artifacts are available.','Compare the training-row and fold metadata for available checkpoints.',checkpoint_regime=1)
# Combination, calibration, and test-time inference.
C('combine','The metric rewards ordering and members have different score scales.','Read the metric definition and inspect per-member score histograms and calibration ranges.',rank=1)
C('combine','Members expose logits and probabilities for a distribution-based metric.','Inspect output activations and probability row sums, and identify where normalization occurs relative to averaging.',probability=1)
C('combine','Model families contribute unequal numbers of fold or seed predictions.','Count predictions per family and derive each family\'s effective weight from the current formula.',hierarchy=.9)
C('combine','Aligned leakage-free out-of-fold predictions exist for a simple learned blender.','Verify every meta-training prediction excludes its own row and compare meta-feature count with the calibration sample size.',stack=.9)
C('combine','An established stacker has plateaued and its model class or penalty is untested.','Inspect held-out meta-learner errors and previous linear, kernel, or tree comparisons.',stack_type=.8)
C('combine','Probability saturation may make arithmetic averaging overly dominated by confident members.','Inspect member probability distributions and held-out comparisons of raw and transformed predictions.',power=.7)
C('combine','Only tiny or noisy calibration data are available relative to meta-model flexibility.','Compare calibration size and subgroup coverage with meta-feature count and tuning history.',stack=-.7,stack_type=-.7)
C('weights_rule','Members differ reliably in quality or complementary error structure.','Compare aligned out-of-fold scores and correlations, rather than standalone public scores alone.',weights=.9,uniform=-.3)
C('weights_rule','Equal weighting matches tuned weights within measured score noise.','Compare previous equal-weight and tuned-weight results with repeat variability.',uniform=1,weights=-.6,adaptive=-.7)
C('weights_rule','Prior unconstrained or signed fits suggest a component can cancel correlated error.','Inspect fitted coefficients and independent validation, and confirm the output is not required to remain a convex probability mixture.',negative=.8)
C('weights_rule','Component strengths differ consistently by an observable class or subgroup.','Compare per-class or per-group held-out errors and verify the condition is available at inference.',adaptive=.8)
C('weights_rule','Member quality, count, augmentation, or scaling changed after weights were selected.','Compare the current component and transform manifest with the weight-search manifest.',reweight=1)
C('weights_rule','Component prediction scales differ substantially or contain heavy outliers.','Inspect means, standard deviations, medians, interquartile ranges, and extreme predictions.',scale_blend=.9)
C('stack_inputs','Training meta-features include in-sample predictions or inconsistent fold assignments.','Join prediction provenance with training indices and verify that each row was excluded from the generating model\'s fit.',oof=1,stack_expand=-.8)
C('stack_inputs','Additional aligned auxiliary outputs provide signal not captured by existing base scores.','Inspect held-out correlation or incremental predictive value of available embeddings, logits, or auxiliary outputs.',stack_expand=.9)
C('stack_inputs','The meta-feature pool has grown while validation stagnates or regresses.','Compare pool versions and ablation results and inspect redundancy among prediction columns.',stack_prune=1,stack_expand=-.5)
C('discretize','The ordinal metric is sensitive to cutpoints and representative held-out predictions are available.','Compare naive rounding errors with target levels and inspect out-of-fold coverage of each class.',threshold=.9)
C('discretize','Optimized thresholds have unstable or worse independent performance than simple rounding.','Compare held-out results across folds or previous threshold variants with the clip-and-round baseline.',round=1,threshold=-.5)
C('discretize','Known target frequencies are stable enough to support a distribution-matching comparison.','Compare label frequencies across training sources and held-out folds with the stated test sampling.',quantile=.8)
C('discretize','Continuous predictions correspond to a small set of repeated target levels.','Inspect unique labels, prediction gaps, and per-target histograms.',bin=.9)
C('discretize','Subgroups exhibit different residual-to-label mappings and are observable at prediction time.','Compare held-out calibration curves by group and audit the source of inference-time group assignments.',group_cut=.8)
C('discretize','Existing binning collapses a column or creates many artificial ties.','Count distinct predictions per column before and after binning and inspect the metric\'s tie convention.',degenerate=1,bin=-.5)
C('discretize','The checkpoint or ensemble changed since calibration was fitted.','Compare the threshold-fit prediction manifest with the current checkpoint and blend manifest.',threshold=.9)
C('calibrate','Outputs have the wrong units, activation, range, or probability sum.','Compare output summaries and training target transforms with the submission specification.',link=1,temperature=-.5)
C('calibrate','Some components rank risk in the opposite direction.','Check each output convention against its target transform and its signed held-out association with outcomes.',direction=1)
C('calibrate','Valid probabilities show systematic confidence or per-class mass bias.','Inspect held-out reliability curves, predicted class mass, and observed label distributions.',temperature=.9)
C('calibrate','A systematic additive or reference-relative bias remains in valid predictions.','Inspect held-out mean residuals or predictions of fixed reference examples under the same model.',offset=.8)
C('calibrate','A high-precision auxiliary classifier or metadata rule identifies a predictable error subset.','Measure rule precision and subset residuals on held-out data and confirm the rule uses inference-available information.',rule=.8)
C('calibrate','A previously helpful post-processing step has not been reassessed after upstream changes.','Compare model/ensemble versions with the last isolated post-processing on/off trial.',post_ablate=1)
C('calibrate','The proposed global monotone rescaling cannot change the metric\'s ordering.','Check that the metric is purely rank-based and the transform introduces no clipping, rounding, or changed blending.',temperature=-.7,offset=-.7,post_ablate=.6)
C('tta','A deterministic flip or sensor symmetry preserves the label.','Inspect the domain meaning of each axis or channel and the training augmentation record.',geometric_tta=.9)
C('tta','Multiple valid windows or compatible resolutions cover the same prediction target.','Compare label scope, available context, and checkpoint preprocessing for each view.',crop_tta=.9)
C('tta','Repeated forward passes intentionally vary and prior stochastic-view evidence is promising.','Compare saved per-pass predictions and inspect active-dropout or random-transform code.',stochastic_tta=.8)
C('tta','Repeated passes should be identical but differ because training-mode layers or random transforms remain active.','Inspect model evaluation mode, dropout and batch-normalization state, RNG use, and per-pass outputs.',deterministic=1,stochastic_tta=-.5)
C('tta','The proposed augmentation changes signal meaning or previously hurt this branch.','Inspect branch-specific augmentation ablations and whether axes represent time or frequency rather than interchangeable space.',geometric_tta=-.8,stochastic_tta=-.8,deterministic=.6)
# Execution choices.
C('memory','The full data or feature table cannot fit, but complete entities can be processed independently.','Inspect memory use by data stage and whether entity-level aggregation crosses proposed partition boundaries.',chunk=1)
C('memory','Memory accumulates across successive model loads.','Track allocated memory before and after each model and find live references retained past their final use.',release=1)
C('memory','Large feature matrices use wider dtypes than their range and required precision justify.','Inspect per-column dtype, min/max, precision requirements, and memory footprint.',downcast=.9)
C('memory','Peak memory occurs inside one forward pass and scales with batch size.','Compare failure point and allocation logs for existing batch sizes.',batch=1)
C('memory','Model activations dominate memory and reduced precision is supported by the inference stack.','Inspect dtype/backend support and any prior full- versus mixed-precision prediction comparisons.',precision=.8)
C('memory','A metric, transform, or repeated device transfer dominates elapsed time.','Profile the relevant stage and compare available equivalent implementations on a small fixed sample.',accelerate=.9)
C('iteration','The current task is checking correctness and failures occur after expensive work.','Identify the smallest data slice and training settings that still execute the failing path.',debug=1)
C('iteration','Only downstream settings change while upstream features or predictions remain identical.','Compare experiment diffs with feature/model artifact hashes and stage runtimes.',cache=1)
C('iteration','Some folds or training stages are complete but session limits prevent finishing the rest.','Inspect saved checkpoint manifests for completed and missing stages or fold indices.',resume=1)
C('iteration','The next evaluated run must use the complete selected configuration but debug shortcuts remain enabled.','Audit fold limits, early exits, stage flags, and output-generation guards against the final configuration.',production=1,debug=-.8)
C('structure','Adding model variants repeatedly requires editing duplicated code and shared globals.','Inspect duplicated inference functions, per-model preprocessing differences, and recent integration bugs.',modular=.9)
C('structure','Dead code or training-only paths obscure a stable inference pipeline.','Compare active dependencies and a saved reference prediction before removing unused code.',refactor=.9)
C('structure','Identical code can load different artifacts or settings across runs.','Inspect mutable checkpoint directories, file discovery order, seed handling, and saved weight/configuration manifests.',pin=1)
C('structure','Some component files are missing or current exception handlers silently inject placeholders.','Inspect file-existence checks, caught exceptions, fallback arrays, and denominator adjustment.',fallback=1)
# Materialize positional IDs and references after all decisions and placements are final.
root=dict(key='root',id='T',name='Improve the solution',decision='what can I change to improve my solution?',description='Choose the next concrete intervention using the available evidence, then revisit the tree after measuring its effect.',source='data',children=branches,unassigned=[])
key_nodes={}
def index(n,id):
 n['id']=id
 if n['key'] in key_nodes: raise ValueError(('duplicate authoring key',n['key']))
 key_nodes[n['key']]=n
 for j,c in enumerate(n['children'],1):index(c,f'{id}.{j}')
index(root,'T')
des={'nodes':{}}
for k,n in key_nodes.items():
 if n['children']:
  if k not in checks:raise ValueError(('missing checks',k))
  childkeys={c['key'] for c in n['children']}
  out=[]
  for c in checks[k]:
   if not set(c['pushes'])<=childkeys:raise ValueError(('nonchild push',k,c))
   out.append(dict(check=c['check'],how=c['how'],pushes={key_nodes[x]['id']:w for x,w in c['pushes'].items()}))
  des['nodes'][n['id']]={'groups':[{'under':'WHAT FITS THIS CASE?','checks':out}]}
# Preserve input order within each leaf for easy evidence lookup.
order={r['id']:r['idx'] for r in rows}
def clean(n):
 n.pop('key')
 if not n['children']:n['items'].sort(key=order.__getitem__)
 for c in n['children']:clean(c)
clean(root)
json.dump(root,open(P/'tree.json','w'),indent=2,ensure_ascii=False)
json.dump(des,open(P/'desiderata.json','w'),indent=2,ensure_ascii=False)
def count(n):return len(n.get('items',[]))+sum(count(c) for c in n['children'])
counts='\n'.join(f"| {n['id']} — {n['name']} | {count(n)} |" for n in branches)
notes='''# Clustering and limitations

Reviewed 856 episodes and 1,674 rationales in bounded batches. Explicit item placements primarily follow `general.goal` and `general.action`, using context and instance evidence for ambiguous or bundled edits. Each item remains intact under its main actionable rationale; leaf IDs reference the original evidence.

The tree selects **the next intervention or controlled experiment**. Siblings are alternative next actions, not a sequence; several may be useful on later visits. Broad routes overlap in applicability. Clusters separate repairs from modeling, replacement from addition, and seed from fold averaging. Unresolved comparisons remain experimental actions, such as comparing rank and raw averaging. All nodes are data-derived; checks supplement observed contexts with methodological requirements. Weights are qualitative directions, not fitted probabilities; omitted pushes assert no effect, and NO does not automatically invert YES.

The least sharply defined decisions are broad intervention routing, mixed-lever experiments, and checkpoint versus membership changes. A separate bundle action preserves coordinated-change rationales without claiming causal attribution. Tiny public leaderboards, nondeterminism, and confounded edits weaken many source conclusions. Repeated items establish recurring practice, not independent proof; strong claims become comparisons requiring held-out evidence.

The subgroup-allocation leaf retains five rationales advocating overlapping training and validation rows. That procedure leaks information: its local scores must not be treated as generalization estimates. The leaf and checks require a separate disjoint evaluation and discourage overlapping allocation. Similarly, tokenizer changes, inference preprocessing changes, rank ties, and output scaling require compatibility and metric checks; source claims about gains are not assumed true.

All items have an actionable rationale, including engineering changes that enable valid performance comparisons; none were discarded as bookkeeping. `validate_output.py` independently checks source coverage, positional IDs, schema, and all decision/check references.

| Top-level choice | Items |
|---|---:|
'''+counts+'\n'
(P/'notes.md').write_text(notes)
