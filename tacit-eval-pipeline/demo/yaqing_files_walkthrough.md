# Yaqing 流水线的文件，是怎么一个个生成的

例子：RANZCR 比赛 archanabenur（15173072）调归一化参数的那几步（v15→v21 乱试，v22 改回标准值）。
文件都在 `/data/user_data/pengchej/yaqing_1105/new_extraction/archive_old_runs/_per_competition_attempt/ranzcr-clip-catheter-line-classification/episode/`。

## 先看全貌：主线只有十来个文件

```
输入（data/）
  actions.parquet ──整理──▶ trans.json           每一步 vN→vN+1 一行：TraceML 的一句话目的、改动摘要、标签、分数
  episode_items.jsonl                             她更早那条流水线写的"段落 + item"
  scores.json                                     每个版本的 Kaggle 分数

主线（按顺序）
  ① 1_topdown.json        LLM    不看数据，写一棵"怎么提分"的骨架树
  ② 2a_items.json         程序   把 item 摘出来，准备归类
  ③ 2b_bottomup.json      程序+LLM  把 item 归成"动作"，再往上归成"决定"
  ④ 3_merged_tree.json    LLM    把归好的动作挂到骨架上，合成一棵树（另有 3_match、3_action_map、3_check）
  ⑤ 4_desiderata.json     LLM    每个岔路口写一张检查单
  ⑥ 5_visits.json         LLM    每一步、每个岔路口，填一遍检查单（visit record）
  ⑦ 6_scores.json         LLM    猜每条检查有多重要、支持哪个选项
  ⑧ 7_enough.json         程序   统计：先查什么、查多少就够
  ⑨ 8_returns.json        程序   统计：什么时候会回头
  ⑩ application/          程序   导出给 agent 读的文件

可以不看的（缓存、日志、中间稿）
  2b_pairs_*.jsonl、2b_review_*.jsonl   第③步里问 LLM"这两条是不是同一件事"的原始回答
  4_desiderata.jsonl、4_dedupe.jsonl、4b_new_checks.jsonl、4_desiderata_base.json   第⑤步的原始回答和中间稿
  5_visits_r1.jsonl、5_visits_r2.jsonl、5_new_checks.json   第⑥步两轮的原始回答、补充的新检查
  6_guess.jsonl                         第⑦步的原始回答
  9_*.json                              稳定性检验：专家分两半各建一次树再比较
```

LLM 做的是需要"读懂、判断、写字"的步骤（①③④⑤⑥⑦）；程序做的是"拼接、统计、导出"（②⑧⑨⑩，以及③里的距离计算）。

## 一步步看这个例子

### 输入：`trans.json`（由 `data/actions.parquet` 整理而来）
每一步一行。v16→17 这一行是：
- 目的："调整推理时的归一化均值，让它和训练时的预处理一致"
- 摘要："均值从 [0.495, 0.446, 0.416] 改成 [0.475, 0.436, 0.406]"
- 分数：0.9522 → 0.9571

### ① `1_topdown.json`：骨架树（LLM，不看任何数据）
LLM 凭常识写出"想提分可以改哪里"的 4 层树。和这个例子有关的节点：

```json
{"id": "T.2.5", "name": "Preprocessing and scaling", "decision": "How should I transform raw features?",
 "children": ["Normalize or standardize", "Log or power transforms", "Categorical encoding schemes", "Dimensionality reduction"]}
```

意思是：在"数据与输入 → 预处理和缩放"下面，骨架认为有 4 种选择：归一化、取对数、类别编码、降维。

### ② `2a_items.json`：待归类的 item（程序）
从 `episode_items.jsonl` 里把每条 item 摘出来，RANZCR 一共 121 条。这个例子的 item 是：

```json
{"id": "15173072:e4#1",
 "step_ids": ["15173072:15->16", "15173072:16->17", "15173072:17->18", "15173072:18->19", "15173072:20->21"],
 "text": "Default to the canonical normalization statistics for the pretraining dataset ..."}
```

- `step_ids`：这条 item 覆盖了 5 步，也就是专家乱试的那 5 步。
- `text`：用来归类的那段话，意思是"默认用标准值"。这是事后才得出的结论，和这 5 步里专家实际做的事正好相反。

### ③ `2b_bottomup.json`：归类（程序算距离 + LLM 判断和起名）
程序先把每段 `text` 变成向量、算距离，相近的合并，拿不准的交给 LLM 判断。合成的每一堆，LLM 都给起一个名字。这条 item 的归类结果是：

```
R    Get a better score                           （根）
└ D1.7  Normalization statistics strategy        （第 1 层：一个"决定"）
  └ A69  Align inference normalization with training statistics   （第 0 层：一个"动作"）
         items: ["15173072:e4#1"]   experts: ["15173072"]
```

**A69 这堆里只有这一条 item、一位专家**，这就是"零散"的样子。

