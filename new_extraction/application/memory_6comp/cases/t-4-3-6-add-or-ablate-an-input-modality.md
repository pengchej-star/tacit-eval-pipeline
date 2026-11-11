# Add or ablate an input modality  `T.4.3.6`   18 edits, 0 experts
16 scored cases, median improvement -0.00966, 4 improved


- expert 49576186 (Expert) · hms · v2→v4   Add a 1D convolutional branch that processes the raw time-series in parallel with the spectrogram branch. Also switch normalization from per-patch to per-sample scope, and verify the bandpass filter design matches the frequency range of interest. Expect a meaningful but not dramatic first-step gain.
    evidence: ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.42923 → 0.40619 (-0.02304)
- expert 49576186 (Expert) · hms · v181→v183   Create a parallel input branch from the same raw signal but with different temporal sampling, window length, or frequency resolution. Give it its own convolutional feature extractor and merge its embeddings with the existing branches before the classification head. Evaluate on the leaderboard to con
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.27700 → 0.25555 (-0.02145)
- expert 49576186 (Expert) · hms · v66→v70   Remove the underperforming branch and instead invest the computational budget in improving the quality of existing inputs (higher resolution, better filtering, correct time-window alignment). A simpler model with higher-fidelity inputs often outperforms a more complex model with redundant or noisy a
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.44543 → 0.35346 (-0.09197)
- expert 50376011 (Grandmaster) · hms · v21→v22   Run inference once with the auxiliary channel enabled and once without, comparing leaderboard or validation scores. If disabling it matches or improves the score, drop it to reduce complexity and potential noise. Even a tiny improvement justifies removal because it also simplifies the pipeline.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.39943 → 0.39939 (-0.00003)
- expert 49524919 (Grandmaster) · hms · v53→v54   Before adding a second model family for ensembling, first clean the codebase: remove dead inference paths, centralize configuration, and ensure the surviving pipeline is modular. This makes it straightforward to add a second model's predictions and combine them via stacking or averaging in the next 
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.42162 → 0.41624 (-0.00538)
- expert 49576186 (Expert) · hms · v38→v41   Test a small range of channel counts (fewer and more than the current default) while keeping other settings fixed. If both increasing and decreasing the channel count worsen the score, the current count is likely near-optimal. Avoid assuming more channels always help—redundant or noisy channels can 
    evidence: ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone. | ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.38150 → 0.39003 (+0.00853)
- expert 49576186 (Expert) · hms · v41→v48   After two or three cycles of adding and removing the branch with no improvement, abandon the new modality and redirect effort to fixing existing architecture issues (tensor shapes, concatenation axes, input dimensions) which are more likely to yield gains.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone.
    leaderboard score 0.39003 → 0.38574 (-0.00429)
- expert 49576186 (Expert) · hms · v95→v100   Add the new modality behind a feature flag, submit quickly to measure impact, and if the score degrades, disable the modality while keeping the code infrastructure for future experiments. Ensure that data assembly (e.g., concatenation) is guarded by the flag so removing the modality doesn't leave de
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.32367 → 0.27844 (-0.04522)
- expert 49576186 (Expert) · hms · v109→v113   Test single-modality ablations by disabling other input branches. If the score degrades substantially, the dropped modalities carry complementary information and should be retained. Revert quickly if the ablation shows a large regression.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.27616 → 0.35418 (+0.07802)
- expert 49576186 (Expert) · hms · v113→v125   Restore all modalities, then systematically refine the spectrogram branch (windowing function, FFT size, frequency range, colormap for rendered spectrograms) and the cross-validation split strategy (pure group-based instead of stratified). Change one or two preprocessing details per iteration and su
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information.
    leaderboard score 0.35418 → 0.26861 (-0.08558)
- expert 49576186 (Expert) · hms · v133→v138   Run a systematic ablation: remove one modality at a time and score each variant on the leaderboard or a held-out set. If every removal hurts, keep all modalities. If removing one improves or is neutral, drop it to reduce complexity. Compare each ablation against the full-modality baseline, not again
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.28049 → 0.31300 (+0.03251)
- expert 49576186 (Expert) · hms · v138→v144   Test the single-modality ablation, but if the score regresses substantially, immediately restore all modalities. Treat the ablation as a diagnostic, not a permanent simplification. Gains are more likely from adding or refining modalities than from removing them once the fusion is working.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.31300 → 0.28850 (-0.02450)
- expert 52551258 (Expert) · hms · v19→v21   First verify the new-modality model works standalone at a reasonable level before adding it to the ensemble. If standalone performance is far below the existing baseline, do not replace existing models; instead add the new modality alongside existing ones so the ensemble can benefit from complementa
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.28876 → 0.33979 (+0.05102)
- expert 52551258 (Expert) · hms · v21→v22   Never remove the existing strong models when testing a new modality. Add the new modality's predictions to the existing ensemble so the incremental effect can be measured cleanly. If the combined score regresses or barely improves, the new modality needs further tuning before inclusion.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.33979 → 0.29324 (-0.04655)
- expert 49576186 (Expert) · hms · v70→v76   Add the new modality as a separate input branch, ensure per-sample grouping and target normalization are consistent across modalities, set deterministic seeds for reproducibility, and restore proven preprocessing parameters (e.g., resolution) that may have been inadvertently changed. If intermediate
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.35346 → 0.34054 (-0.01292)
- expert 52200959 (Master) · hms · v11→v16   Add an out-of-fold cross-validation loop to the inference notebook that computes the competition metric locally. Iterate through each composite variant one at a time, comparing CV scores before committing to a leaderboard submission. Use a dictionary mapping variant names to checkpoint versions so s
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.41926 → n/a
- expert 52200959 (Master) · hms · v19→v23   Submit each variant alone in a quick sweep (one submission per variant, changing only the variant identifier). Record each variant's leaderboard score, then use those scores as inverse-error weights when blending all variants into a final ensemble.
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score n/a → 0.36365
- expert 52200959 (Master) · hms · v26→v32   Build a 1D convolutional + recurrent model that processes the raw time-series directly, with domain-appropriate preprocessing (bandpass filtering, pairwise channel differences). Iterate in stages: first get the architecture running, then refine feature engineering and activations, then simplify infe
    evidence: ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone. | ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.34131 → 0.33165 (-0.00966)