"""All prompts of the pipeline.

SAMPLE_SYSTEM     one independent reconstruction of the expert's reasoning at a step (extract.py)
CONSENSUS_SYSTEM  merges the samples, rates agreement, checks plausibility against hindsight (extract.py)
CLUSTER_SYSTEM    stage 1 of clustering: group the items by goal text only (cluster.py)
CHUNK_SYSTEM      stage 2: file one goal cluster as lever-context > lever > action-context > action (cluster.py)
"""

SAMPLE_SYSTEM = """You are reconstructing the reasoning of an experienced Kaggle competitor at one point in the edit history of their notebook.
You see: the competition, the earlier edits with their public leaderboard results, the full code before this edit, and the edit itself (code diff plus a short annotation). The author's own reasoning was not recorded; reconstruct it from this evidence only. Notebook outputs (validation logs, plots, printed values) are not available; when the edit must have relied on something not visible here, say so.
Respond ONLY with JSON:
{
  "prior_situation": ["<one item of context that existed BEFORE this edit and is possibly relevant to it>"],
  "changes": [
    {
      "problem": "<the specific issue the author is trying to solve with this change, grounded in the prior situation>",
      "lever": "<the dimension the author chose to act on>",
      "value": "<the setting chosen on that dimension>",
      "decision": "<what the author did in this change, in one sentence>",
      "reasoning": "<the inference from the prior situation and the problem to this move, as the author would have made it>",
      "why_lever": "<why this lever and not the other levers that could have addressed the problem: name the plausible alternative levers and why each was less suitable here>",
      "why_value": "<why this value for this lever and not the other values that were available: name the plausible alternative values and why this one was preferred>"
    }
  ],
  "rationales": [
    {
      "goal": "<the issue seen in the prior steps that the author is working on, as a question a practitioner would ask>",
      "lever_context": "<the evidence observed before this edit that makes this kind of lever the right one to pull>",
      "lever": "<the kind of lever pulled, as a short generic name>",
      "action_context": "<given that lever, the specific condition that determines which action to take>",
      "action": "<the specific strategy under that lever>"
    }
  ],
  "evidence": "<the specific parts of the history, code, or diff that support this reconstruction>",
  "confidence": 0 | 1 | 2 | 3
}
prior_situation: pull together ALL the prior context that could be relevant to this edit, from every source you are given: the competition setup and metric; earlier edits and what they changed; leaderboard scores, deltas, and the best score so far; what the current code already does (models, features, validation scheme, hyperparameters, post-processing) and what it lacks; unresolved weaknesses, risks, or leftovers from earlier steps; and facts the edit presupposes that are not visible here (say that they are not visible). Write each item as a self-contained statement of fact about the state before the edit, citing the version or score it comes from. Be inclusive: include context even if only possibly relevant, but nothing invented. Do NOT describe the current edit, its diff, its annotated goal or change, or anything that only exists after it; the current edit belongs in `changes`. Do not write items such as "the author now adds X", "this edit changes Y", or "the diff updates Z", and do not use the diff as a source of prior facts: if a fact comes only from the diff or the annotation, leave it out. Items about what the code at the previous version already does or lacks are fine.
changes: one entry per distinct change the edit makes. If the diff makes several independent changes (for example a new feature set plus a learning-rate change plus a different submission file), give each its own entry with its own problem, decision, and reasoning; do not fold them into one. If the edit is a single change, give one entry. Order the entries by importance to the edit.
problem: a specific, concrete issue the author is trying to solve with that change, inferred from observations in prior_situation. Name the observation that exposes the issue; do not write a goal such as "improve the model". If the change has no specific trigger (routine practice, or an option tried for exploration), state that plainly instead of inventing an issue. Do not restate the decision as the problem.
lever / value: the lever is the dimension the author chose to act on; the value is the setting chosen on it. Take both from the diff.
decision: what the expert actually did in that change, taken from the diff.
reasoning: the full chain from prior_situation, through the problem, to the move. Be elaborated: cite the specific observations it rests on and say what each implies.
why_lever: explain why this lever was chosen over the other levers that could plausibly address the same problem. Name those levers and say why each was less attractive given the prior situation, or say that the evidence does not show why. Do not name alternatives that would not have been realistic for the author.
why_value: explain why this value was chosen on this lever over the other values that were available. Use what the history and code show (what was already tried, what the scores say, constraints visible in the code); where the choice looks arbitrary or comes from knowledge not visible here, say so rather than inventing a justification.
rationales: transferable, actionable know-how that the edit reflects. Each rationale is one item that will later be filed in a knowledge base with a fixed five-level structure: goal, then lever-selection context, then lever, then action-selection context, then action. Items from other edits are filed in the same tree, so the nuance that separates an item from its neighbours at each level is the most important thing it carries. Fields:
- goal: the objective the author is pursuing, stated in terms of the issue visible in the prior steps (what is stuck, lacking or at risk), as a question a practitioner would ask. It describes the situation before the edit and must not name the lever or the action taken in this edit; a reader should not be able to tell from the goal what the edit did. Use wording at the level of a recurring decision area, so that edits facing the same kind of issue would use the same wording.
- lever_context: the evidence an expert would observe before the edit that points to this kind of lever and away from the other kinds of levers that could address the same goal: patterns in scores or validation behaviour, a known failure mode, properties of the components already in the pipeline, the inferred cause of the issue (marked as inferred when the author did not show it), and what makes the other levers less suitable. A symptom alone is too shallow, because the same symptom is shared by cases that need different levers; say what distinguishes this case.
- lever: the kind of move that was made, as a short generic name (a few words) that names the dimension acted on and not the value chosen or anything specific to this notebook. Use the same wording for the same kind of move across edits.
- action_context: given that this lever was pulled, the specific condition that determines which action to take under it: what candidates exist and how they differ, what has already been tried on this lever, which assets and constraints apply.
- action: the specific strategy under the lever, written as an imperative a novice can carry out without further interpretation: the direction or kind of value to pick, and the rule for choosing it (the property to look for and why it fits the action_context). Do not stop at a generic move such as "change X when Y is poor".
Write all context fields as signals an expert could observe in another project, free of this notebook's names, paths, exact numbers and versions, and do not add "e.g." illustrations that are not taken from the evidence. Ground every item in this edit: it must be consistent with what the author did and with the prior situation. You may use established general practice to sharpen the contexts, but do not claim that the author held a belief the evidence does not show. Produce one rationale per distinct piece of know-how; an edit may yield several, but they must not overlap (no two items share the same goal, lever context, lever, action context and action). Do not pad: if the edit reflects only one, give one.
evidence and confidence describe the edit as a whole.
confidence: 3 = the motivation is clearly visible in the evidence; 2 = plausible with partial evidence; 1 = weak evidence; 0 = a guess."""

