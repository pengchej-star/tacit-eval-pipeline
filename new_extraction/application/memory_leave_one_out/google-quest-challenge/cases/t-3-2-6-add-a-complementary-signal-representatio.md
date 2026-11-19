# Add a complementary signal representation  `T.3.2.6`   11 edits, 0 experts
10 scored cases (improvement signed by each competition's direction), median +0.02304, 7 improved


- expert 49576186 · hms · v2→v4   Add a 1D convolutional branch that processes the raw time-series in parallel with the spectrogram branch. Also switch normalization from per-patch to per-sample scope, and verify the bandpass filter design matches the frequency range of interest. Expect a meaningful but not dramatic first-step gain.
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✗ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.42923 → 0.40619 (lower is better; improved by 0.02304)
- expert 49576186 · hms · v7→v12   Fix the window extraction to use the correct sampling rate, increase the number of derived input channels, and add per-sample normalization. After making these changes, retrain or load updated checkpoints and compare the leaderboard score. If the score does not improve, the additional channels or no
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score n/a → 0.37612 (lower is better)
- expert 49576186 · hms · v38→v41   Test a small range of channel counts (fewer and more than the current default) while keeping other settings fixed. If both increasing and decreasing the channel count worsen the score, the current count is likely near-optimal. Avoid assuming more channels always help—redundant or noisy channels can 
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.38150 → 0.39003 (lower is better; worse by 0.00853)
- expert 49576186 · hms · v95→v100   Add the new modality behind a feature flag, submit quickly to measure impact, and if the score degrades, disable the modality while keeping the code infrastructure for future experiments. Ensure that data assembly (e.g., concatenation) is guarded by the flag so removing the modality doesn't leave de
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.32367 → 0.27844 (lower is better; improved by 0.04522)
- expert 49576186 · hms · v181→v183   Create a parallel input branch from the same raw signal but with different temporal sampling, window length, or frequency resolution. Give it its own convolutional feature extractor and merge its embeddings with the existing branches before the classification head. Evaluate on the leaderboard to con
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.27700 → 0.25555 (lower is better; improved by 0.02145)
- expert 52551258 · hms · v18→v19   Derive the new channels, add appropriate normalization (e.g., robust statistics, clipping), train or load a model that accepts the expanded input, and include it in the ensemble. If the leaderboard score worsens, the new component may be adding noise or the model checkpoint may not be well-calibrate
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.28137 → 0.28876 (lower is better; worse by 0.00739)
- expert 53762022 · hms · v8→v9   Refactor the data and feature pipeline: add domain-appropriate signal preprocessing (e.g., filtering, derived features), switch to a grouped stratified cross-validation scheme that respects the data's group structure, and rebuild the out-of-fold and inference flow before returning to ensemble tuning
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.68408 → 0.36230 (lower is better; improved by 0.32178)
- expert 50496431 · hms · v8→v10   Train a separate model on the second modality with its own preprocessing pipeline and checkpoints. Ensemble predictions from both modality-specific models by simple averaging. Expect the cross-modal ensemble to yield a substantially larger gain than within-modality tricks, because the modalities pro
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✗ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.42196 → 0.36955 (lower is better; improved by 0.05241)
- expert 50496431 · hms · v109→v111   Try multiple reshape configurations that trade off the two spatial dimensions (e.g., more time steps along width vs. more channels along height). Evaluate each by submitting or validating, and test the interaction with other ensemble members since a reshape that is suboptimal alone may still contrib
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.27038 → 0.25772 (lower is better; improved by 0.01266)
- expert 50496431 · hms · v111→v115   Try several height×width factorizations of the same total length, keeping the longer axis aligned with the primary signal dimension (e.g., time). Evaluate each on a held-out metric. Small changes in aspect ratio can cause large score swings, so test at least 3–4 factorizations before settling.
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.25772 → 0.27768 (lower is better; worse by 0.01995)
- expert 50496431 · hms · v215→v216   Add the extra channels, update the model's input reshape/dimension accordingly, and evaluate. If the gain is visible in isolation but the overall ensemble doesn't improve, the extra channels may help only specific model variants; test them selectively rather than applying globally.
    evidence: ✓ Available signal channels or temporal resolutions are not represented by the current inputs.
    leaderboard score 0.26249 → 0.23945 (lower is better; improved by 0.02304)