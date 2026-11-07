# 交接：Yaqing 的 new_extraction（2026-11-07，Pengcheng）

## 去哪里拿

仓库：<https://github.com/pengchej-star/tacit-eval-pipeline>，目录 `extraction/new_extraction/`。

```bash
git clone https://github.com/pengchej-star/tacit-eval-pipeline.git      # 已经 clone 过的话：git pull
cd tacit-eval-pipeline/extraction/new_extraction
cp -r /你的/new_extraction/data .        # data/ 和 out/ 都不在 git 里，从你自己的文件夹拷过来
cp /你的/new_extraction/.env .
```

**看具体改了什么**：
- `cc38323`：你 11 月 4 日的代码原样拷贝，只有代码，不含 `data/`、`out/`、`archive_old_runs/`。
- 之后的两个提交是我们的修改：`e3347ed` 是 4 处修复，`e308801` 加了选择器 `visits.masked`。代码只动了 4 个文件：`visits.py`、`prompts.py`、`data.py`、`config.yaml`。

```bash
git diff cc38323 e308801 -- extraction/new_extraction
```

网页版：<https://github.com/pengchej-star/tacit-eval-pipeline/compare/cc38323...e308801>。

如果你想继续用自己的文件夹，只要把这 4 个文件拷过去：`visits.py`、`prompts.py`、`data.py`、`config.yaml`。

## 改了什么（只改最必要的，其余逻辑不动）

| # | 改动 | 文件 | 为什么 |
|---|---|---|---|
| 1 | **第 5 步填检查单时遮住答案。** 不再给 LLM 看：选了哪个选项（`Taken:`）、这一步自己的 goal / labels / change summary、episode item 的文字。**每个（改动，路口）单独调用一次**，因为把整条路径列出来，会暴露上面每一层选了哪个选项。"选了哪个选项"仍由程序写进每条 visit record，后面的打分和汇总照常使用 | `visits.py`（`Ctx.prompt`、`make_jobs`、`run`）、`prompts.py`（新增 `VISIT_MASKED`、`NEW_CHECKS_RULE_MASKED`，原来的 `VISIT` 保留） | 我们的对照实验：同样的检查单，给不给答案，约 32% 的标注会变（不给答案的版本自己重跑只变 6%）。不给答案时，"标准值查得到"这类事实不再跟着专家的选择翻转。见 `demo/blind_visit_pilot/` |
| 2 | **第 0 层归类的门槛放宽**：`cluster.max_dist` 从 `[0.30, 0.60]` 改成 `[0.38, 0.60]`，仍然由 LLM 判断"是不是同一个动作" | `config.yaml` | 7 个比赛合跑时，35% 的 item 在 0.30 之内没有任何邻居，根本没有机会合并；而 LLM 对送去判断的配对 85% 都说"是同一个"。见 `demo/yaqing_fragmentation.md` |
| 3 | **检查单的顺序每次打乱**（按 step+node 固定随机种子） | `visits.py` | 原来的"先查什么"基本就是列表顺序：比如某个节点上 E07 在 18 次里都排第一，而它正好是列表的第一条 |
| 4 | **可选：给 LLM 看 v_old 那一版的 notebook**。设置 `paths.notebooks` 指向 TraceML `trajectories_human.tar.gz` 解压出来的 `human/` 文件夹（`<key_id>/versions/vNNN.ipynb`）即可；默认是 `null`，即不给 | `data.py`（`notebook_text()`）、`config.yaml`（`paths.notebooks`、`context.code_max`） | 只看一句话摘要信息太少，摘要也会漏东西，比如 ttahara v34→35 换了训练 checkpoint 这件事。你 11 月 4 日 RANZCR 那次的证据引用了 markdown 和 `model.eval()`，看起来当时是读到了代码的 |

**选择器 `visits.masked`**（在 `config.yaml` 的 `visits:` 下面）：第 1、3、4 条改动只在 `true` 时生效，见下一节。

**缓存文件换了新名字**：`5_visits_masked_r1.jsonl`、`5_visits_masked_r2.jsonl`、`4b_new_checks_masked.jsonl`。在旧的 out 目录里跑，也不会读到旧的、没遮答案的缓存。

