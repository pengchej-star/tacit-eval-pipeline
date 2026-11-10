# 抽查：Yaqing 流水线在 RANZCR 上的 visit record 靠不靠谱

对象是 11 月 4 日只跑 RANZCR 的那次完整运行（`archive_old_runs/_per_competition_attempt/ranzcr-clip-catheter-line-classification/episode/`）。
挑了 3 位我们跑过的专家的 11 步：ttahara（13848868）、kanruwang（15164527）、archanabenur（15173072）。
每一步把原始 notebook 的真实 diff 和流水线的结果对照：这一步被归成了什么动作、挂在哪个节点、visit record 的证据。
引用的分数都和 `data/scores.json` 核对过。生成对照的脚本是 `show_step.py`（在 scratchpad 里，未提交）。

## 逐步结果

| 步 | 真实改动 | 流水线归成的动作 | 动作对不对 | 证据 |
|---|---|---|---|---|
| ttahara v34→35 | 分辨率 640→512；排名转换关掉；换了新训练版本 | sweep inference resolution | 对，但"关排名"那一半丢了 | 对，能指出"分辨率和换 checkpoint 同时发生，没法单独归因" |
| ttahara v10→11 | 分辨率 448→512；换 checkpoint；关排名；去掉 head 里的层 | ① Larger input resolution ② **Isolate single variables per submission** | ① 对 ② **错**：这是事后总结的教训，专家这一步恰恰是一次改了 4 处 | 对，正确识别出"打包改动" |
| ttahara v18→19 | backbone ResNeXt → RegNetY032；关排名 | ① **Simplify classification head** ② 重新比较排名/原始概率 | ① **错**：实际是换 backbone ② 对 | 数字都对；一处推理说反了（把 0.94330 > 0.94301 说成原始概率更好），但结论仍然成立 |
| ttahara v22→23 | 新的 Spatial-Attention 多头结构；backbone 换回 ResNeXt；关排名；换 checkpoint | Substitute and benchmark alternative attention block | 部分对：换 backbone、改回多头没体现 | 对 |
| ttahara v36→37 | 权重换成 640 训练的 v2；分辨率 512→640；关排名 | Align inference resolution with training resolution | 对（关排名又丢了） | 对。但被第 8 步算成一次"回头"，见下文问题 3 |
| kanruwang v23→24 | 注释掉其它模型，只用一折；分数 0.968 → 0.613 | Evaluate individual fold contributions | 对 | 对 |
| kanruwang v28→29 | `fold_id == 2` 改成 `== 3` | Evaluate individual fold contributions | 对 | 对（引用的各折分数都对） |
| kanruwang v43→44 | 恢复所有模型的推理和融合 | ① Reassemble verified ensemble components ② Add debugged model to rank-based ensemble | 对 | 对 |
| archanabenur v7→8 | 取消注释 `model.eval()`；换 checkpoint 文件；0.510 → 0.556 | Fix model evaluation mode and checkpoint loading | 对 | 对 |
| archanabenur v16→17 | 归一化均值从一组手调值换成另一组手调值 | Align inference normalization with training statistics | 节点对，名字有误导：实际是在乱试，不是"对齐" | 对，证据里说的是"trial-and-error probing" |
| archanabenur v21→22 | 归一化改回 ImageNet 标准值；加了第二个模型做融合 | ① Match normalization to pretrained backbone statistics ② Simple averaging | 对 | 对 |

**汇总**：11 步里，动作归类 7 步对，2 步部分对，2 步错。证据里引用的分数、代码细节全部对得上，只有 1 处推理说反了。

## 发现的问题

1. **一步改了几件事时，经常漏掉一部分。** 11 步里有 7 步同时改了不止一件事，只有 2 步把每件事都记下来了。最常丢的是"排名转换开/关"：它被单独写成一条 item，只分给了别的步骤。这就是 Yaqing 问的"一步多个动作怎么办"，而且它确实在丢信息。
2. **事后教训被当成了专家当时的选择。** item 是 LLM 回看整个 episode 后写的，里面会有"本该一次只改一个变量"这种总结。流水线把它当成一个动作，于是 visit record 说专家在 v10→11"选了每次只改一个变量"，而专家其实是一次改了 4 处。
3. **重复的选项会制造假的"回头"。** "扫推理分辨率"和"推理分辨率对齐训练分辨率"在树上是两个兄弟选项，其实是一回事。ttahara 先做了前者（v34→35），再做了后者（v36→37），第 8 步就把这记成了一次"回头"。
4. **visit 记下的大多是"当时成立的事实"，而不是"专家看了什么"。** 例如"比赛指标是 AUC""胸片和 ImageNet 照片分布不同""提交次数还够"，这些几乎每一步都是 yes。真正决定选择的证据（比如"上次改动后分数掉了"）混在一大堆恒为 yes 的检查里，一次常常有 10 条以上被标成"查过了"。这会让"先查什么、查多少就够"失去意义。
5. **这次运行看到了原始代码。** 证据里引用了 markdown 链接、`model.eval()` 等只在代码里出现的内容，所以证据才这么准。现在的代码只给 LLM 看 TraceML 的一句话摘要，按现在的代码跑，证据会少很多，问题 1 也会更严重（摘要本身就漏东西，比如 v34→35 换训练版本这件事）。需要找 Yaqing 确认。

## 顺带发现：我们自己文档里的一个错误

10 月 30 日的 pivot 说明写的是"ranzcr 15173072：agent 做了和专家 v17 相同的归一化修正"。实际上专家的 v17 只是换了一组手调的均值，**直到 v22 才改回 ImageNet 标准值**。已在 `docs/agent_pivots_2026-10-30.md` 里改正。上周 slide 的演讲者备注里也有同样的说法。
