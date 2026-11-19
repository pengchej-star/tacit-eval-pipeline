# Select input branches by ablation  `T.3.2.7`   9 edits, 0 experts
7 scored cases (improvement signed by each competition's direction), median +0.00429, 5 improved


- expert 50376011 · hms · v21→v22   Run inference once with the auxiliary channel enabled and once without, comparing leaderboard or validation scores. If disabling it matches or improves the score, drop it to reduce complexity and potential noise. Even a tiny improvement justifies removal because it also simplifies the pipeline.
    evidence: ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.39943 → 0.39939 (lower is better; improved by 0.00003)
- expert 49576186 · hms · v41→v48   After two or three cycles of adding and removing the branch with no improvement, abandon the new modality and redirect effort to fixing existing architecture issues (tensor shapes, concatenation axes, input dimensions) which are more likely to yield gains.
    evidence: ✓ Several trained input branches exist and one may add little or harmful information. | ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.39003 → 0.38574 (lower is better; improved by 0.00429)
- expert 49576186 · hms · v66→v70   Remove the underperforming branch and instead invest the computational budget in improving the quality of existing inputs (higher resolution, better filtering, correct time-window alignment). A simpler model with higher-fidelity inputs often outperforms a more complex model with redundant or noisy a
    evidence: ✓ Several trained input branches exist and one may add little or harmful information. | ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.44543 → 0.35346 (lower is better; improved by 0.09197)
- expert 49576186 · hms · v109→v113   Test single-modality ablations by disabling other input branches. If the score degrades substantially, the dropped modalities carry complementary information and should be retained. Revert quickly if the ablation shows a large regression.
    evidence: ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.27616 → 0.35418 (lower is better; worse by 0.07802)
- expert 49576186 · hms · v113→v125   Restore all modalities, then systematically refine the spectrogram branch (windowing function, FFT size, frequency range, colormap for rendered spectrograms) and the cross-validation split strategy (pure group-based instead of stratified). Change one or two preprocessing details per iteration and su
    evidence: ✓ Several trained input branches exist and one may add little or harmful information. | ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.35418 → 0.26861 (lower is better; improved by 0.08558)
- expert 49576186 · hms · v133→v138   Run a systematic ablation: remove one modality at a time and score each variant on the leaderboard or a held-out set. If every removal hurts, keep all modalities. If removing one improves or is neutral, drop it to reduce complexity. Compare each ablation against the full-modality baseline, not again
    evidence: ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.28049 → 0.31300 (lower is better; worse by 0.03251)
- expert 49576186 · hms · v138→v144   Test the single-modality ablation, but if the score regresses substantially, immediately restore all modalities. Treat the ablation as a diagnostic, not a permanent simplification. Gains are more likely from adding or refining modalities than from removing them once the fusion is working.
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.31300 → 0.28850 (lower is better; improved by 0.02450)
- expert 52200959 · hms · v11→v16   Add an out-of-fold cross-validation loop to the inference notebook that computes the competition metric locally. Iterate through each composite variant one at a time, comparing CV scores before committing to a leaderboard submission. Use a dictionary mapping variant names to checkpoint versions so s
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.41926 → n/a (lower is better)
- expert 52200959 · hms · v19→v23   Submit each variant alone in a quick sweep (one submission per variant, changing only the variant identifier). Record each variant's leaderboard score, then use those scores as inverse-error weights when blending all variants into a final ensemble.
    evidence: ✓ Several trained input branches exist and one may add little or harmful information. | ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score n/a → 0.36365 (lower is better)