"""All prompts. Task-specific wording is a placeholder <<name>> filled from config.yaml `task:` (see common.fill), so the prompts carry no
domain knowledge and can be reused for another task by editing the config. Other slots (<<depth>>, <<tree>>, ...) are passed to fill()."""

TOPDOWN = """You are an <<actor>> and researcher. You write a taxonomy of the decisions a practitioner faces when trying to <<objective>> in <<domain>>.

The tree is a decision tree:
- every internal node is a DECISION: a question the practitioner answers at that moment ("<<example_question>>").
- its children are the OPTIONS: real alternatives an expert picks between at the same moment (mutually exclusive in focus, though they may be combined later).
- leaves are concrete ACTIONS ("<<example_action>>").

Rules:
- Root = "<<root_name>>". Go <<depth>> levels deep (root = level 0; leaves at level <<depth>>; a branch may stop earlier if it cannot be refined).
- Children of one node must be siblings at the same granularity and the same moment of choice. Do not mix a narrow knob with a broad area.
- Cover the whole space: <<areas>>. Stay generic to the kind of task, but name task-type-specific options where they are standard.
- 3 to 7 children per node; short names (<= 6 words).
- Do not use any information about a specific instance of the task.

Return ONLY JSON: {"name": "<<root_name>>", "decision": "<question>", "children": [{"name": "...", "decision": "<question, only for internal nodes>", "children": [...]}, ...]}. Leaves have only "name" and an optional one-line "description"."""

PAIR_0 = """You decide whether two groups of <<edit>>s are the SAME ACTION: the same kind of change to the same knob/component in the same direction (e.g. both '<<example_action>>'). Different values of the same change count as the same action; different knobs, components, or opposite directions do not.
Return ONLY JSON: {"same": true|false, "confidence": "high"|"low", "reason": "<one sentence>"}"""

PAIR_1 = """You decide whether two actions/groups are ALTERNATIVES IN THE SAME DECISION: would an expert, at one moment, be choosing between them (e.g. '<<example_action>>' vs '<<example_action_2>>' are both answers to '<<example_decision>>')? Things that are done together in sequence or answer different questions are NOT the same decision.
Return ONLY JSON: {"same": true|false, "confidence": "high"|"low", "reason": "<one sentence>"}"""

PAIR_2 = """You decide whether two decision groups belong to the same BRANCH of a decision tree about how to <<objective>>: would an expert, when answering the broader question 'which area / knob family do I work on next?', see them as siblings under one heading (e.g. both are '<<example_branch_1>>', both are '<<example_branch_2>>')? Different knobs of the same area are siblings; different areas are not.
Return ONLY JSON: {"same": true|false, "confidence": "high"|"low", "reason": "<one sentence>"}"""

PAIR_BATCH_NOTE = """

You get several numbered pairs. Judge each pair independently of the others. Return ONLY JSON: {"results": [{"pair": 1, "same": true|false, "confidence": "high"|"low", "reason": "<one sentence>"}, ...]} with one entry per pair, using the pair numbers given."""

REVIEW = """You review one cluster that was built by merging groups; some merges are uncertain. Decide whether all members belong together (as stated in the task). If not, partition the members into the fewest coherent subsets. Keep members together when in doubt.
Return ONLY JSON: {"coherent": true|false, "groups": [[member numbers], ...]}  (groups must cover every member exactly once)"""
REVIEW_TASK = {0: "the same ACTION", 1: "ALTERNATIVES IN THE SAME DECISION", 2: "siblings under one branch (same area / knob family)"}

NAME_ACTION = """You name an ACTION: a group of <<edit>>s that share one intent. Give it a short imperative name that would still make sense in another instance of the task (e.g. "<<example_label>>"), and a one-sentence summary that states the direction and the typical reason.
Return ONLY JSON: {"label": "...", "summary": "..."}"""

NAME_ACTION_BATCH = """You name several ACTIONS. Each is a group of <<edit>>s that share one intent. For each group give a short imperative name that would still make sense in another instance of the task (e.g. "<<example_label>>"), and a one-sentence summary that states the direction and the typical reason. Name each group from its own items only.
Return ONLY JSON: {"results": [{"group": 1, "label": "...", "summary": "..."}, ...]} with one entry per group, using the group numbers given."""

NAME_DECISION = """You name a DECISION node in a tree of what an expert can change to <<objective>>. The children below are options that were grouped because they are alternatives at the same moment. Name the node by the question it answers (which direction, which knob, which part), give it a short label, and give each child a short option name (how it answers the question).
Return ONLY JSON: {"question": "...", "label": "...", "options": [{"child": "<child id>", "option": "..."}]}"""

MATCH = """You attach observed expert ACTIONS to a pre-written taxonomy of decisions for how to <<objective>>.

For each action decide:
- match: the id of the most specific taxonomy node that names this action (a leaf is best). null if no node covers it.
- fit: "exact" (the node IS this action), "broader" (the node is a more general category containing the action), or "none".
- parent: only if match is null or fit is "broader": the id of the INTERNAL taxonomy node under which the action should become a new option (the decision at which an expert would choose it). Always give parent when fit != exact.

Taxonomy (id | name | decision question; indentation = depth):
<<tree>>

Return ONLY JSON: {"results": [{"action": "<action id>", "match": "<node id>"|null, "fit": "exact|broader|none", "parent": "<node id>"|null}]}"""

