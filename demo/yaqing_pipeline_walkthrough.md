# 顺着一步改动，看懂 Yaqing 的提取流水线

例子：RANZCR 比赛，ttahara（Grandmaster，key 13848868）的 **v34 → v35**。我们 10 月 29 日的 pilot 跑过这一步。

用的是 Yaqing 在 11 月 4 日、只针对 RANZCR 一个比赛的那次完整运行（10 个专家，走完了全部 8 步）：
`/data/user_data/pengchej/yaqing_1105/new_extraction/archive_old_runs/_per_competition_attempt/ranzcr-clip-catheter-line-classification/episode/`。
下文的文件名都在这个目录下。

## 0. 这一步实际改了什么（原始 notebook）

```diff
 # markdown 单元格（说明文字）
-# * image size: 3x**640x640**
+# * image size: 3x**512x512**
+# * add more augmentations to version 15
-# https://www.kaggle.com/ttahara/ranzcr-multi-head-model-training?scriptVersionId=52606857
+# https://www.kaggle.com/ttahara/ranzcr-multi-head-model-training?scriptVersionId=52614442
 # 代码
-IMAGE_SIZE = (640, 640)
-CONVERT_TO_RANK = True
+IMAGE_SIZE = (512, 512)
+CONVERT_TO_RANK = False
```

一共三件事：推理图片从 640 改回 512；预测不再转成排名；说明里换了一个新的训练 notebook 版本（"加了更多数据增强"），也就是说用的模型权重可能也换了。Kaggle 分数 0.9484 → 0.9559，是这条轨迹当时的最好成绩。

## 1. 输入：TraceML 对这一步的描述（`data/actions.parquet`）

- 一句话目的：*Match a different input size for inference (smaller 512x512) and disable converting probabilities to ranks …*
- 改动摘要：*IMAGE_SIZE changed from (640, 640) to (512, 512); CONVERT_TO_RANK flipped from True to False.*
- 标签：`image_resize`（大类 features）、`postprocess_change`（大类 inference）

**注意**：摘要漏掉了 markdown 里"换了训练版本"这件事。

## 2. 切成 episode，写成 item（Yaqing 更早的流水线做的，`data/episode_items.jsonl`）

LLM 把这位专家的 41 个版本切成若干段（episode）。v30–v36 是一段，目标是"扫一遍分辨率"。每段再写出几条 item，每条是一个"目的 / 背景 / 做法"三元组，分具体版（instance）和通用版（general）：

| item | 通用版的"做法"（缩写） | 包含哪几步 |
|---|---|---|
| `e8#1` | 在训练分辨率附近一档一档试推理分辨率，变大变差就退回 | 30→31、32→33、**34→35** |
| `e8#2` | 每次大改后都重新比较"原始概率平均"和"排名平均" | 31→32、33→34、35→36 |

**注意**：34→35 同时也关掉了排名转换，但它只被分给了 `e8#1`。这一步的"排名"那一半，在后面的流程里就丢了。这正是 Yaqing 问的"一步有多个动作怎么办"。

## 3. 自下而上聚类（第 2 步，`2b_bottomup.json`）

用 item 通用版的"做法"文字做 embedding，相近的合并，拿不准的问 LLM。RANZCR 的 121 条 item 聚成 90 个动作，再往上逐层合并：90 → 37 → 19 → 18 → 根。

`e8#1` 和另外两位专家（13521245、13577502）的同类做法合成了一个动作 **A4 "sweep inference resolution"**。三个不同的专家做了同一件事，这是聚类想得到的结果。往上依次是："推理分辨率策略" → "推理配置" → "优化流水线的哪一环" → 根。

## 4. 挂到 Sherry 的骨架上（第 3 步，`3_merged_tree.json`）

骨架是 LLM 不看数据、凭常识写的 4 层树（`1_topdown.json`）。每个动作找最匹配的骨架节点，找不到就在合适的位置新开节点。这一步走过的路径（walk）是：

```
T        Get a better score                  （骨架）
└ T.6    Inference & Post-processing        （骨架）
  └ T.6.n74   Inference resolution strategy  （数据里新长出来的）
    └ T.6.n74.n75  sweep inference resolution（叶子，3 个专家的 3 次改动）
```

**能看到的问题**：
- "推理分辨率策略"下面的 5 个选项，好几个其实是同一件事：*sweep inference resolution*、*Align inference resolution with training resolution*、*reduce inference resolution to match training distribution*、*probe adjacent resolutions*。它们不是"同一时刻要做的几选一"。
- 根节点下面除了 8 个大方向，还混进了一个 *tune resolution and ensemble folds*，层级不对。

## 5. 每个岔路口要回答的问题（第 4 步，`4_desiderata.json`）

LLM 看了每个节点的选项和落在下面的改动，写出"选之前要弄清楚的问题"，每个问题下面有几条 yes/no 检查，并猜每条检查支持哪个选项。以 "推理分辨率策略" 节点为例：

- 训练和推理的预处理有没有已知的不一致？ → E07 推理分辨率和训练分辨率不一致；E30 归一化参数不一致
- 最优分辨率是不是已经大致找到了？ → E244 已经在训练分辨率和至少一个别的分辨率上有分数；E245 还一次都没试过
- 现在的分辨率比训练时大多少？ → E246、E64
- 还剩多少提交次数？ → E23、E247
- 另外 6 条是第 5 步从专家轨迹里补出来的（E391–E396）

整个 RANZCR 树一共攒了 433 条检查（`evidence/registry.md`）。

## 6. visit record：推断专家在每个岔路口查了什么（第 5 步，`5_visits.json`）