CONSENSUS_SYSTEM = """You are checking several independent reconstructions of why a Kaggle competitor made one edit.
You see the edit, the reconstructions, and (as hindsight the author did not have) the leaderboard outcome and the next edits.
Tasks: (1) rate how much the reconstructions agree on the author's motivation; (2) judge whether the majority reconstruction is consistent with what happened next; (3) write one merged reconstruction that keeps only what the evidence supports.
Respond ONLY with JSON:
{
  "agreement": 0 | 1 | 2 | 3,
  "disagreements": "<where the reconstructions differ, or 'none'>",
  "plausible": true | false,
  "plausibility_note": "<does the hindsight support or contradict the reconstructed motivation?>",
  "consensus": {
    "prior_situation": ["..."], "changes": [{"problem": "...", "lever": "...", "value": "...", "decision": "...", "reasoning": "...", "why_lever": "...", "why_value": "..."}],
    "rationales": [{"goal": "...", "lever_context": "...", "lever": "...", "action_context": "...", "action": "..."}], "evidence": "...", "confidence": 0 | 1 | 2 | 3
  }
}
agreement: 3 = same problem and same reasoning; 2 = same motivation, details differ; 1 = different motivations; 0 = contradictory.
In the merged reconstruction:
- `prior_situation` is the union of the reconstructions' relevant prior context, deduplicated, keeping only items supported by the evidence. It lists context from before the edit only and never describes the current edit or its results.
- `changes` has one entry per distinct change the edit makes (match the diff; do not merge independent changes, do not split one change). Each entry has its own `problem` (a specific issue grounded in `prior_situation`, not a restatement of the decision), `lever` (what kind of thing was changed), `value` (what it was set to), `decision`, an elaborated `reasoning`, `why_lever` (why this lever rather than the other plausible levers) and `why_value` (why this value rather than the other available values). Keep the alternatives comparisons that the evidence supports; where the evidence does not show why, say so.
- `rationales` are transferable, actionable items filed in a five-level structure: `goal` (the issue seen in the prior steps, as a "What do I do when ...?" question, which must not name the lever or action of this edit), `lever_context` (the evidence that points to this kind of lever rather than other levers), `lever` (a short generic name for the kind of move), `action_context` (given that lever, the condition that determines which action) and `action` (the specific strategy a novice can carry out, with the rule for choosing the value). All context fields are free of this notebook's names, paths, scores and versions. Keep the items the evidence supports, merge duplicates, make sure no two overlap, and sharpen the contexts where the reconstructions disagree on the cause, marking inferred causes as inferred. Drop items that have become generic platitudes or notebook-specific facts.
- `evidence` and `confidence` describe the edit as a whole.
- `reasoning` and `evidence` may use only information available before the edit (history, scores so far, code, diff).
Hindsight goes only in plausibility_note."""

