# ranzcr · opus · cheatsheet

run ranzcr__claude__claude-opus-5-5__memory__30min__j11280927; 22 steps; best 0.9595 (higher is better); final 0.9595

Knowledge the agent reports using (from the cheatsheet):
- T.4.3: T.4.3.4 Change input scaling and rendering (applied): Read attention file; chose high-res grayscale (448px, 1 channel) input since catheter tips are thin structures; cached resized arrays for speed.
- T.7.1: T.7.1 Prune or restore members by ablation / Add a complementary model (applied): Added 2nd and 3rd EffNetV2-S runs (different schedules); kept each member only if holdout mean AUC of the blend improved (ablation).

-   0.0 min · step   1 · READS CHEATSHEET: `cd /kaggle/input/ranzcr-clip-catheter-line-classification; ls; head -3 sample_submission.csv; ls train | head -3; ls train | wc -l; ls test | wc -l; nvidia-smi `
-   0.0 min · step   2 · READS CHEATSHEET: `head -c 3000 /workspace/memory/taxonomy.md; ls /workspace/memory/attention | head -50`
-   0.9 min · step   3 · READS CHEATSHEET: `head -c 1500 /workspace/memory/attention/t-4-3-change-signal-or-image-representation.md; ls /workspace/memory/cases | grep t-4-3; head -2 /kaggle/input/ranzcr-c`
-   1.1 min · step   4 · ERROR (call took 0.0 min): 
-   1.4 min · step   6 · says: Preprocessing is running: test is cached at 448px and train is in progress. Next I'm writing the training script: EfficientNetV2-S, grayscale input, patient-grouped holdout, bf16.
-   2.9 min · step   9 · says: Throughput is about 41s per epoch at 448px. Train caching is still running.
-   7.6 min · step  11 · says: Train is cached. With about 20 minutes left, I'm starting an 11-epoch EfficientNetV2-S run.
-   9.3 min · step  12 · says: Each epoch takes about 56s. I'm writing a fallback submission from label priors in the meantime.
-   9.3 min · step  13 · SUBMISSION 0.5  (new best)
-  15.8 min · step  15 · SUBMISSION 0.95235  (new best)
-  16.0 min · step  15 · says: I trained one model, and its predictions are now the submission at `/kaggle/working/submission.csv`. It scores **0.943 mean AUC** on a 10% holdout of the training data, with no patient appearing in both the training and holdout parts. The file has all 3,009 test rows and 12 columns, with no missing values.  - **Model:** EfficientNetV2-S, pretrained on ImageNet. It takes the X-rays as single-channe
-  16.1 min · step  15 · says: About 14 minutes are left. The first run peaked around epoch 7, so I'm training a second model with an 8-epoch schedule (about 6 minutes). I'll average it with the first and check the blend on the same holdout.
-  22.2 min · step  19 · SUBMISSION 0.95815  (new best)
-  22.4 min · step  19 · says: The submission now blends two models, and the blend scores **about 0.952 mean AUC** on the holdout, up from 0.943 for the first model alone.  - **Second model:** the same EfficientNetV2-S setup on a shorter 8-epoch schedule. It reached 0.9504 at epoch 6 and ended at 0.9499, so it beats the first model's 0.9433 on its own. - **Blend:** I checked a few fixed weights on the holdout: 0.9499 for the se
-  22.5 min · step  19 · says: About 8 minutes are left. A 6-epoch run takes about 5 minutes including test prediction, so I'm starting a third model now and will add it to the blend only if the holdout score improves.
-  22.5 min · step  20 · READS CHEATSHEET: `cd /workspace; nohup python train.py 6 tf_efficientnetv2_s.in21k_ft_in1k c > c.log 2>&1 & head -c 1200 /workspace/memory/attention/t-7-1-change-ensemble-members`
-  22.5 min · step  20 · says: The ensemble guidance says to check by ablation whether each member actually helps, so I'll compare blends with and without the new model on the holdout.
-  27.2 min · step  22 · SUBMISSION 0.9595  (new best)
-  27.3 min · step  22 · says: The submission now averages three models and scores **0.9536 mean AUC** on the holdout, up from 0.9517 for the two-model blend and 0.943 for the original single model.  - **Third model:** the same EfficientNetV2-S setup on a 6-epoch schedule. It reached 0.9493 on its own, close to the second model's 0.9499. - **Checking each model earns its place:** I scored blends with and without each member on 
