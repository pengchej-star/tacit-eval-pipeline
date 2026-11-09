# goal clusters, kp representation, complete linkage, 200 clusters

## 92 items, 43 kernels
- What do I do when I add new features and new ensemble members simultaneously and the score regresses?  *[score regression, simultaneous changes, feature and ensemble addition, change isolation]*
- What do I do when I change multiple components at once (architecture + ensembling removal) and get a regression?  *[score regression, simultaneous changes, change isolation, architecture change, ensemble modification]*
- What do I do when I change multiple things at once and get a bad result?  *[score regression, multiple simultaneous changes, isolating individual effects]*
- What do I do when I make a multi-factor change and get a regression?  *[score regression, multi-factor change, change isolation]*
- What do I do when I swap a pretrained backbone to a larger variant and the score collapses?  *[score regression, backbone upgrade, larger model variant, score collapse]*
- What do I do when I try a new component (e.g., optimizer) and the score drops, but the change was bundled with a bug fix?  *[score regression, bundled changes, ablation study, bug fix isolation]*
- What do I do when I want to test multiple independent improvements but the first one already regresses?  *[score regression, multiple pending changes, first change failure, change isolation]*
- What do I do when I'm iterating on a model component and a change causes a severe score regression?  *[score regression, model component change, iterative debugging, revert decision]*
- What do I do when I'm unsure whether a regression is due to a code bug or a genuinely bad model choice?  *[score regression, bug vs bad choice, root cause diagnosis, debugging pipeline]*
- What do I do when I've bundled multiple changes and the score regresses?  *[score regression, bundled changes, change isolation, debugging]*
- What do I do when a bug fix or restoration attempt produces a worse score than expected?  *[score regression, bug fix attempt, code restoration, unexpected outcome]*
- What do I do when a bundle of changes produces a regression and I need to identify which change caused it?  *[score regression, bundled changes, change isolation, root cause analysis]*
## 62 items, 29 kernels
- What do I do when I add a new model to an ensemble but need to verify it works before blending?  *[new model verification, ensemble member addition, standalone validation, pre-blend testing]*
- What do I do when I find a new single component that outperforms the current best single component?  *[new best component, single model improvement, ensemble member selection]*
- What do I do when I have a large ensemble of tree-based and MLP models and want to add further diversity?  *[ensemble diversity, model diversity, large ensemble expansion, new model type addition]*
- What do I do when I have a multi-model ensemble and want to improve the final score with minimal risk?  *[multi-model ensemble, score improvement, low-risk tuning, blend weight optimization]*
- What do I do when I have a new model variant trained offline and want to decide whether to include it in an ensemble?  *[new model variant, offline training, ensemble member selection]*
- What do I do when I have a new model variant trained offline and want to know if it improves my inference ensemble?  *[new model variant, offline training, ensemble integration, contribution test]*
- What do I do when I have a new set of model artifacts trained with a different data augmentation strategy and want to evaluate whether they improve my  *[new model artifacts, data augmentation strategy, ensemble member selection, contribution test]*
- What do I do when I have a simple ensemble of two similarly-performing models and want to improve the combined score?  *[simple ensemble, ensemble weighting, score improvement, two-model blend]*
- What do I do when I have a strong ensemble of one model family and want to improve further?  *[strong ensemble, model diversity, ensemble expansion, incremental improvement]*
- What do I do when I have a working ensemble and want to improve it by swapping one component for a stronger one?  *[component replacement, stronger model swap, ensemble improvement]*
- What do I do when I have a working ensemble baseline and want to improve it by adding more diverse models?  *[model diversity, ensemble expansion, diverse models addition]*
- What do I do when I have a working ensemble of fine-tuned transformers and want to improve its representational diversity?  *[representational diversity, ensemble improvement, transformer fine-tuning, model diversity]*
## 62 items, 30 kernels
- What do I do when A/B testing two component variants in an ensemble yields a regression for one variant?  *[score regression, ensemble variant comparison, a/b testing, component selection]*
- What do I do when I add a new model to an ensemble but it degrades the score?  *[score regression, ensemble member addition, ensemble debugging]*
- What do I do when I add multiple new prediction sources to an ensemble and the score regresses catastrophically?  *[catastrophic regression, ensemble expansion, new prediction sources, ensemble debugging]*
- What do I do when I introduce a new model architecture into an ensemble and it causes a score regression?  *[score regression, new architecture, ensemble debugging]*
- What do I do when I suspect a blending/averaging bug is causing catastrophic score regression?  *[score regression, blending bug, averaging error, ensemble debugging]*
- What do I do when a complex new ensemble pipeline fails to run or produces worse results than a simpler prior approach?  *[execution failure, score regression, ensemble pipeline, complexity reduction]*
- What do I do when a new base model added to an ensemble worsens the score?  *[score regression, ensemble member selection, new model addition, ensemble weighting]*
- What do I do when a new ensemble strategy scores worse than the simpler baseline on the leaderboard?  *[score regression, ensemble strategy, baseline comparison, pipeline complexity]*
- What do I do when a newly introduced model component degrades ensemble performance?  *[score regression, ensemble degradation, component removal decision]*
- What do I do when a simplified ensemble scores much worse than my best complex ensemble?  *[score regression, ensemble simplification, ensemble complexity tradeoff]*
- What do I do when a single-backbone ensemble regresses compared to a multi-backbone blend?  *[score regression, single backbone ensemble, backbone diversity, multi-backbone blend]*
- What do I do when a single-backbone probe regresses relative to a multi-model ensemble?  *[score regression, single backbone probe, backbone diversity, multi-model ensemble]*
## 52 items, 21 kernels
- What do I do when I have a new model architecture's checkpoints available and want to integrate them into an existing ensemble?  *[new checkpoints available, ensemble integration, new model architecture]*
- What do I do when I have a new model checkpoint and want to know whether it improves my ensemble?  *[new checkpoints available, ensemble member selection, contribution test]*
- What do I do when I have a new set of model checkpoints and want to understand their standalone contribution before integrating them into an existing   *[new checkpoints available, standalone evaluation, ensemble integration]*
- What do I do when I have a new set of model checkpoints to incorporate into an existing meta-learned ensemble that is already near its best score?  *[new checkpoints available, meta-learned ensemble, near-best score, incremental improvement]*
- What do I do when I have a new, potentially better model checkpoint and want to quickly assess whether it outperforms my current ensemble?  *[new checkpoint available, quick evaluation, ensemble comparison]*
- What do I do when I have a working submission but want to swap in a better checkpoint before building an ensemble?  *[checkpoint swap, better checkpoint, pre-ensemble improvement]*
- What do I do when I have access to a new set of trained checkpoints and want to know if they improve my ensemble?  *[new checkpoints available, ensemble member selection, contribution test]*
- What do I do when I have access to additional pretrained model checkpoints and want to know if they improve my existing ensemble?  *[new checkpoints available, ensemble member selection, contribution test]*
- What do I do when I have access to additional trained checkpoints and want to improve an ensemble?  *[new checkpoints available, ensemble improvement, ensemble member selection]*
- What do I do when I have access to incrementally improved external model checkpoints for an ensemble?  *[improved external checkpoints, ensemble update, ensemble member selection]*
- What do I do when I have base-size transformer fold checkpoints and want to improve ensemble quality?  *[base-size transformer checkpoints, ensemble quality improvement, fold checkpoints, model scaling]*
- What do I do when I have fold-specific fine-tuned BERT checkpoints and want to improve prediction quality at inference time?  *[fold-specific checkpoints, inference quality improvement, bert fine-tuning, test-time strategy]*
## 43 items, 27 kernels
- What do I do when I add a large new component to my pipeline and the leaderboard score drops significantly?  *[score regression, new pipeline component, large component addition, pipeline debugging]*
- What do I do when I get a significant leaderboard regression after an exploratory episode?  *[score regression, leaderboard regression, exploratory rollback, recovery after change]*
- What do I do when I need to debug a multi-step pipeline change that broke the score but I'm unsure which part is wrong?  *[score regression, multi-step pipeline change, change isolation]*
- What do I do when I try a new model variant and it regresses significantly on the leaderboard?  *[score regression, new model variant, leaderboard evaluation]*
- What do I do when a change causes a large leaderboard regression on a very small public test set?  *[score regression, small test set, leaderboard noise, bundled changes]*
- What do I do when a change to the inference pipeline causes a large regression?  *[score regression, inference pipeline change, pipeline debugging]*
- What do I do when a code fix causes a score regression and I'm unsure whether the regression is real or due to noise?  *[score regression, leaderboard noise, bug diagnosis, code fix]*
- What do I do when a large multi-component change causes a regression on the leaderboard?  *[score regression, multi-component change, leaderboard regression, recovery after change]*
- What do I do when a large refactor causes a score regression but I believe the approach is correct?  *[score regression, refactor regression, persisting with approach, debugging pipeline]*
- What do I do when a major experiment fails on the leaderboard and I need to recover?  *[score regression, leaderboard failure, recovery after change]*
- What do I do when a major pipeline restructuring causes a small LB regression but I believe the new architecture is fundamentally sound?  *[score regression, pipeline restructuring, architecture confidence, minor regression]*
- What do I do when a model swap causes a catastrophic regression on the leaderboard?  *[score regression, model swap, leaderboard failure, recovery after change]*
## 39 items, 25 kernels
- What do I do when I achieve a new best leaderboard score and want to confirm it is real before changing direction?  *[new best score, score validation, leaderboard confirmation, direction change decision]*
- What do I do when I achieve a new best score and want to squeeze further improvement?  *[new best score, incremental improvement, further optimization]*
- What do I do when I achieve a new best score and want to test whether a previously-rejected feature set now helps on top of the improved baseline?  *[new best score, feature set re-evaluation, improved baseline, previously rejected features]*
- What do I do when I get a new best score and want to confirm it is stable before moving on?  *[new best score, stability verification, score validation]*
- What do I do when I get a new best score and want to confirm it's real before moving on?  *[new best score, score improvement validation, noise versus signal]*
- What do I do when I get a new best score and want to confirm it's real rather than noise?  *[new best score, noise versus signal, score improvement validation]*
- What do I do when I get a new best score and want to confirm it's stable before moving on?  *[new best score, stability verification, score validation]*
- What do I do when I get a new best score but want to confirm it's real before building on it?  *[new best score, score validation, reproducibility check]*
- What do I do when I have a new best score and a candidate variant of the same model that performed well in local validation?  *[new best score, candidate model variant, local validation, model selection]*
- What do I do when I have a new best score and want to explore multiple changes before submitting?  *[new best score, multi-change exploration, submission strategy]*
- What do I do when I have a new best score and want to explore whether alternative model variants can improve further?  *[new best score, model variant exploration, further improvement]*
- What do I do when I have a new best score and want to explore whether preprocessing or ensemble changes can improve it further?  *[new best score, preprocessing change, ensemble change, further improvement]*
## 36 items, 26 kernels
- What do I do when I have a score plateau and want to find better hyperparameters by sweeping two interacting settings?  *[score plateau, hyperparameter sweep, interaction between settings, grid search]*
- What do I do when I have a single-model inference pipeline that has plateaued on the leaderboard?  *[score plateau, single model baseline, pipeline improvement]*
- What do I do when I have a single-model pipeline that has plateaued after hyperparameter and ensemble-size tuning?  *[score plateau, single model pipeline, hyperparameter exhaustion, new strategy needed]*
- What do I do when I want to improve a GBDT+NN ensemble but in-notebook tuning has plateaued?  *[performance plateau, gbdt nn ensemble, tuning saturation, external resource search]*
- What do I do when I want to meaningfully improve my score after exhausting hyperparameter tuning of existing components?  *[score plateau, hyperparameter tuning exhaustion, new approach exploration, pipeline diversification]*
- What do I do when I'm at a plateau (tied personal best) and want to push higher by adjusting multiple configuration knobs?  *[score plateau, multi-parameter tuning, hyperparameter exploration]*
- What do I do when I'm at a score plateau and want to squeeze out improvement by tuning preprocessing hyperparameters?  *[score plateau, preprocessing hyperparameters, fine-grained tuning]*
- What do I do when I've been tuning hyperparameters for many iterations and want to understand per-fold behavior before continuing?  *[per-fold analysis, hyperparameter tuning plateau, fold behavior diagnosis]*
- What do I do when a multi-head CNN classification model plateaus and I want to improve per-head predictions?  *[training plateau, multi-head cnn, per-head prediction improvement, classification model]*
- What do I do when adding more stacked features to an already-strong ensemble doesn't clearly help on CV?  *[score plateau, stacking features, strong baseline, cv evaluation]*
- What do I do when ensemble performance has plateaued after tuning the meta-learner?  *[score plateau, meta-learner tuning, ensemble performance stagnation]*
- What do I do when fine-tuning a BERT model on a small dataset (~6K samples) and my score is plateauing from hyperparameter tuning alone?  *[score plateau, small dataset, bert fine-tuning, hyperparameter tuning limits]*
## 36 items, 20 kernels
- What do I do when I have a regression after swapping one ensemble member for another?  *[score regression, ensemble member swap, recovery after change]*
- What do I do when I want to find the optimal preprocessing parameter but my submissions keep regressing from a known best?  *[score regression, preprocessing parameter search, recovery after change, submission debugging]*
- What do I do when I want to test a new architectural idea (input reshape, new backbone) but the submission produces a catastrophic score?  *[catastrophic score, architecture change, debugging regression, score regression]*
- What do I do when I've regressed twice in a row and partially recovered but still can't beat my best score?  *[repeated score regression, partial recovery, plateau breaking]*
- What do I do when a catastrophic score regression occurs after reverting a recent fix?  *[catastrophic score regression, revert attempt, code restoration, root cause analysis]*
- What do I do when a code change causes a catastrophic score regression far below any previous result?  *[catastrophic score regression, code change, bug investigation, root cause analysis]*
- What do I do when a code change that adds a new inference technique causes a large score regression?  *[large score regression, inference technique, change rollback]*
- What do I do when a complex change causes a large regression on the leaderboard?  *[large score regression, complex change, change rollback, change attribution]*
- What do I do when a complex preprocessing step caused a leaderboard regression and I want to recover the lost performance?  *[score regression, preprocessing change, performance recovery]*
- What do I do when a config/hyperparameter change causes a score regression?  *[score regression, hyperparameter change, recovery after change]*
- What do I do when a configuration change causes a catastrophic score regression?  *[catastrophic score regression, configuration change, change rollback]*
- What do I do when a configuration change causes a large score regression and I need to recover quickly?  *[large score regression, configuration change, quick recovery]*
## 31 items, 18 kernels
- What do I do when I have been tuning blend weights for many iterations with diminishing returns?  *[diminishing returns, blend weight tuning, ensemble weighting plateau]*
- What do I do when I have multiple models in an ensemble and the score has plateaued?  *[score plateau, ensemble composition, multiple models, ensemble improvement]*
- What do I do when I want to improve an ensemble score but have been making small incremental weight changes with diminishing returns?  *[diminishing returns, ensemble weight tuning, incremental changes]*
- What do I do when I want to squeeze marginal gains from an already-strong ensemble component?  *[marginal gain extraction, ensemble component tuning, performance plateau]*
- What do I do when I want to squeeze more performance from a ResNet-family model that is already near its plateau?  *[performance plateau, resnet tuning, marginal gain extraction]*
- What do I do when I'm near a local optimum in ensemble composition and small weight tweaks yield negligible improvement?  *[local optimum, ensemble weight tuning, diminishing returns]*
- What do I do when I've exhausted gains from tuning blend weights across existing ensemble members?  *[blend weight plateau, ensemble diversity, next improvement strategy]*
- What do I do when I've matched my best score and want to know whether a recent addition (weighted ensemble) is actually helping?  *[score plateau, weighted ensemble, component contribution test, ablation study]*
- What do I do when a new ensemble component doesn't improve over the existing best score?  *[score plateau, ensemble member selection, contribution test, revert to best]*
- What do I do when adding more diverse model predictions to a stacking ensemble doesn't improve the score?  *[score plateau, stacking ensemble, diverse model predictions, diminishing returns]*
- What do I do when adding more models to an ensemble stops improving the score?  *[score plateau, ensemble expansion, diminishing returns, ensemble member selection]*
- What do I do when adding more transformer embeddings and ensemble members to a LightGBM stack doesn't improve the score?  *[score plateau, stacking ensemble, transformer embeddings, ensemble member selection]*
## 31 items, 20 kernels
- What do I do when I have a known-best ensemble configuration and want to check if reweighting can improve it further?  *[ensemble reweighting, known-best ensemble, weight optimization, incremental improvement]*
- What do I do when I have a multi-model ensemble and want to quickly check whether one component deserves more weight before investing in larger change  *[multi-model ensemble, weight sensitivity check, quick validation, ensemble weighting]*
- What do I do when I have a new multi-model ensemble and need to find the optimal contribution of each model?  *[multi-model ensemble, ensemble weighting, weight optimization]*
- What do I do when I have a small additive blending weight that was recently changed and I want to know if the previous value was actually better?  *[blending weight change, score regression check, weight rollback, ensemble weighting]*
- What do I do when I have a small ensemble of 2-3 transformer models and want to find the best blend?  *[small transformer ensemble, blend optimization, ensemble weighting]*
- What do I do when I have a small number of ensemble members and need to find optimal blend weights?  *[small ensemble, optimal blend weights, ensemble weighting]*
- What do I do when I have a two-model ensemble and want to find the optimal weighting between them?  *[two-model ensemble, ensemble weighting, weight optimization]*
- What do I do when I have a working ensemble and want to squeeze out more performance by adjusting the blend?  *[blend weight tuning, ensemble weighting, marginal improvement]*
- What do I do when I have manually assigned non-uniform combination weights to fold models and want to check if this is actually helping?  *[non-uniform ensemble weights, fold model weighting, weight validation]*
- What do I do when I have many ensemble members with equal weights and want to improve the blend?  *[equal weight ensemble, ensemble weight optimization, blend improvement]*
- What do I do when I have multiple ensemble components and need to set blend weights?  *[ensemble components, blend weight setting, ensemble weighting]*
- What do I do when I have two different model types in an ensemble and need to find the optimal weighting between them?  *[ensemble weighting, heterogeneous model types, weight optimization]*
## 29 items, 19 kernels
- What do I do when I have a blend that just achieved a new best score and I want to know if one component deserves even more weight?  *[new best score, blend weight adjustment, ensemble weighting, component contribution test]*
- What do I do when I have a multi-model ensemble and want to find the best blend weights?  *[multi-model ensemble, blend weight optimization, weight search]*
- What do I do when I have a new best ensemble score and want to extract more from the blend weight between NN and GBDT components?  *[new best score, blend weight optimization, nn-gbdt ensemble]*
- What do I do when I have a new best score from a complex ensemble and want to squeeze out more by tuning blend weights?  *[new best score, complex ensemble, blend weight optimization, incremental gains]*
- What do I do when I have many pretrained model predictions and want to find the best weighted blend?  *[ensemble weight optimization, pretrained model predictions, weighted blend search]*
- What do I do when I have multiple diverse model architectures and want to find the best ensemble blend?  *[diverse model architectures, ensemble blend search, blend weight optimization]*
- What do I do when I have multiple diverse model architectures producing predictions on the same data and want to find good blend weights?  *[diverse model architectures, blend weight optimization, ensemble blending]*
- What do I do when I have multiple heterogeneous model predictions and need to find the best blend weights without local validation?  *[heterogeneous model predictions, blend weight optimization, no local validation]*
- What do I do when I have multiple inference models and need to find the best blend?  *[ensemble blend optimization, multiple inference models, blend weight search]*
- What do I do when I have multiple model predictions and need to find the best blend weights for submission?  *[blend weight search, multiple model predictions, ensemble blend optimization, submission preparation]*
- What do I do when I have multiple model predictions to combine and want to find the best blending configuration?  *[multiple model predictions, blend weight optimization, ensemble configuration search]*
- What do I do when I have multiple models of varying individual quality and need to set blend weights?  *[varying model quality, blend weight optimization, ensemble weighting]*
## 25 items, 15 kernels
- What do I do when I have a multi-member ensemble at a good score and want to understand which members contribute?  *[ensemble member contribution, member ablation, multi-member ensemble, contribution analysis]*
- What do I do when I have a multi-member ensemble that achieves a new best score and want to know if all members are contributing?  *[ensemble member contribution, new best score, member ablation, multi-member ensemble]*
- What do I do when I have a multi-model ensemble and want to know whether a weaker member is helping or hurting?  *[multi-model ensemble, member contribution test, ensemble member selection]*
- What do I do when I have a multi-model ensemble but suspect one component is not contributing or is hurting performance?  *[multi-model ensemble, member contribution test, underperforming component, ensemble member selection]*
- What do I do when I have a new model's predictions available and want to know whether adding them to an existing ensemble improves performance?  *[new predictions available, ensemble member selection, contribution test]*
- What do I do when I have a new prediction source (e.g., retrieval-based features) that scored poorly on its own but might add diversity to an existing  *[new prediction source, ensemble diversity, weak model integration, contribution test]*
- What do I do when I have a strong ensemble and want to check whether blending in a weak auxiliary model helps?  *[strong ensemble, auxiliary model blending, ensemble member selection, contribution test]*
- What do I do when I have a working ensemble and want to know if adding more members improves it?  *[ensemble member addition, ensemble size, contribution test]*
- What do I do when I have many candidate models and need to find the best subset and aggregation method?  *[ensemble member selection, aggregation method comparison, model subset search]*
- What do I do when I want to decide whether to invest effort improving a secondary model in my ensemble?  *[ensemble member selection, secondary model improvement, effort allocation]*
- What do I do when I want to evaluate a new model's contribution to an existing ensemble before committing to a full blend?  *[ensemble member selection, new model contribution, contribution test]*
- What do I do when I want to evaluate a single model component's contribution within a multi-model blend?  *[ensemble member selection, component contribution, ablation study]*
## 25 items, 20 kernels
- What do I do when I add a large batch of new features and the leaderboard score regresses?  *[score regression, batch feature addition, feature debugging]*
- What do I do when I change multiple hyperparameters at once and the score drops?  *[score regression, multiple hyperparameter changes, isolating individual effects]*
- What do I do when I change two hyperparameters at once and get a large regression?  *[score regression, multiple hyperparameter changes, isolating individual effects]*
- What do I do when I'm exploring multiple hyperparameters and each change produces a regression?  *[score regression, hyperparameter exploration, multiple parameter changes]*
- What do I do when a KNN-augmented prediction method scores worse than direct model outputs?  *[score regression, knn augmentation, prediction method comparison, baseline underperformance]*
- What do I do when a hyperparameter change causes a large score regression?  *[score regression, hyperparameter change, large regression, rollback decision]*
- What do I do when a hyperparameter change causes a leaderboard regression?  *[score regression, hyperparameter change, leaderboard evaluation, rollback decision]*
- What do I do when a hyperparameter change worsens the leaderboard score?  *[score regression, hyperparameter change, leaderboard evaluation, rollback decision]*
- What do I do when a larger model variant scores worse than a smaller one on the leaderboard?  *[score regression, model scaling, smaller model superiority, model size selection]*
- What do I do when a novel augmentation-based inference strategy causes a large score regression?  *[score regression, augmentation-based inference, novel strategy evaluation, revert decision]*
- What do I do when a previously added technique (TTA) showed a regression and I'm restructuring the ensemble?  *[score regression, test-time augmentation, ensemble restructuring, technique removal]*
- What do I do when a single-point probe of a previously successful hyperparameter shows a small regression?  *[score regression, hyperparameter probe, single-point evaluation, revert decision]*
## 25 items, 9 kernels
- What do I do when I have a single high-scoring checkpoint and access to multiple fold checkpoints from the same training run?  *[single checkpoint submission, fold checkpoints available, ensemble member selection]*
- What do I do when I have a single-model submission and multiple saved checkpoints from cross-validation folds?  *[single model submission, cross-validation checkpoints, fold ensemble, checkpoint selection]*
- What do I do when I have many candidate checkpoints and limited submission budget?  *[checkpoint selection, limited submission budget, candidate prioritization]*
- What do I do when I have many trained checkpoints from different runs and epochs and want to find which one generalizes best?  *[multiple checkpoints available, checkpoint selection, generalization evaluation, cross-run comparison]*
- What do I do when I have many trained fold/checkpoint indices but haven't tried all of them individually?  *[multiple fold checkpoints, checkpoint evaluation, individual checkpoint testing, unexplored candidates]*
- What do I do when I have multiple candidate model checkpoints and several inference-time knobs (augmentation, post-processing) to evaluate?  *[multiple checkpoints available, inference-time augmentation, post-processing tuning, joint hyperparameter search]*
- What do I do when I have multiple fine-tuned checkpoints and want to find the best submission?  *[fine-tuned checkpoints, best submission selection, checkpoint choice]*
- What do I do when I have multiple saved checkpoints from cross-validation folds and need to pick the best one for submission?  *[cross-validation checkpoints, checkpoint selection, submission strategy]*
- What do I do when I have multiple saved model checkpoints and want to find the best single one for submission?  *[multiple checkpoints available, best single checkpoint, submission selection]*
- What do I do when I have multiple trained checkpoint variants (different training stages, selection criteria) and want to find the best one for submis  *[multiple checkpoint variants, checkpoint selection, submission selection]*
- What do I do when I have multiple trained checkpoint versions and need to find which one performs best on the leaderboard?  *[multiple checkpoint versions, leaderboard evaluation, checkpoint selection]*
- What do I do when I have multiple trained checkpoints (different seeds/indices) and need to pick the best single model for inference?  *[multiple checkpoints different seeds, best single checkpoint, inference configuration]*
## 24 items, 9 kernels
- What do I do when I have a new best score but the public leaderboard uses very few rows, making the score noisy?  *[new best score, noisy leaderboard, small test set, score reliability]*
- What do I do when I observe high variance in leaderboard scores across identical submissions and need to determine which of two configurations is trul  *[score variance, leaderboard noise, configuration comparison, non-determinism]*
- What do I do when I want to test whether a novel inference-time trick (e.g., stochastic/entropy-based behavior) helps, but the leaderboard has high ru  *[inference-time trick, run-to-run variance, leaderboard noise, stochastic inference]*
- What do I do when a code change produces a small regression but I suspect leaderboard noise rather than a real degradation?  *[small score regression, leaderboard noise, score interpretation]*
- What do I do when a code change shows a tiny improvement that could be noise?  *[marginal improvement, leaderboard noise, score interpretation]*
- What do I do when a hyperparameter change causes a small LB regression but I'm not sure if it's noise?  *[marginal regression, hyperparameter change, leaderboard noise, significance assessment]*
- What do I do when identical re-runs produce very different leaderboard scores?  *[score variance, non-reproducibility, leaderboard instability, identical reruns]*
- What do I do when identical re-runs produce very different leaderboard scores?  *[score variance, non-reproducibility, leaderboard instability, identical reruns]*
- What do I do when leaderboard differences between weight configurations are very small (< 0.002)?  *[small score differences, ensemble weight tuning, leaderboard noise]*
- What do I do when leaderboard scores are highly variable across identical re-runs?  *[leaderboard variance, score instability, reproducibility]*
- What do I do when leaderboard scores are noisy and I cannot trust a single submission's result?  *[leaderboard noise, submission reliability, score aggregation]*
- What do I do when multiple hyperparameter changes each produce LB movements smaller than expected noise?  *[marginal improvement, hyperparameter tuning, leaderboard noise, signal detection]*
## 23 items, 14 kernels
- What do I do when I have exhausted continuous hyperparameter tuning and objective changes but want further gains from the same model family?  *[hyperparameter tuning exhaustion, diminishing returns, discrete design choices, same model family]*
- What do I do when I need to tune a continuous hyperparameter but full training is too slow for rapid iteration?  *[hyperparameter tuning, training speed bottleneck, rapid iteration strategy, continuous hyperparameter]*
- What do I do when I want to efficiently sweep a single integer hyperparameter using local validation before spending leaderboard submissions?  *[hyperparameter sweep, integer hyperparameter, local validation, submission budget]*
- What do I do when I want to quickly iterate on model hyperparameters but submitting each variant is slow?  *[hyperparameter iteration, slow submission cycle, rapid experimentation]*
- What do I do when I want to test multiple interacting hyperparameters but can only submit one configuration at a time?  *[interacting hyperparameters, submission budget, sequential testing, hyperparameter search]*
- What do I do when I want to tune a meta-learner's hyperparameters but the tuning loop is too slow to run every submission?  *[meta-learner hyperparameter tuning, slow tuning loop, submission budget]*
- What do I do when I want to tune hyperparameters but also need to stabilize the training environment?  *[hyperparameter tuning, training environment stability, environment configuration]*
- What do I do when I want to tune multiple coupled hyperparameters efficiently without wasting submissions?  *[coupled hyperparameter tuning, submission budget, efficient search strategy]*
- What do I do when I want to tune multiple small hyperparameters simultaneously without wasting leaderboard submissions?  *[joint hyperparameter tuning, submission budget, efficient search strategy]*
- What do I do when I want to use leaderboard scores to guide a hyperparameter sweep but each submission takes significant time?  *[leaderboard-guided tuning, hyperparameter sweep, submission budget]*
- What do I do when I'm near a plateau and want to squeeze out the last few thousandths of a metric from a continuous hyperparameter?  *[performance plateau, continuous hyperparameter tuning, fine-grained optimization, diminishing returns]*
- What do I do when I'm sweeping a single hyperparameter and seeing diminishing returns on the leaderboard?  *[hyperparameter sweep, diminishing returns, optimal stopping]*
## 22 items, 14 kernels
- What do I do when I have a new DeBERTa fine-tuned checkpoint and need to decide which pretrained backbone size to pair with it?  *[new checkpoint available, backbone size selection, model pairing, deberta fine-tuning]*
- What do I do when I have a new model architecture and multiple trained checkpoint sets to evaluate?  *[new model architecture, checkpoint evaluation, model selection]*
- What do I do when I have a new model variant (e.g., ordinal head) and want to find the best checkpoint configuration for it?  *[new model variant, checkpoint configuration, hyperparameter search]*
- What do I do when I have a strong 2D CNN pipeline and am iterating on training runs to find the best checkpoint version?  *[checkpoint selection, 2d cnn pipeline, training run iteration, best checkpoint search]*
- What do I do when I have access to a much better pretrained checkpoint than my current one?  *[better pretrained checkpoint, checkpoint upgrade, model initialization]*
- What do I do when I have both 'final' and 'best validation' checkpoints available for each fold?  *[checkpoint selection, final vs best validation, fold checkpoint comparison]*
- What do I do when I have fine-tuned checkpoints at different backbone sizes and want to find the best inference configuration?  *[multiple backbone sizes, inference configuration search, checkpoint selection, model scaling]*
- What do I do when I have multiple checkpoint variants of the same model architecture (e.g., different training configs like scale vs cope)?  *[checkpoint variants, training config comparison, same architecture, checkpoint selection]*
- What do I do when I have multiple checkpoint versions of the same model architecture and want to find the best one for inference?  *[checkpoint versions, same architecture, checkpoint selection, inference quality maximization]*
- What do I do when I have multiple saved model weight variants and want to know which gives the best test-time performance?  *[multiple weight variants, checkpoint selection, test-time performance evaluation]*
- What do I do when I have multiple trained checkpoints with different architectural variants (e.g., pooling strategies) and want to find the best infer  *[architectural variants, checkpoint selection, inference configuration, pooling strategy]*
- What do I do when I have multiple trained model checkpoints and library versions and need to select which to deploy in an inference notebook?  *[multiple checkpoints available, library version selection, deployment decision, inference notebook]*
## 22 items, 14 kernels
- What do I do when I have fold-level predictions from two transformer families and want to combine them?  *[cross-family ensemble, fold-level predictions, transformer combination, blend strategy]*
- What do I do when I have many base model predictions and want to find the best way to combine them into a final prediction?  *[prediction combination, ensemble aggregation method, base model predictions]*
- What do I do when I have many transformer model predictions and want to find the best blend composition?  *[transformer models, blend composition, ensemble weighting, multiple predictions available]*
- What do I do when I have multiple diverse base model OOF predictions and need to combine them into a final prediction?  *[diverse base models, oof prediction combination, ensemble blending]*
- What do I do when I have multiple diverse model predictions and need to find the best way to combine them?  *[diverse model predictions, prediction combination strategy, ensemble blending]*
- What do I do when I have multiple diverse models producing predictions and want to combine them optimally?  *[diverse model predictions, optimal combination, ensemble blending]*
- What do I do when I have multiple external prediction sources available for stacking and need to decide which combination improves the ensemble?  *[external predictions, stacking combination, ensemble member selection, contribution test]*
- What do I do when I have multiple fold models and need to choose how to combine their predictions?  *[fold model predictions, prediction combination strategy, ensemble blending]*
- What do I do when I have multiple fold-level model predictions and want to improve beyond a simple average?  *[fold-level predictions, beyond simple average, ensemble weighting]*
- What do I do when I have multiple model predictions and need to find the best way to combine them?  *[prediction combination, ensemble blend optimization, multiple model predictions]*
- What do I do when I have multiple team members' probability predictions and want to improve ensemble quality beyond simple probability averaging?  *[team member predictions, ensemble strategy, beyond simple averaging]*
- What do I do when I have multiple transformer models trained with different seeds/folds and I'm currently just averaging their predictions?  *[prediction averaging, multiple seeds, ensemble composition, transformer models]*
## 21 items, 12 kernels
- What do I do when I have a new model variant that I want to test but it requires a different inference pipeline?  *[new model variant, inference pipeline change, pipeline adaptation]*
- What do I do when I have a new pretrained model variant that shares a feature schema with an existing model but needs its own inference path?  *[new model variant, shared feature schema, inference pipeline adaptation]*
- What do I do when I have new model artifacts to integrate into an inference pipeline but am unsure they work correctly?  *[new model artifacts, inference pipeline integration, correctness verification]*
- What do I do when I need to iterate quickly on a complex multi-model inference notebook that is slow and memory-heavy?  *[multi-model inference, memory constraints, notebook iteration speed, pipeline optimization]*
- What do I do when I need to replace a monolithic heavy model with a multi-model ensemble pipeline in a Kaggle inference kernel?  *[monolithic to ensemble, multi-model pipeline, inference kernel constraints, architecture migration]*
- What do I do when I want to integrate a completely new model framework into an existing inference pipeline?  *[new model framework, pipeline integration, inference pipeline]*
- What do I do when I want to integrate a major new component (new model) into a complex inference pipeline without risking a broken submission?  *[new model integration, complex inference pipeline, submission safety, incremental integration]*
- What do I do when I want to integrate a new feature into an inference pipeline that requires multiple coordinated code changes?  *[new feature integration, coordinated code changes, inference pipeline, multi-step refactor]*
- What do I do when I want to integrate a new model variant into an existing inference pipeline?  *[new model variant, inference pipeline integration, pipeline extension]*
- What do I do when I want to safely introduce a new component into a complex inference pipeline?  *[new component integration, inference pipeline, safe introduction, regression prevention]*
- What do I do when a new model component is ready but its code path was disabled during development?  *[disabled code path, model component activation, inference pipeline integration]*
- What do I do when assembling multiple pretrained models from different source notebooks into a single inference pipeline that fails to run?  *[multi-model assembly, inference pipeline failure, notebook integration]*
## 20 items, 8 kernels
- What do I do when I have a Ridge-based stacking meta-learner and want to know if L1 regularization (sparsity) would improve generalization?  *[stacking meta-learner, regularization type selection, l1 vs l2 regularization, generalization improvement]*
- What do I do when I have a ridge-stacked ensemble over multiple folds and want to improve it by changing which folds and base models participate?  *[ridge stacking, fold selection, base model selection, ensemble composition]*
- What do I do when I have a working stacked ensemble (neural + GBDT) and want to improve it further?  *[stacked ensemble, ensemble improvement, neural gbdt combination]*
- What do I do when I have both a meta-learner (ridge stacking) and raw transformer predictions and need to decide how to combine them?  *[stacking vs raw predictions, meta-learner combination, ridge stacking, ensemble strategy selection]*
- What do I do when I have fold-level ridge meta-models stacking transformer logits and predictions, and I want to improve beyond the stacked output?  *[stacking output improvement, ridge meta-model, post-stacking gains, ensemble refinement]*
- What do I do when I have many diverse base models feeding into a stacking ensembler and want to improve ensemble quality?  *[stacking ensemble, diverse base models, ensemble quality improvement]*
- What do I do when I have multiple model predictions and a meta-learner and want to find the best way to combine them?  *[meta-learner stacking, prediction combination, ensemble blend optimization]*
- What do I do when I have multiple pretrained model predictions and need to choose a meta-learner for stacking?  *[multiple model predictions, meta-learner selection, stacking strategy]*
- What do I do when I have two independently-trained meta-learners (ensemblers) and want to combine them for a better final prediction?  *[meta-learner combination, stacking ensemble, prediction blending]*
- What do I do when I want to enrich a stacking ensemble's inputs beyond the base model predictions?  *[stacking ensemble, meta-feature enrichment, input augmentation]*
- What do I do when I want to improve a classical regressor ensemble used as a stacking meta-learner?  *[stacking meta-learner improvement, classical regressor ensemble, meta-learner selection]*
- What do I do when I want to simplify the stacking/blending head of a transformer ensemble?  *[stacking head simplification, transformer ensemble, blending architecture]*
## 20 items, 16 kernels
- What do I do when I have a new, larger pretrained model available and want to test whether it improves an already-strong ensemble?  *[larger pretrained model, ensemble integration, contribution test, strong baseline]*
- What do I do when I have a new, stronger pretrained model available and an existing Spearman-optimized weighted ensemble?  *[stronger pretrained model, weighted ensemble, ensemble integration, ranking metric optimization]*
- What do I do when I have multiple gradient boosting models and want to maximize QWK on an ordinal scoring task?  *[gradient boosting models, qwk optimization, ordinal scoring, ensemble blending]*
- What do I do when I have multiple model backbones of different sizes available for a video/3D CNN ensemble member?  *[backbone selection, model size tradeoff, ensemble member selection, video model]*
- What do I do when I have multiple pre-trained meta-learner artifacts (trained offline) and want to find which one works best in the inference ensemble  *[pretrained meta-learner artifacts, meta-learner selection, ensemble member selection]*
- What do I do when I need to blend predictions from models with different architectures or training configurations?  *[prediction blending, heterogeneous models, ensemble weighting]*
- What do I do when I want to combine predictions from a neural model and a gradient boosting model?  *[heterogeneous model blending, neural and gbdt ensemble, prediction combination]*
- What do I do when I want to combine two fundamentally different prediction approaches (gradient-boosted features vs. neural inference ensemble) into o  *[heterogeneous model blending, submission pipeline, gbdt and neural ensemble]*
- What do I do when I've just added new ensemble members and want to improve the meta-learner's performance?  *[new ensemble members, meta-learner tuning, stacking optimization]*
- What do I do when a new pretrained model becomes available and I want to add it to an existing multi-model ensemble?  *[new pretrained model available, ensemble member addition, multi-model ensemble]*
- What do I do when adding pre-trained base learners to a stacking ensemble alongside a newly-trained model?  *[pretrained base learners, stacking ensemble, ensemble member integration, new model addition]*
- What do I do when blending DeBERTa regressors for essay scoring and I have models trained with different objectives or preprocessing?  *[model blending, heterogeneous training objectives, ensemble compatibility]*
## 18 items, 11 kernels
- What do I do when I change the model or ensemble strategy and have a post-processing step with tuned hyperparameters?  *[model change, ensemble strategy change, post-processing retuning, hyperparameter dependency]*
- What do I do when I discover a bug or mismatch during an ensemble tuning sweep?  *[bug discovery, ensemble tuning, sweep debugging]*
- What do I do when I have multiple trained checkpoints and adding more members to the ensemble is hurting rather than helping?  *[ensemble score regression, diminishing ensemble returns, ensemble member pruning]*
- What do I do when I want to add a new ensembling strategy but it requires changes to the model architecture?  *[ensembling strategy change, architecture modification, ensemble method design]*
- What do I do when I want to improve an ensemble score but am unsure whether to change models, features, or tuning?  *[improvement strategy selection, ensemble improvement, models vs features vs tuning]*
- What do I do when I want to improve my score but individual model tuning is yielding diminishing returns?  *[diminishing returns, model tuning plateau, ensemble strategy shift]*
- What do I do when I've tested multiple individual model variants and none consistently beats my best score?  *[model variant comparison, no consistent improvement, ensemble strategy]*
- What do I do when a new model gives a big score jump but adding variants of it yields diminishing returns?  *[diminishing returns, model variant exploration, ensemble diversity]*
- What do I do when adding more base models to a Ridge-stacked ensemble yields diminishing returns?  *[diminishing returns, stacking ensemble, ensemble expansion, base model diversity]*
- What do I do when each new ensemble member yields diminishing marginal gains?  *[diminishing returns, ensemble member addition, marginal gain analysis]*
- What do I do when fold-ensemble gains are diminishing but I haven't saturated my submission budget?  *[diminishing returns, fold ensemble saturation, submission budget remaining, exploration strategy]*
- What do I do when multi-seed ensembling yields only marginal improvement on top of an already-ensembled model?  *[marginal improvement, multi-seed ensembling, diminishing returns, ensemble strategy]*
## 18 items, 8 kernels
- What do I do when I have a feature selection step with an arbitrary hard cap on feature count?  *[feature count threshold, feature selection, hard cap tuning]*
- What do I do when I have a feature that was previously removed/disabled and I want to know if it helps the current improved pipeline?  *[feature re-evaluation, previously removed feature, pipeline improvement, feature selection]*
- What do I do when I have a hand-crafted heuristic feature that improved my score and I want to test a variant of it?  *[heuristic feature variant, feature engineering iteration, feature ablation]*
- What do I do when I have a high-dimensional feature set with a feature-importance-based selection cutoff and want to find the optimal number of featur  *[feature selection cutoff, optimal feature count, high-dimensional features, feature importance threshold]*
- What do I do when I have a large candidate set of features to remove based on importance analysis?  *[feature removal, importance analysis, feature pruning, candidate feature set]*
- What do I do when I have a set of aggregation functions and want to know which combination maximizes performance?  *[aggregation function selection, feature combination search, performance maximization]*
- What do I do when I have importance-based feature selection and need to find the right fraction of features to keep?  *[feature selection threshold, importance-based selection, feature fraction tuning]*
- What do I do when I have many correlated text-derived features (same metric computed on multiple preprocessing variants) and want to find the best sub  *[correlated features, feature subset selection, text-derived features]*
- What do I do when I need to find the right fraction of features to keep from an importance-based filter?  *[feature selection threshold, importance-based filtering, feature fraction tuning]*
- What do I do when I want to add a batch of new engineered features but am unsure which ones help?  *[feature selection, batch feature evaluation, engineered feature evaluation]*
- What do I do when I want to test whether a specific feature group is helping or hurting the model?  *[feature group ablation, feature selection, contribution test]*
- What do I do when I'm exploring multiple new feature ideas and need to decide which to keep?  *[feature selection, multiple feature ideas, feature contribution analysis]*
## 17 items, 13 kernels
- What do I do when I change two hyperparameters at once and see a large improvement?  *[score improvement, multiple hyperparameter changes, ablation study]*
- What do I do when I changed two hyperparameters at once and got an improvement, but I'm unsure which change helped?  *[score improvement, multiple hyperparameter changes, attribution uncertainty, ablation study]*
- What do I do when I have a multi-component pipeline (ensemble + postprocessing) and want to verify each component's contribution before committing?  *[component contribution verification, ensemble plus postprocessing, ablation study, pipeline validation]*
- What do I do when I have a new best score and want to confirm whether a specific inference technique (like flip TTA) is helping or hurting?  *[new best score, test-time augmentation, inference technique evaluation, contribution test]*
- What do I do when I have a novel architectural idea that changes both input representation and model structure simultaneously?  *[novel architecture, input representation change, joint structural change, ablation study]*
- What do I do when I have a post-processing step enabled by default and I'm unsure whether it helps the current pipeline configuration?  *[post-processing step, ablation study, pipeline configuration]*
- What do I do when I have achieved a new best score with a large ensemble and want to see if a leaner configuration can match or beat it?  *[ensemble size reduction, lean configuration search, new best score, ablation study]*
- What do I do when I suspect a post-processing step (e.g., weighted ensemble) may not be helping and want to verify quickly?  *[post-processing validation, weighted ensemble, ablation study]*
- What do I do when I want to compare two alternative inference pipelines on the same model checkpoint?  *[inference pipeline comparison, same checkpoint, pipeline ablation]*
- What do I do when I want to test whether a new idea (e.g., class-imbalance handling or text normalization) helps?  *[new idea validation, class imbalance handling, text normalization, ablation study]*
- What do I do when I want to test whether a variance-reduction technique (multi-seed averaging) is actually helping after achieving a new best score?  *[variance reduction validation, multi-seed averaging, new best score, ablation study]*
- What do I do when I want to verify whether a recently improved configuration is truly better than a simpler alternative?  *[configuration comparison, ablation study, simpler baseline check]*
## 17 items, 10 kernels
- What do I do when I have a GBDT baseline and want to quickly find a better regularization setting?  *[regularization tuning, gbdt baseline, quick hyperparameter search]*
- What do I do when I have a working CV pipeline with a modest GBDT score and want to improve it through model configuration?  *[model configuration tuning, gbdt improvement, cross-validation pipeline]*
- What do I do when I have multiple GBDT models in an ensemble sharing generic hyperparameters, and I want to squeeze out more performance?  *[gbdt ensemble, shared hyperparameters, hyperparameter tuning, performance squeeze]*
- What do I do when I need to find the optimal learning rate for a gradient boosting model with early stopping?  *[learning rate tuning, gradient boosting, early stopping, hyperparameter search]*
- What do I do when I want to find the best boosting type and tree hyperparameters for a GBDT model?  *[gbdt hyperparameter tuning, boosting type selection, tree hyperparameters]*
- What do I do when I want to find the best tree depth for a GBDT model on a tabular classification task?  *[tree depth tuning, gbdt hyperparameter search, tabular classification]*
- What do I do when I want to rapidly iterate on GBDT hyperparameters without wasting compute?  *[gbdt hyperparameter tuning, compute efficiency, rapid iteration]*
- What do I do when I want to speed up a GBDT ensemble pipeline that uses many CV folds?  *[inference speedup, gbdt ensemble, cv fold reduction]*
- What do I do when building an initial GBDT baseline on a large tabular dataset and I need to find reasonable hyperparameters quickly?  *[gbdt baseline, large tabular dataset, hyperparameter search, quick iteration]*
- What do I do when increasing tree model capacity (num_leaves) to improve a GBDT model's contribution to an ensemble?  *[model capacity tuning, GBDT num_leaves, tree model complexity, ensemble contribution]*
- What do I do when my GBDT model's default tree complexity seems insufficient and I want to increase capacity?  *[tree complexity, model capacity, gbdt hyperparameter tuning, tree depth]*
- What do I do when my ensemble of GBDT models shows a score regression and I suspect the individual model configs are suboptimal?  *[score regression, gbdt config tuning, hyperparameter search]*
## 17 items, 12 kernels
- What do I do when I have a GBDT ensemble that may be overfitting and I want to find the right complexity level?  *[overfitting mitigation, gbdt complexity tuning, regularization search, ensemble pruning]*
- What do I do when I have a working GBDT ensemble with basic features and want to improve concordance on a survival prediction task?  *[feature engineering, survival prediction, concordance metric, gbdt ensemble]*
- What do I do when I suspect my tree-based model is overfitting and want to test regularization strength?  *[overfitting, regularization tuning, tree-based model]*
- What do I do when I want to find the right number of boosting rounds for a gradient boosting model without automated early stopping?  *[boosting rounds tuning, gradient boosting, manual early stopping, iteration count selection]*
- What do I do when I want to tune the patience parameter for early stopping in a gradient boosting model?  *[early stopping patience, hyperparameter tuning, gradient boosting]*
- What do I do when I want to use the competition's custom metric as the training objective/eval metric for a GBDT?  *[custom metric, training objective, gbdt configuration, eval metric alignment]*
- What do I do when I've added early stopping to a gradient boosting model but I'm not sure it helps?  *[early stopping, gradient boosting, regularization ablation]*
- What do I do when ensemble averaging shows diminishing returns in a GBDT/NN survival prediction pipeline?  *[diminishing returns, ensemble averaging, gbdt nn pipeline, survival prediction]*
- What do I do when my GBDT model may be overfitting and I want to find the right regularization strength?  *[overfitting, regularization strength, gbdt hyperparameter tuning]*
- What do I do when my GBDT model may be underfitting because the number of boosting rounds is too low?  *[underfitting, boosting rounds, gbdt hyperparameter tuning, model capacity]*
- What do I do when my GBDT model trains too slowly with many low-learning-rate boosting rounds?  *[training speed, learning rate schedule, gbdt hyperparameter tuning, boosting rounds]*
- What do I do when my GBDT model uses a small manually-selected feature subset and scores poorly?  *[poor feature subset, feature selection, gbdt underperformance, manual feature choice]*
## 17 items, 13 kernels
- What do I do when I change multiple things at once and want to confirm the improvement is real before iterating further?  *[multiple simultaneous changes, score improvement validation, ablation study]*
- What do I do when I have multiple untested changes (new features, bug fixes, hyperparameter changes) accumulated without evaluation?  *[accumulated changes, missing evaluation, ablation study, change isolation]*
- What do I do when I introduce a new technique and need to confirm it actually helps versus confounded checkpoint changes?  *[technique validation, confounded changes, ablation study]*
- What do I do when I need to disentangle the effect of multiple simultaneous changes?  *[isolating change effects, ablation study, multiple simultaneous changes]*
- What do I do when I want to make two coupled changes (add a data source and adjust a capacity parameter) but need to understand their individual effec  *[coupled changes, ablation study, individual effect isolation, data source and capacity]*
- What do I do when I want to reliably measure the impact of a single change on leaderboard score?  *[single change measurement, leaderboard score impact, controlled experiment, ablation study]*
- What do I do when I want to test multiple changes (feature flags, callbacks, regularization) but need to isolate which change helps?  *[multiple simultaneous changes, change isolation, ablation study, improvement attribution]*
- What do I do when I want to test multiple changes but need to attribute improvements correctly?  *[multiple simultaneous changes, improvement attribution, ablation study, change isolation]*
- What do I do when I want to test whether a recent change actually helped, by reverting it alongside another change?  *[change reversion, ablation study, confounded changes, score validation]*
- What do I do when I want to test whether a recently added component (augmentation) is actually helping?  *[augmentation contribution, ablation study, component validation]*
- What do I do when I want to test whether two changes each help, but I changed them simultaneously and got a regression?  *[confounded experiment, score regression, simultaneous changes, ablation study]*
- What do I do when I'm changing multiple things at once and can't tell which change helped or hurt?  *[multiple simultaneous changes, change attribution, ablation study]*
## 16 items, 8 kernels
- What do I do when I have a model that processes multi-channel EEG arranged in a spatial grid and want cheap test-time augmentation?  *[test-time augmentation, spatial grid input, eeg signal processing, low-cost augmentation]*
- What do I do when I have a model trained on spectrograms generated from raw signals and want to improve its inference-time performance?  *[spectrogram model, inference-time improvement, test-time augmentation, signal-derived input]*
- What do I do when I have a trained image classification ensemble and want a quick inference-time accuracy boost without retraining?  *[test-time augmentation, inference-time boost, image classification ensemble, no retraining]*
- What do I do when I have already benefited from spatial flip TTA on image inputs and want further gains from multi-modal data that has its own spatial  *[test-time augmentation, multi-modal spatial symmetry, flip augmentation extension]*
- What do I do when I have multiple inference paths in an ensemble and some already use test-time augmentation but others do not?  *[test-time augmentation, inconsistent augmentation, ensemble component alignment, inference path standardization]*
- What do I do when I have test-time augmentation and post-processing (softmax) applied outside the model in a multi-model ensemble pipeline?  *[test-time augmentation, post-processing pipeline, multi-model ensemble]*
- What do I do when I want to add MC-dropout or multi-sample inference to a transformer regression model?  *[mc-dropout, test-time augmentation, transformer regression, uncertainty estimation]*
- What do I do when I want to know whether a specific augmentation/TTA toggle helps or hurts the current ensemble?  *[test-time augmentation, ablation study, ensemble impact, augmentation toggle]*
- What do I do when I want to know whether multi-view test-time augmentation helps an ensemble of models that were trained on center crops only?  *[test-time augmentation, multi-view tta, training-inference mismatch, center crop models]*
- What do I do when I want to squeeze more performance from an ensemble that already includes multiple models and image-level TTA?  *[marginal gain extraction, ensemble saturation, test-time augmentation, advanced tta strategy]*
- What do I do when I'm unsure whether flip test-time augmentation helps my spectrogram/EEG ensemble?  *[test-time augmentation, flip augmentation, spectrogram eeg ensemble, ablation test]*
- What do I do when I'm unsure whether test-time augmentation helps or hurts a given checkpoint?  *[test-time augmentation, checkpoint evaluation, augmentation ablation]*
## 16 items, 13 kernels
- What do I do when I have a single GBDT model scoring well on a survival/ranking metric and want to improve further?  *[single model baseline, gbdt model, survival ranking metric, score improvement]*
- What do I do when I have a single fine-tuned transformer model and want to improve leaderboard score beyond what post-processing and feature engineeri  *[single model baseline, fine-tuned transformer, score plateau, ensemble expansion]*
- What do I do when I have a single gradient-boosted model and want a meaningful score improvement?  *[single model baseline, gradient boosted model, score improvement]*
- What do I do when I have a single-model inference pipeline and want a quick accuracy boost before exploring ensembles?  *[single model baseline, quick accuracy boost, pre-ensemble improvement]*
- What do I do when I have a strong single-fold model and want to push the score higher without retraining?  *[strong single model, post-training optimization, score improvement without retraining]*
- What do I do when I have a well-tuned base-size model and want to push the score higher?  *[model scaling, strong baseline, larger model capacity, incremental improvement]*
- What do I do when I have a well-tuned feature set and want to check whether model capacity is limiting performance?  *[model capacity, performance plateau, architecture scaling, well-tuned features]*
- What do I do when I have a well-tuned pipeline and want a significant accuracy jump beyond hyperparameter/postprocessing tweaks?  *[well-tuned pipeline, performance plateau, architectural change, significant accuracy jump]*
- What do I do when I have a working GBDT ensemble and want to push the score higher?  *[score improvement, gbdt ensemble, pushing score higher]*
- What do I do when I have a working ensemble of two prediction sources and want to squeeze out marginal gains without retraining?  *[marginal gains, ensemble weighting, no retraining, post-hoc optimization]*
- What do I do when I have a working fold-averaged ensemble and want incremental improvement without retraining?  *[incremental improvement, fold ensemble, no retraining, post-hoc optimization]*
- What do I do when I want to maximize score from a promising model family through incremental refinements?  *[incremental refinement, hyperparameter tuning, promising model family, score maximization]*
## 16 items, 10 kernels
- What do I do when I have a model trained on noisy data and a variant trained on cleaned data, and I want to decide which to use in an ensemble?  *[noisy vs cleaned data, data cleaning impact, ensemble member selection, training data quality]*
- What do I do when I have a neural network that works well and want to extract more value from it in an ensemble?  *[strong neural network, ensemble integration, value extraction, ensemble member selection]*
- What do I do when I have many candidate ensemble members and need to find the best subset and weights for a final blend?  *[ensemble member selection, ensemble weight optimization, subset search]*
- What do I do when I have many model families in an ensemble and want to identify which ones are helping vs hurting?  *[ensemble member selection, model family contribution, ensemble pruning]*
- What do I do when I have multiple model families in an ensemble and want to find the best subset?  *[ensemble subset selection, multiple model families, ensemble pruning]*
- What do I do when I have several candidate components to combine and need to find the best subset?  *[subset selection, candidate components, ensemble optimization]*
- What do I do when I want to add a new ensemble member but previous additions have been hit-or-miss?  *[new ensemble member, inconsistent improvements, ensemble member selection]*
- What do I do when I want to test whether a simpler ensemble method can replace a more complex one?  *[ensemble simplification, complexity reduction, ensemble method selection]*
- What do I do when I've been incrementally improving an ensemble by swapping/adding members and want to find the best subset?  *[ensemble subset selection, incremental ensemble improvement, member swapping]*
- What do I do when a complex multi-group weighted ensemble doesn't beat my previous best score?  *[no score improvement, weighted ensemble, ensemble member selection]*
- What do I do when adding a larger ViT backbone to an equal-weight ensemble doesn't improve the score?  *[no improvement, larger backbone addition, equal-weight ensemble, ensemble member selection]*
- What do I do when adding a new ensemble member (e.g., bi-encoder retrieval features) sometimes helps and sometimes hurts?  *[inconsistent improvement, ensemble member addition, ensemble member selection, robustness evaluation]*
## 15 items, 13 kernels
- What do I do when I have accumulated many incremental experiments with mixed results and scores have plateaued?  *[score plateau, experiment consolidation, mixed results, strategy reassessment]*
- What do I do when I have multiple trained checkpoints and my single-model score has plateaued after many re-runs?  *[score plateau, single model saturation, multiple checkpoints available]*
- What do I do when a major refactor produces scores close to but not better than the previous best?  *[score plateau, code refactor, marginal improvement]*
- What do I do when a series of incremental configuration changes all fail to beat my previous best score?  *[no improvement, incremental configuration changes, plateau, best score baseline]*
- What do I do when a series of tweaks all fail to beat my current best score?  *[no improvement, incremental tweaks, plateau, best score baseline]*
- What do I do when multiple different changes all produce the exact same leaderboard score?  *[score plateau, identical scores, leaderboard stagnation, change ineffectiveness]*
- What do I do when multiple incremental changes yield no score improvement?  *[score plateau, incremental changes, no improvement, strategy reassessment]*
- What do I do when multiple iterations of tuning one lever fail to beat a previous best score?  *[score plateau, single lever tuning, repeated failed experiments, diminishing returns]*
- What do I do when multiple small changes to different components all fail to improve a plateau score?  *[score plateau, multiple component changes, failed improvements, strategy reassessment]*
- What do I do when my current model family seems to have plateaued and I want to explore whether a fundamentally different approach could help?  *[score plateau, model family exploration, alternative approach, paradigm shift]*
- What do I do when several attempted improvements all fail to beat my best score?  *[score plateau, multiple failed improvements, strategy reassessment]*
- What do I do when single-model checkpoint swaps fail to improve over my best score?  *[score plateau, checkpoint swap failure, single model limitation]*
## 15 items, 12 kernels
- What do I do when I have a known reference score and my current approach is far below it?  *[score gap, reference score comparison, approach improvement, underperformance diagnosis]*
- What do I do when a new approach consistently underperforms my current best after several submissions?  *[score regression, new approach underperformance, repeated submission failure, revert to best]*
- What do I do when a new feature engineering idea produces multiple variants and early submissions show regression from the best score?  *[score regression, feature engineering, variant selection, repeated submission failure]*
- What do I do when a new feature idea produces scores below my best baseline after multiple submission attempts?  *[score regression, feature engineering, repeated submission failure, baseline comparison]*
- What do I do when a new feature/preprocessing idea consistently underperforms my existing best across multiple configurations?  *[score regression, feature engineering, preprocessing change, repeated submission failure, revert to best]*
- What do I do when a new idea produces scores well below my current best across multiple configurations?  *[score regression, new approach underperformance, repeated submission failure, revert to best]*
- What do I do when a new model's first submission underperforms the existing best?  *[score regression, new model underperformance, submission evaluation]*
- What do I do when a rank-based metric returns a near-zero or negative score after my first submission?  *[near-zero score, rank-based metric, first submission, prediction debugging]*
- What do I do when my first submission scores far below what I expect given the model quality?  *[score regression, first submission gap, train-inference mismatch]*
- What do I do when my initial baseline model scores very poorly relative to competitive solutions?  *[poor baseline score, competitive gap, model improvement strategy]*
- What do I do when my initial submission produces a near-zero or negative score, suggesting predictions are essentially meaningless?  *[near-zero score, broken predictions, initial submission debugging]*
- What do I do when my initial submission score is drastically lower than expected, suggesting broken predictions rather than a weak model?  *[score regression, broken predictions, initial submission debugging]*
## 15 items, 14 kernels
- What do I do when I want to make a large improvement and have been iterating on post-processing and checkpoint selection with diminishing returns?  *[diminishing returns, post-processing plateau, strategy pivot, large improvement search]*
- What do I do when I want to test a qualitatively new idea (data cleaning) after exhausting hyperparameter tuning?  *[new qualitative idea, hyperparameter tuning exhaustion, data cleaning, exploration after plateau]*
- What do I do when I'm stuck at a plateau and multiple small hyperparameter tweaks all produce worse leaderboard scores?  *[performance plateau, hyperparameter tuning, score regression, search strategy]*
- What do I do when I'm stuck at a plateau and multiple small parameter tweaks keep producing regressions?  *[performance plateau, parameter tuning, score regression, search strategy]*
- What do I do when I'm stuck on a plateau and have multiple configuration knobs (model type, blending, preprocessing) to try?  *[performance plateau, multiple configuration knobs, search strategy, exploration prioritization]*
- What do I do when continuous hyperparameter sweeps have plateaued and I need a qualitatively different improvement?  *[hyperparameter tuning plateau, qualitative improvement, strategy shift]*
- What do I do when feature engineering improvements have plateaued and I haven't yet tuned model hyperparameters?  *[feature engineering plateau, hyperparameter tuning, workflow transition]*
- What do I do when hyperparameter/blend-weight tuning has plateaued and I want further improvement?  *[tuning plateau, blend weight tuning, hyperparameter tuning, new improvement strategy]*
- What do I do when incremental augmentation tuning yields diminishing or negative returns?  *[diminishing returns, augmentation tuning, incremental tuning plateau]*
- What do I do when incremental single-variable changes yield negligible improvements?  *[negligible improvement, single variable tuning, incremental tuning plateau, new improvement strategy]*
- What do I do when incremental tuning of existing components stops yielding improvements?  *[tuning plateau, incremental tuning saturation, new component exploration]*
- What do I do when incremental tuning of the same hyperparameter has plateaued but I still want score gains?  *[tuning plateau, hyperparameter tuning, single parameter saturation, new improvement strategy]*
## 15 items, 10 kernels
- What do I do when I have a new set of engineered features (e.g., from text preprocessing) and need to determine whether they help a tree-based ensembl  *[new engineered features, feature selection, tree-based ensemble, contribution test]*
- What do I do when I have a strong ensemble and want to test whether a novel feature type improves it?  *[strong ensemble, novel feature type, feature engineering, contribution test]*
- What do I do when I have a working baseline and want to test whether adding a batch of new engineered features improves performance?  *[new features batch, feature engineering, contribution test]*
- What do I do when I have pre-trained pipelines using different target transformations for a new model family and want to improve an ensemble?  *[target transformation diversity, new model family, ensemble improvement, pipeline integration]*
- What do I do when I want to add a fundamentally new model component (e.g., transformer predictions) to an existing GBDT pipeline?  *[new model component, heterogeneous pipeline, transformer integration, gbdt pipeline]*
- What do I do when I want to add a new feature representation to an already-strong ensemble?  *[new feature representation, strong ensemble augmentation, feature diversity]*
- What do I do when I want to add a new feature source to an existing ensemble pipeline in a Kaggle notebook with offline dependencies?  *[new feature source, offline dependencies, kaggle notebook constraints, ensemble pipeline]*
- What do I do when I want to add a new model component to an ensemble but the pipeline is cluttered with inline feature generation code?  *[new model component, code refactoring, pipeline organization, ensemble expansion]*
- What do I do when I want to add a new model type to an existing ensemble pipeline?  *[new model type, ensemble expansion, pipeline integration]*
- What do I do when I want to add a new signal source (e.g., transformer predictions) to an existing tabular pipeline?  *[new signal source, feature integration, tabular pipeline, stacking features]*
- What do I do when I want to test a new spectrogram representation (e.g., multitaper) in an existing ensemble?  *[new feature representation, ensemble integration, spectrogram variant]*
- What do I do when I want to test whether a new feature source improves a stacked ensemble?  *[new feature source, stacked ensemble, feature contribution test]*
## 15 items, 13 kernels
- What do I do when I have a new modeling approach (e.g., prompt-based inference) and want to know if it improves over my current best pipeline?  *[new modeling approach, pipeline comparison, baseline benchmark]*
- What do I do when I have many model variants and need to quickly test whether a new pipeline is competitive?  *[pipeline competitiveness, rapid evaluation, model variant comparison]*
- What do I do when I inherit or fork an existing pipeline and need to understand its true performance before investing effort in improvements?  *[forked pipeline, baseline performance, pipeline understanding]*
- What do I do when I need to ensure my pipeline produces stable results before building on top of it?  *[pipeline stability, reproducibility verification, baseline validation]*
- What do I do when I need to restructure a complex multi-model pipeline without losing my current best score?  *[pipeline restructuring, multi-model pipeline, score preservation, regression prevention]*
- What do I do when I want to quickly test whether a simpler pipeline outperforms a more complex one?  *[pipeline complexity comparison, simple vs complex, quick validation]*
- What do I do when I want to substantially upgrade a pipeline from simple tabular features to a complex multi-source feature + multi-model ensemble?  *[pipeline upgrade, multi-source features, multi-model ensemble, tabular to complex transition]*
- What do I do when I've found a good hyperparameter setting but want to improve further and my training pipeline lacks proper evaluation and ensembling  *[pipeline infrastructure, evaluation setup, ensembling infrastructure, hyperparameter plateau]*
- What do I do when I've refactored my inference pipeline and need to verify it reproduces prior performance before making further changes?  *[pipeline refactoring, reproducibility check, baseline verification]*
- What do I do when building a complex ensemble pipeline from scratch in a competition?  *[ensemble pipeline construction, pipeline from scratch, competition workflow]*
- What do I do when building a new ML pipeline from scratch for a competition with a custom metric and large data?  *[pipeline from scratch, custom metric, large dataset, competition setup]*
- What do I do when building a new competition pipeline from scratch and I want to iterate quickly while still producing valid submissions?  *[pipeline from scratch, rapid iteration, valid submission, competition setup]*
## 14 items, 12 kernels
- What do I do when I have a working fine-tuned model and want to know if a different checkpoint or model size improves test performance?  *[checkpoint comparison, model size selection, test performance evaluation]*
- What do I do when I have many saved checkpoints from different folds, epochs, and training runs and need to find the best single one for submission?  *[checkpoint selection, best single model, multi-fold multi-epoch candidates]*
- What do I do when I have multiple saved checkpoints and want to know if ensembling them beats the best single one?  *[multiple checkpoints, ensemble versus single model, checkpoint ensembling]*
- What do I do when I have multiple trained fold checkpoints and need to decide whether to ensemble them or pick the best single one?  *[fold checkpoints available, ensemble vs single model, ensemble member selection]*
- What do I do when I have multiple trained model variants and need to find which one scores best on the leaderboard?  *[model variant comparison, leaderboard evaluation, checkpoint selection]*
- What do I do when I need to verify that each fold checkpoint in a multi-fold model loads and produces reasonable predictions?  *[checkpoint validation, multi-fold model, prediction sanity check, model loading verification]*
- What do I do when I want to compare two model families fairly in a CV pipeline?  *[model family comparison, fair evaluation, cross-validation pipeline]*
- What do I do when I want to determine the best single-seed checkpoint from a set of seed-varied training runs?  *[checkpoint selection, seed variation, best single model, local validation]*
- What do I do when I want to evaluate whether a different model family improves over my current baseline?  *[model family selection, baseline comparison, model evaluation]*
- What do I do when I want to test whether an alternative algorithm variant improves over a working baseline?  *[algorithm variant comparison, baseline comparison, model selection]*
- What do I do when a model component is trained without proper cross-validation and per-fold persistence, limiting its reliability as an ensemble membe  *[cross-validation, model persistence, ensemble member reliability, training methodology]*
- What do I do when individual checkpoint scores plateau or I've exhausted my best single-model options?  *[checkpoint score plateau, single model saturation, ensemble member selection, new model exploration]*
## 14 items, 10 kernels
- What do I do when I add many new features at once and the notebook fails to produce a submission?  *[submission failure, batch feature addition, pipeline debugging]*
- What do I do when I make a large code change but the submission fails or isn't recognized?  *[submission failure, large code change, error diagnosis]*
- What do I do when a configuration change doesn't get submitted and I suspect a silent error?  *[submission failure, silent error, configuration change, bug diagnosis]*
- What do I do when a large code change doesn't produce a submission?  *[submission failure, large code change, debugging pipeline]*
- What do I do when a large expansion (many new features, models, and hyperparameters) doesn't produce a submittable result?  *[submission failure, feature expansion, large code change, debugging pipeline]*
- What do I do when a major code refactor introduces runtime failures and I need to debug before submitting?  *[runtime failure, code refactor, debugging, submission readiness]*
- What do I do when a new configuration change doesn't produce a submission or produces suspicious results?  *[submission failure, configuration change, suspicious results, debugging]*
- What do I do when a new experiment variant fails to produce a submission (not submitted)?  *[submission failure, experiment variant, debugging, pipeline error]*
- What do I do when a new inference pipeline variant fails to run or submit on the first try?  *[submission failure, inference pipeline debugging, new variant integration]*
- What do I do when a notebook version fails to submit (runtime error) after making structural changes?  *[submission failure, runtime error, structural change debugging]*
- What do I do when a submission attempt fails or is not submitted?  *[submission failure, submission pipeline, error diagnosis]*
- What do I do when an experimental model swap produces no submission and likely poor or broken validation results?  *[broken submission, model swap, validation failure]*
## 14 items, 10 kernels
- What do I do when I have rank-based post-processing (discretization, 0-1 scaling) for a Spearman-correlation metric and want to know if it still helps  *[rank-based postprocessing, spearman correlation, ensemble change, postprocessing validation]*
- What do I do when I need to decide whether to optimize postprocessing thresholds on the full OOF set or a specific subset?  *[threshold optimization, postprocessing, validation subset selection]*
- What do I do when I want to quickly test whether a simple postprocessing idea improves an ensemble score?  *[postprocessing idea, quick validation, ensemble score improvement]*
- What do I do when I want to test whether a two-stage post-processing transform is helping or hurting survival predictions?  *[post-processing ablation, survival prediction, two-stage transform evaluation]*
- What do I do when I'm unsure whether a score problem comes from post-processing or from the model itself?  *[score diagnosis, post-processing vs model, error attribution]*
- What do I do when I'm unsure whether to clip or transform model outputs before writing a submission for a rank-based metric?  *[output clipping, prediction transformation, rank-based metric, submission post-processing]*
- What do I do when a blanket application of a post-processing step causes a regression compared to a selective application?  *[score regression, post-processing strategy, selective vs blanket application, conditional logic]*
- What do I do when a post-processing idea degrades the score through one approach (weighted averaging) and I want to try a different post-processing ap  *[post-processing strategy, score regression, alternative approach, weighted averaging failure]*
- What do I do when my GBDT model's raw output scores need to be converted to probabilities for a ranking-based competition metric?  *[score calibration, probability conversion, ranking metric, gbdt postprocessing]*
- What do I do when my Ridge stacking ensemble's score is sensitive to whether I rank-transform the base model predictions before stacking?  *[rank transformation, stacking ensemble, prediction preprocessing, score sensitivity]*
- What do I do when my ensemble predictions are well-performing but I suspect systematic per-class bias in the predicted probability distribution?  *[per-class bias, probability calibration, ensemble postprocessing]*
- What do I do when my postprocessing (e.g., optimized rounding thresholds) might be overfitting to validation data and hurting leaderboard performance?  *[postprocessing overfitting, rounding threshold optimization, validation vs leaderboard gap]*
## 14 items, 5 kernels
- What do I do when I already compute readability/linguistic features at the document or section level and want more signal?  *[feature granularity, linguistic features, finer-grained features, feature engineering]*
- What do I do when I need to find the right text vectorization settings (frequency thresholds, n-gram ranges) for a tree-based model on essay data?  *[text vectorization tuning, n-gram range selection, frequency threshold, tree-based model]*
- What do I do when I want to add a large new category of features (e.g., NLP-derived linguistic features) to an existing pipeline?  *[new feature category, nlp-derived features, feature pipeline expansion]*
- What do I do when I want to add new text features (spelling, preprocessing, paragraph stats) to an already-tuned LightGBM pipeline?  *[text feature engineering, feature addition, tuned pipeline modification, lightgbm pipeline]*
- What do I do when I want to find which dense text representations help a tree-based model on text scoring?  *[text embedding selection, feature selection, tree-based model, dense text representations]*
- What do I do when I want to give a tree-based model (LightGBM) richer semantic understanding of text beyond bag-of-words and topic features?  *[text feature enrichment, semantic embeddings, lightgbm feature engineering, beyond bag-of-words]*
- What do I do when I want to test whether a complex new feature source (auxiliary data + pretrained embeddings) improves my model?  *[new feature source, auxiliary data, pretrained embeddings, feature contribution test]*
- What do I do when I want to test whether a new category of engineered features improves a well-tuned model?  *[new feature category, feature contribution test, well-tuned model]*
- What do I do when I want to test whether a new hand-crafted feature improves a tree-based model in an NLP regression task?  *[hand-crafted feature, tree-based model, nlp regression, feature contribution test]*
- What do I do when adding NLP-derived sentence features (sentiment, lexical richness) to a TF-IDF + LightGBM essay scoring pipeline?  *[nlp feature engineering, sentence-level features, tfidf lgbm pipeline]*
- What do I do when adding handcrafted linguistic features (NER counts, POS ratios, readability scores) to a LightGBM + transformer-embedding pipeline?  *[handcrafted features, linguistic features, feature engineering, tree-based model]*
- What do I do when adding latent topic features (LDA/LSA/NMF) to a LightGBM text-scoring pipeline?  *[topic model features, feature engineering, text scoring pipeline, tree-based model]*
## 13 items, 9 kernels
- What do I do when I have a multi-component ensemble that achieves a new best score and want to understand whether the ensemble is truly better than it  *[ensemble vs single model, new best score, ensemble contribution analysis, component comparison]*
- What do I do when I have achieved a new best score with a blended ensemble and want to verify the blend is actually better than its components?  *[new best score, ensemble blend validation, component comparison, ablation study]*
- What do I do when I have an ensemble of multiple model variants and want to understand each component's individual contribution?  *[ensemble component contribution, ablation study, model variant analysis]*
- What do I do when I have multiple model groups in an ensemble and want to understand each group's contribution and find the best combination?  *[ensemble contribution analysis, model group selection, ablation study, ensemble composition]*
- What do I do when I want to test whether a sub-component of my ensemble is strong enough to use alone?  *[ensemble sub-component evaluation, standalone model strength, ablation study]*
- What do I do when I want to understand the contribution of individual ensemble members after building a large ensemble?  *[ensemble member contribution, large ensemble analysis, ablation study]*
- What do I do when I want to understand whether an ensemble is actually helping versus a single strong model?  *[ensemble vs single model, ensemble benefit evaluation, ablation study]*
- What do I do when I want to understand whether individual ensemble members outperform the full ensemble?  *[ensemble member contribution, single model comparison, ablation study]*
- What do I do when I want to understand which components of a complex ensemble are actually contributing to performance?  *[ensemble component contribution, complex ensemble analysis, ablation study]*
- What do I do when I want to understand which components of a multi-fold ensemble are strongest or weakest?  *[fold-level analysis, ensemble member contribution, strength assessment]*
- What do I do when I've just set a new best score and want to know whether every component of my ensemble is contributing?  *[new best score, ensemble member ablation, component contribution test]*
- What do I do when a larger ensemble scores better but I want to understand individual model contributions?  *[ensemble improvement, model contribution analysis, ablation study, ensemble member selection]*
## 13 items, 5 kernels
- What do I do when I have both raw-signal and spectrogram models available for an EEG classification ensemble?  *[raw signal vs spectrogram, eeg classification, multi-representation ensemble, model diversity]*
- What do I do when I need to improve EEG classification from spectrograms?  *[eeg classification, spectrogram features, model improvement]*
- What do I do when I want to add a diverse model to a spectrogram-based ensemble for EEG classification?  *[ensemble diversity, new model addition, spectrogram-based ensemble, eeg classification]*
- What do I do when I want to enrich EEG input features for a brain activity classification model?  *[feature engineering, eeg features, input enrichment, brain activity classification]*
- What do I do when I want to evaluate a spectrogram-based EfficientNet model for EEG classification?  *[model evaluation, spectrogram features, efficientnet, eeg classification]*
- What do I do when I want to extract spectrogram features from EEG for a classification ensemble?  *[spectrogram feature extraction, eeg signal processing, classification ensemble]*
- What do I do when I want to improve an EEG classification ensemble that uses both precomputed and model-generated spectrograms?  *[eeg classification, ensemble improvement, spectrogram types, multi-source features]*
- What do I do when considering adding a mel-spectrogram branch to a spectrogram+EEG model for EEG classification?  *[additional input branch, mel spectrogram, multimodal architecture, eeg classification]*
- What do I do when deciding the EEG branch input dimensions and backbone size for a dual-branch (spectrogram + EEG) CNN model?  *[input dimensions, backbone size, dual-branch architecture, eeg spectrogram model]*
- What do I do when expanding an ensemble for a spectrogram/EEG classification task to maximize diversity?  *[ensemble diversity, spectrogram classification, model expansion, eeg task]*
- What do I do when switching from single-modality models to a multimodal model that consumes both EEG and spectrogram inputs?  *[multimodal model adoption, modality fusion, architecture swap, eeg spectrogram inputs]*
- What do I do when trying to improve spectrogram-based EEG model inputs after reverting a failed feature change?  *[feature engineering recovery, spectrogram input design, reverted change, eeg classification]*
## 13 items, 9 kernels
- What do I do when I add a large new model component (e.g., a big transformer for embedding extraction) and the notebook crashes from GPU memory exhaus  *[gpu memory exhaustion, large model component, resource constraint, memory optimization]*
- What do I do when I need to run inference on a dataset too large to fit in memory with my preprocessing pipeline?  *[memory constraints, large dataset inference, preprocessing pipeline, batch processing]*
- What do I do when I need to run inference on a test set that is too large to fit in memory alongside the trained model?  *[memory constraints, large dataset inference, model loading, batch processing]*
- What do I do when I want to increase inference throughput by raising batch size but I'm unsure about GPU memory limits?  *[inference throughput, batch size increase, gpu memory limits, resource uncertainty]*
- What do I do when adding more models to an inference pipeline causes GPU memory issues?  *[gpu memory issues, inference pipeline, model count scaling, resource constraints]*
- What do I do when building a complex feature pipeline that requires heavy GPU memory and multiple model loads?  *[gpu memory management, feature pipeline construction, multiple model loading]*
- What do I do when multiple transformer models for embedding extraction exceed available GPU memory or runtime?  *[gpu memory constraint, runtime constraint, transformer model selection, embedding extraction]*
- What do I do when my inference pipeline crashes due to memory constraints from loading multiple large models simultaneously?  *[memory constraints, multiple model loading, inference pipeline crash, resource optimization]*
- What do I do when my inference pipeline hits resource constraints during a refactoring episode?  *[resource constraints, inference pipeline refactor, memory management]*
- What do I do when my inference pipeline is hitting memory limits or timing out due to too many large models?  *[memory constraints, inference timeout, model count reduction, resource optimization]*
- What do I do when my notebook runs many large model inferences sequentially and may hit memory limits?  *[memory management, sequential inference, resource limits, large model inference]*
- What do I do when running inference with multiple large vision models sequentially causes GPU out-of-memory errors?  *[gpu out-of-memory, sequential model inference, large vision models, memory management]*
## 13 items, 7 kernels
- What do I do when I have a good multi-model ensemble and want to squeeze out more performance by adding another model family or adjusting composition?  *[ensemble composition, new model family, ensemble expansion, marginal gain]*
- What do I do when I have a stacking ensemble and pretrained models from another model family are available?  *[stacking ensemble, new model family available, ensemble expansion, model diversity]*
- What do I do when I have a strong ensemble baseline and want to improve further by adding a new model family?  *[strong ensemble, new model family, model diversity, ensemble expansion]*
- What do I do when I have a working ensemble and want to improve it by adding a new model family?  *[new model family, ensemble diversity, ensemble improvement]*
- What do I do when I have multiple diverse model families with known individual scores and need to combine them into a single submission?  *[diverse model families, submission combination, ensemble blending, known individual scores]*
- What do I do when I want to add a new model family to an existing ensemble without risking a broken submission?  *[new model family, submission safety, ensemble expansion, regression prevention]*
- What do I do when I want to add a new model family to an existing ensemble without risking a regression?  *[new model family, regression prevention, ensemble expansion, safe integration]*
- What do I do when I want to improve an ensemble that already combines two model families and has plateaued?  *[ensemble plateau, multi-family ensemble, model diversity exhaustion]*
- What do I do when I want to test whether a fundamentally different model family (e.g., a large generative LLM) can improve an already-tuned ensemble?  *[new model family, ensemble diversity, generative model integration, strong baseline]*
- What do I do when I want to test whether a new model family improves my ensemble?  *[new model family, ensemble diversity, contribution test]*
- What do I do when my ensemble includes diverse model families that require different missing-value handling?  *[diverse model families, missing value handling, preprocessing alignment]*
- What do I do when my incremental tuning of ensemble weights and checkpoint swaps has plateaued and I want a qualitatively different prediction source?  *[ensemble plateau, new prediction source, diversity injection, qualitative model change]*
## 12 items, 7 kernels
- What do I do when I have hundreds of engineered features and want to find the right subset size for a GBDT model?  *[feature subset size, feature selection, gbdt tuning, engineered features]*
- What do I do when I suspect certain engineered features (e.g., max/min/shift aggregations) are adding noise to a GBDT model?  *[noisy features, feature selection, engineered feature evaluation, gbdt model]*
- What do I do when I want to add new derived feature types (interactions, custom aggregations) to a tabular GBDT pipeline that already has many feature  *[derived feature types, feature engineering, tabular pipeline, feature interactions, gbdt pipeline]*
- What do I do when I want to add simple derived features to a GBDT model that already uses standard aggregations?  *[derived feature engineering, gbdt model, feature augmentation]*
- What do I do when I want to create domain-motivated interaction features (e.g., balance minus payment) for a tabular GBDT model?  *[interaction features, domain knowledge, feature engineering, tabular gbdt]*
- What do I do when I want to create useful interaction features for a GBDT model on tabular financial data?  *[interaction features, feature engineering, tabular financial data, gbdt model]*
- What do I do when an in-notebook feature selection wrapper adds complexity and instability to a TF-IDF + LightGBM pipeline?  *[feature selection, pipeline complexity, instability, tfidf lightgbm pipeline]*
- What do I do when choosing between SHAP-based and native tree-importance-based feature selection for GBDT?  *[feature selection method, shap importance, tree importance, gbdt model]*
- What do I do when choosing how many preselected features to keep for a tree-based model?  *[feature count selection, preselected features, tree-based model]*
- What do I do when my LightGBM model uses high-dimensional TF-IDF/count features and I want to control which features enter the model?  *[high-dimensional features, feature selection, lightgbm, tfidf features]*
- What do I do when per-customer row-level difference features are slow and may not improve a GBDT model that already has rich aggregation features?  *[row-level difference features, computational cost, feature redundancy, gbdt model, aggregation features]*
- What do I do when using GBDT on high-cardinality tabular data with many monthly records per entity?  *[high-cardinality features, tabular data, temporal aggregation, GBDT modeling]*
## 12 items, 8 kernels
- What do I do when I have multiple encoder architectures (cross-encoder vs bi-encoder) and multiple preprocessing options for a text ranking/labeling t  *[encoder architecture selection, preprocessing options, text ranking task, configuration search]*
- What do I do when I have multiple interacting configuration choices (feature sets, model members, loss hyperparameters) and need to find a good combin  *[interacting configuration choices, joint optimization, feature selection, ensemble member selection, hyperparameter tuning]*
- What do I do when I have multiple interacting configuration dimensions (model ensemble members, feature sets, hyperparameters) and need to find a good  *[interacting configuration dimensions, joint optimization, ensemble member selection, feature selection, hyperparameter tuning]*
- What do I do when I have multiple interacting configuration dimensions to explore and each experiment requires offline training before submission?  *[interacting configuration dimensions, offline training cost, experiment prioritization, joint optimization]*
- What do I do when I have multiple model configs in an ensemble and want to tune a shared hyperparameter?  *[shared hyperparameter tuning, ensemble configuration, joint optimization]*
- What do I do when I have multiple model configurations with the same hyperparameter at different values and want to tune that hyperparameter?  *[hyperparameter tuning, multiple configurations, shared parameter alignment]*
- What do I do when I have multiple trained checkpoints from different training stages and want to find the best one for inference?  *[multiple training stages, checkpoint selection, inference configuration]*
- What do I do when I need to tune multiple interacting hyperparameters (e.g., scaler type and solver precision) for an ensemble blend?  *[hyperparameter interaction, ensemble blending, joint tuning, scaler and solver selection]*
- What do I do when I want to decide whether to invest time in hyperparameter tuning vs. feature engineering?  *[effort allocation, hyperparameter tuning, feature engineering, priority decision]*
- What do I do when I want to improve training robustness and have several promising ideas (augmentation, sampling, scheduler, backbone)?  *[training robustness, multiple candidate ideas, experiment prioritization, augmentation strategy, scheduler selection]*
- What do I do when I've changed regularization settings and need to re-tune how many features to keep?  *[regularization change, feature selection, hyperparameter re-tuning, interaction between settings]*
- What do I do when fine-tuning a multi-stage model and I'm unsure which stage's data selection to use for the final stage?  *[multi-stage training, data selection, stage configuration, fine-tuning pipeline]*
## 12 items, 10 kernels
- What do I do when I have no local validation metric for an ensemble and must rely on leaderboard scores?  *[no local validation, leaderboard reliance, ensemble evaluation]*
- What do I do when I have several model variants with known CV scores but unknown LB scores, and I need to build an ensemble?  *[cv-lb disagreement, ensemble construction, unknown leaderboard scores, model selection uncertainty]*
- What do I do when I want to improve an ensemble but can only evaluate on a tiny public leaderboard?  *[limited leaderboard signal, ensemble selection, small public test set]*
- What do I do when I want to improve an ensemble but have limited leaderboard signal (very few public test rows)?  *[limited leaderboard signal, ensemble selection, small public test set]*
- What do I do when I've tried adding and removing several large transformer backbones to an ensemble with inconsistent leaderboard improvements?  *[inconsistent leaderboard results, transformer backbone selection, ensemble composition, large model evaluation]*
- What do I do when a hyperparameter change that looked promising locally produces a LB regression?  *[local-leaderboard disagreement, hyperparameter change, score regression, overfitting to validation]*
- What do I do when exploring new model architectures in an ensemble competition with a tiny public leaderboard?  *[architecture exploration, ensemble competition, small leaderboard, validation strategy]*
- What do I do when local CV suggests different optimal blend weights than what worked on the leaderboard?  *[cv-leaderboard disagreement, blend weight tuning, ensemble weight selection]*
- What do I do when offline training metrics suggest a new spectrogram variant should help but LB scores regress?  *[offline-online disagreement, spectrogram variant, score regression, leaderboard validation]*
- What do I do when swapping checkpoint versions of the same architecture yields inconsistent leaderboard results?  *[checkpoint version swap, inconsistent leaderboard results, same architecture, result instability]*
- What do I do when the public leaderboard has very few evaluation rows and I need to decide whether a small score change is real?  *[small evaluation set, leaderboard reliability, score variance, overfitting detection]*
- What do I do when tuning GBDT hyperparameters and validation metrics don't correlate well with leaderboard scores?  *[validation-leaderboard mismatch, gbdt hyperparameter tuning, evaluation reliability]*
## 11 items, 10 kernels
- What do I do when I have a trained model with decent validation but no submission yet, and the test set is too large to process in one pass?  *[large test set, batch inference, first submission, memory constraint]*
- What do I do when I need to convert a training notebook into a submission pipeline while preserving score?  *[training to inference conversion, submission pipeline, score preservation]*
- What do I do when I need to get a first working submission from a training notebook that was not designed for inference?  *[training to inference conversion, first submission, inference pipeline setup]*
- What do I do when I need to validate that a DeBERTa regression pipeline will handle the full test set within Kaggle's time and memory limits?  *[inference time constraint, memory limit validation, deberta regression pipeline, kaggle submission constraints]*
- What do I do when I want to ensemble multiple deep learning models at inference time under Kaggle's resource constraints?  *[inference ensembling, resource constraints, deep learning models, kaggle submission]*
- What do I do when I want to improve an ensemble of pretrained transformer models at inference time without retraining?  *[inference-time improvement, transformer ensemble, no retraining constraint]*
- What do I do when I want to reduce inference cost without hurting prediction quality?  *[inference cost reduction, prediction quality preservation, model efficiency]*
- What do I do when I want to use runtime prediction statistics to gate or filter submissions?  *[runtime prediction, submission filtering, inference gating]*
- What do I do when adapting a training notebook into an inference/submission notebook?  *[training to inference conversion, submission notebook, pipeline adaptation]*
- What do I do when my ensemble post-processing (ranking/scoring) is a bottleneck or imprecise, and I want to improve both speed and prediction quality?  *[post-processing bottleneck, ranking optimization, inference speed, prediction quality]*
- What do I do when transformer inference is too slow or fragile for a Kaggle submission kernel but I need transformer-quality features?  *[inference speed constraint, transformer distillation, feature extraction, submission kernel limitation]*
## 11 items, 9 kernels
- What do I do when I have multiple potential fixes that I believe are all correct?  *[multiple candidate fixes, change prioritization, simultaneous improvements]*
- What do I do when I want to add multiple changes at once but the code has bugs preventing execution?  *[multiple simultaneous changes, code debugging, execution failure, bug fixing]*
- What do I do when I want to make multiple interdependent changes (model architecture, checkpoints, and post-processing) to improve a pipeline?  *[multiple simultaneous changes, interdependent changes, architecture and post-processing, end-to-end verification]*
- What do I do when I want to make multiple model/hyperparameter changes but need to verify they work end-to-end before submitting?  *[multiple simultaneous changes, end-to-end verification, submission quota conservation]*
- What do I do when I want to make multiple related improvements (architecture, aggregation, bug fixes) before submitting?  *[multiple simultaneous changes, batched updates, architecture and bug fixes, pre-submission verification]*
- What do I do when I want to test a new idea but it requires multiple code changes?  *[new idea testing, multiple code changes, change isolation]*
- What do I do when I want to test a new training idea but also have a bug fix and an output-format improvement ready?  *[multiple pending changes, change isolation, bug fix prioritization, training idea test]*
- What do I do when I've made many untested changes and want to check if they work?  *[multiple untested changes, sanity check, batch verification]*
- What do I do when I've made multiple interacting changes and need to verify them before iterating further?  *[multiple interacting changes, verification before iteration, sanity check]*
- What do I do when a large experimental change requires multiple bug-fix iterations before it can even be evaluated?  *[bug fixing, large experimental change, iterative debugging, evaluation delay]*
- What do I do when a multi-part code change might introduce bugs and I want to isolate issues before submitting?  *[multi-change experiment, bug isolation, incremental testing, pre-submission validation]*
## 11 items, 8 kernels
- What do I do when I have a pre-trained transformer inference notebook and want to improve prediction stability on a small, noisy regression dataset?  *[prediction stability, small noisy dataset, transformer inference, regression task]*
- What do I do when I want to improve a fine-tuned transformer's predictions on a small regression dataset?  *[small dataset, transformer fine-tuning, regression task improvement]*
- What do I do when I want to improve a transformer's prediction quality on a regression task with small, noisy data?  *[transformer prediction quality, small noisy data, regression task improvement, fine-tuning strategy]*
- What do I do when I want to improve a transformer's representation quality for regression on small text data?  *[representation quality, transformer fine-tuning, small text data, regression task]*
- What do I do when choosing a learning rate for fine-tuning a BERT-base model on a small regression/ranking dataset?  *[learning rate selection, bert fine-tuning, small dataset, regression task]*
- What do I do when exploring model size variants (small/base/large) for a fine-tuned transformer regressor?  *[model size selection, transformer variants, fine-tuning, regression task]*
- What do I do when increasing MLP capacity doesn't improve performance on a small tabular/embedding dataset?  *[model capacity saturation, MLP architecture, small dataset, tabular embedding data]*
- What do I do when my 1D time-series classification model is underperforming and I suspect it lacks representational capacity?  *[model capacity, underperformance, time-series classification, architecture scaling]*
- What do I do when training classical regressors (SVR/Ridge) on transformer embeddings with small, noisy data?  *[small noisy data, classical regressor selection, transformer embeddings, feature-based regression]*
- What do I do when trying advanced pooling (layer-weighted mean+max + attention) over transformer hidden states for a regression task on small data?  *[pooling strategy, transformer hidden states, small noisy data, regression task]*
- What do I do when working with a small, noisy regression dataset where individual transformer models overfit?  *[small noisy dataset, transformer overfitting, regression task, ensemble regularization]*
## 11 items, 7 kernels
- What do I do when I have pretrained sentence embeddings and want to maximize Spearman correlation on a multi-label prediction task?  *[pretrained embeddings, spearman correlation, multi-label prediction, feature utilization]*
- What do I do when I want to boost a specific target column's Spearman correlation in a multi-target prediction task?  *[per-target optimization, spearman correlation, multi-target prediction]*
- What do I do when building a regression pipeline for targets that are averages of crowd ratings (near-continuous) and the metric is rank-based (Spearm  *[regression pipeline, rank-based metric, crowd-rated targets, loss function selection]*
- What do I do when my Spearman-correlation metric depends on rank ordering and some target columns have near-binary distributions?  *[near-binary distribution, spearman correlation, rank-based metric, target distribution]*
- What do I do when my Spearman-evaluated predictions may contain many tied values?  *[tied values, spearman correlation, rank-based metric, prediction resolution]*
- What do I do when my metric is rank-based (Spearman) and my model outputs continuous predictions for targets that take only a few discrete values?  *[rank-based metric, discrete target values, prediction post-processing]*
- What do I do when my predictions are continuous but the ground truth takes only a few discrete values, and the metric is rank-based (Spearman)?  *[continuous predictions, discrete ground truth, rank-based metric, prediction discretization]*
- What do I do when my rank-based metric (Spearman) is sensitive to prediction ties and my model outputs near-continuous values?  *[rank-based metric, prediction ties, spearman sensitivity, continuous outputs]*
- What do I do when my regression predictions target labels that take only a few discrete values and the metric is rank-based (Spearman)?  *[continuous predictions, discrete ground truth, rank-based metric, regression output mapping]*
- What do I do when predictions are continuous but the target metric (Spearman correlation) depends on ranks and the ground truth takes discrete values?  *[rank-based metric, discrete target, continuous predictions, spearman correlation, prediction discretization]*
- What do I do when the metric depends on rank ordering and targets take discrete values from averaged crowd ratings?  *[rank-based metric, discrete target values, crowd-averaged labels, label preprocessing]*
## 11 items, 10 kernels
- What do I do when I make a multi-part code change and the notebook fails to run?  *[notebook failure, multi-part code change, error diagnosis]*
- What do I do when I need multiple code fixes before a notebook will produce valid output?  *[multiple code fixes, notebook failure, incremental debugging]*
- What do I do when I need to get a complex notebook running before I can iterate on model quality?  *[complex notebook debugging, pipeline setup, end-to-end execution]*
- What do I do when I try to upgrade a model component but the notebook fails to run or produce valid output?  *[model component upgrade, notebook execution failure, debugging pipeline]*
- What do I do when I'm adapting someone else's inference notebook and it doesn't run or produces wrong outputs?  *[notebook adaptation, inference debugging, code reuse errors]*
- What do I do when I'm adapting someone else's notebook that doesn't run end-to-end due to variable name mismatches and dead code paths?  *[notebook adaptation, code debugging, variable name mismatch, dead code paths]*
- What do I do when a notebook fails to run or submit after adding GPU execution alongside new features?  *[submission failure, gpu execution error, notebook debugging]*
- What do I do when my first notebook submission either fails or doesn't produce a valid result?  *[first submission failure, notebook submission debugging, pipeline validation]*
- What do I do when my notebook fails to execute and I suspect an import or environment issue?  *[notebook execution failure, import error, environment issue, dependency debugging]*
- What do I do when my notebook keeps failing on syntax or API errors during an iterative tuning loop?  *[notebook execution failure, syntax error, API error, iterative debugging]*
- What do I do when my notebook keeps failing or producing unexpected outputs and I need to verify execution before submitting?  *[notebook execution failure, output verification, pre-submission validation]*
## 11 items, 6 kernels
- What do I do when I have a new best score from a single-fold model and want to know if a multi-fold ensemble or individual folds improve it?  *[new best score, single-fold baseline, multi-fold ensemble, fold selection]*
- What do I do when I have a new best score from a single-fold model and want to know if multi-fold averaging improves it?  *[new best score, single-fold baseline, multi-fold averaging, cross-validation ensemble]*
- What do I do when I have per-fold CV scores and want to improve ensemble predictions?  *[per-fold cv scores, ensemble improvement, fold-level analysis]*
- What do I do when I have per-fold model quality scores and want to improve ensemble predictions?  *[per-fold cv scores, ensemble improvement, model quality weighting]*
- What do I do when I have per-fold validation scores suggesting some folds are much better than others and I want to improve the ensemble?  *[per-fold score variance, fold weighting, ensemble improvement]*
- What do I do when I've been using fewer CV folds for fast iteration and now want to maximize final score?  *[cv fold count, fast iteration tradeoff, final score maximization, cross-validation strategy]*
- What do I do when a single-fold model scores well but I want more gains without changing the training recipe?  *[single fold model, post-training gains, ensemble strategy, fold aggregation]*
- What do I do when choosing the number of CV folds for a LightGBM ensemble on a medium-sized tabular dataset?  *[cv fold count, lightgbm ensemble, tabular dataset]*
- What do I do when deciding how many CV folds to use for a tree-based ensemble on ~17k samples?  *[cross-validation fold count, tree-based ensemble, small dataset size]*
- What do I do when deciding how many cross-validation folds to average for a CNN ensemble submission?  *[cross-validation fold count, cnn ensemble, submission averaging]*
- What do I do when the number of CV folds affects leaderboard score in an ensemble-averaging pipeline?  *[fold count selection, ensemble averaging, cross-validation tuning, leaderboard score]*
## 11 items, 9 kernels
- What do I do when I have a working baseline submission and want to substantially improve it by adding new model components and features?  *[model components addition, feature engineering, substantial improvement]*
- What do I do when I have a working pipeline with incremental feature additions yielding small gains?  *[incremental feature addition, small gains, feature engineering]*
- What do I do when I've been toggling a heavy feature (like transformer embeddings) on and off across many versions with inconsistent results?  *[inconsistent results, feature toggle, transformer embeddings, heavy feature ablation]*
- What do I do when a complex new feature engineering effort doesn't beat my previous best after extensive tuning?  *[no score improvement, feature engineering, extensive tuning, diminishing returns]*
- What do I do when a feature set addition has been tried multiple times with inconsistent results?  *[inconsistent results, feature set addition, repeated experiments, feature selection]*
- What do I do when a newly added model modality (e.g., mel-spectrogram features) doesn't improve the ensemble after several attempts?  *[new modality failure, ensemble improvement plateau, feature modality evaluation]*
- What do I do when a recently added complex feature set didn't improve the leaderboard score?  *[no improvement, complex feature set, feature selection, leaderboard score]*
- What do I do when a recently added feature/modality showed no improvement across several submissions?  *[no improvement, feature modality addition, persistent failure, feature selection]*
- What do I do when adding a preprocessing step (e.g., notch filter) doesn't improve the score?  *[no score improvement, preprocessing step, feature engineering evaluation]*
- What do I do when my initial submitted pipeline scores poorly and I suspect the feature engineering and preprocessing are suboptimal?  *[poor baseline score, feature engineering, preprocessing improvement]*
- What do I do when my tabular model on time-series customer data has a low score and I'm only using simple aggregation features?  *[low score, feature engineering, time-series aggregation, tabular model improvement]*
## 11 items, 11 kernels
- What do I do when I have an untested pipeline that has never been submitted and may have infrastructure bugs?  *[untested pipeline, first submission, infrastructure debugging, end-to-end validation]*
- What do I do when I need to establish a working inference pipeline before optimizing model quality?  *[inference pipeline setup, first submission, end-to-end pipeline]*
- What do I do when I need to get a complex multi-model pipeline to produce its first valid submission?  *[multi-model pipeline, first valid submission, end-to-end pipeline]*
- What do I do when I need to get a working end-to-end pipeline before any leaderboard submission?  *[end-to-end pipeline, first submission, pipeline setup]*
- What do I do when I need to rebuild a pipeline across multiple edits before submitting?  *[pipeline rebuild, multiple edits, submission preparation, incremental development]*
- What do I do when I need to wire together outputs from two separate model stages into a single submission file?  *[multi-stage pipeline, submission file assembly, model output integration]*
- What do I do when I'm making a major pipeline change and want to minimize wasted submissions?  *[major pipeline change, submission budget conservation, local validation]*
- What do I do when I've just made a major structural change to my pipeline and want to confirm it works before submitting?  *[structural pipeline change, sanity check, pre-submission validation]*
- What do I do when assembling a multi-contributor ensemble pipeline for the first time before any leaderboard submission?  *[ensemble pipeline assembly, multi-contributor integration, first submission]*
- What do I do when building a complex multi-component feature pipeline across many edits without submitting?  *[feature pipeline construction, multi-component pipeline, deferred submission]*
- What do I do when building a complex multi-component pipeline from scratch that must run end-to-end before I can evaluate it?  *[end-to-end pipeline construction, multi-component pipeline, deferred validation]*
## 11 items, 9 kernels
- What do I do when I have multiple pretrained models that each need different feature preprocessing?  *[multiple pretrained models, feature preprocessing, model-specific pipelines]*
- What do I do when I need to add a complex new feature source (e.g., transformer embeddings) to an existing tabular pipeline?  *[complex feature source, transformer embeddings, tabular pipeline integration]*
- What do I do when I need to integrate multiple new models into an ensemble and each has different preprocessing requirements?  *[ensemble integration, multiple models, preprocessing requirements, pipeline compatibility]*
- What do I do when I need to transition from a monolithic notebook pipeline to using external pretrained model scripts?  *[pipeline refactoring, pretrained model integration, notebook to scripts transition]*
- What do I do when I want to add a complex new feature pipeline that requires external libraries, text preprocessing, and integration with existing fea  *[feature pipeline integration, external library dependency, text preprocessing, feature merging]*
- What do I do when I want to add a new high-dimensional feature source (e.g., pretrained embeddings) to an existing pipeline that is already performing  *[high-dimensional features, pretrained embeddings, strong pipeline augmentation, feature integration]*
- What do I do when I want to add a significant new preprocessing or data pipeline feature to inference?  *[preprocessing addition, data pipeline feature, inference integration]*
- What do I do when I want to switch from a feature-extraction pipeline to an end-to-end fine-tuning pipeline while keeping the notebook functional?  *[pipeline paradigm shift, feature extraction to fine-tuning, notebook compatibility]*
- What do I do when building a complex new pipeline that involves multiple new components (embeddings, features, models, blending)?  *[multi-component pipeline, pipeline from scratch, embeddings features models blending]*
- What do I do when my BERT-based model has many heterogeneous input features (text embeddings, one-hot categoricals, engineered numerics) and I want to  *[heterogeneous input features, feature simplification, bert-based model, input pipeline design]*
- What do I do when setting up a BERT fine-tuning pipeline and the model checkpoint, tokenizer, and hyperparameters need to be configured correctly befo  *[pipeline setup, bert fine-tuning, initial configuration, tokenizer setup]*
## 10 items, 9 kernels
- What do I do when I have found a good test-time input resolution and want to confirm it's optimal?  *[test-time resolution, optimality confirmation, resolution sweep, hyperparameter verification]*
- What do I do when I want to efficiently sweep a continuous hyperparameter whose optimal value is unknown?  *[hyperparameter sweep, continuous hyperparameter, search efficiency]*
- What do I do when I'm sweeping two coupled hyperparameters (checkpoint and a discrete config) and the first combination is best?  *[coupled hyperparameter sweep, first combination best, joint optimization, early stopping]*
- What do I do when I've found an approximate optimum for one hyperparameter but want to confirm it's robust?  *[hyperparameter robustness, optimum confirmation, sensitivity analysis]*
- What do I do when a hyperparameter sweep has found a peak and I want to recover or improve further?  *[hyperparameter sweep, peak found, further improvement, fine-tuning search]*
- What do I do when a hyperparameter sweep over a single knob returns to the starting value as best?  *[hyperparameter sweep, original value optimal, single parameter search, search conclusion]*
- What do I do when a hyperparameter sweep shows the original value was already optimal?  *[hyperparameter sweep, original value optimal, search conclusion, confirmation of baseline]*
- What do I do when a sweep produces confounded results partway through?  *[confounded results, hyperparameter sweep, experiment validity]*
- What do I do when manually sweeping hyperparameters without a clear signal of which parameter matters?  *[hyperparameter sweep, manual tuning, unclear parameter importance, feature attribution]*
- What do I do when sweeping a hyperparameter without submitting and I see a sharp degradation in local CV?  *[hyperparameter sweep, local cv degradation, sharp degradation, offline evaluation]*
## 10 items, 9 kernels
- What do I do when I have a single 2D CNN backbone in my ensemble and want to improve further?  *[single backbone ensemble, model diversity, 2d cnn, ensemble expansion]*
- What do I do when I have a stacking ensemble of one backbone type and want to improve further?  *[stacking ensemble, single backbone type, model diversity, ensemble expansion]*
- What do I do when I have diverse models (CNN on spectrograms, 1D models on raw signals, pretrained image models) for the same classification task?  *[diverse model ensemble, multi-architecture combination, model diversity, ensemble construction]*
- What do I do when I have multiple ViT backbones of different sizes and want to combine them in a single model for multi-source EEG/spectrogram inputs?  *[multiple vit backbones, architecture combination, multi-source inputs, model size diversity]*
- What do I do when I have multiple model variants with similar individual scores but different architectures/heads?  *[multiple model variants, architecture diversity, ensemble member selection, similar individual scores]*
- What do I do when I want to improve a multi-backbone ensemble for image classification?  *[multi-backbone ensemble, image classification, backbone diversity]*
- What do I do when I want to increase ensemble diversity without changing model architectures?  *[ensemble diversity, fixed architectures, diversity without architecture change]*
- What do I do when a mean ensemble of diverse architectures doesn't match a previous weighted ensemble's score?  *[ensemble weighting, mean ensemble, diverse architectures, score regression]*
- What do I do when choosing between mean and weighted ensemble blending for diverse model architectures?  *[ensemble blending strategy, mean vs weighted, diverse model architectures]*
- What do I do when ensembling two models from the same architecture trained on different folds?  *[same architecture, different folds, ensemble combination, fold diversity]*
## 10 items, 8 kernels
- What do I do when I have a new model to integrate into an existing ensemble and need to determine whether it helps?  *[new model available, ensemble integration, contribution test]*
- What do I do when I have a new pretrained model to add to an existing high-performing ensemble?  *[new model available, ensemble integration, high-performing ensemble]*
- What do I do when I have a strong multi-fold ensemble result and want to test whether a different training variant could do better?  *[strong ensemble, training variant exploration, ablation study, incremental improvement]*
- What do I do when I have a well-tuned single-architecture ensemble and want to check whether a different architecture improves the score?  *[architecture diversity, ensemble improvement, new architecture evaluation]*
- What do I do when I have a working ensemble submission and want to test an alternative training variant?  *[training variant exploration, ensemble improvement, alternative configuration]*
- What do I do when I want to test a new/upgraded component in an existing ensemble?  *[component upgrade, ensemble integration, incremental replacement]*
- What do I do when I want to test whether a new architectural idea improves an ensemble without excessive experimentation?  *[new architecture idea, ensemble improvement, experiment efficiency]*
- What do I do when I want to track which ensemble configurations produced which scores during rapid iteration?  *[experiment tracking, ensemble configuration logging, rapid iteration]*
- What do I do when a new resource (e.g., retrained or differently-trained component models) becomes available and I want to test whether it improves an  *[new resources available, ensemble improvement test, component model update]*
- What do I do when adding a new component to an ensemble causes data or code integration errors?  *[integration errors, ensemble member addition, data flow debugging, code debugging]*
## 10 items, 9 kernels
- What do I do when I have a multi-stage training pipeline and need to determine which stage's checkpoint to use for inference?  *[multi-stage pipeline, checkpoint choice, inference stage selection]*
- What do I do when I have a working single-stage training pipeline and want to improve performance further?  *[single-stage pipeline, performance improvement, training strategy]*
- What do I do when I need to debug a multi-step inference pipeline change that involves both a new model type and potential configuration mismatches?  *[inference pipeline debugging, new model type, configuration mismatch]*
- What do I do when I want to iterate quickly on a complex pipeline with multiple model components?  *[rapid iteration, complex pipeline, multiple model components]*
- What do I do when I want to iterate quickly on an inference pipeline but full training takes too long?  *[rapid iteration, inference pipeline, training time constraint, shortcut evaluation]*
- What do I do when I want to test whether an alternative precomputed data source improves over my current pipeline?  *[alternative data source, precomputed data evaluation, pipeline replacement test]*
- What do I do when I want to test whether precomputed/cached predictions can replace live inference to save compute?  *[cached predictions, compute optimization, inference replacement, pipeline efficiency]*
- What do I do when adding a new component to an ensemble requires setting up an inference pipeline that may have multiple configuration errors?  *[inference pipeline setup, ensemble member addition, configuration errors, pipeline debugging]*
- What do I do when building a new inference pipeline from scratch and I have no leaderboard signal yet?  *[inference pipeline from scratch, no leaderboard signal, pipeline correctness]*
- What do I do when building a new model pipeline from scratch for inference that involves unfamiliar architecture, preprocessing, and post-processing?  *[inference pipeline from scratch, unfamiliar architecture, preprocessing, post-processing]*
## 10 items, 7 kernels
- What do I do when I suspect a feature component may be unnecessary and want to know if removing it simplifies the pipeline without hurting performance  *[feature ablation, pipeline simplification, component necessity test]*
- What do I do when I want to know whether a recently added inference-time technique is actually contributing to my score?  *[inference-time technique, component contribution test, ablation study]*
- What do I do when I want to simplify a complex pipeline to identify which components actually contribute?  *[pipeline simplification, component contribution, ablation study]*
- What do I do when I want to test a new model component but need to isolate its effect from the existing ensemble?  *[new model component, ensemble isolation, ablation testing, change isolation]*
- What do I do when I want to test whether a new architectural component or modality combination improves over a strong baseline?  *[architectural component test, modality combination, strong baseline, contribution test]*
- What do I do when I want to test whether a previously disabled component improves the ensemble?  *[disabled component, ensemble improvement test, component reactivation, ablation study]*
- What do I do when I want to test whether a single component change improves an ensemble?  *[single component change, ensemble improvement test, ablation study]*
- What do I do when I want to test whether a single input modality can match or beat a multi-modality ensemble?  *[single modality test, multi-modality comparison, input ablation, complexity reduction]*
- What do I do when a single-modality experiment produces a large regression compared to a multimodal baseline?  *[large score regression, single modality experiment, multimodal baseline, modality ablation]*
- What do I do when my pipeline has accumulated multiple components and I want to verify each component's contribution before continuing?  *[component contribution, ablation study, pipeline validation, component isolation]*
## 9 items, 6 kernels
- What do I do when I have a well-performing stochastic ensemble pipeline and want to lock it down for a final reproducible submission?  *[stochastic ensemble, reproducibility, final submission, random seed fixing]*
- What do I do when I observe that repeated submissions of the same code yield different scores?  *[score variance, non-determinism, submission reproducibility]*
- What do I do when I see score variance across identical or near-identical re-runs?  *[score variance, non-determinism, run reproducibility]*
- What do I do when I see score variance across identical re-runs of a non-deterministic inference pipeline?  *[score variance, non-deterministic inference, reproducibility diagnosis]*
- What do I do when I suspect my best ensemble score may be partly due to run-to-run variance rather than genuine model quality?  *[run-to-run variance, ensemble score reliability, reproducibility check]*
- What do I do when a re-run of supposedly identical code gives a substantially different leaderboard score?  *[score variance, reproducibility issue, non-determinism diagnosis]*
- What do I do when my inference pipeline has high run-to-run variance and I need to identify which configuration is actually better?  *[run-to-run variance, inference reproducibility, configuration comparison]*
- What do I do when my pipeline involves stochastic components (NN training, random sampling) and I plan to ensemble multiple runs?  *[stochastic components, reproducibility, seed diversity, multi-run ensemble]*
- What do I do when repeated re-runs of the same code produce significantly better scores, suggesting upstream improvements?  *[score improvement, run variance, upstream improvement confirmation, reproducibility check]*
## 9 items, 8 kernels
- What do I do when I can run many cheap experiments but leaderboard submissions are limited?  *[limited submissions, experiment strategy, offline experimentation, submission budget]*
- What do I do when I have multiple improvements to try (more features, different hyperparameters, simpler preprocessing) and limited submission budget?  *[multiple improvements, limited submission budget, experiment prioritization]*
- What do I do when I have multiple interacting configuration changes (data, checkpoint, stage) and limited submission budget?  *[interacting configuration changes, limited submission budget, experiment prioritization, joint optimization]*
- What do I do when I have multiple potential improvements (new external model versions, output scaling, blend coefficients) and limited submission budg  *[multiple candidate improvements, submission budget constraint, experiment prioritization]*
- What do I do when I want to test multiple changes (backbone, learning rate, sampling strategy) but each submission is costly?  *[multiple simultaneous changes, submission budget, change prioritization, cost-efficient experimentation]*
- What do I do when I want to test multiple hypotheses about what improves my score?  *[multiple hypotheses, experiment prioritization, systematic testing, improvement attribution]*
- What do I do when I want to test multiple interacting changes (new features, feature drops, CV folds) but each full run is expensive?  *[interacting changes, expensive full run, cost-efficient experimentation, experiment prioritization]*
- What do I do when I want to test multiple new feature ideas but have limited submission budget?  *[limited submission budget, multiple feature ideas, experiment prioritization]*
- What do I do when I want to test multiple new ideas (custom eval metric, different feature ranking, hyperparameter tweaks) but each submission is cost  *[limited submission budget, multiple experiment ideas, experiment prioritization, cost-efficient testing]*
## 9 items, 6 kernels
- What do I do when I need to debug a complex pipeline that fails or regresses after a major refactor?  *[pipeline debugging, major refactor, score regression]*
- What do I do when I need to refactor a complex pipeline (many model variants, repetitive code) without regressing leaderboard performance?  *[pipeline refactor, code complexity, score preservation, regression prevention]*
- What do I do when I want to make a large configuration change but need to verify the baseline still works?  *[large configuration change, baseline verification, regression prevention]*
- What do I do when I want to refactor code for future extensibility without risking the current score?  *[code refactoring, future extensibility, score regression prevention]*
- What do I do when I want to refactor infrastructure without risking a score regression?  *[infrastructure refactoring, score regression prevention, safe refactoring]*
- What do I do when I want to test whether a new configuration improves over a strong baseline?  *[new configuration test, strong baseline, incremental improvement]*
- What do I do when I've just improved my score by changing the model checkpoint, and I have a configuration choice that was suboptimal before?  *[score improvement, checkpoint change, revisiting suboptimal configuration]*
- What do I do when an infrastructure change causes a small score regression but is needed for future improvements?  *[infrastructure change, small score regression, tradeoff future improvement]*
- What do I do when an infrastructure refactor causes a tiny score regression?  *[infrastructure refactor, small score regression]*
## 9 items, 7 kernels
- What do I do when I suspect my predictions have a systematic bias that hurts the rounding-based metric?  *[systematic bias, rounding-based metric, prediction calibration]*
- What do I do when I want to reduce systematic bias or shift in transformer regression predictions?  *[systematic bias, prediction shift, transformer regression, bias correction]*
- What do I do when a recent change caused a regression and I suspect the cross-validation scheme or postprocessing is misaligned with the test distribu  *[score regression, cross-validation alignment, postprocessing mismatch, distribution shift]*
- What do I do when my ensemble predictions may have a systematic bias (mean offset)?  *[systematic bias, mean offset correction, ensemble postprocessing]*
- What do I do when my model outputs are in an unknown or wrong range and I need to produce valid bounded predictions for a rank-based metric?  *[prediction range mismatch, output calibration, rank-based metric, bounded predictions]*
- What do I do when my model's predicted score distribution doesn't match the expected test distribution?  *[prediction distribution mismatch, output calibration, distribution alignment]*
- What do I do when my model's prediction distribution may not match the test distribution?  *[prediction distribution mismatch, output calibration, distribution alignment]*
- What do I do when my model's raw predictions may have a different distribution than the training/validation targets?  *[prediction distribution mismatch, output postprocessing, distribution alignment]*
- What do I do when my neural network's raw output range seems poorly calibrated relative to the ensemble's other components?  *[output calibration, ensemble component scaling, prediction range mismatch]*
## 8 items, 6 kernels
- What do I do when I want to change multiple aspects of the training pipeline (infrastructure, CV logic, hyperparameters) at once?  *[multiple simultaneous changes, pipeline refactoring, infrastructure and hyperparameters]*
- What do I do when I want to confirm that an infrastructure change (batch size) doesn't affect prediction quality?  *[infrastructure change, batch size change, prediction quality verification]*
- What do I do when I want to test a hyperparameter change but also have an unrelated improvement (extra data, new checkpoint) ready?  *[hyperparameter change, unrelated improvement, change isolation, batched changes]*
- What do I do when I want to test multiple pipeline changes but need to attribute score movements?  *[multiple pipeline changes, score attribution, ablation study, experiment isolation]*
- What do I do when I want to test whether hyperparameter changes help but also have a minor feature cleanup to make?  *[hyperparameter tuning, feature cleanup, concurrent changes, ablation study]*
- What do I do when I want to test whether specific preprocessing changes help, given that I'm also changing model checkpoints simultaneously?  *[concurrent changes, preprocessing ablation, checkpoint change, confounded experiment]*
- What do I do when I want to validate a new infrastructure change (like fold averaging) before tuning within it?  *[infrastructure change validation, fold averaging, baseline comparison before tuning]*
- What do I do when I'm unsure whether a configuration change (e.g., a filter or preprocessing step) is actually helping?  *[configuration change, preprocessing step, ablation study, uncertain improvement]*
## 8 items, 5 kernels
- What do I do when I have a new inference pipeline and need to verify it works as well as the old one?  *[inference pipeline change, pipeline verification, score parity check]*
- What do I do when I want to clean up inference code without risking a score regression?  *[code refactoring, inference pipeline, score regression prevention]*
- What do I do when I want to test a new input branch or preprocessing change but the first attempt regresses?  *[preprocessing change, score regression, iterative debugging, input branch]*
- What do I do when I want to test whether a new preprocessing step improves an already-tuned pipeline?  *[preprocessing change, pipeline improvement test, tuned baseline comparison]*
- What do I do when I want to test whether a preprocessing change improves my pipeline?  *[preprocessing change, pipeline improvement test, ablation study]*
- What do I do when my pipeline has been producing nonsensical scores for many iterations despite model/postprocessing changes?  *[persistent bad scores, pipeline debugging, data pipeline bug, root cause analysis]*
- What do I do when my score drops dramatically despite no code changes or only minor changes?  *[score regression, unexpected score drop, pipeline debugging]*
- What do I do when my score is unexpectedly bad and I suspect submission pipeline issues rather than model issues?  *[unexpected score drop, submission pipeline debugging, inference error diagnosis]*
## 8 items, 4 kernels
- What do I do when I change the training loss or evaluation metric mid-experiment?  *[loss function change, evaluation metric change, mid-experiment modification]*
- What do I do when I have a custom loss function with tunable scalar constants and want to find the best values?  *[custom loss function, scalar constant tuning, hyperparameter search]*
- What do I do when I have a well-tuned model and want to test whether an alternative loss function improves the score?  *[loss function exploration, well-tuned model, alternative objective, ablation study]*
- What do I do when I want to switch from categorical cross-entropy to KL-divergence loss for a soft-label classification task?  *[loss function change, kl-divergence loss, soft-label classification]*
- What do I do when I've changed the loss function and activation of a fine-tuned pretrained model and need to re-tune the head's hyperparameters?  *[loss function change, head hyperparameter tuning, pretrained model fine-tuning, activation change]*
- What do I do when my gradient-boosted model uses a custom loss with label-shift constants that were tuned to specific decimal values?  *[custom loss tuning, label shift constants, gradient boosting, hyperparameter sensitivity]*
- What do I do when my multi-label regression targets are independent continuous values in [0,1] but my model uses softmax output and categorical cross-  *[loss function mismatch, multi-label regression, output activation choice]*
- What do I do when tuning a custom loss function's constants and the score is sensitive to small changes?  *[loss function tuning, sensitivity to constants, custom loss function, score sensitivity]*
## 8 items, 8 kernels
- What do I do when I have a multi-model ensemble and suspect one member is degrading the blend?  *[ensemble member degradation, blend diagnosis, member removal, ensemble quality check]*
- What do I do when I have a working ensemble but suspect one component is undertrained or poorly structured?  *[undertrained component, ensemble diagnosis, component restructuring]*
- What do I do when I want to scale up the number of ensemble members but the current inference loop is hardcoded to a fixed set?  *[ensemble scaling, hardcoded member set, inference loop refactoring, dynamic ensemble members]*
- What do I do when I've decomposed an ensemble into individual components for debugging/refactoring and no single component matches the original ensemb  *[ensemble decomposition, component debugging, score gap analysis, ensemble synergy]*
- What do I do when I've fixed a bug in one ensemble member and want to maximize the gain?  *[bug fix, ensemble member update, gain maximization, re-tuning after fix]*
- What do I do when one component in my ensemble has an ad-hoc training loop that doesn't match the rigor of other components?  *[training rigor mismatch, ensemble component, training loop quality, pipeline consistency]*
- What do I do when recent additions to a blend have all degraded performance and I suspect the ensemble is over-complicated?  *[ensemble overcomplexity, blend degradation, ensemble simplification, score regression]*
- What do I do when removing one ensemble member worsens the score after I just confirmed both members help together?  *[ensemble member removal, score regression, member interdependence, ensemble composition]*
## 8 items, 7 kernels
- What do I do when I have a new structural idea that is binary (on/off) rather than a continuous hyperparameter?  *[binary structural change, ablation study, architecture decision]*
- What do I do when I have a working ensemble and want to test whether a different backbone could improve or replace it?  *[backbone replacement, ensemble improvement, architecture exploration]*
- What do I do when I want to evaluate whether a new model architecture or backbone improves over the current best?  *[new architecture evaluation, backbone selection, baseline comparison]*
- What do I do when I want to explore whether a lighter/different backbone can match my current best model?  *[lighter backbone, backbone selection, model comparison, efficiency tradeoff]*
- What do I do when I want to test whether a simpler architecture can match a complex one that holds the current best score?  *[architecture simplification, complexity reduction, strong baseline comparison]*
- What do I do when switching a transformer backbone from base to large size for inference?  *[backbone scaling, base to large, transformer backbone, architecture swap]*
- What do I do when switching to a different model backbone family (e.g., EfficientNet → EfficientNetV2) for inference?  *[backbone family swap, architecture swap, model selection, inference evaluation]*
- What do I do when testing a new model architecture variant (e.g., separated heads) across backbone sizes to find the best configuration?  *[architecture variant search, backbone size selection, model head design, configuration sweep]*
## 8 items, 8 kernels
- What do I do when I fork or adapt someone else's notebook and it fails to run due to missing optional dependencies?  *[forked notebook, missing dependencies, environment setup, dependency resolution]*
- What do I do when I need to get a borrowed/forked inference notebook to produce a valid submission for the first time?  *[forked notebook adaptation, first valid submission, inference pipeline debugging]*
- What do I do when I want my notebook to behave differently in local testing vs. competition submission without manual edits?  *[environment detection, local vs submission, notebook automation]*
- What do I do when I want to simplify dependencies in an inference notebook that uses custom-packaged model code?  *[dependency simplification, inference notebook, custom model packaging]*
- What do I do when adapting a complex public notebook to get my first working submission?  *[first submission, public notebook adaptation, pipeline setup]*
- What do I do when setting up a Kaggle inference notebook that depends on custom libraries and model checkpoints stored as dataset uploads?  *[inference notebook setup, kaggle dataset dependencies, custom library integration]*
- What do I do when setting up a new inference notebook that depends on pretrained model artifacts stored as Kaggle datasets?  *[inference notebook setup, kaggle dataset dependencies, pretrained model artifacts]*
- What do I do when starting a competition inference notebook from scratch with pre-trained artifacts?  *[inference notebook setup, pretrained artifacts, competition start]*
## 8 items, 7 kernels
- What do I do when I have a strong baseline score and want to explore whether a feature-processing parameter can yield further improvement?  *[strong baseline, feature processing parameter, incremental improvement]*
- What do I do when I have a well-performing CNN inference pipeline and want to push the score higher?  *[strong baseline, cnn inference pipeline, score improvement]*
- What do I do when I want to improve a two-stage fine-tuning pipeline by filtering training samples more strictly?  *[training sample filtering, two-stage fine-tuning, data quality improvement]*
- What do I do when I've just added a new inference technique (like TTA) that improved my score and I have a multi-component blended submission?  *[score improvement, test-time augmentation, blended submission update, multi-component pipeline]*
- What do I do when I've just made a structural change to the ensemble that improved the score?  *[score improvement, ensemble structural change, consolidation after improvement]*
- What do I do when a neural network component has shown strong gains but was trained with ad-hoc code lacking proper fold-wise saving and DataLoader us  *[code quality improvement, neural network component, fold-wise saving, dataloader refactoring]*
- What do I do when a nonlinear prediction transform (e.g., sqrt) improved the score and I want to build on that?  *[score improvement, prediction transform, iterative refinement]*
- What do I do when my baseline uses a small model at low resolution with a slow data pipeline and scores poorly?  *[weak baseline, model scaling, data pipeline improvement, resolution increase]*
## 8 items, 4 kernels
- What do I do when I suspect the meta-learner's hyperparameter search may be under-exploring the solution space?  *[hyperparameter search, meta-learner, search space exploration]*
- What do I do when I want to expand a hyperparameter search space but am near the end of a competition?  *[hyperparameter search space, time constraint, late-stage exploration]*
- What do I do when I want to explore a hyperparameter whose effect direction and optimal magnitude are unknown?  *[unknown hyperparameter effect, hyperparameter exploration, search strategy]*
- What do I do when I want to explore many hyperparameter combinations but each run is expensive and I have no leaderboard submissions to calibrate?  *[expensive training runs, hyperparameter exploration, no leaderboard calibration, search strategy]*
- What do I do when a large improvement suggests I'm in a productive region of the search space?  *[large improvement, search space exploration, momentum exploitation]*
- What do I do when a long hyperparameter sweep on one lever yields diminishing or unclear returns?  *[diminishing returns, hyperparameter sweep, search space exhaustion, exploration strategy]*
- What do I do when a long hyperparameter sweep yields no clear improvement?  *[no improvement, hyperparameter sweep, search space exhaustion, exploration strategy]*
- What do I do when my Ridge meta-learner's Optuna-tuned hyperparameters might be constrained by the search bounds?  *[search space bounds, hyperparameter tuning, ridge meta-learner, optuna constraints]*
## 8 items, 7 kernels
- What do I do when I have many variable-renaming and column-alignment bugs after refactoring an inference pipeline?  *[pipeline refactoring bugs, variable renaming errors, column alignment, inference pipeline debugging]*
- What do I do when I need to integrate a new cross-validation scheme that touches multiple parts of the pipeline (imports, variable names, data sources  *[cross-validation integration, multi-component refactor, pipeline restructuring]*
- What do I do when I need to set many interdependent constants in a refactored pipeline?  *[interdependent constants, pipeline configuration, refactored pipeline, parameter management]*
- What do I do when I reduce the dimensionality of a feature-generation step and the pipeline breaks or produces wrong results?  *[dimensionality reduction, pipeline breakage, feature generation change, debugging after refactor]*
- What do I do when I want to refactor a complex inference pipeline that has been incrementally built up over many versions?  *[pipeline refactoring, complex inference pipeline, code maintainability, incremental complexity]*
- What do I do when a new feature integration requires multiple debugging iterations before I can even evaluate it?  *[debugging, feature integration, pipeline error, iterative fixing]*
- What do I do when integrating a complex new component (new model type) into an existing pipeline that may have bugs?  *[new model integration, pipeline debugging, bug prevention, complex component]*
- What do I do when my feature pipeline uses multiple ML models (sentence transformers, topic models) that share generic variable names and may conflict  *[variable name conflict, feature pipeline, namespace management]*
## 8 items, 8 kernels
- What do I do when I have been iterating on a complex pipeline for many versions without submitting?  *[long iteration without submission, pipeline validation, submission verification]*
- What do I do when I need to iterate on edge-case fixes in a post-processing pipeline without wasting submission budget?  *[post-processing edge cases, submission budget conservation, iterative debugging, offline validation]*
- What do I do when I want to finalize a submission after a period of fast iteration with shortcuts?  *[submission finalization, code cleanup, fast iteration shortcuts]*
- What do I do when I want to iterate quickly on ensemble composition without wasting LB submissions?  *[rapid iteration, ensemble composition, submission quota conservation, local validation]*
- What do I do when I want to iterate quickly on hyperparameters without wasting submission quota?  *[rapid iteration, hyperparameter tuning, submission quota conservation, local validation]*
- What do I do when I want to make multiple interacting changes to a training pipeline without wasting leaderboard submissions?  *[multiple simultaneous changes, training pipeline, submission quota conservation, local validation]*
- What do I do when I want to test a new post-processing idea that requires multiple code changes before it can produce a valid submission?  *[post-processing idea, multi-step code change, staged implementation, valid submission requirement]*
- What do I do when iterating on ensemble composition requires multiple submissions just to fix bugs and get valid scores?  *[ensemble composition, debugging submissions, iteration overhead, bug fixing]*
## 8 items, 4 kernels
- What do I do when I have a two-stage survival prediction pipeline and want to find the best subset and weighting of diverse model families?  *[survival prediction, model selection, ensemble weighting, diverse model families, two-stage pipeline]*
- What do I do when I have an ensemble of survival models trained on multiple target transformations and want to improve diversity/performance?  *[ensemble diversity, survival models, target transformation, performance improvement]*
- What do I do when I want to move from linear survival models to gradient-boosted trees for a survival prediction task?  *[model family switch, survival prediction, gradient boosted trees, linear to tree transition]*
- What do I do when a survival model outputs both a binary classifier and a continuous regressor and I need to combine them into a single risk score?  *[prediction combination, survival model, binary and continuous output, risk score design]*
- What do I do when adding a new GBDT variant (different target transformation) to a survival prediction ensemble?  *[ensemble diversity, gbdt variant addition, target transformation, survival prediction]*
- What do I do when linear survival models (Cox PH variants) plateau on a tabular survival prediction task?  *[model plateau, survival prediction, linear model limitations, model selection]*
- What do I do when my survival prediction ensemble needs a better target representation for tree-based regressors?  *[target representation, survival prediction, tree-based regressors, ensemble target engineering]*
- What do I do when predicting survival risk scores and need a regression target for tree/NN models?  *[survival prediction, target engineering, regression target, risk score formulation]*
## 7 items, 6 kernels
- What do I do when I want to add infrastructure (feature selection, new features) without risking my leaderboard position?  *[infrastructure addition, feature selection, risk management, leaderboard preservation]*
- What do I do when I want to test a risky model change without wasting a leaderboard submission?  *[risky model change, submission budget, leaderboard conservation, risk mitigation]*
- What do I do when I'm changing multiple hyperparameters at once and need to interpret leaderboard feedback?  *[multiple simultaneous changes, leaderboard feedback interpretation, change attribution]*
- What do I do when a leaderboard probe shows a clear regression?  *[leaderboard regression, leaderboard probe, recovery after change]*
- What do I do when a leaderboard probe shows a regression from the current best?  *[leaderboard regression, leaderboard probe, comparison to best, recovery after change]*
- What do I do when a leaderboard regression occurs after a small hyperparameter change?  *[leaderboard regression, hyperparameter change, small change sensitivity, recovery after change]*
- What do I do when a leaderboard score drops after a change and I have limited submissions?  *[leaderboard regression, limited submissions, submission budget, recovery after change]*
## 7 items, 7 kernels
- What do I do when I get a clear improvement from a regularization change and want to push further?  *[regularization improvement, pushing further, hyperparameter exploration]*
- What do I do when I have many manually-set regularization hyperparameters and I'm unsure which ones help?  *[regularization hyperparameters, hyperparameter validation, manual tuning uncertainty]*
- What do I do when exploring hyperparameters but unsure whether changes are truly improving the model?  *[hyperparameter exploration, improvement uncertainty, validation reliability]*
- What do I do when leaderboard scores are noisy and I need to find the best value of a single hyperparameter?  *[leaderboard noise, hyperparameter tuning, single parameter optimization]*
- What do I do when sweeping a small discrete set of options and getting noisy leaderboard feedback?  *[discrete option sweep, noisy leaderboard feedback, small search space, hyperparameter tuning]*
- What do I do when tuning a continuous parameter using only a noisy leaderboard signal with very few evaluation rows?  *[noisy leaderboard signal, continuous hyperparameter tuning, small evaluation set, signal-to-noise ratio]*
- What do I do when tuning a hyperparameter at inference time produces no leaderboard change after the first probe?  *[inference hyperparameter tuning, no leaderboard change, initial probe result]*
## 7 items, 7 kernels
- What do I do when I have multiple transformer backbones of varying quality and want to combine them?  *[backbone comparison, varying quality, ensemble composition, transformer models]*
- What do I do when I have multiple transformer checkpoints of varying quality in a stacking ensemble?  *[varying quality, stacking ensemble, checkpoint selection, transformer models]*
- What do I do when I want to add a retrieval-based (bi-encoder) signal to an existing transformer ensemble?  *[retrieval signal integration, bi-encoder addition, ensemble expansion, transformer ensemble]*
- What do I do when I want to add an SVR-on-embeddings member to a transformer ensemble?  *[new model type, embedding-based model, ensemble expansion, transformer ensemble]*
- What do I do when I want to test whether expanding the transformer embedding ensemble improves a tree-based downstream model?  *[embedding ensemble expansion, transformer embeddings, stacking improvement test]*
- What do I do when choosing between more transformer ensemble members with more embedding features versus fewer members with fewer features for a Light  *[ensemble member count, embedding feature count, stacker input tradeoff, transformer ensemble]*
- What do I do when ensembling transformer models that use different architectures or tokenizers?  *[heterogeneous architectures, tokenizer mismatch, ensemble combination, transformer models]*
## 7 items, 5 kernels
- What do I do when I want to evaluate whether a new training technique (e.g., pseudo-labels) improves my ensemble?  *[new training technique, pseudo-labels, ensemble improvement, contribution test]*
- What do I do when I want to improve regularization for a multi-class soft-label classification task with limited expert labels?  *[regularization improvement, soft-label classification, limited labeled data, multi-class task]*
- What do I do when I want to test whether noise-augmented base models can replace large pseudo-labeled models in a fold-averaged ensemble?  *[noise augmentation vs pseudo labeling, model replacement test, ensemble composition]*
- What do I do when a new training variant (pseudo-labeling) has been tested across several submissions and consistently underperforms my best ensemble?  *[consistent underperformance, pseudo-labeling evaluation, training variant abandonment]*
- What do I do when my ensemble model has plateaued on a survival prediction task with noisy positive-class labels?  *[score plateau, noisy labels, survival prediction, label noise handling]*
- What do I do when my survival model's training set may contain noisy or contradictory samples that hurt generalization?  *[noisy training samples, survival model, data cleaning, generalization improvement]*
- What do I do when training data has class imbalance and variable label quality in a multi-class soft-label setting?  *[class imbalance, label noise, soft-label classification, training strategy]*
## 7 items, 5 kernels
- What do I do when I have a handcrafted-feature LightGBM baseline and want to incorporate pretrained language model signals?  *[pretrained language model, feature augmentation, lightgbm baseline, hybrid model integration]*
- What do I do when I want to improve a LightGBM model that already uses transformer embeddings as features?  *[lightgbm improvement, transformer embeddings as features, feature engineering]*
- What do I do when I want to incorporate categorical metadata into a pretrained transformer model?  *[categorical metadata integration, pretrained transformer, feature incorporation]*
- What do I do when I want to use transformer embeddings as features for a gradient boosting model but extraction is slow and memory-intensive?  *[transformer embeddings, feature extraction efficiency, memory optimization, gbdt feature pipeline]*
- What do I do when adding expensive high-dimensional features (e.g., pretrained embeddings) fails to improve the score over multiple attempts?  *[pretrained embeddings, high-dimensional features, no improvement, feature cost-benefit]*
- What do I do when adding high-dimensional transformer embeddings as features to a tree-based model gives inconsistent leaderboard results?  *[pretrained embeddings, high-dimensional features, leaderboard instability, tree-based model]*
- What do I do when integrating transformer embeddings with gradient-boosted tree ensembles for a text regression task?  *[transformer embeddings, gradient-boosted trees, text regression, hybrid model integration]*
## 7 items, 6 kernels
- What do I do when I suspect a latent bug in fold-level inference that may be suppressing ensemble quality?  *[fold-level inference bug, ensemble quality, latent bug diagnosis]*
- What do I do when I suspect a logic/scoping bug in my inference loop is silently producing wrong predictions?  *[inference loop bug, silent prediction error, scoping bug, logic debugging]*
- What do I do when a 1D CNN model produces runtime errors or unexpectedly bad scores during inference?  *[runtime error, 1d cnn inference, score regression, model debugging]*
- What do I do when adding a neural network to a fold-based ensemble and test predictions look wrong?  *[incorrect predictions, neural network integration, fold-based ensemble, prediction debugging]*
- What do I do when model.predict() fails and I suspect the batch_size parameter is the cause?  *[prediction failure, batch size debugging, inference error]*
- What do I do when my ensemble inference pipeline has a runtime flag that may behave incorrectly in a special inference mode (e.g., hack/test mode)?  *[inference pipeline bug, runtime flag correctness, inference mode debugging]*
- What do I do when spectrogram-based model inference produces very poor results compared to expectations?  *[poor inference results, spectrogram preprocessing, debugging predictions]*
## 7 items, 5 kernels
- What do I do when I have many candidate ensemble members and two aggregation methods (mean vs weighted blend)?  *[aggregation method comparison, ensemble member selection, mean vs weighted blend]*
- What do I do when I have multiple discrete configuration options (e.g., blending methods, model subsets) and need to find the best combination quickly  *[configuration search, discrete option combination, blending method selection]*
- What do I do when I need to decide whether to apply rank-based averaging to ensemble predictions?  *[rank averaging, ensemble method selection, prediction blending]*
- What do I do when I want to test whether a specific blend component is better than another in a multi-component weighted average?  *[blend component comparison, ensemble weighting, member substitution]*
- What do I do when I'm unsure whether rank-based averaging or raw probability averaging is better for a given model ensemble?  *[ensemble averaging strategy, rank averaging vs probability averaging, blending method selection]*
- What do I do when probability-based ensemble averaging has plateaued and I want another way to combine predictions?  *[ensemble averaging plateau, combination strategy, probability ensembling, alternative blending]*
- What do I do when weighted arithmetic blending of predictions produces unexpected results or errors?  *[weighted blending, arithmetic averaging, prediction combination, blending debugging]*
## 7 items, 4 kernels
- What do I do when I have a working image classification pipeline and want to improve accuracy by tuning input resolution?  *[input resolution tuning, image classification, accuracy improvement]*
- What do I do when I have an EfficientNet model and need to choose the right test-time input resolution?  *[test-time input resolution, efficientnet configuration, resolution selection]*
- What do I do when I need to ensure the inference image resolution matches what the model expects?  *[image resolution mismatch, inference preprocessing, input resolution alignment]*
- What do I do when I want to find the best inference image resolution for a pretrained CNN ensemble on medical images?  *[inference resolution tuning, pretrained cnn ensemble, medical image classification]*
- What do I do when I want to improve inference quality by changing the input image size for a pretrained CNN?  *[input image resolution, pretrained cnn, inference-time improvement]*
- What do I do when increasing input resolution for a CNN inference pipeline trained at a different resolution?  *[input resolution mismatch, CNN inference pipeline, resolution scaling, test-time resolution]*
- What do I do when my pretrained model's expected input resolution doesn't match the image size used in the inference pipeline?  *[input resolution mismatch, pretrained model, inference pipeline]*
## 7 items, 5 kernels
- What do I do when I have a working baseline and want to try a fundamentally different model architecture?  *[architecture change, model exploration, working baseline]*
- What do I do when I have a working baseline and want to try a substantially different model head?  *[model head change, architecture modification, working baseline]*
- What do I do when I want to add a new model variant to an ensemble but the integration involves multiple simultaneous changes (preprocessing, TTA, arc  *[multiple simultaneous changes, new model variant, ensemble integration, preprocessing change, TTA addition, architecture change]*
- What do I do when I want to test a new model but also need to adjust preprocessing parameters simultaneously?  *[new model testing, preprocessing adjustment, simultaneous changes, change isolation]*
- What do I do when I want to test a new model variant that also requires infrastructure changes (different preprocessing, different device handling)?  *[new model variant, infrastructure changes, preprocessing adjustment, multi-component change]*
- What do I do when I want to try a different model artifact but am unsure it will work?  *[model artifact swap, uncertainty about compatibility, safe experimentation]*
- What do I do when switching to a new model variant that reuses the same codebase but has a different experiment identifier?  *[model variant switching, experiment identifier update, codebase reuse]*
## 7 items, 6 kernels
- What do I do when I introduce a new feature source alongside other changes and the result improves but doesn't beat my overall best?  *[new feature source, confounded changes, incremental improvement]*
- What do I do when I need to integrate a new feature that changes multiple code paths before I can evaluate it?  *[new feature integration, multi-path code change, end-to-end validation]*
- What do I do when I want to add both a new feature source and a new model type to an existing pipeline?  *[new feature source, new model type, multiple simultaneous changes, pipeline integration]*
- What do I do when I want to test a new feature and it requires changing multiple hyperparameters simultaneously?  *[new feature testing, simultaneous hyperparameter changes, change isolation]*
- What do I do when I want to test a new feature or modality but the pipeline has multiple untested code changes?  *[new feature testing, untested code changes, change isolation, pipeline integrity]*
- What do I do when I'm adding multiple new feature sources and need to validate the pipeline before submitting?  *[new feature sources, pipeline validation, pre-submission verification, feature integration]*
- What do I do when adding a substantial new feature source that requires new library imports, data processing, and integration into both train and test  *[new feature source integration, data processing pipeline, library dependency management, train test consistency]*
## 7 items, 2 kernels
- What do I do when I want to add custom aggregation functions (e.g., lag values, differences) to a groupby feature pipeline for tabular time-series dat  *[custom aggregation functions, feature engineering, groupby features, tabular time-series]*
- What do I do when I want to add richer temporal features to a customer-level aggregation pipeline for sequential transaction data?  *[temporal feature engineering, customer-level aggregation, sequential transaction data]*
- What do I do when I want to capture recent customer behavior from time-series data that has been aggregated to one row per customer?  *[recency features, customer-level aggregation, time-series feature engineering]*
- What do I do when I want to capture temporal dynamics in customer-level aggregated features for a GBDT model?  *[temporal feature engineering, customer-level aggregation, gbdt model]*
- What do I do when I want to incorporate a date column into customer-level aggregated features for a GBDT model?  *[date feature engineering, customer-level aggregation, temporal features, gbdt model]*
- What do I do when I'm unsure which aggregation functions (count, first, size, var) to include in my customer-level feature set?  *[aggregation function selection, feature selection, customer-level features]*
- What do I do when building customer-level features from panel data with many raw columns for a GBDT model?  *[feature engineering, panel data, customer-level aggregation, gbdt model]*
## 7 items, 4 kernels
- What do I do when I introduce a new multi-step feature-engineering block that involves fit/predict on derived data and need to get it working correctl  *[feature engineering block, fit-predict pipeline, implementation debugging]*
- What do I do when I'm iterating on feature engineering but many runs have bugs that prevent meaningful evaluation?  *[buggy runs, feature engineering iteration, evaluation blocked, debugging pipeline]*
- What do I do when a promising feature engineering idea turns out to be computationally infeasible on the full dataset?  *[computational feasibility, feature engineering, scalability constraint, full dataset]*
- What do I do when adding a new category of handcrafted features requires significant infrastructure work before I can evaluate them?  *[feature engineering infrastructure, handcrafted features, implementation overhead, pipeline setup]*
- What do I do when aggregation of many features causes memory issues during cross-validation?  *[memory issues, feature aggregation, cross-validation, resource constraints]*
- What do I do when iterating on feature code that has bugs I can only see at runtime?  *[feature engineering, runtime bugs, iterative debugging]*
- What do I do when my aggregation-based feature pipeline is hitting memory limits on Kaggle's fixed-RAM environment?  *[memory limits, feature pipeline, resource constraints, aggregation features]*
## 7 items, 7 kernels
- What do I do when I have a model with both a regression head and a categorical/binning head and need to decide whether the binning head helps at infer  *[multi-head output, regression vs binning head, head selection, inference strategy comparison]*
- What do I do when I have multiple trained model variants with different output heads (sigmoid vs softmax vs log-softmax) and need to find the best one  *[model variant comparison, output head selection, inference configuration]*
- What do I do when I have trained checkpoints with an auxiliary output head and want to test whether the multi-task architecture improves inference?  *[auxiliary output head, multi-task architecture, inference evaluation]*
- What do I do when I want to simplify inference by loading a full saved model instead of reconstructing the architecture and loading weights separately  *[inference simplification, model loading strategy, saved model vs architecture reconstruction]*
- What do I do when I want to test a new inference configuration but it's expensive to run on all folds?  *[inference configuration, computational cost management, fold subset testing]*
- What do I do when I'm migrating to a new inference architecture (e.g., loading pretrained models) and need to verify correctness before iterating furt  *[inference architecture migration, pretrained model loading, correctness verification]*
- What do I do when fold models need to be reused at test time in a memory-constrained environment?  *[memory constraints, fold model reuse, test-time inference, model serialization]*
## 7 items, 5 kernels
- What do I do when I want to integrate multiple new components into a working pipeline?  *[multiple component integration, working pipeline, incremental integration, regression risk]*
- What do I do when I want to introduce multiple interacting changes (bug fix, feature expansion, normalization, new dependency) to a pipeline?  *[multiple interacting changes, pipeline modification, incremental integration, change isolation]*
- What do I do when I'm bootstrapping a new pipeline and need to decide the order of infrastructure setup, hyperparameter tuning, and submission?  *[pipeline bootstrapping, setup ordering, workflow prioritization, new pipeline initialization]*
- What do I do when building a new end-to-end pipeline that involves multiple untested components (data split, preprocessing, training, inference)?  *[end-to-end pipeline, multiple untested components, pipeline correctness, incremental development]*
- What do I do when building a new multi-step pipeline that may have bugs at each stage?  *[multi-step pipeline, bug detection, incremental development, pipeline correctness]*
- What do I do when building a new pipeline component that requires multiple interdependent code changes?  *[interdependent code changes, pipeline component, incremental development]*
- What do I do when building an initial pipeline where I need to verify multiple interacting changes (preprocessing, architecture, normalization) but ha  *[multiple interacting changes, limited submission budget, pipeline correctness, incremental development]*
## 7 items, 4 kernels
- What do I do when I suspect the training distribution doesn't match the test distribution and want to subset training data to the matching portion?  *[distribution mismatch, training data subsetting, domain adaptation]*
- What do I do when OneHotEncoder fitted on training data encounters unseen categories in test data?  *[unseen categories, one-hot encoding, train-test mismatch, categorical encoding]*
- What do I do when adding a new tree-based model that needs slightly different feature engineering than the shared pipeline?  *[new model type, feature engineering mismatch, tree-based model, pipeline adaptation]*
- What do I do when categorical encoding fails at test time because the test set contains categories unseen during training?  *[unseen categories, categorical encoding, train-test mismatch]*
- What do I do when feature generation code uses label-derived information that won't be available at test time?  *[target leakage, feature generation, train-test mismatch, label-derived features]*
- What do I do when my tabular model has underrepresented subgroups in training that differ from the test distribution?  *[underrepresented subgroups, distribution shift, tabular model, data augmentation]*
- What do I do when the training set contains a known subpopulation with a different distribution from the test set?  *[distribution shift, subpopulation mismatch, train-test discrepancy, data filtering]*
## 7 items, 3 kernels
- What do I do when I have a multi-input fusion model and want to know if the fusion head is contributing beyond simple averaging of single-backbone pre  *[fusion head contribution, multi-input fusion, fusion vs averaging, ablation study]*
- What do I do when I have a new set of models from a different modality and want to integrate them into an existing ensemble?  *[new modality, ensemble integration, multimodal fusion]*
- What do I do when I have predictions from multiple modalities (raw EEG, short spectrograms, longer spectrograms) and need to combine them?  *[multi-modality fusion, prediction combination, ensemble strategy]*
- What do I do when I have predictions from two modalities of very different quality and want to combine them?  *[multi-modality fusion, quality imbalance, ensemble weighting]*
- What do I do when I have separately developed models on different input modalities that each plateau at a moderate score?  *[score plateau, multi-modality fusion, ensemble combination]*
- What do I do when I want to add a multi-modal fusion model (e.g., EEG + spectrogram) to an existing single-modality ensemble?  *[multi-modal fusion, ensemble expansion, modality integration]*
- What do I do when a multi-head model can fuse features by averaging or concatenation, and I have pretrained weights for one configuration?  *[feature fusion strategy, multi-head model, pretrained weights compatibility, averaging vs concatenation]*
## 7 items, 3 kernels
- What do I do when I want to improve a multi-modal EEG/spectrogram classification model that has plateaued?  *[performance plateau, multi-modal model, eeg classification, architecture exploration]*
- What do I do when I want to improve an ensemble of 2D spectrogram CNNs that has plateaued?  *[ensemble plateau, spectrogram cnn, performance stagnation]*
- What do I do when my multimodal model has plateaued and I want to extract more signal from an existing modality?  *[score plateau, multimodal model, modality signal extraction]*
- What do I do when my single-modality CNN on spectrograms has plateaued and I have access to raw EEG signals?  *[performance plateau, new modality available, raw signal input, multimodal fusion]*
- What do I do when my spectrogram-based CNN ensemble has plateaued and I want to squeeze out more performance via preprocessing?  *[performance plateau, preprocessing improvement, spectrogram pipeline, cnn ensemble]*
- What do I do when my spectrogram-based ensemble has plateaued and I want to squeeze out more performance?  *[performance plateau, spectrogram ensemble, score improvement]*
- What do I do when my spectrogram-based model ensemble has reached a plateau and I suspect the input image region doesn't optimally cover the informati  *[performance plateau, frequency band selection, spectrogram crop region, input coverage optimization]*
## 6 items, 6 kernels
- What do I do when I'm near a local optimum and small perturbations in both directions yield regressions?  *[local optimum, score regression, perturbation sensitivity, hyperparameter tuning]*
- What do I do when I'm sweeping a post-processing hyperparameter and get a regression after an initial improvement?  *[postprocessing hyperparameter sweep, score regression, non-monotonic response, optimal stopping]*
- What do I do when I've just changed a hyperparameter but validation metrics suggest it may be worse?  *[hyperparameter change, score regression, validation metric comparison]*
- What do I do when a combined change (new features + hyperparameter tweak) produces a small regression on the leaderboard?  *[small score regression, combined change, feature engineering, hyperparameter tuning, change attribution]*
- What do I do when a sweep of a particular lever has produced several submissions all below my best score?  *[hyperparameter sweep, score regression, sweep analysis]*
- What do I do when fine-tuning a single continuous hyperparameter yields only partial recovery from a regression?  *[partial score recovery, score regression, single hyperparameter tuning, diminishing returns]*
## 6 items, 4 kernels
- What do I do when I have multiple candidate ensemble members and want to find the best combination?  *[multiple candidates available, ensemble member selection, best combination search]*
- What do I do when I have multiple candidate models and need to find the best subset for an ensemble?  *[multiple candidate models, ensemble subset selection, best combination search]*
- What do I do when I have multiple proven ensemble members and want to find the best combination?  *[proven ensemble members, ensemble configuration search, optimal combination]*
- What do I do when I want to find the best subset of diverse models for an ensemble on a small, noisy dataset?  *[ensemble subset selection, model diversity, small noisy dataset]*
- What do I do when I want to find the best subset of models for an ensemble but the search space of combinations is too large for exhaustive evaluation  *[ensemble subset selection, large search space, combinatorial optimization, efficient search strategy]*
- What do I do when I want to optimize an ensemble blend but have many candidate members and limited submission budget?  *[ensemble blend optimization, many candidate members, limited submission budget, member selection]*
## 6 items, 5 kernels
- What do I do when I need to iterate on infrastructure changes that have no direct leaderboard signal?  *[infrastructure changes, no leaderboard signal, offline iteration, pipeline refactor]*
- What do I do when I need to make multiple infrastructure changes before I can test a new idea on the leaderboard?  *[infrastructure changes, batched updates, leaderboard testing, pipeline refactor]*
- What do I do when I want to iterate on infrastructure without polluting my leaderboard history?  *[infrastructure iteration, leaderboard hygiene, offline development, submission management]*
- What do I do when a code change fails to produce a submission due to an infrastructure error?  *[infrastructure error, submission failure, code change debugging]*
- What do I do when a code change introduces a potential infrastructure bug that prevents execution?  *[infrastructure bug, execution failure, code change debugging]*
- What do I do when multiple infrastructure issues (temp files, verbose logging, package installs, row alignment) accumulate during pipeline assembly?  *[infrastructure issues, pipeline assembly, technical debt accumulation, debugging overhead]*
## 6 items, 5 kernels
- What do I do when I have multiple training seeds for the same model and want to maximize inference quality?  *[multiple seeds, inference quality, seed averaging, single model inference]*
- What do I do when I need to confirm an inference notebook is stable before submitting?  *[inference stability, notebook validation, pre-submission check]*
- What do I do when I want to determine whether an inference-time ensembling strategy (e.g., multi-seed averaging) is actually helping versus a simpler   *[inference ensembling, multi-seed averaging, baseline comparison, strategy evaluation]*
- What do I do when I want to improve ensemble quality but already have a working inference pipeline?  *[ensemble improvement, working inference pipeline, post-pipeline refinement]*
- What do I do when I want to know if my ensemble improvement is real vs. noise from non-deterministic inference?  *[ensemble improvement validation, non-deterministic inference, noise vs signal]*
- What do I do when I want to verify a new inference technique before committing to a leaderboard submission?  *[inference technique validation, pre-submission verification, new method testing]*
## 6 items, 1 kernels
- What do I do when I have both ordinal and regression inference pipelines for the same backbone size?  *[ordinal vs regression, inference pipeline selection, same backbone comparison]*
- What do I do when converting a regression inference pipeline to classification for an ordinal scoring task?  *[regression to classification, ordinal task, pipeline conversion]*
- What do I do when my ordinal regression model's rounding thresholds may not be optimal for the test distribution?  *[threshold optimization, ordinal regression, rounding thresholds, test distribution shift]*
- What do I do when per-class or per-group threshold tuning hurts ordinal regression performance?  *[threshold tuning, ordinal regression, per-class optimization, score regression]*
- What do I do when tuning optimized rounding thresholds for a regression-to-ordinal model and each submission costs a leaderboard attempt?  *[rounding threshold tuning, regression to ordinal, limited submission budget, leaderboard probing]*
- What do I do when tuning ordinal rounding thresholds for a regression-based essay scorer?  *[rounding threshold tuning, regression to ordinal, ordinal classification]*
## 6 items, 6 kernels
- What do I do when I have many DeBERTa-based ensemble members and cannot improve the blend score by adjusting membership?  *[ensemble plateau, homogeneous ensemble members, blend improvement]*
- What do I do when I have multiple model groups and augmentation options and need to find the best ensemble composition?  *[ensemble composition, augmentation options, model group selection, joint optimization]*
- What do I do when I want to determine whether adding more members to a blend improves score?  *[ensemble size selection, blend member addition, score improvement test]*
- What do I do when I want to test whether a new component variant improves an ensemble while also tuning blend weights?  *[ensemble member selection, component variant test, blend weight tuning]*
- What do I do when I've changed the composition of an ensemble (added/removed models or changed model paths) and need to re-tune the blend?  *[ensemble composition change, blend weight re-tuning, model addition removal]*
- What do I do when adding a new ensemble member to a large blend that already has many components?  *[new ensemble member, large ensemble, ensemble member selection, blend complexity]*
## 6 items, 4 kernels
- What do I do when I have pretrained checkpoints loaded with zero dropout and want to check if inference-time dropout regularization helps?  *[inference-time dropout, regularization experiment, pretrained checkpoints]*
- What do I do when a transformer ensemble member's inference dropout setting may not match training?  *[inference dropout, train-test mismatch, transformer ensemble, configuration consistency]*
- What do I do when adjusting dropout at inference time for a pretrained transformer checkpoint?  *[dropout adjustment, inference configuration, pretrained transformer, checkpoint adaptation]*
- What do I do when my inference preprocessing must match training preprocessing but I'm loading a custom checkpoint?  *[preprocessing consistency, train-inference alignment, custom checkpoint loading]*
- What do I do when my training pipeline used text normalization but my inference pipeline does not?  *[train-inference mismatch, text normalization, preprocessing consistency]*
- What do I do when spectrogram preprocessing parameters (scaling, frequency crop, normalization) need to match what the model was trained with?  *[preprocessing consistency, spectrogram parameters, train-inference alignment]*
## 6 items, 6 kernels
- What do I do when I have a multi-component inference pipeline that is failing and I need to fix several interdependent issues before I can evaluate it  *[pipeline debugging, interdependent failures, multi-component pipeline, inference pipeline fix]*
- What do I do when I introduce a code change that breaks the pipeline?  *[pipeline breakage, code change debugging, error recovery]*
- What do I do when I want to transition from a debug/development mode to a full production run?  *[debug to production transition, full training run, pipeline mode switch]*
- What do I do when my feature matrix construction fails with type or key errors in a mixed feature pipeline?  *[pipeline error, feature matrix construction, type error debugging]*
- What do I do when my model produces nonsensical predictions (e.g., negative scores on a positive metric) indicating a broken pipeline?  *[broken pipeline, nonsensical predictions, pipeline debugging]*
- What do I do when my notebook pipeline fails at runtime and I can't see the full error until I run it?  *[runtime failure, error visibility, pipeline debugging, logging improvement]*
## 6 items, 6 kernels
- What do I do when I have a working pipeline but haven't yet submitted to the leaderboard?  *[first submission, leaderboard baseline, working pipeline]*
- What do I do when I have a working single-holdout training pipeline but haven't yet submitted, and want to establish a robust baseline score?  *[robust baseline, first submission, single holdout, cross-validation setup]*
- What do I do when I need to establish a first working submission for a competition?  *[first submission, baseline pipeline, competition entry]*
- What do I do when I need to establish a working baseline quickly before exploring model diversity?  *[quick baseline, first submission, model diversity exploration]*
- What do I do when starting a competition with no prior submissions and needing to establish a working pipeline?  *[competition start, baseline pipeline, first submission]*
- What do I do when starting from a public baseline notebook and I want to make a first competitive submission quickly?  *[competition start, public baseline, first submission, quick iteration]*
## 6 items, 4 kernels
- What do I do when I need to iterate quickly on a notebook that has expensive preprocessing and inference steps?  *[expensive preprocessing, expensive inference, notebook iteration speed, development efficiency]*
- What do I do when I need to iterate quickly on a notebook that has expensive preprocessing steps?  *[expensive preprocessing, notebook iteration speed, development efficiency]*
- What do I do when I want to add a stacked model's predictions as features but the in-notebook training is unstable or slow?  *[stacking features, training instability, in-notebook training, slow training]*
- What do I do when I want to iterate quickly on model/feature changes but preprocessing is expensive?  *[rapid iteration, expensive preprocessing, feature engineering, caching intermediate results]*
- What do I do when adding many features causes memory or runtime issues in a Kaggle notebook environment?  *[memory constraints, runtime constraints, feature scalability, notebook environment]*
- What do I do when my notebook has grown complex with inline feature engineering that slows iteration and risks memory issues?  *[notebook complexity, inline feature engineering, code modularization, memory management]*
## 6 items, 6 kernels
- What do I do when I want to add a novel postprocessing component to an existing pipeline?  *[postprocessing addition, pipeline extension, novel component integration]*
- What do I do when I want to improve a complex ensemble pipeline that has multiple sub-models and post-processing steps?  *[complex ensemble pipeline, multi-component optimization, post-processing refinement]*
- What do I do when I want to improve multiple aspects of my pipeline (data format, features, hyperparameters, preprocessing) simultaneously?  *[simultaneous pipeline changes, multi-aspect optimization, preprocessing and features]*
- What do I do when I want to test whether a simpler post-processing step can replace a tuned one?  *[postprocessing simplification, complexity reduction, pipeline improvement test]*
- What do I do when a first batch of post-processing rules gives a large gain and I want more?  *[post-processing rules, large gain, iterative refinement, rule expansion]*
- What do I do when a postprocessing tweak yields a marginal improvement and I want to refine it?  *[marginal improvement, post-processing refinement, iterative tuning]*
## 6 items, 5 kernels
- What do I do when I need to train more models than fit in a single compute session's time budget?  *[compute constraints, training time budget, multi-session training, model training]*
- What do I do when I need to train multiple cross-validation folds but face runtime constraints on a single kernel session?  *[cross-validation folds, runtime constraints, kernel session limits, training time budget]*
- What do I do when I want to add a new model component to an ensemble but the notebook has memory/runtime constraints?  *[new model component, memory constraints, runtime constraints, ensemble expansion]*
- What do I do when I want to improve ensemble quality but am constrained by inference time/memory budget?  *[inference budget constraint, ensemble quality, memory limitation]*
- What do I do when I want to integrate a computationally expensive model into an ensemble on a resource-constrained platform?  *[expensive model integration, ensemble construction, resource constraints, inference budget]*
- What do I do when adding a new heavy inference component to a resource-constrained notebook?  *[resource constraints, new ensemble member, inference efficiency, notebook environment]*
## 6 items, 3 kernels
- What do I do when changing spectrogram resolution and sampling rate together causes a regression in a CNN spectrogram model?  *[score regression, spectrogram resolution, sampling rate, coupled hyperparameter change]*
- What do I do when my EEG model's inference score degrades after changing frequency-domain preprocessing parameters?  *[score regression, preprocessing parameter change, frequency-domain preprocessing, eeg model]*
- What do I do when my EEG-to-spectrogram pipeline has multiple interacting preprocessing parameters (clipping, filter band, FFT window, scaling) that j  *[interacting preprocessing parameters, joint hyperparameter tuning, spectrogram pipeline, eeg preprocessing]*
- What do I do when my spectrogram model uses instance normalization on multi-channel inputs?  *[instance normalization, multi-channel spectrogram, normalization strategy]*
- What do I do when tuning input windowing/cropping parameters for spectrogram-based EEG models at inference time?  *[inference-time tuning, input windowing, spectrogram parameters, eeg models]*
- What do I do when tuning the input window/crop size for spectrogram or EEG-based models at inference time?  *[inference-time tuning, input windowing, crop size, spectrogram parameters, eeg models]*
## 5 items, 4 kernels
- What do I do when integrating a custom metric into a training framework that has a specific callback signature?  *[custom metric integration, training framework, callback signature, code adaptation]*
- What do I do when the competition metric is a composite of sub-metrics and I want to use it as a custom training objective/eval metric?  *[composite metric, custom loss function, metric alignment, training objective design]*
- What do I do when the competition metric weights classes asymmetrically and I want to align training with it?  *[asymmetric class weighting, loss function alignment, competition metric]*
- What do I do when using a custom QWK evaluation metric across both LightGBM and XGBoost training loops?  *[custom evaluation metric, quadratic weighted kappa, multi-framework consistency, gradient boosting training]*
- What do I do when using a custom QWK-approximating objective for gradient boosting and training seems unstable or underperforming?  *[custom loss function, training instability, quadratic weighted kappa, gradient boosting objective]*
## 5 items, 5 kernels
- What do I do when I have a transformer ensemble and want incremental improvement without changing architectures?  *[transformer ensemble, incremental improvement, hyperparameter tuning, fixed architecture]*
- What do I do when I have a working transformer regression head and want to squeeze out small gains from the head architecture?  *[regression head architecture, transformer model, incremental improvement, head design tuning]*
- What do I do when I want to improve a transformer ensemble's score on a small-data NLP regression task?  *[transformer ensemble improvement, small data nlp, regression task]*
- What do I do when I want to test whether a transformer-centric ensemble can replace a handcrafted-feature + gradient-boosting pipeline?  *[architecture comparison, transformer vs gradient boosting, pipeline replacement test]*
- What do I do when blending transformer models of different architectures for a regression task on small data?  *[transformer ensemble, architecture diversity, small data regression]*
## 5 items, 4 kernels
- What do I do when I have a binary classifier mask that additively adjusts a regression/ranking model's predictions and I need to find the right magnit  *[classifier mask adjustment, additive correction magnitude, postprocessing calibration, hyperparameter search]*
- What do I do when I have a well-tuned global post-processing step and suspect that subgroup-specific calibration could help?  *[subgroup calibration, post-processing refinement, group-specific tuning, well-tuned pipeline]*
- What do I do when I have hand-tuned post-processing thresholds that improved my score, and I want to rebuild them from scratch for a changed model?  *[post-processing thresholds, threshold recalibration, model change adaptation, hand-tuned rebuild]*
- What do I do when I switch to a new model variant and need to calibrate post-processing?  *[model variant change, post-processing calibration, threshold tuning]*
- What do I do when I want to try a new post-processing normalization on model outputs?  *[post-processing normalization, output calibration, new technique trial]*
## 5 items, 4 kernels
- What do I do when my LightGBM regressor outputs continuous scores that must be mapped to integer labels for a QWK metric?  *[continuous to discrete mapping, threshold optimization, qwk metric, lightgbm postprocessing]*
- What do I do when my Spearman-correlated predictions contain continuous values but the ground truth takes only a few discrete levels?  *[continuous to discrete mapping, spearman correlation, prediction discretization]*
- What do I do when my continuous regression outputs need to be mapped to discrete ordinal labels to maximize quadratic weighted kappa?  *[continuous to discrete mapping, threshold optimization, quadratic weighted kappa, ordinal labels]*
- What do I do when my model predicts continuous values but the metric (Spearman correlation) depends on ranks and the true labels take only a few discr  *[continuous to discrete mapping, rank-based metric, prediction discretization]*
- What do I do when my regression model outputs continuous scores that must be mapped to discrete ordinal labels for a QWK metric?  *[continuous to discrete mapping, ordinal labels, qwk metric, rounding threshold optimization]*
## 5 items, 5 kernels
- What do I do when I want to probe multiple training configurations but each run is expensive?  *[expensive training runs, configuration search, compute efficiency, experiment prioritization]*
- What do I do when I want to test a computationally expensive new feature idea that requires iterative debugging?  *[expensive feature idea, iterative debugging, computational cost management]*
- What do I do when I want to test a risky new idea (e.g., a different algorithm variant) that may also be much slower?  *[risky algorithm variant, compute cost concern, runtime increase, risk mitigation]*
- What do I do when I want to test an expensive training variant without wasting too much compute?  *[expensive training variant, compute budget, cost-efficient experimentation]*
- What do I do when iterating on ensemble composition and each run is expensive (full inference pipeline)?  *[ensemble composition, expensive inference, iteration efficiency]*
## 5 items, 4 kernels
- What do I do when I suspect numerical precision issues may be hurting prediction quality?  *[numerical precision, prediction quality, floating point issues]*
- What do I do when a transformation applied to predictions (e.g., power transform) gives mixed signals about whether it helps?  *[prediction transformation, mixed signals, power transform, improvement uncertainty]*
- What do I do when competition data is stored in float16 and may contain artificial noise at that precision level?  *[data precision, float16 storage, artificial noise, data preprocessing]*
- What do I do when inference scores are noisy and I suspect floating-point non-determinism from mixed precision?  *[score noise, mixed precision, floating-point non-determinism, inference debugging]*
- What do I do when switching to mixed-precision inference causes a score regression with a transformer regressor?  *[score regression, mixed-precision inference, numerical precision, transformer regressor]*
## 5 items, 2 kernels
- What do I do when I have a binary post-processing toggle whose effect varies across model versions?  *[postprocessing toggle, interaction with model version, robustness across configurations]*
- What do I do when I have a binary postprocessing toggle (e.g., rank-averaging vs raw-score averaging) and I'm also changing another hyperparameter?  *[postprocessing toggle, hyperparameter interaction, joint parameter search, confounded comparison]*
- What do I do when I have a binary postprocessing toggle and want to know whether it helps across different model/ensemble configurations?  *[postprocessing toggle, robustness across configurations, ensemble generalization]*
- What do I do when I have a binary postprocessing toggle that sometimes helps and sometimes hurts?  *[postprocessing toggle, inconsistent effect, conditional application, robustness assessment]*
- What do I do when I want to test a new preprocessing idea but have multiple interacting toggles (feature flags, checkpoints)?  *[preprocessing idea, interacting feature flags, experiment isolation, toggle management]*
## 5 items, 4 kernels
- What do I do when I want to evaluate a new architectural component that requires retraining, and I also have a binary postprocessing toggle that inter  *[architecture change, postprocessing toggle, interaction effect, joint evaluation]*
- What do I do when I want to test a fundamentally new input representation that requires both architecture changes and new checkpoints?  *[new input representation, architecture change, checkpoint update, multi-component change]*
- What do I do when I want to try an infrastructure change (e.g., mixed precision) on an already-optimized pipeline?  *[infrastructure change, mixed precision, optimized pipeline modification]*
- What do I do when I'm exploring multiple architectural changes (new model types, new feature groups) simultaneously without submitting?  *[multiple architectural changes, offline exploration, new model types, feature group exploration]*
- What do I do when testing a model architecture change and I also have a binary post-processing toggle (rank conversion) that sometimes helps?  *[architecture change, post-processing toggle, rank conversion, ablation study]*
## 5 items, 5 kernels
- What do I do when I want to improve my score by changing input preprocessing but the model weights are already frozen?  *[input preprocessing change, frozen model weights, inference-time improvement]*
- What do I do when I want to test a different pretrained model size to see if it performs comparably or better?  *[pretrained model size, model scaling, performance comparison]*
- What do I do when I want to test multiple pretrained backbones or model variants in an inference-only notebook?  *[pretrained backbone selection, model variant comparison, inference-only notebook]*
- What do I do when I want to test whether a different pretrained backbone improves over my current best?  *[pretrained backbone selection, model comparison, baseline improvement]*
- What do I do when loading a fine-tuned checkpoint into a model architecture that also supports pretrained initialization from a library like timm?  *[checkpoint loading, pretrained initialization, fine-tuned weights, timm integration]*
## 5 items, 5 kernels
- What do I do when I discover that a debug shortcut (e.g., early exit after one fold) was accidentally left in a submitted notebook that achieved a new  *[debug shortcut, accidental submission, score validity, result verification]*
- What do I do when I have trained a new model offline and want to verify whether it improves over my current best public score?  *[new model evaluation, public score verification, score improvement check]*
- What do I do when I want to test whether a single addition improves my score but the first run may have failed silently?  *[silent failure, single change test, result validation, score verification]*
- What do I do when I've been debugging a new component in isolation and each partial run scores far below my best ensemble?  *[component debugging, isolation testing, score gap, partial run evaluation]*
- What do I do when a single change produces a large score jump but I want to confirm it's real and not a fluke?  *[large score jump, result validation, fluke detection, single change verification]*
## 5 items, 5 kernels
- What do I do when a large multi-lever change produces a modest improvement but not a new best?  *[modest improvement, multi-lever change, diminishing returns, incremental progress]*
- What do I do when a quick probe of an alternative doesn't show improvement and I have limited submissions?  *[no improvement, quick probe, limited submissions, resource-aware decision]*
- What do I do when a quick probe on a low-impact lever yields a tiny improvement?  *[marginal improvement, low-impact lever, quick probe, cost-benefit assessment]*
- What do I do when a single-feature probe shows no improvement or slight regression?  *[no improvement, feature probe, feature selection, marginal regression]*
- What do I do when a single-variable probe doesn't beat my best score?  *[no improvement, single-variable probe, baseline comparison]*
## 5 items, 5 kernels
- What do I do when I have a promising new feature idea and want to efficiently validate variants without burning LB submissions?  *[new feature idea, offline validation, submission budget, feature variant selection]*
- What do I do when I want to test a major architectural change but don't want to waste submission quota?  *[major architecture change, submission quota conservation, local validation]*
- What do I do when I want to test a new architectural idea but need to minimize wasted submissions?  *[new architecture idea, submission quota conservation, local validation]*
- What do I do when I want to validate feature changes locally before committing to a leaderboard submission?  *[local validation, feature changes, pre-submission verification]*
- What do I do when I've made a large code addition and want to avoid wasting a submission on a buggy version?  *[large code addition, bug detection, pre-submission validation, submission budget]*
## 5 items, 5 kernels
- What do I do when I have a working notebook with leftover/unused code before starting an optimization campaign?  *[code cleanup, unused code removal, optimization preparation]*
- What do I do when I have accumulated dead code and unused model paths in an inference notebook?  *[dead code cleanup, inference notebook, code maintenance]*
- What do I do when my notebook has accumulated heavy EDA code that will slow down or clutter the modeling phase?  *[notebook cleanup, EDA code removal, code organization, modeling phase preparation]*
- What do I do when my notebook has accumulated many commented-out code blocks and ad-hoc configurations from past experiments, making it hard to iterat  *[notebook cleanup, dead code removal, code organization, iteration efficiency]*
- What do I do when my pipeline has accumulated unused feature-engineering code and I want to add more model variants to the ensemble?  *[notebook cleanup, dead code removal, ensemble expansion, code organization]*
## 5 items, 4 kernels
- What do I do when I want to migrate a working pipeline to a GPU-accelerated library that has API incompatibilities with the original?  *[gpu acceleration, library migration, api incompatibility, pipeline porting]*
- What do I do when a hardware-specific configuration (e.g., GPU flags) causes failures across environments?  *[hardware configuration, cross-environment failure, gpu flags, environment portability]*
- What do I do when adding a GPU-accelerated library for feature computation introduces import or runtime errors in a notebook environment?  *[gpu library import error, notebook environment, dependency debugging, feature computation]*
- What do I do when loading a pretrained checkpoint into a timm model on Kaggle where the environment may lack GPU or the right library version?  *[checkpoint loading, kaggle environment, library compatibility, gpu availability]*
- What do I do when my spectrogram pipeline uses a GPU-specific library (CuPy) that may cause portability or numerical issues?  *[gpu library dependency, portability issue, numerical reproducibility, spectrogram pipeline]*
## 5 items, 5 kernels
- What do I do when I have a working ensemble at a competitive score and want to extract the next marginal improvement?  *[marginal improvement, competitive score, ensemble refinement]*
- What do I do when I have a working ensemble at a competitive score and want to push further?  *[competitive score, pushing score higher, ensemble refinement]*
- What do I do when I've just achieved a new best score and want to know if the ensemble size is optimal?  *[new best score, ensemble size tuning, optimal member count]*
- What do I do when I've just added a new model to an ensemble and achieved a new best score?  *[new best score, new ensemble member, ensemble expansion]*
- What do I do when my ensemble is already well-tuned and I want further improvement?  *[well-tuned ensemble, further improvement, ensemble refinement]*
## 5 items, 5 kernels
- What do I do when I want to add a new feature that depends on an external library and unfamiliar data types?  *[external library dependency, unfamiliar data types, new feature integration]*
- What do I do when I want to integrate an external model/checkpoint into an existing ensemble but it requires complex setup (exec scripts, different fr  *[external checkpoint integration, complex setup, cross-framework ensemble, dependency management]*
- What do I do when iterative code changes keep breaking due to environment-specific library compatibility issues?  *[library compatibility, environment mismatch, iterative code changes, dependency management]*
- What do I do when my ensemble of heterogeneous models (PyTorch 1D CNN + TensorFlow/Keras spectrogram CNN) is hard to tune and debug?  *[heterogeneous ensemble, pipeline complexity, debugging difficulty, framework mismatch]*
- What do I do when switching to a new model/checkpoint that requires updated dependencies and produces runtime errors?  *[dependency conflict, runtime error, checkpoint switching, environment setup]*
## 5 items, 5 kernels
- What do I do when I have a single-model baseline and want to improve a metric that rewards both accuracy and fairness across subgroups?  *[single model baseline, fairness across subgroups, accuracy fairness tradeoff, score improvement]*
- What do I do when I have a working ensemble of GBDTs and want to improve a concordance-based metric that rewards both accuracy and equity across subgr  *[concordance metric, subgroup equity, gbdt ensemble, fairness-aware optimization]*
- What do I do when starting a competition where the metric rewards both accuracy and fairness across subgroups?  *[competition start, fairness metric, subgroup accuracy, metric understanding]*
- What do I do when the competition metric rewards both accuracy and equity across subgroups?  *[fairness metric, subgroup equity, metric-aware training]*
- What do I do when the evaluation metric penalizes performance variance across demographic subgroups?  *[fairness metric, subgroup variance penalty, demographic parity]*
## 5 items, 5 kernels
- What do I do when I have accumulated large blocks of commented-out experimental code alongside a new feature I want to test?  *[commented-out code cleanup, code maintenance, new feature testing]*
- What do I do when I introduce a large code addition that combines new features, new infrastructure, and refactoring?  *[large code addition, combined changes, refactoring integration]*
- What do I do when I need to submit a large refactor that changes many things at once?  *[large refactor, batched changes, regression prevention, submission risk]*
- What do I do when I want to swap the underlying model/checkpoint while also cleaning up accumulated local code patches?  *[checkpoint swap, code cleanup, accumulated patches, model replacement]*
- What do I do when I want to test a feature change but the code has noisy debug output that could obscure results or cause timeout?  *[noisy debug output, code cleanup, feature change testing, timeout risk]*
## 5 items, 3 kernels
- What do I do when I have a sequence of incrementally trained checkpoints and need to find the best one for a spectrogram CNN ensemble?  *[checkpoint selection, incremental training, spectrogram cnn, ensemble member selection]*
- What do I do when I want to improve an already-strong CNN ensemble on spectrogram/EEG data?  *[strong baseline plateau, cnn ensemble, spectrogram eeg data]*
- What do I do when I want to test whether spectrogram preprocessing changes (scaling, windowing, log transforms) improve a CNN ensemble on spectrograms  *[spectrogram preprocessing, scaling and windowing, cnn ensemble, ablation study]*
- What do I do when a 3D CNN (r3d_18) caused a large regression in a spectrogram/EEG classification ensemble?  *[score regression, 3d cnn, ensemble member selection, spectrogram classification]*
- What do I do when my spectrogram-based EEG classification model has a reasonable but improvable baseline score?  *[improvable baseline, spectrogram model, eeg classification, score improvement]*
## 5 items, 4 kernels
- What do I do when I have a 1D signal model that reshapes raw inputs into 2D for a pretrained CNN backbone, and I need to find the right reshape dimens  *[input reshape dimensions, 1d to 2d reshape, pretrained cnn backbone, hyperparameter search]*
- What do I do when I want to find the best combination of pretrained vision backbones for a spectrogram/image classification ensemble?  *[backbone selection, vision ensemble, spectrogram classification, pretrained models]*
- What do I do when I want to test a 1D CNN backbone against a spectrogram-based CNN for EEG classification?  *[backbone comparison, 1d cnn vs spectrogram cnn, eeg classification, architecture selection]*
- What do I do when I want to try a newer/different CNN backbone variant to improve classification performance?  *[backbone selection, cnn architecture variant, classification performance]*
- What do I do when comparing two CNN backbone sizes for spectrogram classification?  *[backbone size comparison, cnn architecture selection, spectrogram classification]*
## 4 items, 1 kernels
- What do I do when a bag-of-words model's score is sensitive to vocabulary size but I'm near a plateau?  *[vocabulary size tuning, bag-of-words model, score plateau, hyperparameter sensitivity]*
- What do I do when a large vocabulary size causes a score collapse in a bag-of-words + Ridge regression pipeline?  *[score collapse, vocabulary size, bag-of-words pipeline, feature dimensionality]*
- What do I do when my bag-of-words model only uses one text field but the task requires predicting labels about multiple text fields (e.g., both questi  *[multiple text fields, feature engineering, bag-of-words limitation, input coverage]*
- What do I do when using a bag-of-words linear model on a small dataset (~6K rows) and the feature dimensionality seems too high relative to sample siz  *[feature dimensionality, small dataset, bag-of-words features, linear model regularization]*
## 4 items, 4 kernels
- What do I do when I have made many untested changes and need to decide whether to submit?  *[untested changes, submission decision, risk assessment]*
- What do I do when I want to test a risky change but cannot validate locally?  *[risky change, no local validation, remote-only evaluation]*
- What do I do when I want to test a speculative idea that might break training?  *[speculative idea, training stability risk, risk mitigation, safe experimentation]*
- What do I do when I want to test an infrastructure change that might break the pipeline?  *[infrastructure change, pipeline stability risk, risk mitigation, safe experimentation]*
## 4 items, 3 kernels
- What do I do when I have many engineered features and want to reduce noise from columns with excessive missing values?  *[missing value filtering, feature selection, noise reduction]*
- What do I do when adding aggregation functions (like std) introduces NaN values in the feature matrix?  *[nan values, aggregation features, feature engineering, missing value handling]*
- What do I do when adding categories to a pandas Categorical column before fillna, and the check for existing categories fails on some chunks?  *[categorical encoding, missing value handling, chunked processing, pandas data pipeline]*
- What do I do when deciding how to handle missing values in aggregated features for tree-based models?  *[missing value handling, aggregated features, tree-based model]*
## 4 items, 3 kernels
- What do I do when I have an imbalanced binary classification and want to tune the class-weight parameter for a GBDT model?  *[class imbalance, class weight tuning, gbdt hyperparameter, binary classification]*
- What do I do when I have an imbalanced ordinal regression target and want to improve QWK?  *[class imbalance, ordinal regression, qwk optimization, target distribution handling]*
- What do I do when I want to emphasize certain training samples in a gradient boosting model but sample_weight doesn't help?  *[sample weighting, gradient boosting, training emphasis, alternative weighting strategy]*
- What do I do when my GBDT model has class imbalance and I want a more nuanced weighting than a binary is_unbalance flag?  *[class imbalance, sample weighting, gbdt hyperparameter tuning, class weight design]*
## 4 items, 2 kernels
- What do I do when I discover a data leakage or column contamination bug in my pipeline?  *[data leakage, pipeline bug, column contamination, bug fix impact]*
- What do I do when I suspect my pretrained model pipelines have data leakage in their OOF predictions?  *[data leakage, oof predictions, pretrained model pipeline, validation integrity]*
- What do I do when I want to test a new data-cleaning idea without risking my best submission?  *[data cleaning idea, risk management, best submission preservation]*
- What do I do when my notebook pipeline writes intermediate outputs that can overwrite the final submission file?  *[file overwrite risk, intermediate outputs, submission file integrity, pipeline output management]*
## 4 items, 4 kernels
- What do I do when I add a new complex component (new model type, external data) and the score doesn't clearly improve?  *[no improvement, new complex component, component evaluation, cost-benefit analysis]*
- What do I do when I want to test a new component (e.g., a new model) but am unsure it will help?  *[new component testing, uncertain benefit, change isolation]*
- What do I do when a newly introduced component doesn't immediately help and I have a working baseline?  *[new component underperformance, baseline preservation, component evaluation]*
- What do I do when building a complex new component that I can't validate until it produces end-to-end output?  *[new component development, end-to-end validation, deferred validation]*
## 4 items, 3 kernels
- What do I do when I have a working baseline for a medical image classification task and want a quick score improvement?  *[quick score improvement, medical image classification, working baseline]*
- What do I do when I want to improve TTA beyond simple horizontal flip averaging for a medical image classification model?  *[test-time augmentation strategy, medical image classification, augmentation diversity]*
- What do I do when adding augmentation to a medical image classifier causes score regression?  *[score regression, data augmentation, medical image classification, augmentation strategy]*
- What do I do when my local CV score doesn't correlate with leaderboard performance for a medical image classification task?  *[cv-leaderboard disagreement, validation strategy, medical image classification]*
## 4 items, 4 kernels
- What do I do when I implement a new feature but suspect it may contain a bug before submitting?  *[new feature implementation, bug suspicion, pre-submission verification]*
- What do I do when a large code addition introduces a subtle bug that may silently produce wrong predictions?  *[silent bug, large code addition, prediction correctness, debugging verification]*
- What do I do when a newly engineered feature has a suspected bug and I cannot easily verify correctness?  *[suspected bug, feature correctness verification, feature engineering debugging]*
- What do I do when many of my experiment iterations are spent fixing bugs rather than testing hypotheses?  *[bug fixing overhead, experiment velocity, debugging vs hypothesis testing]*
## 4 items, 3 kernels
- What do I do when I need to determine whether a preprocessing parameter or an ensemble member swap is responsible for a score change?  *[score attribution, preprocessing parameter, ensemble member swap, change isolation]*
- What do I do when I want to confirm a score is attributable to a specific change and not to stochastic variation?  *[score attribution, stochastic variation, ablation confirmation]*
- What do I do when I want to isolate whether a code change or randomness caused a score change?  *[score change attribution, randomness isolation, reproducibility, ablation study]*
- What do I do when I want to know how much of my score improvement comes from more compute (folds/seeds) vs. code changes?  *[score attribution, compute scaling, code changes, ablation study]*
## 4 items, 4 kernels
- What do I do when I switch to a slower booster variant (e.g., DART) and need to find the right learning rate?  *[booster variant change, learning rate tuning, dart booster, training speed tradeoff]*
- What do I do when I've just switched to a slower boosting method (DART) that doesn't support standard early stopping and need to find the right number  *[boosting method change, early stopping unavailable, iteration count tuning, dart boosting]*
- What do I do when a global batch-size setting is silently overridden by a framework default after disabling an initialization call?  *[framework default override, batch size setting, silent configuration bug, training configuration]*
- What do I do when considering DART boosting as a replacement for GBDT in LightGBM on a tabular classification task?  *[boosting algorithm selection, dart vs gbdt, lightgbm configuration, tabular classification]*
## 4 items, 4 kernels
- What do I do when a feature probe shows a marginal regression on the leaderboard?  *[marginal regression, feature probe, leaderboard evaluation, feature selection]*
- What do I do when a probe of a new technique yields a marginal regression on the leaderboard?  *[marginal regression, new technique probe, leaderboard validation, technique evaluation]*
- What do I do when a quick probe shows a marginal regression and I have other promising levers to try?  *[marginal regression, quick probe, prioritization of levers]*
- What do I do when a single exploratory change produces a marginal regression on the leaderboard?  *[marginal regression, exploratory change, leaderboard evaluation]*
## 4 items, 4 kernels
- What do I do when I bundle multiple changes into one version and it fails to produce a valid submission?  *[submission failure, bundled changes, change isolation, debugging]*
- What do I do when I bundle multiple changes together and the run fails or looks bad?  *[run failure, bundled changes, change isolation, debugging]*
- What do I do when a major data source change breaks multiple downstream dependencies in the pipeline?  *[data source change, pipeline breakage, downstream dependencies]*
- What do I do when a single component change breaks an ensemble and I cannot quickly fix it?  *[ensemble breakage, component change, rollback decision, recovery after change]*
## 4 items, 4 kernels
- What do I do when I fix a bug that was silently failing and the 'correct' behavior produces worse results?  *[bug fix, score regression, correct behavior worse, silent failure]*
- What do I do when a code change doesn't produce the expected improvement and I suspect a bug rather than a bad idea?  *[expected improvement missing, bug suspicion, code change, debugging]*
- What do I do when a code change produces no score improvement and I'm unsure whether the change itself or a bug is responsible?  *[no score improvement, bug diagnosis, change attribution]*
- What do I do when a targeted bug fix yields negligible improvement?  *[bug fix, negligible improvement, expected gain missing]*
## 4 items, 4 kernels
- What do I do when my iteration cycle is too slow for the experiments I want to run, but I need to verify the speed-up doesn't hurt quality?  *[slow iteration cycle, training speedup, quality verification]*
- What do I do when my notebook is slow due to heavy inference (transformers) and feature engineering running every submission, limiting iteration speed  *[slow iteration cycle, expensive inference, precomputation caching, transformer inference]*
- What do I do when my notebook's iteration cycle is too slow because expensive preprocessing reruns every time?  *[slow iteration cycle, preprocessing caching, precomputation caching, redundant computation]*
- What do I do when my pipeline has a complex on-the-fly feature extraction step that is slow and hard to iterate on?  *[slow iteration cycle, feature extraction, precomputation caching, code modularization]*
## 4 items, 4 kernels
- What do I do when I want to add a complex new feature pipeline (external data + new model type + new embeddings) to an existing working notebook?  *[complex pipeline integration, external data, incremental development, notebook modularity]*
- What do I do when I want to consolidate multiple external model scripts into a single notebook for easier iteration?  *[code consolidation, notebook workflow, multiple scripts integration, iteration efficiency]*
- What do I do when I want to expand an ensemble with models trained in a separate notebook/environment?  *[ensemble expansion, cross-environment integration, separate notebook]*
- What do I do when assembling a complex multi-model notebook from public kernels that may have different hardware assumptions?  *[multi-model assembly, hardware compatibility, notebook integration]*
## 4 items, 3 kernels
- What do I do when my ensemble of sigmoid-output models has a reasonable score but predictions may be poorly calibrated or overly peaked?  *[prediction calibration, sigmoid output calibration, post-processing adjustment]*
- What do I do when my model outputs logits but the competition metric expects probability distributions?  *[logit to probability conversion, output activation, competition metric alignment]*
- What do I do when my model outputs may already be normalized probabilities but I'm unsure whether to apply softmax?  *[softmax application uncertainty, output normalization check, probability calibration]*
- What do I do when my model outputs probabilities via sigmoid that may be too diffuse/uncalibrated for a ranking metric?  *[sigmoid output calibration, diffuse probabilities, ranking metric optimization]*
## 4 items, 1 kernels
- What do I do when I have a classifier mask that additively boosts risk predictions for predicted-positive cases?  *[classifier mask, additive risk adjustment, postprocessing calibration, predicted-positive boosting]*
- What do I do when I have a post-hoc additive adjustment in an ensemble and want to know if its magnitude is well-calibrated?  *[post-hoc adjustment, ensemble calibration, magnitude tuning, additive correction]*
- What do I do when I want to boost predictions for a classifier-flagged subset of records in an ensemble?  *[classifier-flagged subset, ensemble boosting, conditional prediction adjustment]*
- What do I do when a small additive correction applied to a subset of predictions has been improving scores as I reduce it?  *[additive correction, prediction subset, incremental tuning, diminishing adjustment]*
## 4 items, 3 kernels
- What do I do when I want to understand prediction behavior before optimizing further?  *[prediction analysis, model behavior understanding, pre-optimization diagnostics]*
- What do I do when bringing up a multi-branch deep model for inference requires multiple iterative fixes?  *[multi-branch inference, iterative debugging, complex model deployment]*
- What do I do when my inference pipeline is a black-box call to a training framework's script and I suspect it's not loading models or running predicti  *[black-box inference, pipeline inspection, prediction optimization, framework script debugging]*
- What do I do when my notebook has multiple interacting model loops and I need to debug which component is producing the submitted predictions?  *[pipeline debugging, prediction provenance, multiple model loops, component isolation]*
## 4 items, 3 kernels
- What do I do when loading a checkpoint trained with a different model architecture variant (e.g., hybrid head) into a base model class?  *[checkpoint loading, architecture mismatch, key mismatch, model variant compatibility]*
- What do I do when loading checkpoints saved from multi-GPU (DataParallel) training fails due to key mismatches?  *[checkpoint loading, multi-gpu training, key mismatch, dataparallel compatibility]*
- What do I do when switching model checkpoints that were trained with different preprocessing pipelines?  *[checkpoint swap, preprocessing mismatch, pipeline compatibility, inference configuration]*
- What do I do when switching to a new set of model checkpoints that were trained under a different configuration than the default config file assumes?  *[checkpoint switching, config mismatch, training configuration alignment]*
## 4 items, 3 kernels
- What do I do when I have extensively tuned one model variant and want to know if a different variant could do better?  *[model variant comparison, architecture exploration, tuning exhaustion, alternative variant evaluation]*
- What do I do when I want to test whether a new model variant improves over the current best?  *[model variant comparison, baseline improvement, incremental improvement]*
- What do I do when I want to test whether a qualitatively different model variant helps?  *[new model variant, model diversity, contribution test]*
- What do I do when I'm near a performance plateau and want to determine which model variant is best?  *[performance plateau, model variant comparison, model selection]*
## 4 items, 1 kernels
- What do I do when a prompt-based (PET) DeBERTa model needs the mask token position at inference time but the tokenization pipeline doesn't expose it?  *[mask token position, tokenization pipeline, inference implementation, prompt-based model]*
- What do I do when deciding whether to add special tokens (e.g., newline tokens) to a pretrained tokenizer at inference time for a fine-tuned model?  *[special token handling, tokenizer modification, inference consistency, pretrained model]*
- What do I do when my fine-tuned language model was trained with special tokens (e.g., explicit newline tokens) that aren't in the default pretrained t  *[special token mismatch, tokenizer configuration, fine-tuned model loading]*
- What do I do when switching to a model that was trained with extra tokens added to the tokenizer, and inference fails or produces bad results?  *[tokenizer mismatch, model switching, inference failure, extra tokens]*
## 3 items, 3 kernels
- What do I do when I make an extreme or likely erroneous parameter change and the notebook run doesn't produce useful results?  *[erroneous parameter change, invalid results, parameter correction]*
- What do I do when I notice my OOF evaluation may be corrupted by post-processing applied before storage?  *[oof evaluation corruption, post-processing bug, evaluation integrity]*
- What do I do when my inference pipeline computes the right result but the submission file doesn't reflect it?  *[submission file mismatch, output formatting bug, inference postprocessing]*
## 3 items, 3 kernels
- What do I do when ablation experiments show consistent regressions?  *[ablation study, consistent regression, feature importance]*
- What do I do when ablation of a feature group shows a tiny score drop?  *[ablation study, feature group removal, small score drop, feature importance]*
- What do I do when permutation-importance-based feature removal hurts GBDT performance?  *[permutation importance, feature removal, score regression, gbdt model]*
## 3 items, 3 kernels
- What do I do when my multi-fold ensemble predictions might be noisy due to individual fold variance?  *[fold variance, ensemble noise reduction, multi-fold aggregation]*
- What do I do when my neural-network ensemble predictions are noisy and I want to reduce variance without changing the model?  *[prediction variance, ensemble averaging, test-time augmentation, noise reduction]*
- What do I do when trying multi-seed ensemble averaging with a GBDT model to improve robustness?  *[multi-seed ensemble, gbdt robustness, variance reduction]*
## 3 items, 3 kernels
- What do I do when I'm sweeping configurations but none beats my current best score?  *[configuration sweep, no improvement, search strategy, current best retention]*
- What do I do when a parameter sweep in both directions from the current value yields worse results?  *[parameter sweep, no improvement found, local optimum, hyperparameter tuning]*
- What do I do when a sweep of one type of post-processing fails to improve over baseline?  *[post-processing sweep, no improvement, baseline comparison]*
## 3 items, 3 kernels
- What do I do when I have a model trained on a fixed-position temporal crop but the input signal is longer than the crop window?  *[temporal crop mismatch, sliding window inference, input length exceeds crop, test-time aggregation]*
- What do I do when I want to leverage ImageNet-pretrained weights but my input is single-channel spectrograms?  *[pretrained weights, input channel mismatch, single-channel spectrogram, transfer learning adaptation]*
- What do I do when my ensemble includes a spectrogram model trained on a long temporal window and I suspect a shorter window better matches the target   *[temporal window mismatch, spectrogram model tuning, input window selection]*
## 3 items, 3 kernels
- What do I do when reverting a failed change but I also want to clean up other code?  *[revert failed change, code cleanup, codebase maintenance]*
- What do I do when reverting a failed experiment but wanting to also improve the restored baseline?  *[revert failed change, baseline improvement, incremental refinement]*
- What do I do when reverting an unsuccessful change and cleaning up code at the same time?  *[revert failed change, code cleanup, codebase maintenance]*
## 3 items, 2 kernels
- What do I do when I have an external labeled dataset with richer annotations (sub-scores) than my target task and want to leverage it?  *[external labeled dataset, richer annotations, auxiliary pretraining, transfer learning]*
- What do I do when adding an auxiliary/external dataset to training does not improve the leaderboard score?  *[external data addition, score plateau, auxiliary dataset, training data selection]*
- What do I do when adding external labeled data improved my score in training but I need to verify whether it helps or hurts at inference time?  *[external data addition, train inference gap, leaderboard validation, auxiliary dataset]*
## 3 items, 3 kernels
- What do I do when CV rankings of multi-input model combinations don't clearly predict LB performance?  *[cv lb disagreement, model combination ranking, validation reliability, multi-input model]*
- What do I do when my cross-validation estimates seem unstable and I want more reliable model selection signals?  *[cv instability, model selection, validation strategy, reliable evaluation]*
- What do I do when my cross-validation grouping strategy (e.g., unsupervised clustering) doesn't reflect the true data structure and CV scores are unre  *[cv strategy, grouping strategy, unreliable validation, data structure mismatch]*
## 3 items, 3 kernels
- What do I do when I have OOF predictions from a strong model (e.g., a transformer) and want to boost a downstream gradient-boosted tree ensemble?  *[oof predictions, stacking features, transformer features, gradient boosted tree ensemble]*
- What do I do when I need OOF predictions from pre-trained models as features but loading them from external files is fragile?  *[oof predictions, pretrained model loading, feature engineering robustness]*
- What do I do when I want more stable OOF estimates from a tree-based model on a moderately sized dataset?  *[oof stability, tree-based model, cross-validation design]*
## 3 items, 3 kernels
- What do I do when I have multiple model architectures/training approaches (e.g., prompt-based vs. regression) and want to find the best single-model s  *[multiple architectures, model selection, single-model submission, approach comparison]*
- What do I do when a generative LLM used for direct score prediction produces much worse results than a discriminative model?  *[generative llm, score regression, model architecture selection, discriminative model comparison]*
- What do I do when a simpler single-head model underperforms my multi-head model on the same backbone?  *[architecture comparison, single-head vs multi-head, model simplification, score regression]*
## 3 items, 2 kernels
- What do I do when I want to swap the CNN backbone at inference time without retraining?  *[backbone swap, inference-time replacement, cnn architecture selection]*
- What do I do when switching to a larger CNN backbone variant for spectrogram-based inference?  *[backbone scaling, cnn backbone variant, architecture swap, spectrogram model]*
- What do I do when trying to improve a CNN classification model by replacing one spatial attention mechanism with another?  *[attention mechanism swap, cnn architecture change, classification improvement]*
## 3 items, 3 kernels
- What do I do when I find a good configuration but want to verify it's optimal by exploring alternatives?  *[good configuration found, optimality verification, alternative exploration]*
- What do I do when I've lost track of which configuration was best after many exploratory edits?  *[lost best configuration, exploratory edits, configuration tracking]*
- What do I do when an exploration branch consistently underperforms my best known configuration?  *[exploration underperformance, configuration comparison, abandon exploration]*
## 3 items, 2 kernels
- What do I do when I need to iterate quickly on a Kaggle notebook but full CV takes too long on the competition platform?  *[slow cross-validation, notebook iteration speed, compute constraints, development efficiency]*
- What do I do when I need to iterate quickly on a pipeline fix but full CV is too slow?  *[slow cross-validation, pipeline debugging, fast iteration, development efficiency]*
- What do I do when starting a new competition with a large, unfamiliar dataset that is too big to iterate on quickly?  *[competition start, large dataset, data subsampling, iteration speed]*
## 3 items, 2 kernels
- What do I do when I need to move from raw data exploration to a modeling-ready pipeline on a very large dataset?  *[data exploration to modeling, large dataset, pipeline construction, preprocessing pipeline]*
- What do I do when considering reordering training data by category in a cross-validation pipeline?  *[training data ordering, cross-validation pipeline, category-based sorting]*
- What do I do when transitioning from EDA/preprocessing to model training on a large tabular dataset with a custom competition metric?  *[workflow transition, model training setup, custom metric, large tabular dataset]*
## 3 items, 2 kernels
- What do I do when I have models trained on different temporal windows of the same signal?  *[temporal window variation, multiple trained models, signal segmentation, model combination]*
- What do I do when I have spectrogram models at different temporal resolutions and want to combine them?  *[multi-resolution models, spectrogram features, ensemble combination]*
- What do I do when my model uses only the last time-step per customer in a multi-statement dataset and I want to extract more signal from the full hist  *[temporal feature engineering, sequence history utilization, feature extraction]*
## 3 items, 3 kernels
- What do I do when I have a working ensemble and want to improve it further?  *[ensemble improvement, score improvement, iterative refinement]*
- What do I do when I have a working ensemble submission and want to improve it further?  *[ensemble improvement, iterative refinement, working baseline]*
- What do I do when I have a working fold-ensemble and want to squeeze out more score?  *[fold ensemble, score improvement, marginal gains]*
## 3 items, 3 kernels
- What do I do when a new approach consistently underperforms across multiple checkpoint versions?  *[persistent underperformance, new approach, multiple checkpoints, approach abandonment]*
- What do I do when an exploration episode fails to beat my starting score after several attempts?  *[exploration failure, score plateau, abandon exploration]*
- What do I do when multiple small probes all fail to beat the current best score?  *[score plateau, exploratory probes, consecutive failed experiments, best score ceiling]*
## 3 items, 3 kernels
- What do I do when I have a new model architecture variant trained offline and want to validate it improves leaderboard score?  *[new model architecture, offline training, leaderboard validation]*
- What do I do when I have a promising new model variant that performed well offline but I haven't tested it on the leaderboard?  *[promising offline model, leaderboard submission, online validation]*
- What do I do when I have trained models offline and need to verify they reproduce expected performance in a submission notebook?  *[offline trained models, submission notebook, performance reproduction]*
## 3 items, 3 kernels
- What do I do when I want to evaluate both a model change and a post-processing toggle, and each submission is costly?  *[joint evaluation, model change, postprocessing toggle, submission budget]*
- What do I do when I want to test whether a regularization technique helps but don't want to spend many iterations on it?  *[regularization technique, quick experiment, compute budget, contribution test]*
- What do I do when I want to understand the effect of multiple potential improvements but have limited submission budget?  *[multiple improvements evaluation, submission budget, ablation study]*
## 3 items, 2 kernels
- What do I do when fine-tuning a pretrained language model with a very low learning rate and wanting to explore whether a higher rate improves converge  *[learning rate exploration, low learning rate, convergence speed, pretrained language model]*
- What do I do when fine-tuning a pretrained transformer and the learning rate seems too high?  *[learning rate too high, transformer fine-tuning, learning rate reduction]*
- What do I do when my neural network uses a cosine-warmup schedule but I suspect the learning rate trajectory is suboptimal for a short training run?  *[learning rate schedule, cosine warmup tuning, short training run]*
## 3 items, 2 kernels
- What do I do when I suspect a file path error is causing my pipeline to use the wrong preprocessed data?  *[file path error, wrong data usage, preprocessing pipeline debugging]*
- What do I do when I'm wiring up file-loading code that references external artifacts and keep hitting path or import errors?  *[path errors, import errors, file loading, external artifact references]*
- What do I do when my inference notebook fails to load a model artifact and I'm unsure of the exact file path?  *[model loading failure, file path debugging, inference notebook error]*
## 3 items, 3 kernels
- What do I do when I have a dual-branch model that averages two feature embeddings and want to improve its representational capacity?  *[dual-branch model, feature embedding fusion, representational capacity, architecture improvement]*
- What do I do when I have a multi-branch fusion model and want to improve feature quality without exceeding compute/memory limits?  *[multi-branch fusion, feature quality improvement, compute budget constraint, memory constraint]*
- What do I do when concatenating multi-branch CNN features from a 5D tensor (batch, H, W, C, regions)?  *[multi-branch feature concatenation, tensor reshaping, cnn architecture, high-dimensional input]*
## 3 items, 3 kernels
- What do I do when I have reached a satisfactory score and the competition is ending?  *[competition ending, final submission selection, satisfactory score]*
- What do I do when I want to maximize my leaderboard score near the end of a competition and have many similar configurations to try?  *[competition deadline, configuration search, leaderboard score maximization, submission strategy]*
- What do I do when starting a new competition notebook from a rough draft?  *[competition start, rough draft, notebook setup]*
## 3 items, 3 kernels
- What do I do when I have a new checkpoint but the optimized rounding thresholds are unknown?  *[new checkpoint available, rounding threshold optimization, postprocessing calibration]*
- What do I do when I have a new model checkpoint and an optional post-processing calibration step, and I need to determine whether the calibration stil  *[new checkpoint available, postprocessing calibration, ablation study]*
- What do I do when I have a newly trained checkpoint and need to evaluate it quickly on the leaderboard?  *[new checkpoint available, quick evaluation, leaderboard submission]*
## 3 items, 2 kernels
- What do I do when I add a new input modality but leaderboard scores regress or don't improve?  *[score regression, new input modality, modality integration, no improvement]*
- What do I do when I want to introduce a new input modality requiring major pipeline changes?  *[new input modality, major pipeline changes, modality integration]*
- What do I do when I want to test whether adding a new input modality improves performance?  *[new input modality, feature addition test, multimodal evaluation]*
## 3 items, 2 kernels
- What do I do when I want to condition a DeBERTa prompt template on dataset-specific metadata (e.g., source corpus) to improve scoring?  *[prompt template design, dataset-specific metadata, deberta conditioning]*
- What do I do when ensembling DeBERTa regression checkpoints and I have variants trained with different positional encoding schemes?  *[checkpoint diversity, positional encoding variants, deberta ensemble, regression task]*
- What do I do when my DeBERTa regressor might benefit from domain-aware context in the input?  *[domain-aware context, input augmentation, deberta regressor, prompt engineering]*
## 3 items, 2 kernels
- What do I do when I have a regression model and want to try a different prediction head formulation to improve ordinal scoring metrics?  *[prediction head formulation, ordinal scoring metric, regression model, architecture decision]*
- What do I do when I want to test whether a fundamentally different prediction head (classification vs regression) improves my score?  *[prediction head design, task formulation change, classification vs regression]*
- What do I do when a hyperparameter change causes a small regression but I believe the direction is correct?  *[small regression, hyperparameter change, directional conviction, persistence decision]*
## 3 items, 3 kernels
- What do I do when I want to improve QWK by changing the training objective and post-processing thresholds simultaneously?  *[training objective selection, threshold optimization, qwk metric optimization, joint tuning]*
- What do I do when my tree-based model has plateaued and I want to squeeze out more QWK?  *[score plateau, tree-based model, qwk optimization, performance squeeze]*
- What do I do when optimizing a non-differentiable ranking metric like QWK with tree-based models?  *[non-differentiable metric, qwk optimization, tree-based model, threshold tuning]*
## 3 items, 1 kernels
- What do I do when I have two candidate subgroup columns to oversample and I'm unsure which one the pipeline should use?  *[oversampling strategy, subgroup column selection, candidate comparison]*
- What do I do when I want to improve cross-validation reliability for a dataset with distinct subpopulations?  *[cross-validation reliability, data subpopulations, stratification strategy]*
- What do I do when choosing between GroupKFold (by prompt) and StratifiedKFold (by score) for a text regression task with multiple prompts?  *[cross-validation strategy, group-based splitting, stratified splitting, text regression]*
## 2 items, 2 kernels
- What do I do when I have a working small ensemble and infrastructure that supports more members?  *[ensemble expansion, adding members, infrastructure capacity]*
- What do I do when I want to add a large new component to an ensemble but need to manage resource constraints or interaction effects?  *[ensemble expansion, resource constraints, interaction effects, new component integration]*
## 2 items, 1 kernels
- What do I do when I want to modernize my neural architecture for tabular data but risk losing performance from a proven component?  *[architecture modernization, tabular neural network, proven component risk, score regression prevention]*
- What do I do when considering switching from a well-tuned optimizer to a trendy alternative (e.g., Lion) for a tabular neural network?  *[optimizer selection, well-tuned baseline, trendy alternative, tabular neural network]*
## 2 items, 2 kernels
- What do I do when I have a pure refactoring change that doesn't alter predictions?  *[code refactoring, prediction equivalence, sanity check]*
- What do I do when moving code out of a disabled block (e.g., `if False`) into the active path?  *[code activation, disabled code block, pipeline refactoring]*
## 2 items, 2 kernels
- What do I do when I want to test a new augmentation idea that requires multiple implementation steps before it can be evaluated end-to-end?  *[new augmentation idea, multi-step implementation, end-to-end evaluation]*
- What do I do when I want to try a new idea from a discussion forum on an already-strong submission?  *[new idea from discussion, strong baseline, incremental improvement]*
## 2 items, 2 kernels
- What do I do when a quick hypothesis test yields a worse score?  *[score regression, hypothesis test, quick experiment, negative result]*
- What do I do when a quick local experiment shows no improvement?  *[no improvement, local experiment, quick experiment, negative result]*
## 2 items, 2 kernels
- What do I do when adding heavy unsupervised text features (LDA, LSA, NMF) causes instability or unclear benefit?  *[topic model features, unsupervised text features, feature instability, unclear benefit]*
- What do I do when adding lag/difference features to a GBDT model on aggregated time-series data doesn't clearly help?  *[lag features, time-series features, unclear benefit, tree-based model]*
## 2 items, 2 kernels
- What do I do when I need to understand a wide dataset (~190 columns) with grouped feature names before engineering features?  *[exploratory data analysis, wide dataset understanding, grouped feature names, feature engineering planning]*
- What do I do when feature column names in my saved feature-selection list no longer match the DataFrame after renaming aggregation aliases?  *[column name mismatch, feature selection list, aggregation aliases, data pipeline consistency]*
## 2 items, 2 kernels
- What do I do when I've pruned components for efficiency and want to recover lost accuracy?  *[component pruning, accuracy recovery, efficiency-accuracy tradeoff]*
- What do I do when my fine-tuned transformer model shows signs of overfitting after reducing epochs?  *[overfitting, epoch reduction, regularization strategy]*
## 2 items, 2 kernels
- What do I do when I suspect a data loading bug but need to confirm it before making a fix?  *[data loading bug, bug confirmation, debugging before fix]*
- What do I do when reading a file twice in Python (once for a set, once for a list) produces an empty second result?  *[file reading bug, python iterator exhaustion, data loading]*
## 2 items, 2 kernels
- What do I do when my model consistently underperforms on a specific target column that has a clear domain signal?  *[per-target underperformance, domain signal, target-specific modeling]*
- What do I do when my tree-based model (LightGBM/XGBoost) for ordinal regression on essays seems to underperform on certain score classes?  *[class-level underperformance, ordinal regression, tree-based model, per-class analysis]*
## 2 items, 2 kernels
- What do I do when I want to add diversity to an ensemble by varying the signal preprocessing applied to the same raw input?  *[ensemble diversity, signal preprocessing variation, preprocessing augmentation]*
- What do I do when my image preprocessing has manual numpy operations that should be part of the augmentation pipeline for consistency?  *[preprocessing consistency, augmentation pipeline integration, image preprocessing refactor]*
## 2 items, 2 kernels
- What do I do when my EEG time-window extraction uses an offset that's already in seconds but needs to be in samples?  *[unit conversion bug, time-window extraction, eeg preprocessing, offset calculation]*
- What do I do when sweeping checkpoint versions for a 1D EEG model yields diminishing returns?  *[checkpoint version sweep, diminishing returns, search stopping criterion, eeg model]*
## 2 items, 1 kernels
- What do I do when I need to create group labels for StratifiedGroupKFold from unlabeled data?  *[group label creation, stratified group kfold, unlabeled data clustering]*
- What do I do when switching to group-aware cross-validation and I need to decide what column to use as the group variable?  *[group-aware cross-validation, group variable selection, data leakage prevention]*
## 2 items, 2 kernels
- What do I do when I have exhausted checkpoint sweeping with a fixed architecture and scores have plateaued or regressed?  *[score plateau, checkpoint sweeping exhaustion, architecture change trigger, fixed architecture limit]*
- What do I do when I've been iterating on a new component (attention block) for several versions without surpassing my overall best score?  *[score plateau, attention block iteration, component stagnation, architecture change]*
## 2 items, 2 kernels
- What do I do when I have a model trained at one resolution and want to squeeze more performance at inference time?  *[inference resolution change, resolution upscaling, test-time resolution, performance squeeze]*
- What do I do when I have a working inference pipeline and want to check whether the inference resolution matches what the model needs?  *[inference resolution, resolution mismatch, pipeline verification]*
## 1 items, 1 kernels
- What do I do when I need to get predictions from a native XGBoost Booster object trained via xgb.train?  *[xgboost inference, booster prediction api, native model prediction]*
## 1 items, 1 kernels
- What do I do when fine-tuning a current lever yields diminishing returns?  *[diminishing returns, strategy switching, current lever exhausted]*
## 1 items, 1 kernels
- What do I do when I want to give a transformer model a reference point for relative scoring?  *[reference point design, relative scoring, transformer input engineering]*
## 1 items, 1 kernels
- What do I do when I want to make multiple improvements (TTA, backbone swap, code cleanup) at once?  *[multiple simultaneous changes, batched updates, tta, backbone swap]*
## 1 items, 1 kernels
- What do I do when I want to sort a dataset by sequence length for efficient bucketed padding during inference?  *[sequence length sorting, bucketed padding, inference efficiency]*
## 1 items, 1 kernels
- What do I do when I want to capture surface-level text patterns beyond handcrafted statistics?  *[text feature extraction, surface-level patterns, beyond handcrafted features]*
## 1 items, 1 kernels
- What do I do when I want to test whether a per-instance (per-fold) adaptive transformation improves over a fixed global transformation?  *[adaptive transformation, per-instance adaptation, global vs local strategy, fold-level customization]*
## 1 items, 1 kernels
- What do I do when my notebook uses polars for data loading but I need to apply row-wise Python functions (e.g., nltk/textstat)?  *[dataframe compatibility, polars to pandas, row-wise functions, library interoperability]*
## 1 items, 1 kernels
- What do I do when NMF features are generated with default iteration limits that may not converge?  *[nmf convergence, iteration limit, feature generation, default hyperparameters]*
## 1 items, 1 kernels
- What do I do when a preprocessing change (e.g., clipping bounds) was tried in one context and hurt, but I'm now in a different ensemble context?  *[preprocessing change, context dependence, ensemble context, re-evaluation]*