ALT_CHECK = """You check one decision node of a tree. Its children should be REAL ALTERNATIVES: options an expert picks between at the same moment, at the same granularity, answering the node's question.
List problems: children that answer a different question, that are a special case of a sibling, that duplicate a sibling, or that an expert would do together rather than choose between. Do not invent problems; an empty list is fine.
Return ONLY JSON: {"ok": true|false, "issues": [{"child": "<child id>", "problem": "..."}]}"""

DESIDERATA = """You write the DESIDERATA of one decision node: what a person has to know in order to choose among its options.

You see the decision, its options (children) and real edits that experts made under each option. Write the questions an expert would have to answer to pick among THESE options.
Rules:
- Specific to this decision. "Which part is the bottleneck?" is acceptable when it tells the agent what to go and look at; generic items like "cost" or "is it worth it?" that could sit on every node are NOT acceptable.
- Each check is a yes/no STATEMENT about the situation that can be settled BEFORE choosing, by looking at something the agent can observe (<<evidence_sources>>).
- Group checks under 2-4 short questions in capitals (e.g. "WHAT FITS THIS CASE?"). 4 to 8 checks in total.
- For each check give `how`: the concrete observation that settles it.
- For each check also give `pushes`: which options a YES makes more likely, as {option id: weight in [-1,1]} (negative = makes the option less likely). Only options that really move.

Return ONLY JSON: {"groups": [{"under": "WHAT ... ?", "checks": [{"check": "<statement>", "how": "...", "pushes": {"<option id>": 0.8}}]}]}"""

DEDUPE = """Below are checks (yes/no statements an expert settles before a decision), written independently for different nodes of one tree. Find the ones that are the SAME check (same observation, same yes/no meaning, wording aside) and should share one definition.
Only merge when truly equivalent; a check that is merely related stays separate.
Return ONLY JSON: {"merges": [{"canonical": "<statement>", "how": "<observation>", "ids": ["<id>", "<id>", ...]}]}  (list only groups of 2+ ids)"""

VISIT = """You reconstruct what an <<actor>> could SEE just before an edit, to fill in a record of the evidence they had at each decision.

You are given the expert's earlier edits with their <<progress_signal>>, a summary of the edit itself (labels, goal, change summary; no raw code) and the intents behind it (an intent may describe a sequence of edits; judge it at THIS edit). For each intent you get the decision nodes it passes through, the option the expert took, and the checks (yes/no statements) that belong to each node.

For every check give a state:
- "yes" / "no": the expert had enough visible evidence BEFORE the edit (<<evidence_sources>>; which options were already tried) to settle the statement, and the evidence says yes / no.
- "not_checked": nothing visible shows that the expert looked at or could have settled this. This is the default; do not guess.
Never use the outcome of the edit (the <<progress_signal>> after it) as evidence. The summary may show what the expert looked at or reacted to, but not how it turned out.
Give a short `evidence` (quote or 1 sentence) for yes/no, and `order`: the plausible order (1, 2, ...) in which the settled checks were looked at at that node (null for not_checked).
<<new_checks_rule>>
Return ONLY JSON: {"visits": [{"item": "<item id>", "node": "<node id>", "checks": [{"id": "E01", "state": "yes|no|not_checked", "evidence": "...", "order": 1}]<<new_checks_field>>}]}  (one entry per item and node listed)."""

NEW_CHECKS_RULE = """If the visible evidence shows the expert relied on something that NO listed check captures, add it under `new_checks`: a yes/no statement specific to this node's decision (same standard as the listed checks: observable before choosing, not generic), `how` it is observed, and its state ("yes" or "no" only, with evidence and order). Only add what the edit really shows; an empty list is the normal case."""
NEW_CHECKS_FIELD = ""","new_checks": [{"check": "<statement>", "how": "<observation>", "state": "yes|no", "evidence": "...", "order": 2}]"""

NEW_CHECK_MERGE = """A decision node has a list of existing checks (yes/no statements an expert settles before choosing). Annotators proposed additional checks while reading expert behaviour. For each proposal decide: is it the SAME check as an existing one (same observation and yes/no meaning, wording aside) -> give that id; or the same as another proposal -> give them one shared new group; or genuinely new. Reject proposals that are generic (could sit on every node) with group null.
Return ONLY JSON: {"proposals": [{"id": "p1", "existing": "<existing id>"|null, "new_group": "<g1, g2, ...>"|null, "canonical": "<statement for a new group>", "how": "<observation for a new group>"}]}  (exactly one of existing / new_group per accepted proposal; both null = rejected)"""

GUESS = """You assign weights to the evidence items of one decision node of an expert-knowledge tree.

You get the node (question and options), its checks, and a handful of recorded visits: what the expert had checked (yes/no) and which option they took. Write for every check:
- importance in [0,1]: how much this check should matter when choosing among the options;
- pushes: {option id: weight in [-1,1]} — how a YES moves each option (negative = makes it less likely; a NO acts in the opposite direction). Only options that actually move.
Use the visits as evidence but also what you know about practice in <<domain>>. Do not copy the option an example expert took unless the check explains it.
Return ONLY JSON: {"scores": {"E01": {"importance": 0.7, "pushes": {"T.3.1": 0.8}}}}"""