### ④ 挂到骨架上：`3_match.jsonl` → `3_action_map.json` → `3_merged_tree.json`；检查：`3_check.jsonl`（LLM）
- `3_match.jsonl`：LLM 判断 A69 对应骨架上的哪个节点。答案是 `T.2.5.1 Normalize or standardize`，匹配程度是 `broader`，意思是骨架那个节点比这个动作宽泛。
- 因为不是"正好对上"，程序就在 T.2.5 下面新开一个节点 `T.2.5.n16 Normalization statistics strategy`，把 A69 挂在它下面，成为 `T.2.5.n16.n18`。`3_action_map.json` 记下的就是这个结果：

  ```json
  "A69": {"attached": "T.2.5.n16.n18", "verdict": {"match": "T.2.5.1", "fit": "broader", "parent": "T.2.5"}}
  ```

- `3_merged_tree.json`：骨架和所有挂上去的动作合成的完整树。这个新节点下面最后有 3 个选项：n17 按目标领域重新对齐（另一位专家的）、n18（就是 A69）、n19 与预训练值保持一致（v22 改回标准值那步）。
- `3_check.jsonl`：LLM 检查每个节点的子选项是不是真的几选一。它在 T.2.5 下面指出："n16 是 T.2.5.1（Normalize or standardize）的一个特例"。也就是说，它发现新节点和骨架原有的节点重复了，**但只记录，不修**。

### ⑤ `4_desiderata.json`：每个岔路口的检查单（LLM，Opus）
对 `T.2.5.n16`，LLM 写了 4 个问题，每个问题下有几条 yes/no 的检查。所有检查都放在一张总表 `registry` 里，每条带一个编号和"怎么去查"。例如：

```json
"E133": {"check": "The exact mean and std used during pretraining are documented or retrievable ...",
         "how": "Check the model card, library documentation (e.g., timm's model.default_cfg, ...)"}
```

大白话："预训练时用的均值和方差是公开可查的"；查法是"看模型说明，或 timm 的默认配置"。

### ⑥ `5_visits.json`：填检查单，也就是 visit record（LLM，Opus，分两轮）
对每一步、它经过的每个岔路口，LLM 填一张检查单。v16→17 在这个节点上的记录：

```json
{"step_id": "15173072:16->17", "node": "T.2.5.n16", "child": "T.2.5.n16.n18",
 "score_old": 0.9522, "score_new": 0.9571, "effect": "better",
 "checks": {"E133": {"state": "no", "order": 3,
            "evidence": "The checkpoint is from a third-party Kaggle dataset ... not documented or retrievable."}, ...}}
```

- `child`：专家选了哪个选项。**这个信息在填单子时就给了 LLM**，这就是"答案泄漏"。
- `checks`：每条检查填 yes / no / not_checked，附上证据和"第几个查的"。

第一轮里，LLM 还可以提议新的检查（存在 `5_new_checks.json` 里，E364–E367 就是这样来的），第二轮再按补全后的检查单重填。

### ⑦ `6_scores.json`：每条检查有多重要（LLM）
LLM 读这个节点、它的检查单和最多 10 条记录，猜每条检查的重要度，以及它是 yes 时更支持哪个选项：

```json
"E133": {"importance": 0.8, "pushes": {"T.2.5.n16.n19": 0.8, "T.2.5.n16.n18": -0.3}}
```

意思是：E133 很重要（0.8）；它为 yes 时支持"与预训练值保持一致"（n19），不支持"继续调"（n18）。

### ⑧ `7_enough.json`：先查什么、查多少就够（程序）
用上一步的打分，对这个节点的 9 次访问做统计：

```json
{"n_visits": 9, "median_checked": 8.0, "enough_top_prob_q25": 0.90, "top_matches_taken": 1.0,
 "check_first": [{"check": "E31", "first": 9, "checked": 9}, ...]}
```

意思是：专家每次中位数查了 8 条；领先选项的概率到 90% 时就拍板；用这套打分"预测"专家的选择，命中率 100%；最先查的总是 E31。

### ⑨ `8_returns.json`：什么时候回头（程序）
同一位专家在同一个节点上，后来选了以前没选过的选项，记为一次回头。RANZCR 一共记到 31 次，最常见的触发条件是"单个改动后分数下降"（10 次）。这个节点一次也没记到（原因见 `yaqing_example_normalization.md`）。

### ⑩ `application/`：导出给 agent 读的文件（程序）
- `taxonomy.md`：整棵树，每个节点写明决定、选项、检查单；
- `attention/t-2-5-n16-normalization-statistics-strategy.md`：这个节点的小抄，由 ⑤⑦⑧⑨ 拼成；
- `cases/t-2-5-n16-n19-...md`：选过这个选项的先例，即谁、哪几步、当时的证据、分数变化；
- `evidence/registry.md`：所有检查的定义和查法。

## 一句话串起来
TraceML 的每步描述和 episode item → ① 骨架 + ③ 归类 → ④ 合成一棵树 → ⑤ 每个岔路口一张检查单 → ⑥ 每一步都填一遍 → ⑦⑧⑨ 汇总成重要度、先查什么、何时拍板、何时回头 → ⑩ 写成小抄文件。

我们发现的问题分别出在：③（零散）、④（重复选项只记录不修）、②⑥（事后结论、答案泄漏）、⑦⑧（打分是照着泄漏的记录猜的，所以命中 100%）。