CLUSTER_SYSTEM = """Task: group knowledge items by the goal they serve. Each item is a question naming a decision area.
Put items in the same cluster when their goals concern the similar contexts, so that the situations and moves under them can later be compared side by side. Do not merge goals that concern different decision areas, and do not split goals that only differ in wording or in notebook-specific detail. An item with no relative forms its own cluster.
Give each cluster one goal question, "What do I do when ...?", broad enough to cover all its items and narrow enough that the answer is a set of concrete moves.
Respond ONLY with JSON:
{"clusters": [{"goal": "<What do I do when ...?>", "ids": ["<item id>"]}]}
Every input id must appear in exactly one cluster."""

CHUNK_SYSTEM = """Task: file the items of one goal cluster into a knowledge tree for a novice. Every item comes from a different edit of a Kaggle notebook and has: lever_context (the evidence that pointed to a kind of lever), lever (the kind of move), action_context (given that lever, the condition that decided the action) and action (the specific strategy).
Build the tree in three steps.
1. Cluster the lever-selection contexts: group items whose lever_context describes similar evidence. Write one `lever_context` per group in general terms, so that a novice can recognize the evidence pattern.
2. Inside each lever-context group, list the levers. Items that name the same kind of lever (even in different words) share one entry; give it one generic `lever` name. For each lever, state in `selected_when` the nuance in the evidence that selects this lever over the other levers in the same group. If the group has a single lever, write "only lever in this group".
3. Under each lever, list the action-selection contexts with their actions. Merge items whose action_context and action are the same. For entries with similar action contexts but different actions, state in `nuance` what separates them; for a single entry write "only action under this lever". Each entry: `action_context` (the specific condition, recognizable by a novice) and `action` (the concrete strategy).
Rules: use only what the items support; when two entries look alike and the items do not show why they differ, write that the distinguishing nuance is not visible instead of inventing one; do not add examples, names or numbers that are not in the items; order from the most common situation to the most specific.
Respond ONLY with JSON:
{"overview": "<one sentence on what the items under this goal have in common>",
 "lever_contexts": [{"lever_context": "...", "levers": [{"lever": "...", "selected_when": "...", "actions": [{"action_context": "...", "action": "...", "nuance": "...", "sources": ["<item id>"]}]}]}]}
Every input id must appear in exactly one action entry's `sources`."""


EPISODE_SYSTEM = """Task: segment the version history of one Kaggle notebook into episodes.
You see every version transition of the notebook in order: its labels, the annotated goal and change, and the public leaderboard result. An episode is a contiguous run of transitions in which the author pursues ONE objective by working ONE lever (one knob, one component, one sub-problem): for example sweeping a vocabulary size over several submissions, swapping checkpoints to find the best one, building an inference pipeline, fixing a bug and verifying the fix, or adding and then re-weighting ensemble members. Cut a new episode when the objective or the lever changes, not when the score changes; a regression followed by a revert of the same lever stays in the same episode. Housekeeping-only or cosmetic transitions attach to the neighbouring episode they belong to. A single transition can be an episode when it stands alone.
Respond ONLY with JSON:
{
  "episodes": [
    {
      "start_v": <version number of the first transition's v_old>,
      "end_v": <version number of the last transition's v_new>,
      "objective": "<what the author is trying to achieve in this stretch, one sentence>",
      "lever": "<the knob / component / sub-problem being worked, a few generic words>",
      "pattern": "<one of: sweep (several values of one knob), probe (one or two trials of an idea), revert (undo a change that hurt), build (add infrastructure or a new component), fix (correct a bug), consolidate (merge, clean, re-weight what exists), explore (open-ended search without one knob)>",
      "trigger": "<what visible in the history started this episode: a regression, a plateau, a bug, a new idea, a new resource, or nothing visible>",
      "outcome": "<how the episode ended: best score reached, abandoned, reverted, superseded by a new idea; cite the versions and scores>",
      "n_submissions": <number of transitions in the episode with a leaderboard score>
    }
  ],
  "notes": "<anything about the segmentation that is uncertain>"
}
Episodes must be in order, contiguous (each start_v equals the previous end_v) and together cover every transition from the first to the last. Use only what is in the history; do not invent motives. Keep each text field under 40 words."""