**没有动的**：骨架、归类方法、挂到骨架、desiderata、新检查的合并、打分（仍然是 LLM 猜）、"查多少就够"、回头、稳定性检验、导出格式。用 TraceML 标签搭上两层、合并重复选项、修回头检测、加回"统计法"打分等，留给你下一次改代码时处理。具体建议见 `demo/yaqing_fragmentation.md` 和 `demo/yaqing_spotcheck_ranzcr.md`。

## 选择器：`visits.masked`（第 5 步用哪种写法）

在 `config.yaml` 里：

```yaml
visits:
  masked: true      # 默认
  new_checks: true
```

| | `masked: true`（默认，新写法） | `masked: false`（11 月 4 日原写法） |
|---|---|---|
| 怎么问 | 每个（改动，路口）单独问一次 | 每次改动问一次，整条路径一起问 |
| LLM 能看到 | 之前的改动和分数、这个路口的选项、它以前在这里选过什么、打乱顺序的检查单；设置了 `paths.notebooks` 时再加上 v_old 的 notebook | 以上全部，再加上：这一步的 goal / labels / 摘要、item 文字、整条路径，以及每个路口选了哪个选项（`Taken:`） |
| 答案泄漏 | 没有 | 有，标注会往专家的选择上靠 |
| 缓存文件 | `5_visits_masked_r1/r2.jsonl`、`4b_new_checks_masked.jsonl` | `5_visits_r1/r2.jsonl`、`4b_new_checks.jsonl`（和你原来的一样） |
| 调用次数（RANZCR 一轮） | 850 次 | 214 次 |
| 适合 | 正式结果 | 和旧结果对比、复现 11 月 4 日的结果、省钱的试跑 |

**两种模式输出的 `5_visits.json` 格式完全一样**，第 6–8 步和导出不用改。

**注意**：
- 两种模式写到同一个 out 目录时，会互相覆盖 `5_visits.json`、`4_desiderata.json` 和之后的文件；缓存不会串。要并排对比，就用不同的 `--suffix`。
- `paths.notebooks` 只在 `masked: true` 时生效；`masked: false` 完全按原样运行，不看 notebook，也不打乱顺序。
- 第 2 条（`cluster.max_dist`）和这个开关无关，两种模式都会用到。

**并排对比两种模式**（RANZCR，从第 5 步开始）：

```bash
# 两个 out 目录都按"怎么重跑 A"里的方法准备好第 1–4 步：
#   out/pooled_episode_ranzcr_masked/  和  out/pooled_episode_ranzcr_orig/
python run.py --comps ranzcr-clip-catheter-line-classification --suffix _ranzcr_masked --from 5      # masked: true
# 把 config.yaml 改成 masked: false，再运行：
python run.py --comps ranzcr-clip-catheter-line-classification --suffix _ranzcr_orig --from 5
```

## 测试到什么程度

用你 11 月 4 日 RANZCR 单独那次运行的第 1–4 步结果做了冒烟测试：
- **只构建 prompt、不调用 API**：RANZCR 一共产生 850 个（改动，路口）任务，覆盖 214 次改动。抽查 3 个 prompt，都**没有** `Taken:`、这一步的 goal 和摘要、item 文字；检查顺序已打乱；notebook 代码已给出。
- **真调用**：用这 3 个任务把第 5 步完整跑了一遍（第一轮、合并新检查、第二轮），再跑了第 6–8 步和导出，全部正常。
- 这 3 条记录里，归一化那个路口的"标准值查得到"在 v16→17 和 v21→22 填的是一样的，不再翻转；平均每条记录只有 3.7 条检查被标为"查过"，原来是 10 条以上。只有 3 条，只能当作现象。

- **开关**：`masked: false` 时，RANZCR 全部 214 个任务生成的 prompt，和原版 `visits.py`（`cc38323`）**逐字相同**，系统提示词也相同；用 1 个任务真跑了一遍，生成 4 条记录，缓存文件名和原来一样。`masked: true` 的检查结果和上面一致。

