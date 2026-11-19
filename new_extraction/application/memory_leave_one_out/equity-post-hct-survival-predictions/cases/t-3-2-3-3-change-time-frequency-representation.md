# Change time-frequency representation  `T.3.2.3.3`   12 edits, 0 experts
12 scored cases (improvement signed by each competition's direction), median -0.00364, 5 improved


- expert 50376011 · hms · v57→v58   Try adjusting the FFT window length (which controls frequency vs. time resolution trade-off) at inference to match what was used during training. If the parameter was not used during training, changing it at inference will create a train-test mismatch and hurt performance. Verify by submitting and c
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.34376 → 0.36034 (lower is better; worse by 0.01659)
- expert 49576186 · hms · v12→v20   Test both high-frequency-resolution and low-frequency-resolution spectrogram settings with corresponding sampling rates. If the higher-resolution setting degrades the score on two separate attempts while the lower-resolution setting consistently performs better, commit to the lower-resolution settin
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.37612 → 0.41352 (lower is better; worse by 0.03740)
- expert 49576186 · hms · v22→v24   Apply a standard colormap (e.g., jet) to map scalar spectrogram values to 3-channel RGB, then feed to the pretrained backbone. Compare against the baseline input format on the leaderboard or validation. Be aware this may not help and can even hurt if the original channel encoding already carries use
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.36216 → 0.37436 (lower is better; worse by 0.01220)
- expert 49576186 · hms · v115→v125   Experiment with restricting the spectrogram to the informative frequency band (removing high-frequency noise) and try perceptually uniform colormaps instead of rainbow-type ones. Evaluate each change on the leaderboard or a robust validation split, as both frequency range and colormap can materially
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.27783 → 0.26861 (lower is better; improved by 0.00923)
- expert 49576186 · hms · v166→v168   Replace the fragile GPU spectrogram with a well-tested CPU library's mel-spectrogram (log-scaled), which produces a perceptually-motivated and more compact frequency representation. Combine this change with training config adjustments (optimizer choice, mixed precision, early stopping) and evaluate 
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.28533 → 0.26603 (lower is better; improved by 0.01930)
- expert 49576186 · hms · v166→v168   Instead of continuing to iterate on augmentation details, make a qualitative change to the input representation itself (e.g., switching the spectral transform type or scaling). Bundle it with aligned training configuration changes and evaluate. A representation-level change can unlock gains that aug
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.28533 → 0.26603 (lower is better; improved by 0.01930)
- expert 50496431 · hms · v12→v15   Sweep the FFT window size and hop length in tandem, halving or doubling each relative to the baseline. Evaluate each combination on the target metric. Prefer shorter windows and shorter hops (higher time resolution) when the signal's discriminative patterns are transient, but verify with the metric 
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Unused channels or modalities contain potentially complementary information, or existing branches may be redundant. | ✓ The input window includes irrelevant context or misses the labeled interval or region.
    leaderboard score 0.36527 → 0.40654 (lower is better; worse by 0.04127)
- expert 50496431 · hms · v17→v18   Generate a different spectrogram variant (e.g., mel-spectrogram vs. STFT spectrogram) from the raw signals, precompute and cache the results, train or load additional backbone architectures on this new representation, and blend their predictions into the existing ensemble. Diversity in both input re
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.34713 → 0.34209 (lower is better; improved by 0.00504)
- expert 50496431 · hms · v47→v48   Change one spectrogram parameter at a time (e.g., double the FFT size) and submit to measure the effect. If the score worsens, revert and try a smaller perturbation or a different parameter. Always ensure inference-time spectrogram settings match or closely approximate those used during training.
    evidence: ✓ The input window includes irrelevant context or misses the labeled interval or region. | ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.36464 → 0.37271 (lower is better; worse by 0.00807)
- expert 50496431 · hms · v48→v55   Sweep one or two spectrogram parameters per submission: clipping range, FFT size, window length, frequency band of the bandpass filter, and the log-scaling transform. Evaluate each on the leaderboard or validation metric. Tightening the clipping range to remove extreme outliers, narrowing the freque
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation. | ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ The input window includes irrelevant context or misses the labeled interval or region.
    leaderboard score 0.37271 → 0.31212 (lower is better; improved by 0.06059)
- expert 50496431 · hms · v57→v60   When probing spectrogram parameters at inference time, keep changes small and revert if the score worsens. If the pretrained weights were trained with a particular FFT size, match that size at inference rather than increasing it, because the model's learned filters expect the original resolution.
    evidence: ✓ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score 0.30899 → 0.31262 (lower is better; worse by 0.00364)
- expert 50496431 · hms · v202→v204   Do not change spectrogram preprocessing parameters (window size, log transforms, normalization) at inference unless the model is retrained with the new settings. Even small mismatches between training and inference preprocessing cause large score regressions. Test one parameter at a time and revert 
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation. | ✓ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Unused channels or modalities contain potentially complementary information, or existing branches may be redundant.
    leaderboard score 0.22738 → 0.34797 (lower is better; worse by 0.12060)