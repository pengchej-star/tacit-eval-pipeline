# 交接：Yaqing 的 new_extraction（2026-11-07，Pengcheng）

## 去哪里拿

仓库：<https://github.com/pengchej-star/tacit-eval-pipeline>，目录 `extraction/new_extraction/`。

```bash
git clone https://github.com/pengchej-star/tacit-eval-pipeline.git      # 已经 clone 过的话：git pull
cd tacit-eval-pipeline/extraction/new_extraction
cp -r /你的/new_extraction/data .        # data/ 和 out/ 都不在 git 里，从你自己的文件夹拷过来
cp /你的/new_extraction/.env .
```

**看具体改了什么**：一共两个提交。
- `cc38323`：你 11 月 4 日的代码原样拷贝，只有代码，不含 `data/`、`out/`、`archive_old_runs/`。
- `e3347ed`：我们的修改，4 个文件，+103/−43 行。

```bash
git diff cc38323 e3347ed -- extraction/new_extraction
```

网页版：<https://github.com/pengchej-star/tacit-eval-pipeline/compare/cc38323...e3347ed>。

如果你想继续用自己的文件夹，只要把这 4 个文件拷过去：`visits.py`、`prompts.py`、`data.py`、`config.yaml`。

## 改了什么（只改最必要的，其余逻辑不动）

| # | 改动 | 文件 | 为什么 |
|---|---|---|---|
| 1 | **第 5 步填检查单时遮住答案。** 不再给 LLM 看：选了哪个选项（`Taken:`）、这一步自己的 goal / labels / change summary、episode item 的文字。**每个（改动，路口）单独调用一次**，因为把整条路径列出来，会暴露上面每一层选了哪个选项。"选了哪个选项"仍由程序写进每条 visit record，后面的打分和汇总照常使用 | `visits.py`（`Ctx.prompt`、`make_jobs`、`run`）、`prompts.py`（新增 `VISIT_MASKED`、`NEW_CHECKS_RULE_MASKED`，原来的 `VISIT` 保留） | 我们的对照实验：同样的检查单，给不给答案，约 32% 的标注会变（不给答案的版本自己重跑只变 6%）。不给答案时，"标准值查得到"这类事实不再跟着专家的选择翻转。见 `demo/blind_visit_pilot/` |
| 2 | **第 0 层归类的门槛放宽**：`cluster.max_dist` 从 `[0.30, 0.60]` 改成 `[0.38, 0.60]`，仍然由 LLM 判断"是不是同一个动作" | `config.yaml` | 7 个比赛合跑时，35% 的 item 在 0.30 之内没有任何邻居，根本没有机会合并；而 LLM 对送去判断的配对 85% 都说"是同一个"。见 `demo/yaqing_fragmentation.md` |
| 3 | **检查单的顺序每次打乱**（按 step+node 固定随机种子） | `visits.py` | 原来的"先查什么"基本就是列表顺序：比如某个节点上 E07 在 18 次里都排第一，而它正好是列表的第一条 |
| 4 | **可选：给 LLM 看 v_old 那一版的 notebook**。设置 `paths.notebooks` 指向 TraceML `trajectories_human.tar.gz` 解压出来的 `human/` 文件夹（`<key_id>/versions/vNNN.ipynb`）即可；默认是 `null`，即不给 | `data.py`（`notebook_text()`）、`config.yaml`（`paths.notebooks`、`context.code_max`） | 只看一句话摘要信息太少，摘要也会漏东西，比如 ttahara v34→35 换了训练 checkpoint 这件事。你 11 月 4 日 RANZCR 那次的证据引用了 markdown 和 `model.eval()`，看起来当时是读到了代码的 |

**缓存文件换了新名字**：`5_visits_masked_r1.jsonl`、`5_visits_masked_r2.jsonl`、`4b_new_checks_masked.jsonl`。在旧的 out 目录里跑，也不会读到旧的、没遮答案的缓存。

**没有动的**：骨架、归类方法、挂到骨架、desiderata、新检查的合并、打分（仍然是 LLM 猜）、"查多少就够"、回头、稳定性检验、导出格式。用 TraceML 标签搭上两层、合并重复选项、修回头检测、加回"统计法"打分等，留给你下一次改代码时处理。具体建议见 `demo/yaqing_fragmentation.md` 和 `demo/yaqing_spotcheck_ranzcr.md`。

## 测试到什么程度

用你 11 月 4 日 RANZCR 单独那次运行的第 1–4 步结果做了冒烟测试：
- **只构建 prompt、不调用 API**：RANZCR 一共产生 850 个（改动，路口）任务，覆盖 214 次改动。抽查 3 个 prompt，都**没有** `Taken:`、这一步的 goal 和摘要、item 文字；检查顺序已打乱；notebook 代码已给出。
- **真调用**：用这 3 个任务把第 5 步完整跑了一遍（第一轮、合并新检查、第二轮），再跑了第 6–8 步和导出，全部正常。
- 这 3 条记录里，归一化那个路口的"标准值查得到"在 v16→17 和 v21→22 填的是一样的，不再翻转；平均每条记录只有 3.7 条检查被标为"查过"，原来是 10 条以上。只有 3 条，只能当作现象。

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

## 花费（粗估，按每次调用约 $0.04 算：Opus 4.6，带 notebook 时输入约 5.7k token；不带 notebook 会便宜一些）

- **A. RANZCR 第 5 步**：第一轮 850 次，第二轮只重跑新增了检查的节点，合计约 $35–70。
- **B. 7 个比赛**：按 RANZCR 每次改动约 3.6 个路口推算，第一轮约 12,000 次，**可能要 $400–600**，加上第二轮还更多。比你原来"一次改动一次调用"的写法贵 2–3 倍，因为现在每个路口单独问。

  省钱的办法：
  - `stage_models.visits` 换成 Sonnet；
  - `visits.new_checks: false`，不跑第二轮；
  - 先用 `--n-experts 3` 小规模试。

  建议先做 A，确认效果再决定 B。

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