**没测的**：
- 完整的 RANZCR 第 5 步和 7 个比赛合跑，都没跑。
- 我们这边没装 `litellm`，冒烟测试时把 `common.call_model` 临时换成了 `openai` 客户端，访问的是同一个网关、同一个模型。你的 `call_model` 没有改动。

## 怎么重跑

**A. RANZCR，从第 5 步开始（推荐先做这个）**，复用你 11 月 4 日那次的第 1–4 步：

```bash
A=/你的/new_extraction/archive_old_runs/_per_competition_attempt/ranzcr-clip-catheter-line-classification/episode
O=out/pooled_episode_ranzcr_masked && mkdir -p $O
cp $A/1_topdown.json $A/2a_items.json $A/2b_bottomup.json $A/3_* $O/
cp $A/4_desiderata_base.json $O/4_desiderata_base.json
cp $A/4_desiderata_base.json $O/4_desiderata.json        # 从"第 5 步补充新检查之前"的检查单开始
# 可选：在 config.yaml 里设置 paths.notebooks
python run.py --comps ranzcr-clip-catheter-line-classification --suffix _ranzcr_masked --from 5
```

和旧结果对比（每次留出一位专家，比较"永远猜最常见 / 统计法 / LLM 猜的权重"）：

```bash
RUN_DIR=$A python ../../demo/blind_visit_pilot/blind_eval.py $O/5_visits.json
```

这里，旧记录按 `RUN_DIR` 读，新记录按参数读。新的 `5_visits.json` 格式和原来一样。

**B. 7 个比赛合跑，用新的归类门槛**：`run.py` 看到已有 `2b_bottomup.json` 就会跳过归类，所以要用一个新的后缀，从头跑：

```bash
python run.py --suffix _v2
```

## 花费（粗估，只算第 5 步第一轮；第二轮只重跑新增了检查的节点，另外再加）

| 设置 | RANZCR | 7 个比赛合跑 |
|---|---:|---:|
| `masked: false`（原写法） | 约 214 次，约 $10–15 | 约 2,900 次，约 $150–200 |
| `masked: true`，不带 notebook（默认） | 约 850 次，约 $20–25 | 约 12,000 次，约 $300 |
| `masked: true`，带 notebook | 约 850 次，约 $35 | 约 $500 |

- 按 Opus 4.6 估算。新写法每次约 $0.025，带 notebook 约 $0.04，后者是我们实测的。原写法每次调用的输入和输出都更长，约 $0.06。
- 新写法调用次数多了约 4 倍，但每次更短，所以总花费大约是原写法的 1.5–3 倍。
- 省钱的办法：
  - `stage_models.visits` 换成 Sonnet，约便宜 40%；
  - `visits.new_checks: false`，不跑第二轮；
  - 先用 `--n-experts 3` 小规模试。
- **建议先跑 RANZCR（新写法，不带 notebook），确认效果后再决定 7 个比赛怎么跑。**

## 相关材料（都在本仓库 `demo/` 下）

| 文件 | 内容 |
|---|---|
| `yaqing_files_walkthrough.md` | 按生成顺序看流水线的每个文件，用一个例子串起来 |
| `yaqing_pipeline_walkthrough.md` | 顺着一步（ttahara v34→35）走完整条流水线 |
| `yaqing_spotcheck_ranzcr.md` | 拿原始代码抽查 RANZCR 的 11 步 |
| `yaqing_example_normalization.md` | 归一化的例子：给答案时标注跟着专家的选择翻转 |
| `yaqing_fragmentation.md` | 零散的原因，以及用 TraceML 标签做动作层的统计 |
| `blind_visit_pilot/` | 遮住答案的对照实验：脚本、结果、评估。479 条记录上，遮住答案后预测专家选择的命中率是 36%，和"永远猜最常见"一样；给答案时是 44% |

## 想请你确认的

1. 11 月 4 日 RANZCR 单独那次运行，visit 是怎么读到原始代码的？现在的 `data.py` 只给摘要。
2. 为什么从第一版的"每一步 LLM 打意图标签"换成了"episode item 归类"？Sherry 的文档要的是前者，而 item 带来了两个问题：事后教训被当成动作，一步改了几件事只记一件。