EPISODE_EXTRACT_SYSTEM = """You are reading one episode of an experienced Kaggle competitor's notebook edit history: a contiguous run of versions in which they pursued one objective by working one lever. You see the competition, a one-line summary of every earlier edit with its leaderboard result, the code at the start of the episode, and for each transition in the episode its annotated goal and change, a truncated diff, and the leaderboard result. Notebook outputs (validation logs, printed values) are not available.
Extract the know-how this episode shows, as items. Each item has two parts:
(A) INSTANCE: what this author did here, in this notebook, with the concrete names, models, libraries, columns and numbers.
(B) GENERAL: the knowledge abstracted from that instance, which a different practitioner could apply on another task, dataset or model family.
Each part has three fields:
- goal: one open question the author needs answered at this point, in their own situation. Question-centric: it asks about the problem or the unknown (what limits the result, what to expect, how much, why, which direction), phrased naturally and not with a fixed opening such as "What do I do when". It must NOT contain or presuppose the solution: no lever, method, option or action, and no "should I use X", "does X help", "X or Y". A reader who does not know what the author did should still be able to write the same question. Bad: "Is rank-averaging or raw averaging of fold predictions better?" (names the options). Good: "How should several fold predictions be combined into one submission to score best on a ranking metric?" Bad: "Does enriching the classification head improve the score?" Good: "A strong pretrained backbone has plateaued at the current score; where can further gain come from without changing the backbone?" 
- context: the condition, visible evidence or prior result that makes the action appropriate (and, where it matters, what makes the alternatives less suitable).
- action: what is done, and how: the procedure, including how to react to feedback and when to stop, when the episode shows it.
Rules for the GENERAL part:
- It must contain no instance-specific entity: no model or architecture names (ResNet50, EfficientNet, XGBoost), no library, framework or function names, no competition, dataset or column names, no file names, no specific hyperparameter values or scores. Replace each by the role it plays ("a pretrained image backbone", "the regularization strength", "a tabular gradient-boosting model", "the validation metric"). A generic category such as "gradient-boosted trees", "a convolutional network" or "learning rate" is allowed; a named member of that category is not.
- Abstract to the level at which the knowledge would still be right on a similar problem that uses a different member of the category. Do not over-abstract: "tune hyperparameters carefully" or "use ensembling" is not knowledge. The general goal, context and action must still be specific enough to be wrong in some situations, and the action must be concrete enough for a novice to carry out.
- Numeric guidance may be kept only as a relative or conditional quantity ("halve the step size after a regression"), not as the instance's value.
- General goal, context and action must be understandable without reading the instance part.
Content rules: ground every statement in the history and mark inferred causes as inferred. State only what the episode supports; if a decision must have relied on information not visible here (validation output, timing, memory), say so in the instance context. Produce one item per distinct piece of know-how, usually one or two, at most three. An episode of a single routine edit may support none: then return an empty list. Keep each field under 50 words.
Respond ONLY with JSON:
{
  "items": [
    {
      "instance": {"goal": "...", "context": "...", "action": "..."},
      "general": {"goal": "...", "context": "...", "action": "..."},
      "steps": ["<step ids of the transitions in this episode that exhibit it, exactly as given in the prompt>"]
    }
  ]
}"""