这一步走过 3 个节点，所以有 3 条 visit record。下面是 "推理分辨率策略" 这个节点上的那条（共 14 条检查，这里列其中 9 条）：

| 检查 | 判断 | LLM 给的证据 |
|---|---|---|
| E07 推理分辨率 ≠ 训练分辨率 | yes（第 1 个查） | 上一版用 640，新的训练 checkpoint（scriptVersionId=52614442）是 512 训练的 |
| E244 已有多个分辨率的分数 | yes | v31 用 512 得 0.95418，v33 用 640 得 0.94942 |
| E245 还没扫过分辨率 | no | 已经试过 512 和 640 |
| E246 现在比训练大 20% 以上 | yes | 640/512 = 1.25 |
| E23 提交次数够用 | yes | 已经迭代 34 版还在继续提交 |
| E391 之前的尝试有明显趋势 | yes | 512→640 变差，所以退回 512 |
| E392 有一个新 checkpoint 还没在它的训练分辨率上试过 | yes | 训练 notebook 链接换成了新版本 |
| E393 分辨率变化和换模型同时发生，没法单独归因 | yes | 同一步既换 checkpoint 又换分辨率 |
| E30 归一化不一致 | not_checked | |

最后记下：选了 *sweep inference resolution*，分数 +0.0075，创了新高。

**我拿原始 notebook 核对过**：
- 证据里引用的链接、"add more augmentations to version 15"、`model.eval()` 都真实存在于代码里，分数也对得上。E393 "没法单独归因"是一个很到位的判断。
- 但这些内容不在 TraceML 的摘要里，说明**这次运行的 visit 看到了原始代码**。而 Yaqing 现在的代码（`data.py`、`visits.py`）只给 LLM 看一句话摘要、分数和之前的改动历史，README 也写了"不读任何原始代码"。所以**按现在的代码跑 7 个比赛，visit 很可能达不到这里的质量**。要找 Yaqing 确认这次运行是怎么拿到代码的。
- 14 条检查里有 12 条被标成"查过了"（yes 或 no），只有 2 条是 not_checked。真实的专家不太可能在一次改动前查 12 件事。"提交次数够不够"这类检查几乎每次都是 yes，信息量很低。

## 7. 汇总成小抄（第 6–8 步，`6_scores.json`、`7_enough.json`、`8_returns.json`）

把 "推理分辨率策略" 节点上所有的 visit record（18 条，来自 6 个专家）汇总：

- **重要度**：每条检查的重要度和方向是 LLM 读了这个节点和最多 10 条 visit 之后猜的，不是统计出来的。Sherry 文档里的"统计法"和"不打分"两个对照方案，在新代码里被删掉了。
- **先查什么**：E07 在 18 次里都是第一个查的，其余检查一次都没排过第一。E07 恰好是这个节点检查列表里的第一条，所以这个"顺序"很可能只是列表顺序，不是专家的习惯。
- **查到多少就够**："领先的选项概率 ≥ 72%"，以及"中位数查 10 条"。Sherry 的设想是"中位数查 2 条"，这里的 10 条来自第 6 节那个问题：LLM 把大部分检查都标成了"查过"。
- **什么时候回头**：观察到 2 次回头，都发生在"单个改动后分数下降"之后，两次回头后分数都涨了。其中一次就是 ttahara 的 v36 → v37。
- **用这套打分预测专家的选择**：67% 的时候，得分最高的选项就是专家实际选的那个。但这些分数是 LLM 看过 visit 之后猜的，有循环论证的成分。

## 8. 最后给 agent 读的文件（导出，`application/`）

- `taxonomy.md`：整棵树，每个节点写"要决定什么 → 有哪些选项"和 desiderata。
- `attention/t-6-n74-inference-resolution-strategy.md`：这个节点的小抄，原文如下：

```
options: sweep inference resolution (3) | Match inference preprocessing to training (3) | Align inference resolution
         with training resolution (1) | reduce inference resolution to match training distribution (1) | probe adjacent resolutions (1)
check first: E07 The inference resolution does not match the training resolution ...  imp 0.55 → +sweep inference resolution
then:        E244 A baseline score exists at the training-matched resolution and at least one other ...  imp 0.60
then:        E245 No resolution sweep has been attempted yet ...  imp 0.70 → -sweep inference resolution
more:        11 further checks, load on request
enough when: top option >= 72% (lower quartile over 18 visits) or >= 62 points ahead; median 10 checks
come back:   after 'regression after a single change' (2/2)  [2 returns, 2 improved the score]
```

- `cases/t-6-n74-n75-sweep-inference-resolution.md`：做过这个动作的 3 个先例，各有当时的证据和分数变化。
- `evidence/registry.md`：所有检查的定义。

## 小结：这一步看下来

**做得好的**
- 链条完整：从一步代码改动，一直到 agent 能读的小抄和先例，每一环都有文件，能对上。
- 跨专家的归类是对的：3 个专家的"扫分辨率"被合成了一个动作。
- 这次运行的 visit record 证据具体、和代码对得上，还指出了"没法单独归因"这种专家级的判断。

**有问题的**
1. 一步改了几件事时，只保留了一件（排名那一半丢了）。
2. 选项列表里有重复：同一件事被说成好几个"选项"。
3. visit 把大部分检查都标成"查过了"，导致"查多少就够"失去意义；"先查什么"很可能只反映了列表顺序。
4. 重要度是 LLM 猜的，用它去预测专家的选择有循环论证。
5. 这次运行的 visit 看到了代码，而现在的代码不给代码。如果真是这样，7 个比赛跑出来的质量会变差。
