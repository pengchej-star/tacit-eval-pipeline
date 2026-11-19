# Change time-frequency resolution  `T.4.3.1`   8 edits, 0 experts
8 scored cases, median improvement +0.00807, 5 improved


- expert 50376011 (Grandmaster) · hms · v57→v58   Try adjusting the FFT window length (which controls frequency vs. time resolution trade-off) at inference to match what was used during training. If the parameter was not used during training, changing it at inference will create a train-test mismatch and hurt performance. Verify by submitting and c
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events.
    leaderboard score 0.34376 → 0.36034 (+0.01659)
- expert 49576186 (Expert) · hms · v12→v20   Test both high-frequency-resolution and low-frequency-resolution spectrogram settings with corresponding sampling rates. If the higher-resolution setting degrades the score on two separate attempts while the lower-resolution setting consistently performs better, commit to the lower-resolution settin
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events.
    leaderboard score 0.37612 → 0.41352 (+0.03740)
- expert 49576186 (Expert) · hms · v115→v125   Experiment with restricting the spectrogram to the informative frequency band (removing high-frequency noise) and try perceptually uniform colormaps instead of rainbow-type ones. Evaluate each change on the leaderboard or a robust validation split, as both frequency range and colormap can materially
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information.
    leaderboard score 0.27783 → 0.26861 (-0.00923)
- expert 49576186 (Expert) · hms · v166→v168   Replace the fragile GPU spectrogram with a well-tested CPU library's mel-spectrogram (log-scaled), which produces a perceptually-motivated and more compact frequency representation. Combine this change with training config adjustments (optimizer choice, mixed precision, early stopping) and evaluate 
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events.
    leaderboard score 0.28533 → 0.26603 (-0.01930)
- expert 50496431 (Grandmaster) · hms · v12→v15   Sweep the FFT window size and hop length in tandem, halving or doubling each relative to the baseline. Evaluate each combination on the target metric. Prefer shorter windows and shorter hops (higher time resolution) when the signal's discriminative patterns are transient, but verify with the metric 
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ The current crop omits relevant context or includes long irrelevant regions. | ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone. | ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.36527 → 0.40654 (+0.04127)
- expert 50496431 (Grandmaster) · hms · v47→v48   Change one spectrogram parameter at a time (e.g., double the FFT size) and submit to measure the effect. If the score worsens, revert and try a smaller perturbation or a different parameter. Always ensure inference-time spectrogram settings match or closely approximate those used during training.
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ The current crop omits relevant context or includes long irrelevant regions.
    leaderboard score 0.36464 → 0.37271 (+0.00807)
- expert 50496431 (Grandmaster) · hms · v48→v55   Sweep one or two spectrogram parameters per submission: clipping range, FFT size, window length, frequency band of the bandpass filter, and the log-scaling transform. Evaluate each on the leaderboard or validation metric. Tightening the clipping range to remove extreme outliers, narrowing the freque
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information. | ✓ The current crop omits relevant context or includes long irrelevant regions. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone.
    leaderboard score 0.37271 → 0.31212 (-0.06059)
- expert 50496431 (Grandmaster) · hms · v57→v60   When probing spectrogram parameters at inference time, keep changes small and revert if the score worsens. If the pretrained weights were trained with a particular FFT size, match that size at inference rather than increasing it, because the model's learned filters expect the original resolution.
    evidence: ✓ Current time-frequency bins merge potentially informative frequencies or time events. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ An available raw or transformed modality contains information absent from the active branch.
    leaderboard score 0.30899 → 0.31262 (+0.00364)