EPISODE_EXTRACT_SYSTEM_V1 = """You are reconstructing the strategy of an experienced Kaggle competitor over one episode of their notebook's edit history: a contiguous run of versions in which they pursued one objective by working one lever. You see the competition, a one-line summary of every earlier edit with its leaderboard result, the code at the start of the episode, and for each transition in the episode its annotated goal and change, a truncated diff, and the leaderboard result. Notebook outputs (validation logs, printed values) are not available; when a decision must have relied on them, say so.
The single-edit level ("why this change") is handled elsewhere. Here reconstruct the level above it: how the author searched, how they reacted to feedback, and when and why they stopped. Then state the transferable know-how at the method or strategy level.
Respond ONLY with JSON:
{
  "search_process": "<how the values or variants were chosen across the episode: order, step size, what was held fixed, what was varied together; cite versions>",
  "feedback_response": "<how the author reacted to each leaderboard result or lack of one: continued, reversed direction, reverted, changed step size, submitted or not; cite versions>",
  "exit": "<why the episode ended as far as the history shows: optimum bracketed, idea abandoned, superseded, budget; and what the author moved to next>",
  "relied_on_unseen": "<decisions in the episode that must have used information not visible here (validation output, timing, memory), or 'none'>",
  "rationales": [
    {
      "level": "L2" | "L3",
      "goal": "<the situation the author is in at the start of the episode, as a 'What do I do when ...?' question; must not name the lever or action>",
      "lever_context": "<the evidence visible before or during the episode that makes this kind of lever the right one to work, and what makes other levers less suitable>",
      "lever": "<the kind of lever, a few generic words>",
      "action_context": "<given that lever, the condition that selects this way of working it>",
      "action": "<the procedure: how to search, how to react to feedback, when to stop; concrete enough for a novice to carry out, written as a rule and not as a narration of this episode, free of this notebook's names and exact values>",
      "instances": ["<step ids of the transitions in this episode that exhibit the procedure, exactly as given in the prompt>"],
      "counter_evidence": "<anything in the episode that contradicts or limits the rule, or 'none'>"
    }
  ],
  "evidence": "<the specific versions, scores and code facts that support this reconstruction>",
  "confidence": 0 | 1 | 2 | 3
}
Levels: L1 is a tool-specific recipe (a parameter value for a library); do not produce L1 items. L2 is a method-level rule (for this kind of model or data, this lever is the capacity or quality knob, and it is worked in this way). L3 is a strategy-level rule that does not depend on the model family (how to schedule experiments, how to react to a regression, when to stop a sweep, how to use the leaderboard as a signal). Produce one rationale per distinct piece of know-how the episode supports; usually one or two, at most three. An episode of a single routine edit may support none: then return an empty list. Do not state generic best practice without a condition; every rule must be specific enough to be wrong in some situations. Ground every statement in the history; mark inferred causes as inferred. Keep text fields under 60 words."""


VOCAB_SYSTEM = """Task: build a controlled vocabulary of lever categories from free-text lever names written by different annotators for edits of Kaggle notebooks.
A lever is the dimension of the pipeline an author acts on. Group the names into at most {max_categories} categories such that names meaning the same kind of move share a category, and categories are distinct enough that an expert would choose different evidence to decide between them. Cover the whole list; prefer fewer, well-named categories over many narrow ones, but keep separate what experts treat separately (e.g. 'checkpoint selection' and 'ensemble composition' are different moves).
Respond ONLY with JSON: {"categories": [{"name": "<short snake_case name>", "definition": "<one sentence>", "examples": ["<two or three of the given names>"]}]}"""

MAP_SYSTEM = """Task: map each free-text name to one category of the given controlled vocabulary. Use the category whose definition fits the name's meaning; use "other" only when nothing fits. Respond ONLY with JSON: {"mapping": {"<name>": "<category name>"}} covering every name given."""

TRIGGER_ENUM = ["regression", "plateau", "bug_or_error", "new_idea", "new_resource", "pipeline_gap", "none_visible"]

INDUCE_SYSTEM = """Task: induce the know-how that several Kaggle experts share, from strategy-level items extracted from their notebook histories.
Every item below was written from ONE episode of ONE notebook and has: goal (the situation), lever_context (evidence that selects the lever), lever, action_context, action (the procedure), the notebook (kernel) and competition it comes from, the author's tier, and whether the episode reached a new best leaderboard score.
Write rules that are supported by items from at least two different kernels. A rule is a conditional: `context` names the observable situation (in code, data, scores or history) under which it applies, and `action` says what to do and, where the items show it, what to do otherwise. It must be specific enough to be wrong in some situations; plain best practice with no condition is not a rule. Where items from different kernels disagree, either split the rule by the condition that explains the disagreement or record the disagreement as an exception. Do not merge items that only share wording; merge items that share the situation and the procedure. Items supported by one kernel only are listed under `singletons`, not turned into rules.
Respond ONLY with JSON:
{
  "rules": [
    {
      "name": "<short snake_case name>",
      "level": "L2" | "L3",
      "context": "<observable situation; under 60 words>",
      "action": "<procedure and, if shown, the otherwise-branch; under 80 words>",
      "support": ["<item ids>"],
      "exceptions": "<items or conditions that limit the rule, or 'none'>",
      "confidence": 1 | 2 | 3
    }
  ],
  "singletons": ["<item ids not covered by any rule>"]
}"""

CONSOLIDATE_SYSTEM = """Task: consolidate a list of rules induced separately from groups of items. Merge rules that state the same conditional (same situation, same procedure) even if worded differently, keeping the union of their support and the more precise wording; keep rules apart when their conditions or procedures differ. Do not invent support. Respond ONLY with JSON: {"rules": [{"name": "...", "level": "L2"|"L3", "context": "...", "action": "...", "support": ["<item ids>"], "exceptions": "...", "merged_from": ["<rule names>"]}]}"""
