# Change signal-to-image layout  `T.4.5.8`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.01266, 1 improved


- expert 50496431 · hms · v109→v111   Try multiple reshape configurations that trade off the two spatial dimensions (e.g., more time steps along width vs. more channels along height). Evaluate each by submitting or validating, and test the interaction with other ensemble members since a reshape that is suboptimal alone may still contrib
    evidence: ✓ An arbitrary signal-to-image factorization creates implausible local neighborhoods. | ✓ A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated.
    leaderboard score 0.27038 → 0.25772 (lower is better; improved by 0.01266)
- expert 50496431 · hms · v111→v115   Try several height×width factorizations of the same total length, keeping the longer axis aligned with the primary signal dimension (e.g., time). Evaluate each on a held-out metric. Small changes in aspect ratio can cause large score swings, so test at least 3–4 factorizations before settling.
    evidence: ✓ An arbitrary signal-to-image factorization creates implausible local neighborhoods. | ✓ The resolution-score curve from prior probes is non-monotonic or has an identified peak region, guiding the next resolution to test. | ✓ A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated.
    leaderboard score 0.25772 → 0.27768 (lower is better; worse by 0.01995)