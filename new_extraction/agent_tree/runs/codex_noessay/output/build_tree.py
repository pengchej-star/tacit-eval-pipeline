import json, collections
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
X=[]
for line in (BASE/'episode_items.jsonl').open():
 e=json.loads(line)
 for k,x in enumerate(e['items'],1): X.append({'id':f"{e['ep_id']}#{k}",**x})
A={}
def put(code, nums):
 for token in nums.split():
  ns=range(int(token.split('-')[0]),int(token.split('-')[1])+1) if '-' in token else [int(token)]
  for n in ns:
   assert n not in A,(n,A.get(n),code)
   A[n]=code
# Assign by the principal reusable intervention, not incidental implementation words.
put('rank','0 3 8 10 12 14 16 18 20 423 481 538 540 572 605 644 647 649 659 1125 1138')
put('resolution','1 4 15 17 1107 1151 1162 1163 1170 1177 1180 1182')
put('head','2 11 13 358 386 396 759 1004 1096')
put('headsimple','9 403 753 994')
put('revert','5 7 174 176 285 344 352 371 414 429 449 461 493 502 539 613 614 633 635 797 810 901 963 969 977 978 984 1046 1072 1117 1245 1266 1269 1288 1289 1297')
put('isolate','6 54 76 82 86 89 92 95 97 122 143 151 169 196 265 291 343 406 410 417 428 439 448 528 561 577 634 637 654 656 657 658 662 664 701 742 746 757 788 830 836 859 895 918 970 974 976 993 1018 1040 1051 1061 1065 1071 1155 1157 1201 1219 1221 1243 1244 1250 1257 1262 1268 1276 1278 1281 1283 1286 1295 1308')
put('pretrain','19 201 342 350 653 968 1024')
put('weights','21 24 32 109 144 177 206 214 215 224 225 228 259 264 268 274 290 298 300 309 313 345 346 357 370 377 381 422 427 432 436 473 475 483 497 501 503 504 505 527 530 552 567 595 597 640 706 771 772 776 777 801 815 888 914 928 931 936 1062 1070 1073 1074 1075 1083 1084 1090 1091 1126 1130 1140 1141 1142 1247 1264 1267 1284 1290 1299 1301 1310 1311')
put('negative','22 466 610')
put('nativeapi','23 180')
put('pivot','25 30 31 33 64 222 234 255 287 319 363 438 478 508 509 554 557 568 626 692 902 909 972 1011 1085 1095 1131 1134 1187 1188')
put('smoke','26 59 68 74 101 111 118 164 194 212 257 315 353 452 629 691 705 744 755 891 962 997 1093 1119 1193')
put('fulldata','27 29 699 700')
put('treecapacity','28 56 79 91 112 142 146 179 184 496 587')
put('repeat','34 55 149 305 408 511 783 804 811 820 821 823 829 834 839 840 843 849 850 851 853 854 855 856 857 864 871 872 875 882 885 1025 1169 1172 1174 1176 1179 1181 1183 1186 1210 1218 1226 1265 1270 1272 1292')
put('fast','35 39 41 66 141 155 156 191 193 584 628 668 669 803')
put('outputlink','36 100 444 537 549 551 1149')
put('chunks','37 102 116 128 161 163')
put('classweight','38 103 183 195')
put('importance','40 44 46 48 115 132 133 166 187 189 190')
put('penalty','42 43 57 65 114')
put('search','45 420 617 627')
put('custommetric','47 49 127 145 152 159')
put('subsample','50')
put('lrrounds','51 53 93 113 140 1191')
put('featureablate','52 62 77 119 121 126 186 395 498 535 687 778')
put('metricbug','58 104 107 153')
put('loss','60 546 754 980 1190')
put('booster','61 94 131 192')
put('duration','63 608 684 708')
put('aggsimple','67 110 178')
put('aggrich','69 124 134 150 170 175 185')
put('calendar','70 75')
put('nativenan','71 171 173 589')
put('lags','72 81 87')
put('quantizeinput','73 105')
put('interact','78 83 90 586')
put('config','80 125 223 387 424 474 779 842 878 910 911 958 1081 1103 1184 1199')
put('schemabug','84 99 220 251 328 394 456 522 529 544 547 579 592 630 704 718 720 722 723 929 933 935 939 947 951 1027 1077 1088 1166 1197 1214 1215')
put('windows','85 930 1207 1246 1252 1275')
put('backend','88 167 168 500 569 578 1006 1175')
put('family','96 477 479 523 564 1086 1216')
put('stack','98 108 208 210 211 213 217 230 246 261 385 598 609')
put('members','106 197 200 203 204 205 227 238 242 243 245 258 260 263 272 275 278 279 281 284 293 294 296 297 304 306 308 312 329 333 339 349 351 354 356 365 367 368 369 372 375 379 384 390 399 407 464 465 476 484 488 489 510 516 521 531 532 533 536 543 553 555 562 575 576 580 588 596 603 618 624 648 677 709 732 747 768 790 792 800 806 807 808 814 816 819 827 832 835 844 847 852 861 862 863 867 869 870 880 881 883 884 921 923 927 932 937 941 942 943 945 948 952 953 954 955 956 1026 1029 1033 1034 1036 1041 1048 1052 1055 1056 1058 1059 1063 1066 1067 1069 1078 1079 1114 1132 1136 1139 1167 1195 1198 1205 1208 1217 1220 1248 1253 1258 1259 1271 1273 1282 1285')
put('dataframeapi','160 271 397 1121')
put('patience','120 148')
put('memory','123 229 231 233 269 383 515 601 698 1120 1124')
put('folds','117 129 135 139 181 216 237 239 249 273 310 360 419 499 666 688 721 724 763 818 822 841 848 858 868 876 879 886 887 964 1100 1112 1123 1192')
put('seeds','130 136 361 393 401 404 405 412 446 447 453 454 459 463')
put('dropmissing','137')
put('cache','138 321 335 430 434 469 670 770 987 1211 1213')
put('proxy','172 188')
put('eda','154')
put('refactor','157 162 165 262 282 337 340 347 440 441 442 520 602 623 638 694 784 789 794 866 873 938 995 981 1037 1068 1076 1092')
put('validation','158 182 336 518 999 1080')
put('cvtrust','198 202 253 1094 1097 1105')
put('textlength','199 652')
put('larger','207 301 341 798 799 890 899 906 917 919 1106 1263')
put('hierarchy','209 226 241 254 318 604 734')
put('stackfeatures','218 248 252 322 326 332 388 600 616 697')
put('checkpoint','219 221 307 359 366 415 625 643 645 651 655 713 714 726 745 795 817 831 845 889 892 898 913 915 944 949 985 990 1012 1015 1016 1020 1023 1043 1060 1104 1161')
put('arithmetic','235 240 244 295 330 331 334 355 507 563 607')
put('diverse','236 280 286 288 289 292 303 314 316 364 374 398 451 467 468 486 487 494 512 514 525 526 541 542 545 558 560 574 581 582 585 593 594 606 611 619 681 712 765 767 780 791 805 826 833 860 912 920 922 924 925 940 946 957 1022 1030 1039 1047 1050 1143 1156 1196 1203 1204 1209 1294 1296 1298 1304')
put('auxcorrection','256 491 495 506 550 556 571')
put('retrieval','266 1045')
put('dependencies','267 311 642 646 773 1109 1137 1144 1146')
put('pool','276 392 418')
put('swa','283')
put('bias','299 416 431 458 894 896 897 1122 1127 1145 1154')
put('assetbug','302 675 689 730 743 748 750 907 1021 1064 1101 1102 1147 1148 1165 1171 1178')
put('equal','317 327 711 775 1113 1255')
put('metatype','320 325 338 389 612')
put('metatune','323 599 615')
put('preprocmatch','324 400 443 480 485 534 559 812 825 903 905 908 916 926 950 973 1038 1044 1057 1087 1098 1160 1164 1168 1222 1242 1251 1300 1302 1306 1307')
put('deterministic','373 378 380 445 513 809 865 1159')
put('mcdropout','376 409')
put('embeddings','382 693')
put('precision','402 874')
put('auxhead','411 421 728')
put('textpair','413 683')
put('trainmember','425 470 517 620 621')
put('schedule','433')
put('cleanlabels','435 437 462 986 988 991 1001 1002')
put('target','426 450 455 457 490 524 573')
put('optimizer','460')
put('predscale','471 472')
put('impute','548 565')
put('local','147')
put('metricfast','519 622')
put('baseline','566 716 766')
put('leakage','590 787')
put('parity','591')
put('encoder','631 632')
put('discretize','636 639 660 665 679 680 710 719 725 733 739 740 741')
put('degenerate','661 667')
put('postablate','492 663 682')
put('unassigned','671')
put('fallback','672 676 678')
put('ties','673 731')
put('submit','482 641 674 1019')
put('dropout','685 756 762 1173')
put('resume','686 690')
put('batch','696 877 1111 1152')
put('textclean','702 703')
put('metadata','707 752')
put('rawoutput','570 715 727 729')
put('normalizeout','717 802 1042')
put('rules','735 736 737 738')
put('lr','749 751 758 760 761')
put('logits','769')
put('fusion','781 785 796 904 959 982 983 992 996 998 1003 1005 1017 1254 1274 1277')
put('tta','782 793 828 838 893 1049 1053 1108 1110 1115 1116 1118 1128 1129 1194 1202 1206 1225 1227 1256')
put('branches','813 961 971 1054 1309')
put('spectral','824 965 1000 1009 1200 1223 1224')
put('norminput','900 967 1089 1099 1153 1158 1303')
put('color','966')
put('filter','975 1287 1293 1305')
put('mixup','979')
put('external','1007 1008 1013 1014')
put('mask','1010')
put('pseudo','1032 1035')
put('probability','846')
put('photoaug','1185 1189')
put('clip','1212 1249')
put('reshape','1260 1261')
put('equal','232 695 1031')
put('stack','247')
put('hierarchy','250 391')
put('metatype','270')
put('trainmember','277')
put('members','348 1082 1235 1240')
put('weights','362 1028')
put('duration','583')
put('assetbug','650 1232 1239')
put('schemabug','764 989 1133')
put('diverse','774 1231')
put('preprocmatch','786 960 1150')
put('batch','837 1230')
put('revert','934')
put('smoke','1135')
put('spectral','1228 1236')
put('tta','1229 1237')
put('windows','1233 1241')
put('repeat','1234 1238')
put('replace','1279 1280 1291')
# Refine large clusters by the actual choice, preserving one placement per item.
def move(code, nums):
 for n in map(int,nums.split()):
  assert n in A
  A[n]=code
move('solo','198 202 242 243 258 275 348 367 368 369 399 407 476 488 489 531 532 724 808 835 844 881 883 923 927 937 953 955 1034 1048 1052 1066 1067 1069 1078 1079 1082 1132 1136 1167')
# Tiny-leaderboard cautions remain under evaluation reliability, not solo probing.
move('cvtrust','198 202 844')
move('replace','204 224 263 288 294 308 366 374 553 603 625 869 1023')
move('restoreensemble','200 245 260 272 344 352 371 465 533 613 810 954 1058 1138 1217 1253')
move('addmember','197 203 238 279 281 293 297 312 329 349 351 354 365 372 379 384 543 555 562 576 596 624 806 807 827 832 880 884 921 932 948 956 1026 1033 1036 1055 1056 1059 1063 1139 1198 1248 1259 1285')
move('diverserep','303 314 398 512 542 594 619 712 912 925 940 946 957 1203 1204 1209 1294 1298')
move('diversetarget','467 468 484 494 514 526 574 588 611')
move('foldsubset','249 308 360 648 709 747 822 852 867 870')
move('groupvalidation','182 999')
move('stratvalidation','127 336')
move('oof','158 518')
move('inputaudit','400 443 480 485 903 908 926 950 960 973 1087 1150 1307')
move('artifactmatch','301 341 750 907 1064 1102 1165 1171 1175 1178 1232 1239')
move('nonlinear','1122 1127 1145')
move('logitscale','431 458')
move('classcalibrate','894 896 897')
move('uniform','232 317 327 695 711 775 1031 1113 1255')
move('fixedweights','362')
move('perclassweights','914')
move('shrinktree','583')
move('checkpaths','311 646 650 689 730 743 748 1021 1109')
move('numaudit','565')
move('modalityablate','813 982 992 996 1003 1005')
move('concat','781 785 1254 1274 1277')
move('featurepool','994')
move('broadprobe','1040')
# The progress-bar import item is bookkeeping rather than a performance intervention.
assert set(A)==set(range(len(X))),sorted(set(range(len(X)))-set(A))
# Semantic refinements after reviewing the context fields.
move('nativeapi','23')
move('wrapperapi','180')
move('local','1080')
move('parity','340 441')
move('metricfast','622')
move('members','618')
move('metatune','617 627')
move('targetgroup','426 455')
move('target','457 450')
move('stratvalidation','181') # Main change is a stratified CV baseline, including fold averaging.
move('rawblend','570')
move('rank','0 3 8 10 12 14 16 18 20')
# Resolve bundled or ambiguous cases against full general and instance evidence.
move('diverse','481')
move('rawblend','538')
move('baseline','523')
move('refactor','124')
move('modalityablate','796')
move('rankfast','519')
move('recentagg','85')
# Tree authoring helpers: pushes use symbolic child keys until stable positional IDs are assigned.
LEAVES={}; DECISIONS={}
def L(key,name,desc):
 assert key not in LEAVES
 ns=sorted(n for n,c in A.items() if c==key)
 assert ns,key
 obj={'_key':key,'name':name,'description':desc,'source':'data','children':[], 'items':[X[n]['id'] for n in ns]}
 LEAVES[key]=obj
 return obj
def C(statement,how,**pushes): return {'check':statement,'how':how,'pushes':pushes}
def D(key,name,desc,question,children,checks):
 assert len(children)>=2,key
 obj={'_key':key,'name':name,'description':desc,'decision':question,'source':'data','children':children}
 DECISIONS[key]=checks
 return obj

assessment=D('assessment','Improve comparison reliability','Choose an evidence-gathering change when current scores cannot reliably distinguish candidate solutions.',
 'What prevents the current evaluation from supporting the next model choice?',[
 D('evaldesign','Change the evaluation sample','Choose how to obtain a representative held-out comparison without training on its labels.',
   'Which evaluation design should replace the current unreliable comparison?',[
   L('local','Score candidates locally','Evaluate candidate changes on saved held-out or out-of-fold predictions before selecting a small number for external evaluation.'),
   L('stratvalidation','Balance target distributions across folds','Create stratified folds using class labels or binned continuous targets and compare fold distributions.'),
   L('groupvalidation','Keep related observations together','Split by entity or subject, comparing grouped and stratified-grouped folds when label balancing conflicts with natural groups.'),
   L('oof','Generate aligned out-of-fold predictions','Train on shared fold indices and save predictions only for each model’s held-out rows to support honest stacking and comparison.'),
   L('cvtrust','Check local-to-external score agreement','Compare local and external scores for a small fixed panel of existing configurations before trusting their ranking.')],[
   C('Several candidate configurations can be scored on an existing representative holdout.','Inspect stored validation predictions, labels, and split provenance; verify candidates used the same rows.',local=.9),
   C('Fold target distributions differ substantially despite independent observations.','Tabulate class proportions or target-bin histograms by fold and compare with the full labeled sample.',stratvalidation=.9),
   C('Several rows or overlapping windows belong to the same prediction entity.','Count repeated entity IDs and intersect IDs or window intervals across the current train and validation partitions.',groupvalidation=1,stratvalidation=-.5),
   C('A proposed stacker lacks held-out predictions aligned to common row and fold identifiers.','Join each base model’s prediction file to saved fold indices and check that no row was predicted by a model trained on it.',oof=1),
   C('Local and public scores have ranked existing checkpoints differently.','Compare the paired local/external score table and public sample size; distinguish ranking reversals from repeated-run variation.',cvtrust=.9,local=-.3)]),
 D('metricchoice','Change the model-selection signal','Choose whether the stopping metric, its implementation, or its computational cost is the evaluation bottleneck.',
   'What should change in the metric used to select training iterations?',[
   L('custommetric','Use the task metric for stopping','Implement the task metric as an evaluation callback and select iterations by held-out task performance.'),
   L('proxy','Use a smoother stopping proxy','Compare a standard smooth evaluation metric with the custom metric for early stopping while retaining the task metric for final validation.'),
   L('metricbug','Repair the metric callback','Check the callback signature, label/prediction shapes, return format, and direction against small hand-verifiable examples.'),
   L('metricfast','Accelerate repeated metric calculation','Replace the slow metric implementation with an optimized equivalent and verify agreement on ordinary and tied predictions.')],[
   C('The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons.','Compare the configured evaluation callback with the task formula and recorded task scores along training.',custommetric=.9),
   C('The task metric fluctuates sharply between nearby iterations while a smooth proxy tracks generalization better.','Inspect validation curves and prior stopping-point comparisons on identical folds.',proxy=.9,custommetric=-.5),
   C('Callback values or shapes disagree with an independent calculation.','Evaluate a small labeled prediction vector through both code paths and inspect the framework callback arguments.',metricbug=1),
   C('Metric computation dominates repeated training or blending evaluations.','Read profiler timings for the callback and compare its output against the existing reference implementation.',metricfast=.9)]),
 D('experiment','Change the experiment design','Choose the experiment that resolves the present attribution or search uncertainty.',
   'What experiment should be run next given the evidence already available?',[
   L('baseline','Establish an end-to-end baseline','Run the simplest complete pipeline through prediction export and obtain an initial task score.'),
   L('isolate','Test one controlled change','Hold the checkpoint, data, and other settings fixed while adding or reverting one factor to isolate its effect.'),
   L('repeat','Measure repeated-run variation','Repeat a fixed configuration and compare score distributions before treating a small difference as an improvement.'),
   L('search','Bracket a bounded search','Use a recorded coarse-to-fine or small factorial sweep over a specified parameter range, including nearby reversals.'),
   L('revert','Recover the last validated configuration','Restore the known-good configuration, or revert the suspected harmful factor, before resuming incremental experiments.'),
   L('pivot','Stop an exhausted local search','Freeze the best validated setting after repeated changes fail to beat the noise floor and move the next experiment to a different lever.'),
   L('broadprobe','Replace a clearly inadequate baseline','Test a coherent package of strongly motivated changes when establishing competitiveness matters more than attributing each component.')],[
   C('No complete pipeline has yet produced a scored prediction file.','Inspect run artifacts and the experiment log for a successful end-to-end scored baseline.',baseline=1,search=-.5),
   C('The last score change followed several simultaneous functional edits.','Diff the last two scored versions and list changed inputs, checkpoints, training settings, and blend formulas.',isolate=1,search=-.4),
   C('Existing unchanged runs vary by as much as the candidate gain.','Compare repeated scores and prediction files for an identical configuration, including pinned artifacts.',repeat=1,search=-.6),
   C('A reproducible parameter trend exists but the optimum has not been bracketed.','Inspect the trial table for consistently improving values and whether values on both sides have been evaluated.',search=.9),
   C('The latest configuration is substantially worse than a reproducible saved baseline.','Compare the regression with measured run variation and locate the exact saved configuration and artifacts.',revert=1),
   C('Several recent settings failed to improve beyond the measured noise floor.','Read the recent sweep table, including failed probes, and compare its range with unchanged-run variation.',pivot=1,search=-.8),
   C('The first baseline is far below existing scored alternatives and several compatible missing components are already evidenced.','Compare available baseline scores and code paths for missing domain preprocessing, suitable models, or averaging; record the loss of attribution before bundling.',broadprobe=.7,isolate=-.2)])],[
 C('Related rows cross folds or fold target distributions are visibly skewed.','Inspect split IDs and per-fold target summaries.',evaldesign=1),
 C('The reported evaluation callback is incorrect, unstable, or a measured runtime bottleneck.','Compare metric code, curves, and profiler output with the task’s scoring definition.',metricchoice=1),
 C('Multiple edits or stochastic reruns make the latest score movement ambiguous.','Review version diffs and repeated baseline scores.',experiment=1)])

correctness=D('correctness','Repair prediction correctness','Choose a repair when predictions are missing, implausible, or inconsistent with the trained model.',
 'Where is there direct evidence that the prediction pipeline is wrong?',[
 D('loadrepair','Repair artifact loading','Choose the correction required to load the intended trained computation.',
   'What prevents the intended checkpoint from being loaded correctly?',[
   L('checkpaths','Verify artifact paths and lifetime','Resolve every configured checkpoint and prediction path, check existence, and defer cleanup until after its final use.'),
   L('dependencies','Resolve dependency and import conflicts','Use the required locally available package version and correct import path before constructing the model.'),
   L('artifactmatch','Match architecture to the checkpoint','Reconstruct the exact checkpoint architecture and tokenizer, normalize known wrapper prefixes, and require matching parameter keys and shapes.'),
   L('assetbug','Verify loaded weights are effective','Inspect loaded tensors and model mode, then run known examples to confirm trained weights actually drive non-degenerate outputs.')],[
   C('A configured artifact is missing or its resolved path differs from the saved artifact.','List available files and compare full resolved paths, including filename punctuation and cleanup commands.',checkpaths=1),
   C('Imports fail or resolve to a different library copy than the checkpoint requires.','Inspect import exceptions, module file locations, local package versions, and path ordering.',dependencies=1),
   C('Checkpoint keys, tensor shapes, tokenizer vocabulary, or head dimensions disagree with the constructed model.','Compare the saved configuration and state dictionary with the instantiated model under strict loading.',artifactmatch=1),
   C('Loading appears successful but predictions resemble an untrained or constant model.','Inspect loaded parameter statistics, missing-key reports, evaluation mode, and predictions on a small known labeled sample.',assetbug=1)]),
 D('flowrepair','Repair data and output flow','Choose the stage whose observable invariant is broken.',
   'Which data-flow invariant is failing?',[
   L('schemabug','Trace rows and executed branches','Assert row IDs, shapes, columns, loop counts, and the final exported variable so every intended model contributes to the correct samples.'),
   L('inputaudit','Audit intermediate feature tensors','Inspect representative tensors after each transformation and forward-pass operation to find wrong variables, axes, or disabled paths.'),
   L('preprocmatch','Restore training-time preprocessing','Apply the saved training encoders, feature extraction, resolution, and normalization in the same order at inference.'),
   L('encoder','Reuse encoders with unknown-category handling','Transform test categories with the training-fitted encoder and an explicit policy for unseen values instead of refitting it.'),
   L('leakage','Remove unavailable or leaking inputs','Remove identifier leakage and label-derived preprocessing dependencies, then rebuild transformations using only prediction-time information.'),
   L('parity','Compare outputs across a refactor','Run the saved and refactored pipelines on identical rows and compare aligned intermediate and final predictions numerically.')],[
   C('Outputs are constant across substantial edits or some configured members never produce predictions.','Trace loop entry counts, array accumulation, input row IDs, and the exact variable written to disk.',schemabug=1),
   C('A new feature branch receives implausible shapes or values.','Print small tensor slices, axis meanings, and statistics before and after each new transform.',inputaudit=1),
   C('Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.','Compare saved training configuration, feature order, scaler/encoder artifacts, and inference call order.',preprocmatch=1),
   C('Test categories include unseen levels or the inference code fits a new encoder.','Compare category sets and inspect calls to fit, fit_transform, and transform.',encoder=1),
   C('A preprocessing or target-building step consumes identifiers or labels unavailable at prediction time.','Trace input dependencies against the test schema and audit fitting boundaries inside each fold.',leakage=1),
   C('A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence.','Locate reference predictions and compare both implementations on the same ordered sample.',parity=.9)]),
 D('numericrepair','Repair prediction semantics','Choose the violated numerical contract before changing model quality.',
   'Which numerical mismatch explains the implausible predictions?',[
   L('outputlink','Align prediction units and direction','Convert logits or scaled targets correctly and align risk versus survival direction before scoring or blending.'),
   L('arithmetic','Correct ensemble arithmetic','Convert predictions to numeric arrays and verify active-member divisors, group means, weights, and output scale.'),
   L('numaudit','Locate non-finite values','Check inputs and intermediate outputs for NaNs or infinities and repair the first stage that creates invalid values.'),
   L('dataframeapi','Correct the prediction or preprocessing API','Match method names, arguments, and mutation semantics to the actual model or dataframe object in use.')],[
   C('Prediction units or monotonic direction disagree with the labels or other members.','Check target scaling and inverse-link code, and compare standalone held-out score direction with a trusted member.',outputlink=1),
   C('Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.','Recompute a few rows by hand and compare active member counts, weights, types, and array shapes.',arithmetic=1),
   C('Inputs or intermediate network outputs contain non-finite values.','Run finite-value checks stage by stage on a small failing batch.',numaudit=1),
   C('The called method or argument belongs to a different API wrapper than the instantiated object.','Inspect object types and local function signatures at the failing call.',dataframeapi=1)]),
 D('executionrepair','Restore a valid end-to-end run','Choose the smallest repair needed for a usable prediction artifact.',
   'What is preventing a valid full prediction run?',[
   L('smoke','Debug a minimal end-to-end run','Run one model or a tiny data slice through all stages and fix the earliest failing operation before restoring scale.'),
   L('submit','Validate prediction export','Always write the final correctly aligned predictions to the required file with the expected schema, including in production mode.'),
   L('fallback','Make missing-member handling explicit','Detect missing or corrupt member outputs and use only verified aligned fallback predictions or renormalized available members rather than placeholders.'),
   L('refactor','Rebuild a tangled pipeline','Replace duplicated or fragile notebook paths with explicit reusable stages and validate equivalent behavior before adding further changes.')],[
   C('The pipeline fails before completing even one sample or model.','Read the first traceback and try the same path on one batch with minimal training.',smoke=1),
   C('Inference finishes but the expected prediction file is absent or malformed.','Read the final artifact and compare its path, row IDs, columns, and numeric values with the required template.',submit=1),
   C('Some ensemble output files are missing or fallback arrays are placeholders.','Inspect each member file, its provenance and row alignment, and logs identifying which fallback path executed.',fallback=1),
   C('Repeated patches leave duplicated transformations or hidden dependencies that prevent reliable fixes.','Trace the current stages and compare duplicate code paths and their outputs.',refactor=.8,smoke=.3)])],[
 C('Failures begin at import, checkpoint resolution, or state loading.','Read the earliest error and loading diagnostics.',loadrepair=1),
 C('The model runs but rows, features, or executed branches do not match the intended pipeline.','Inspect IDs, stage shapes, and per-model prediction counts.',flowrepair=1),
 C('Prediction scale, direction, finiteness, or blending arithmetic is invalid.','Inspect numeric summaries and manually recompute representative outputs.',numericrepair=1),
 C('No usable final output exists or accumulated patches obstruct basic execution.','Inspect the first failure and final artifact schema.',executionrepair=1)])
execution=D('execution','Remove execution bottlenecks','Choose an execution change that enables valid larger runs or more informative experiments.',
 'Which measured execution constraint is limiting useful experiments?',[
 D('memorychoice','Reduce peak memory','Choose the object or operation whose memory footprint must shrink.',
  'What accounts for the memory peak?',[
  L('chunks','Process data in bounded chunks','Partition examples by entity or split aggregations into smaller blocks, retaining only aligned predictions between blocks.'),
  L('memory','Release completed models and intermediates','Delete objects after their last use and clear runtime caches before loading the next model.'),
  L('batch','Reduce inference batch size','Find a batch size that completes inference and verify prediction invariance before using a larger batch for speed.'),
  L('precision','Compare reduced and full precision','Test reduced-precision inference against full precision on the same examples and retain it only when numerical effects are acceptable.')],[
  C('The raw table or engineered feature table exceeds memory before model inference starts.','Compare dataframe sizes and profiler memory peaks during loading and aggregation.',chunks=1,batch=-.5),
  C('Memory grows between sequential model runs because completed objects remain live.','Inspect memory after each model and references to model objects and intermediate arrays.',memory=1),
  C('Memory failure occurs in a single forward pass and grows with batch size.','Inspect the traceback and peak accelerator memory for progressively smaller batches.',batch=1),
  C('Model tensors dominate memory and the current pipeline uses full precision.','Inspect tensor dtypes and allocations and any prior paired precision results.',precision=.7)]),
 D('iteration','Shorten the iteration cycle','Choose which redundant work can be removed without changing the intended final computation.',
  'Which repeated work is slowing development?',[
  L('fast','Use a reduced development configuration','Gate reduced folds, seeds, rows, or iterations behind one explicit development setting and restore the full setting for final evaluation.'),
  L('cache','Cache stable intermediate artifacts','Save aligned embeddings, engineered features, predictions, or stage checkpoints once and reuse them while testing downstream changes.'),
  L('resume','Train unfinished folds across sessions','Persist each completed fold and resume only missing folds in later sessions.'),
  L('rankfast','Accelerate rank post-processing','Replace slow ranking code with a verified exact implementation, testing tied values and subgroup ordering before reusing it in adjustment searches.'),
  L('config','Centralize variant configuration','Use named configurations and explicit artifact mappings to select models, feature branches, and blend members without scattered edits.')],[
  C('A full training run is currently needed just to test code wiring or screen a parameter.','Measure run time and inspect whether fold, seed, and iteration counts can be reduced coherently.',fast=.9),
  C('The expensive upstream outputs are unchanged across downstream experiments.','Compare artifact hashes and configurations for repeated feature extraction or base-model inference.',cache=1),
  C('A session cannot finish all folds but completed fold checkpoints can be reused.','Compare per-fold run time with the session limit and inspect persisted fold manifests.',resume=1),
  C('Repeated ranking or subgroup post-processing dominates the inference-adjustment search.','Inspect stage timings and compare current rank outputs on tied and grouped predictions with a small exact reference.',rankfast=1),
  C('Variant changes require repeated manual edits that have caused configuration drift.','Inspect duplicate constants, path lists, and flags across the notebook.',config=.9)]),
 D('runtimeapi','Change the runtime interface','Choose the interface change required by the observed execution limitation.',
  'Which runtime interface fits the required operation?',[
  L('backend','Use a supported execution backend','Move unsupported operations or model families to a verified CPU path, then enable acceleration only where the environment supports it.'),
  L('nativeapi','Use the native training API','Move training to the native interface when custom callbacks or iteration control are unavailable in the current wrapper.'),
  L('wrapperapi','Use the estimator wrapper','Use the estimator interface when it provides the needed probability prediction and stopping behavior with less integration code.')],[
  C('The configured accelerator or dataframe backend does not support a required operation.','Inspect the device error, available hardware, and a minimal local backend probe.',backend=1),
  C('The current wrapper cannot expose the needed custom metric or iteration control.','Inspect the installed wrapper signature and the native training interface used by existing code.',nativeapi=.9,wrapperapi=-.6),
  C('The estimator wrapper already supports the required stopping and probability outputs.','Inspect its local interface and compare it with the extra dataset and prediction-conversion code currently maintained.',wrapperapi=.8,nativeapi=-.3)])],[
 C('Runs fail or slow sharply at a reproducible memory peak.','Inspect memory profiles and failure traces.',memorychoice=1),
 C('Repeated loading, extraction, or full training dominates otherwise working experiments.','Compare stage timings across recent runs.',iteration=1),
 C('Device support or API limitations block a required operation.','Inspect runtime exceptions and available local interfaces.',runtimeapi=1)])

features=D('features','Change the input information','Choose a representation change to expose missing signal or remove harmful inputs.',
 'What limitation in the current input representation should the next experiment address?',[
 D('tablefeatures','Change tabular summaries','Choose a reusable representation for repeated rows or interacting columns.',
  'Which information is missing from the current tabular summaries?',[
  L('eda','Inspect entity and feature structure','Profile record counts, time ordering, column families, dtypes, and missingness to determine the unit and scope of feature construction.'),
  L('aggsimple','Use a minimal entity summary','Collapse repeated rows into a small last-value or basic-statistics baseline before expanding feature engineering.'),
  L('aggrich','Expand entity summary statistics','Add validated location, spread, range, count, or categorical-diversity aggregates to the entity-level features.'),
  L('recentagg','Summarize recent history separately','Add statistics over the most recent records alongside full-history entity aggregates and compare window lengths on held-out data.'),
  L('lags','Add change-over-time features','Compute ordered lag differences or first-to-last changes within entities and test their incremental value.'),
  L('interact','Add targeted interaction features','Construct a small set of domain-supported differences, ratios, or products, using smoothed summaries when individual values are noisy.'),
  L('calendar','Encode elapsed or calendar time','Convert timestamps into elapsed-time or calendar features and test their value beyond existing entity summaries.')],[
  C('The number and ordering of records per prediction entity are not yet established.','Inspect entity counts, sorted timestamps, feature prefixes, and missingness summaries.',eda=1),
  C('No working entity-level feature baseline exists.','Inspect the feature table and training inputs for duplicate prediction IDs and missing aggregation logic.',aggsimple=1,aggrich=-.4),
  C('Only the last observation or one central statistic is currently retained.','Compare the aggregation specification with within-entity variation and existing importance plots.',aggrich=.9),
  C('Full-history aggregates obscure behavior near the prediction time.','Compare recent and full-history distributions, history lengths, and the label time horizon.',recentagg=.9),
  C('Entities have ordered histories whose recent changes are not represented.','Inspect sequence lengths, time ordering, and whether current aggregates discard direction of change.',lags=.9),
  C('Domain-related columns have a meaningful ratio or deviation not present in the features.','Inspect column definitions and the existing derived-feature list, then review prior interaction ablations.',interact=.8),
  C('Timestamps vary meaningfully across entities and have been discarded from the feature table.','Compare timestamp ranges and target patterns with the current aggregation outputs.',calendar=.7)]),
 D('featureselection','Reduce feature noise','Choose how to identify and remove inputs that do not generalize.',
  'What evidence should guide the next feature reduction?',[
  L('importance','Select a stable importance-ranked subset','Aggregate importance or attribution across folds and sweep the retention cutoff while checking held-out performance.'),
  L('featureablate','Ablate a suspected feature group','Remove or restore one coherent feature family and keep the smaller set only when validation supports it.'),
  L('dropmissing','Test dropping extremely sparse columns','Remove columns above a measured missingness threshold and validate against retaining them.'),
  L('featurepool','Limit the pooled feature dimension','Compare the full pooled embedding with a truncated representation using a compatible trained head.')],[
  C('A wide feature table has stable cross-fold importance estimates.','Compare rankings across fitted folds and inspect whether low-ranked columns dominate feature count.',importance=.9),
  C('A particular added feature family coincided with a regression or is error-prone.','Review feature-version diffs, prior group ablations, and implementation failures.',featureablate=1),
  C('Some columns are almost entirely missing.','Compute column missingness on train and validation and inspect the model’s use of those columns.',dropmissing=.8),
  C('The classifier consumes a truncated backbone embedding and full-dimensional checkpoints are available.','Inspect pooled tensor width, head parameter count, and compatible checkpoint configurations.',featurepool=.9)]),
 D('numericinput','Change numerical preprocessing','Choose how to treat missingness and precision for the actual model family.',
  'Which numerical preprocessing policy fits the inputs and estimator?',[
  L('nativenan','Preserve native tree inputs','Trial removing unnecessary imputation, scaling, or outlier filtering when the tree implementation supports missing values directly.'),
  L('impute','Use model-specific imputation','Give models that require finite inputs a fitted imputation path while retaining native missingness where supported.'),
  L('quantizeinput','Coarsen noisy numerical precision','Round continuous inputs at a justified precision and compare against the original values on the same folds.')],[
  C('The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes.','Inspect estimator capabilities, aggregation-generated NaNs, and prior preprocessing ablations.',nativenan=1),
  C('At least one active model rejects missing values or lacks native handling.','Inspect estimator input checks and the finite-value fraction of its actual feature matrix.',impute=1,nativenan=-.5),
  C('Low-precision storage creates spurious fine-scale differences relative to meaningful measurement resolution.','Compare raw and stored values, unique-value spacing, and dtype conversion code.',quantizeinput=.9)]),
 D('textinput','Change text information','Choose a text representation change based on what the pretrained encoder currently sees.',
  'What text information or formatting should be changed?',[
  L('textlength','Change retained text context','Compare sequence length or task-relevant cropping only where truncation or irrelevant spans plausibly lose useful information.'),
  L('textclean','Remove harmful custom cleaning','Compare aggressive cleaning with the pretrained tokenizer’s expected raw text and retain the better aligned input.'),
  L('textpair','Change text-stream structure','Encode semantically distinct text fields separately or as a tested pair using checkpoints trained for that format.'),
  L('metadata','Append structured text metadata','Concatenate validated text statistics or categorical metadata with the encoded text representation.')],[
  C('Relevant text lies outside the retained token range or is diluted by unrelated spans.','Inspect token-length distributions, truncation examples, and task-relevant span locations.',textlength=.9),
  C('Custom normalization changes text beyond the tokenizer’s training assumptions.','Compare before/after examples and existing cleaning ablations.',textclean=.9),
  C('Distinct text fields are flattened together despite different roles in the target.','Inspect input schema, encoding templates, and available checkpoints for separate or paired streams.',textpair=.9),
  C('Structured metadata or surface statistics vary with targets but are absent from the model.','Inspect train-only metadata summaries, target associations, and the current input signature.',metadata=.8)]),
 D('signalinput','Change image or signal encoding','Choose the encoding parameter whose current setting plausibly hides relevant structure.',
  'Which aspect of the image or signal representation should be changed?',[
  L('resolution','Sweep input spatial resolution','Compare nearby image resolutions with compatible checkpoints, holding other inference choices fixed.'),
  L('windows','Change the retained context window','Sweep temporal-window or spatial-crop extent around the current setting while preserving label alignment.'),
  L('spectral','Change time-frequency resolution','Compare spectral transform, window, or hop settings with matched training preprocessing to trade temporal against frequency detail.'),
  L('norminput','Match input normalization','Use validated per-sample or training-domain normalization consistently in training and inference.'),
  L('filter','Change signal filtering','Test a domain-supported notch, bandpass, or filter implementation while preserving a matched training/inference signal path.'),
  L('clip','Tune signal dynamic-range clipping','Compare nearby clipping thresholds for raw or log-spectral values to suppress extreme artifacts without removing informative signal.'),
  L('color','Test scalar-to-color encoding','Compare colormap-based channels with the original scalar representation using a compatible pretrained image model.'),
  L('reshape','Change signal-to-image layout','Compare height-width factorizations that preserve the sample values while changing the spatial neighborhoods seen by the image backbone.')],[
  C('Useful fine detail is lost at the current resize and compatible higher-resolution weights exist.','Inspect downsampled examples, checkpoint training sizes, and prior resolution probes.',resolution=.9),
  C('The current temporal or spatial window misses the labeled region or includes irrelevant context.','Compare timestamp or crop bounds with label scope, sequence lengths, and current retained content.',windows=1),
  C('Time-frequency bins are too coarse for the event durations or frequency structure of interest.','Inspect spectrograms, transform parameters, sampling rate, and matched checkpoint settings.',spectral=.9),
  C('Input intensity statistics differ from the training preprocessing or target-domain distribution.','Compare per-channel statistics and saved normalization code with inference tensors.',norminput=1),
  C('Known interference frequencies or an unsuitable passband remain in the signal.','Inspect spectra, filter response, sampling rate, and documented signal bandwidth.',filter=.9),
  C('A few extreme values dominate the raw or spectral dynamic range.','Inspect value quantiles and plots before and after current clipping.',clip=.9),
  C('A natural-image backbone receives scalar spectral images and a color encoding has not been tested.','Inspect input channels, pretraining expectations, and any compatible color-encoded checkpoints.',color=.6),
  C('An arbitrary signal-to-image factorization creates implausible local neighborhoods.','Trace the reshape dimensions and visualize adjacent image positions against original time and channel indices.',reshape=.9)]),
 D('modalities','Change modality use','Choose how to add, remove, or fuse complementary input streams.',
  'What should change in how input branches supply information?',[
  L('branches','Add derived input channels','Expose additional signal channels or derived features with matching model input dimensions and normalization.'),
  L('fusion','Add a complementary model branch','Train or load a compatible branch for another modality or resolution and evaluate the resulting joint model.'),
  L('modalityablate','Remove or restore an input branch','Ablate one modality at a time and retain it only if it improves the fixed model or ensemble comparison.'),
  L('concat','Compare concatenation with averaging','Test concatenated versus averaged branch embeddings with the corresponding trained head dimensions.')],[
  C('Useful channels are available in the same signal but excluded from the current tensor.','Compare raw channels and derived-channel definitions with model input indices.',branches=.9),
  C('A different modality or representation carries information the current branch cannot see.','Inspect paired samples, existing standalone modality scores, and available compatible training paths.',fusion=.9),
  C('An existing branch adds substantial complexity and its incremental benefit is unverified or negative.','Inspect previous branch ablations and branch-specific outputs on the same rows.',modalityablate=1),
  C('Equal-width branch embeddings are averaged before classification, potentially discarding distinct information.','Inspect fusion code, feature dimensions, and compatible heads for concatenation and averaging.',concat=.9)])],[
 C('Repeated rows are collapsed into a limited summary or their structure is still unknown.','Inspect entity histories and the current tabular feature specification.',tablefeatures=1),
 C('Many engineered inputs are redundant, sparse, or implicated in prior regressions.','Review importance stability, missingness, and feature-group ablation results.',featureselection=.9),
 C('Missingness or stored numerical precision conflicts with estimator assumptions.','Inspect actual dtypes, NaNs, and active model capabilities.',numericinput=1),
 C('Text truncation, formatting, or omitted metadata plausibly limits the encoder.','Inspect tokenized samples and the text/metadata schema.',textinput=.9),
 C('Spatial or spectral preprocessing removes relevant structure or mismatches trained inputs.','Inspect transformed examples and saved extraction settings.',signalinput=1),
 C('Several aligned modalities or channels exist and their use or fusion remains unresolved.','Inspect available inputs, branch outputs, and existing modality ablations.',modalities=.9)])
supervision=D('supervision','Change the training signal','Choose a data, target, or augmentation change rather than altering prediction combination.',
 'What limits the usefulness of the current labeled training signal?',[
 D('trainrows','Change training examples','Choose which examples should contribute to fitting the model.',
  'How should the training population change?',[
  L('fulldata','Refit on more labeled rows','After model selection, compare a smaller reserved holdout or a full-data refit using a separately established validation protocol.'),
  L('external','Trial additional labeled data','Add compatible external labeled examples, optionally in an earlier training stage, and validate whether their distribution helps.'),
  L('pseudo','Train with validated pseudo-labels','Retrain a weak member with the available pseudo-labeling procedure and compare it with the labeled-only model.'),
  L('cleanlabels','Filter noisy or redundant examples','Compare quality thresholds, class filters, or deduplication using held-out evidence, retaining informative ambiguous examples when filtering harms performance.'),
  L('classweight','Tune class or sample weights','Sweep moderate class-weight values against an unweighted baseline using the task metric rather than assuming full inverse-frequency balancing.')],[
  C('A substantial labeled holdout remains unused after the configuration has already been selected.','Inspect split sizes, stopping strategy, and the independently saved validation evidence.',fulldata=.9),
  C('Additional labeled examples exist with compatible targets and adaptable input shapes.','Inspect their provenance, label definitions, distribution, and previous inclusion experiments.',external=.9),
  C('Unlabeled examples and a pseudo-labeling procedure already improved another comparable member.','Review available pseudo-label artifacts, confidence diagnostics, and labeled-only versus pseudo-labeled validation results.',pseudo=.9),
  C('Training examples contain duplicated windows, flagged outliers, or measurable label-quality variation.','Inspect overlap IDs, out-of-fold residuals, annotator counts, and retained sample counts under proposed filters.',cleanlabels=1),
  C('Class imbalance or subgroup error patterns suggest the current sample weighting is unsuitable.','Compare class counts and per-class held-out errors with the metric’s weighting and earlier weight sweeps.',classweight=.9)]),
 D('targetchoice','Change target construction','Choose how to express a censored or subgroup-dependent outcome for learning.',
  'Should target construction be global or conditioned on evaluation groups?',[
  L('target','Transform the censored outcome','Compare regression-friendly survival or risk transforms and their scalar parameters while fitting target transformations within training folds.'),
  L('targetgroup','Construct targets within evaluation groups','Estimate the outcome transformation separately for known evaluation groups and compare group and aggregate held-out performance.')],[
  C('The outcome is censored and ordinary regression targets do not express the observed event information.','Inspect event indicators, observation times, censoring rates, and current target-building code.',target=1),
  C('The metric scores predefined groups and their outcome distributions differ substantially.','Read the metric grouping definition and compare training-only event and censoring distributions by group.',targetgroup=1),
  C('Some groups have too few observed events for stable group-specific transforms.','Count events and inspect transform stability across training folds within each group.',targetgroup=-.8,target=.6)]),
 D('augmentation','Change training augmentation','Choose a training perturbation justified by the input and label structure.',
  'Which training augmentation is compatible with the task’s invariances?',[
  L('photoaug','Use mild image perturbations','Trial small brightness, contrast, or geometric changes and avoid magnitudes that distort domain-relevant image structure.'),
  L('mask','Mask local signal regions','Apply stochastic time-frequency masking during training and validate against the unmasked baseline.'),
  L('mixup','Blend examples and soft labels','Compare multi-example mixup with the existing mixing scheme while preserving corresponding soft-label weights.')],[
  C('Image intensity varies naturally but strong augmentation has previously distorted useful structure.','Inspect image distributions and augmentation examples alongside prior magnitude sweeps.',photoaug=.9),
  C('The model sees spectrograms and should tolerate missing local time-frequency evidence.','Inspect signal events and candidate masks to confirm they do not systematically erase the full target interval.',mask=.9),
  C('Labels are soft distributions and the existing training code already supports weighted example mixing.','Inspect label normalization and mixup weights and compare previous mixed versus unmixed training results.',mixup=.9)])],[
 C('Data quantity, label quality, duplication, or imbalance is the observed limitation.','Inspect learning curves, sample provenance, counts, and quality-stratified errors.',trainrows=1),
 C('Censoring or evaluation-group fairness is not represented appropriately by the current target.','Inspect outcome schema, target construction, and per-group scores.',targetchoice=1),
 C('Training overfits despite plausible label-preserving input perturbations being available.','Inspect train/validation gaps and examples of domain-compatible transforms.',augmentation=.9)])

model=D('model','Change the model or fitting procedure','Choose a single-model intervention based on capacity, representation, or convergence evidence.',
 'Which single-model limitation should be addressed next?',[
 D('modelclass','Change the predictor family','Choose an alternative predictor according to the existing representation and checkpoint evidence.',
  'What kind of predictor change fits the current data and available artifacts?',[
  L('family','Compare a different model family','Train or load a structurally different predictor on the same valid evaluation split and compare with the incumbent.'),
  L('pretrain','Change the pretrained backbone','Compare a compatible backbone or domain-pretrained checkpoint while holding downstream inference choices fixed.'),
  L('larger','Change backbone capacity','Compare smaller and larger trained backbone variants with matching head dimensions and preprocessing.'),
  L('embeddings','Fit a regressor on fixed embeddings','Extract aligned pretrained representations and fit a regularized classical or small neural predictor on held-out splits.'),
  L('retrieval','Add a retrieval predictor','Use training-only nearest neighbors in an embedding space as features or predictions and validate their incremental value.'),
  L('booster','Compare boosting variants','Test the alternative boosting strategy against the tuned incumbent using an appropriate iteration budget and stopping policy.')],[
  C('The current family has plateaued despite useful features and controlled tuning.','Review the single-model tuning history and whether an alternative family offers a different treatment of the data.',family=.8),
  C('A domain-relevant or structurally different pretrained backbone is available.','Inspect its training domain, expected inputs, and existing standalone validation evidence.',pretrain=.9),
  C('Capacity appears limiting or a smaller model may meet the same quality target.','Compare train/validation errors, resource use, and available size-matched checkpoints.',larger=.8),
  C('Pretrained embeddings are available but end-to-end fine-tuning is noisy or expensive.','Inspect cached representation quality, sample count, and variance across fine-tuning runs.',embeddings=.9),
  C('Similar labeled examples exist and a leakage-free retrieval index can be built for each validation fold.','Inspect nearest-neighbor examples and verify that the query’s label and validation rows are excluded from its index.',retrieval=.8),
  C('The tuned standard tree booster still appears to overfit and a dropout-based variant is supported.','Inspect train/validation curves and prior booster comparisons, including whether early stopping works for the variant.',booster=.8)]),
 D('headchoice','Change the prediction head','Choose a head change that matches the observed representation bottleneck.',
  'Which head modification should be compared with the current trained head?',[
  L('head','Enrich the prediction head','Add a validated attention, normalization, or hidden-layer component between the backbone and prediction output, retraining a compatible checkpoint.'),
  L('headsimple','Simplify the prediction head','Compare a simpler shared or minimally normalized head with the current complex head using correctly matched trained weights.'),
  L('pool','Change representation pooling','Compare learned layer weighting or token mean/max/attention pooling using checkpoints trained for each pooling configuration.'),
  L('auxhead','Add an auxiliary prediction task','Train a parallel discretized classification or summary-target head alongside the main task and ablate its contribution.')],[
  C('The backbone is strong but its current head is only a minimal projection.','Inspect architecture definitions and the plateau under backbone-fixed experiments.',head=.9),
  C('A complex multi-head or normalization design has regressed or overfit.','Compare train/validation behavior and head ablations with matching checkpoints.',headsimple=1,head=-.5),
  C('Useful token or hidden-layer information is discarded by the current pooling.','Inspect pooling code, available hidden states, sequence structure, and earlier pooling comparisons.',pool=.9),
  C('The main regression target has a meaningful discrete or auxiliary structure that can be learned jointly.','Inspect target support and previous auxiliary-task validation results; verify sufficient labels for both tasks.',auxhead=.8)]),
 D('treefit','Change tree fitting','Choose the tree-control adjustment indicated by fit and generalization evidence.',
  'What tree-fitting change should be tested next?',[
  L('treecapacity','Sweep tree depth or leaf capacity','Compare bounded tree-depth or leaf-count settings on the fixed feature set, then recheck coupled regularization when needed.'),
  L('penalty','Tune tree regularization','Sweep leaf-size constraints or coefficient penalties on a coarse scale, reverting uncertain overrides to validated defaults.'),
  L('subsample','Introduce row and feature sampling','Test stochastic row and column subsampling against full-data tree construction with enough stopping patience.'),
  L('lrrounds','Couple learning rate and boosting budget','Adjust learning rate together with sufficient boosting rounds and patience so comparisons do not confuse slow learning with undertraining.'),
  L('shrinktree','Reduce per-member boosting duration','Compare shorter tree fits when ensemble averaging may permit lower individual complexity.')],[
  C('Training fit is poor under shallow trees or prior depth changes show a clear capacity effect.','Inspect train/validation curves, depth and leaf settings, and completed capacity probes.',treecapacity=.9),
  C('Training improves while validation stagnates under the current tree capacity.','Compare curves and prior penalties or minimum-leaf settings on the same feature set.',penalty=.9,treecapacity=-.4),
  C('Every tree sees all rows and columns and the model overfits after feature selection.','Inspect bagging and feature-fraction settings and the held-out gap.',subsample=.9),
  C('Lower learning rates reach the round cap or trigger stopping before sustained convergence.','Inspect best iteration, learning rate, round budget, and metric progression near stopping.',lrrounds=1),
  C('Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.','Compare standalone and ensemble validation curves across saved iteration checkpoints.',shrinktree=.7)]),
 D('neuralfit','Change neural optimization','Choose an optimization adjustment based on observed training behavior.',
  'Which optimization control should be changed first?',[
  L('lr','Bracket the fine-tuning learning rate','Compare nearby learning rates with controlled training duration and retreat from rates that destabilize validation.'),
  L('schedule','Compare learning-rate schedules','Test a different decay schedule while holding optimizer and other training settings fixed.'),
  L('optimizer','Compare optimizers','Evaluate an alternative optimizer against the current one on identical data and model configurations.'),
  L('dropout','Tune head dropout','Sweep head dropout during training and recheck nearby learning rates using compatible trained checkpoints.'),
  L('loss','Align the loss and output parameterization','Compare a task-appropriate loss and activation, such as independent outputs or pairwise ranking, against the current objective.')],[
  C('Training is unstable or converges too slowly under the current fine-tuning rate.','Inspect loss curves, gradient behavior, rate settings, and previous rate trials.',lr=1),
  C('Convergence stalls around the current decay schedule’s transitions.','Plot learning rate and validation metric over steps and compare with earlier schedules.',schedule=.8),
  C('The current optimizer has reproducible convergence limitations after learning-rate tuning.','Inspect optimization traces and prior controlled rate sweeps before comparing another optimizer.',optimizer=.7),
  C('The pretrained backbone fits training data well but the added head overfits.','Inspect train/validation gaps and the head’s current dropout and capacity.',dropout=.9),
  C('The output activation or training loss imposes assumptions inconsistent with the labels or task metric.','Compare mutually exclusive versus independent targets, distributional labels, or pairwise ranking requirements with the current head and loss.',loss=1)]),
 D('trainingselection','Change training duration or checkpoint use','Choose how fitting should stop and which trained state should be retained.',
  'What limits the quality of the currently selected trained state?',[
  L('duration','Sweep training duration','Compare adjacent epoch or iteration budgets and keep the state that generalizes best under the validated evaluation protocol.'),
  L('patience','Retune early-stopping patience','Compare stopping patience around the current setting using the learning rate and validation-curve variability as context.'),
  L('checkpoint','Compare existing trained checkpoints','Evaluate saved epochs, stages, or runs with fixed preprocessing and combination settings before selecting a checkpoint.'),
  L('swa','Average compatible model weights','Average compatible late-training weight states and validate against the original checkpoint before using the smoothed model.'),
  L('trainmember','Repair and retune a weak member’s training','Improve and validate an individual component’s representation or training discipline before building a blend around it or increasing its contribution.')],[
  C('The metric is still improving at the training cap or extra epochs have started to overfit.','Inspect held-out learning curves and saved adjacent-epoch checkpoints.',duration=.9),
  C('Stopping occurs during noisy short plateaus, especially with a reduced learning rate.','Inspect the patience window, curve fluctuations, and later improvements in longer runs.',patience=1),
  C('Several compatible trained states already exist with different validation results.','Inspect checkpoint metadata, stage provenance, and fixed-pipeline scores.',checkpoint=1),
  C('Several late states of one compatible architecture are available and individual weights remain noisy.','Inspect training continuity, parameter keys, and validation behavior of those states.',swa=.8),
  C('A weak ensemble component lacks the fold discipline or tuning used by the stronger components.','Audit its split indices, saved OOF predictions, data loading, and training configuration.',trainmember=1)])],[
 C('The current predictor’s inductive bias or pretraining domain appears unsuitable.','Compare standalone errors, data modality, and available alternative predictors.',modelclass=.9),
 C('The backbone is useful but pooling or the output head is limiting.','Review architecture and head-only ablation results.',headchoice=.9),
 C('A tree model’s capacity, regularization, or round budget is implicated by learning curves.','Inspect tree fit and validation traces.',treefit=1),
 C('Neural optimization or objective mismatch is visible in training diagnostics.','Inspect optimizer, loss, activation, and rate traces.',neuralfit=1),
 C('The available trained states differ more than recent architecture changes or stopping is poorly configured.','Review checkpoint scores, training curves, and component-training audits.',trainingselection=.9)])
ensemble=D('ensemble','Change prediction combination','Choose how to obtain complementary predictions and combine them using held-out evidence.',
 'Which limitation in the current ensemble should be addressed next?',[
 D('membership','Change the active member set','Choose an inclusion experiment rather than changing weights at the same time.',
  'What membership experiment is justified by the existing component evidence?',[
  L('addmember','Trial one additional candidate','Add one validated prediction source to the fixed baseline blend and retain it only if its marginal contribution generalizes.'),
  L('replace','Replace one ensemble slot','Swap a single member or checkpoint group while freezing other members and the initial combination rule.'),
  L('members','Ablate or prune active members','Remove one active prediction source at a time, recompute the valid blend, and retain removals supported by held-out results.'),
  L('solo','Compare a member with the ensemble','Score individual members and the fixed ensemble on the same rows to establish whether combining them adds value.'),
  L('restoreensemble','Restore a proven diverse blend','Re-enable the previously validated contributing members after pruning or an isolated probe degraded performance.')],[
  C('A compatible unused candidate has reasonable standalone predictions and potentially different residual errors.','Inspect aligned candidate predictions, standalone scores, residual correlations, and earlier inclusion trials.',addmember=.9),
  C('A stronger or different candidate is available for a known weak or redundant slot.','Compare the current slot and replacement on the same held-out rows and inspect their correlations with the rest of the blend.',replace=.9),
  C('An active member has repeatedly worsened the fixed blend or seems redundant.','Read leave-one-out results and per-member residual correlations using unchanged weights or renormalized baselines.',members=1,addmember=-.4),
  C('No same-split comparison establishes that the ensemble beats its strongest member.','Inspect saved standalone and ensemble scores on identical examples.',solo=1),
  C('The current regression followed removal of members that previously had positive ablation evidence.','Compare member manifests before and after the regression and locate their validated prediction files.',restoreensemble=1,members=-.7)]),
 D('diversity','Choose a source of diversity','Choose how to generate a prediction source with a different error pattern.',
  'Which source of additional prediction diversity is available and underrepresented?',[
  L('diverse','Add a different model family','Generate compatible predictions from an underrepresented architecture or algorithm and test its contribution to the existing ensemble.'),
  L('diverserep','Add a different input representation','Train or load a model using a distinct feature set, modality, resolution, or preprocessing path and test its ensemble contribution.'),
  L('diversetarget','Add a different target encoding','Fit a model to an alternative valid target transformation and evaluate whether its aligned predictions complement existing members.'),
  L('seeds','Average independent training runs','Generate predictions from multiple independent training seeds and increase the count only while held-out gains persist.'),
  L('folds','Average more fold checkpoints','Include additional compatible held-out-fold models and compare the larger average with the existing fold set.'),
  L('foldsubset','Select a validated fold subset','Compare the full fold average with individually validated fold subsets, avoiding selection from tiny noisy score differences alone.')],[
  C('Most active members share one architecture or algorithm and their residuals are highly correlated.','Inspect the member manifest and held-out residual correlation matrix.',diverse=1),
  C('An available modality, feature set, or preprocessing variant is absent from current members.','Compare training representations and standalone validation results for the alternate path.',diverserep=.9),
  C('Different valid outcome transforms produce complementary residuals for the same task.','Inspect OOF predictions from existing transformed-target models and verify target-direction alignment.',diversetarget=.9),
  C('Training seeds produce substantial variance while architecture and fold setup remain fixed.','Compare saved independent-seed predictions and same-split score distributions.',seeds=1),
  C('Additional compatible fold checkpoints are unused and prior fold additions have improved validation.','Inspect fold coverage, checkpoint provenance, and the marginal-gain table.',folds=1),
  C('One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.','Check checkpoint metadata and fixed-pipeline full-versus-subset scores across held-out samples.',foldsubset=1,folds=-.6)]),
 D('weightchoice','Change blend weights','Choose a weighting rule supported by the strength and reliability of the available evidence.',
  'How should the active prediction sources be weighted?',[
  L('uniform','Use equal member weights','Use a simple equal-weight average as the validated baseline when quality differences or manual weight gains are unreliable.'),
  L('weights','Optimize fixed blend weights','Sweep fixed member weights on aligned held-out predictions, retuning after component changes and retaining only gains larger than evaluation noise.'),
  L('negative','Test signed blend coefficients','Compare allowing negative coefficients with a nonnegative blend under held-out evaluation.'),
  L('hierarchy','Weight model groups separately','Average folds or related members within each group, then blend group outputs so group size does not dictate influence.'),
  L('fixedweights','Replace unstable adaptive weights','Use fixed validated coefficients instead of weights estimated from a tiny or unstable inference batch.'),
  L('perclassweights','Test class-specific blend weights','Compare per-class weights with the global blend when component quality differs consistently by class.')],[
  C('Members have comparable quality and tuned weights have not reliably improved the simple average.','Compare uniform and tuned blend scores across the same held-out samples or repeated evaluations.',uniform=1,weights=-.5),
  C('Component quality differs reproducibly or a member’s predictions have changed since weights were tuned.','Inspect standalone scores, OOF residuals, and artifact versions relative to the saved weight configuration.',weights=1),
  C('A candidate’s residual contribution appears negatively correlated with the remaining blend’s error.','Compute conditional residual associations and inspect prior small signed-weight probes on held-out data.',negative=.8),
  C('Model families contain unequal numbers of folds or variants.','Count members per group and expand the current formula into effective per-family weights.',hierarchy=1),
  C('Current weights depend on statistics of a very small or varying inference sample.','Inspect weight-generation code and the sample count and variability used to estimate adaptive coefficients.',fixedweights=1),
  C('Different components consistently win on different classes with adequate validation examples.','Compare per-class held-out errors and sample counts across folds.',perclassweights=.9)]),
 D('blendscale','Change the combination domain','Choose what quantities to average without confusing rank information with calibrated probabilities.',
  'On what scale should member predictions be combined?',[
  L('rawblend','Preserve raw member magnitudes','Use raw-score averaging when validated magnitude information or downstream additive corrections would be lost by ranking.'),
  L('rank','Trial per-target rank averaging','Compare averaging member ranks with raw averaging on fixed members and recheck after changes to their output distributions.'),
  L('predscale','Normalize prediction columns','Fit standard or robust scaling on out-of-fold member predictions and apply the same transformation before recomputing blend weights.'),
  L('nonlinear','Trial a concave probability transform','Compare a power transform of each member’s probabilities before blending against the untransformed blend.'),
  L('logits','Average logits before softmax','Compare weighted logit averaging followed by softmax with the probability-average baseline.'),
  L('probability','Normalize each member before averaging','Apply the appropriate probability link to each member first and average the resulting distributions.')],[
  C('Useful score magnitudes or calibrated additive corrections are already validated.','Inspect raw-versus-rank comparisons and whether downstream adjustments rely on absolute scale.',rawblend=1,rank=-.6),
  C('The metric is rank-based and member score distributions differ in calibration or scale.','Read the metric definition and plot per-member prediction distributions and held-out raw/rank blend results.',rank=.9),
  C('Stacking or weighted blending mixes columns with different scales or outlier-heavy outputs.','Inspect OOF column quantiles and scaler fitting code; compare spread and outliers across members.',predscale=.9),
  C('Overconfident member probabilities cluster near the boundaries and their magnitude dominates the blend.','Inspect probability histograms and existing held-out power-transform comparisons.',nonlinear=.7),
  C('Compatible pre-softmax logits are available and the task scores categorical probability distributions.','Inspect saved logits, class ordering, and the distributional metric before comparing combination order.',logits=.8),
  C('Current inputs to an arithmetic average are unnormalized outputs although the blend is intended to average distributions.','Inspect each member’s output activation and row sums before averaging.',probability=1)]),
 D('metachoice','Change the stacking stage','Choose the appropriate level of learned combination for the available held-out data.',
  'What change to learned stacking is supported by the current evidence?',[
  L('stack','Compare learned stacking with averaging','Train a regularized stacker on aligned out-of-fold predictions and retain it only if it beats the validated fixed blend.'),
  L('metatype','Compare meta-learner families','Test a low-capacity linear, kernel, or tree meta-learner on the same held-out meta-features and revert added complexity that does not generalize.'),
  L('metatune','Tune meta-learner regularization','Search a bounded regularization and solver range for the existing meta-learner, comparing against a stable default.'),
  L('stackfeatures','Change the stacker’s feature set','Add or remove validated prediction, embedding, or auxiliary columns and retrain the stacker on the matching out-of-fold feature schema.')],[
  C('A fixed blend has plateaued and enough aligned held-out base predictions exist to fit a small combiner.','Inspect OOF coverage, row alignment, sample count relative to member count, and fixed-blend scores.',stack=.9),
  C('The current stacker’s model class underfits or a complex stacker overfits the available meta-data.','Compare training and held-out meta-model errors and prior family ablations.',metatype=.9),
  C('The current meta-learner’s best setting lies at a search boundary or coefficients are unstable.','Inspect search history, convergence warnings, and coefficient variation across folds.',metatune=.9),
  C('Useful new OOF outputs or embeddings exist, or the current meta-feature schema contains weak redundant columns.','Inspect feature provenance, alignment, correlations, and previous meta-feature ablations.',stackfeatures=1)])],[
 C('The value of specific active or candidate members is uncertain.','Inspect addition, replacement, and leave-one-out results.',membership=1),
 C('Current members have highly correlated errors and additional independent prediction sources are available.','Compare residual correlations with available architectures, representations, folds, and seeds.',diversity=1),
 C('Membership is stable but existing weights ignore quality differences or group sizes.','Inspect effective coefficients, member scores, and previous weighting comparisons.',weightchoice=1),
 C('Member output scales or activation order are inconsistent with the intended metric and blend.','Inspect score distributions, links, and the aggregation formula.',blendscale=1),
 C('Aligned OOF predictions support a learned combiner and its capacity or features remain unresolved.','Inspect OOF provenance and meta-model validation results.',metachoice=.9)])

outputs=D('outputs','Change inference or output adjustment','Choose an inference-time action after verifying that the base predictions are correct.',
 'What residual prediction problem can be addressed without changing the base training data?',[
 D('inferenceviews','Change inference averaging','Choose whether variation across inference passes should be introduced or eliminated.',
  'Which inference-pass policy fits the task and current stochastic behavior?',[
  L('tta','Compare valid test-time views','Average predictions over justified flips, crops, channel symmetries, or resolutions and compare with a fixed single-view baseline for each model.'),
  L('mcdropout','Trial stochastic dropout inference','Average genuinely stochastic dropout-enabled passes and compare against deterministic evaluation without assuming configuration dropout is active.'),
  L('deterministic','Make inference deterministic','Disable unintended stochastic transforms and dropout, pin random sources, and verify repeatable predictions before comparing models.')],[
  C('The task has label-preserving transformations represented by the trained model.','Inspect domain symmetries, training augmentations, and prior transformed-view validation results.',tta=1),
  C('A small noisy task may benefit from stochastic head averaging and dropout can be activated deliberately.','Inspect model mode and verify that repeated dropout-enabled passes actually vary while other layers remain appropriate for inference.',mcdropout=.7),
  C('Repeated inference changes scores unexpectedly or dropout settings are being tuned while inactive.','Compare identical-run predictions and inspect evaluation mode, random transforms, seeds, and dynamic batching.',deterministic=1,mcdropout=-.5)]),
 D('calibration','Change output calibration','Choose an adjustment justified by the meaning and observed bias of the predictions.',
  'What systematic output mismatch should be corrected?',[
  L('bias','Correct a validated prediction offset','Estimate a damped bias or reference-example correction from held-out evidence and compare it with the unshifted output.'),
  L('logitscale','Tune logit temperature before blending','Compare temperature-scaled component probabilities in the complete blend, distinguishing calibration effects from unchanged standalone ranks.'),
  L('classcalibrate','Reweight class probabilities','Test per-class probability multipliers followed by row normalization against the unadjusted categorical distribution.'),
  L('normalizeout','Enforce the required output range','Apply only the required range or probability-simplex normalization, avoiding an extra softmax on already normalized probabilities.'),
  L('rawoutput','Keep the raw ordered predictions','Remove unvalidated clipping or scaling when it adds no useful information to the metric or disrupts a downstream mapping.')],[
  C('Held-out regression residuals show a stable offset or a reliable reference example exposes one.','Inspect signed residual means across folds and reference-example prediction error.',bias=.9),
  C('A component’s bounded activation compresses its contribution to a heterogeneous blend.','Inspect pre-activation distributions and held-out blended performance across existing temperature settings.',logitscale=.8),
  C('Class probability mass is systematically biased on a representative validation set.','Compare predicted and observed class distributions and per-class calibration diagnostics.',classcalibrate=.9),
  C('The task requires bounded values or row-normalized probabilities and current outputs violate that contract.','Read the output requirements and compute ranges and row sums after every activation.',normalizeout=1),
  C('Only ordering is scored and added scaling or clipping has no validated benefit.','Inspect the metric’s invariances and compare rank order before and after current transforms, including ties.',rawoutput=1,normalizeout=-.4)]),
 D('discreteoutput','Change output granularity','Choose how to handle discrete labels and ties without collapsing informative rankings.',
  'What should be done about discreteness or ties in the predictions?',[
  L('discretize','Map predictions to label levels','Compare per-target thresholds or quantile mapping to observed label support with continuous predictions on held-out data.'),
  L('degenerate','Fall back for collapsed columns','Detect columns made constant by discretization and preserve their original continuous predictions.'),
  L('ties','Test tie handling explicitly','Compare deterministic tie preservation with a tightly bounded tie-breaking probe only when the metric’s tie treatment makes it justified.')],[
  C('Targets occupy a small set of repeated levels while model outputs are fully continuous.','Inspect unique target values and their frequencies by output column and the metric’s treatment of tied ranks.',discretize=1),
  C('Existing binning collapses one or more prediction columns to a constant.','Count distinct values and variance per column after binning and compare with the raw outputs.',degenerate=1,discretize=-.7),
  C('Exact prediction ties are common and their treatment can change the scored ordering.','Inspect tied-value counts and the metric implementation, then check existing tie-preserving and tie-breaking comparisons.',ties=.8)]),
 D('correctionrules','Change structured output corrections','Choose a correction only when the auxiliary evidence exists at prediction time.',
  'Which structured correction, if any, has supporting evidence?',[
  L('auxcorrection','Use a validated auxiliary prediction','Test confidence-gated or additive adjustments from a compatible auxiliary classifier or second head on the final prediction scale.'),
  L('rules','Apply a high-precision metadata rule','Test a narrowly supported metadata-based adjustment for specific targets and reject broader heuristics that disrupt correct ordering.'),
  L('postablate','Remove or restore an output correction','Ablate the existing post-processing while holding models fixed, restoring it only when its contribution remains validated.')],[
  C('An auxiliary classifier or head gives held-out information not captured by the main prediction.','Inspect its confidence, error correlation, and previously tested correction magnitudes on aligned rows.',auxcorrection=.9),
  C('A prediction-time metadata condition almost determines a particular target in training and held-out examples.','Cross-tabulate the condition and target by split and inspect exceptions and distribution shift.',rules=.9),
  C('The current post-processing was tuned for older checkpoints or its contribution is unverified.','Compare artifact versions and fixed-model correction-on versus correction-off results.',postablate=1)])],[
 C('Validated symmetries or unintended stochastic inference could explain residual variance.','Inspect transforms, evaluation mode, and repeated prediction files.',inferenceviews=1),
 C('Prediction bias, scale, or probability mass conflicts with the output requirements or validation labels.','Inspect residuals, calibration plots, ranges, and row sums.',calibration=1),
 C('Discrete target support or degenerate ties affect the ranking metric.','Inspect target levels and raw/post-processed prediction uniqueness.',discreteoutput=1),
 C('Auxiliary predictions or reliable metadata support a targeted correction.','Inspect held-out conditional errors and correction ablations.',correctionrules=.9)])

root=D('root','Improve the solution','Choose the next intervention according to the strongest observable limitation, then revisit the tree after evaluating it.',
 'what can I change to improve my solution?',[assessment,correctness,execution,features,supervision,model,ensemble,outputs],[
 C('Current scores cannot distinguish model changes because splits, metrics, or experiments are unreliable.','Inspect split overlap, scoring code, version diffs, and repeated-run score variation.',assessment=1,ensemble=-.3),
 C('Predictions fail basic validity or do not match the trained pipeline.','Inspect loading diagnostics, input/output IDs, prediction ranges, and train/inference configurations.',correctness=1,model=-.5),
 C('Correct runs are blocked by memory, session limits, or repeated expensive work.','Use runtime logs and memory profiles to locate the limiting stage.',execution=1),
 C('Available task-relevant information is absent, distorted, or diluted in current inputs.','Compare raw data with feature tensors and existing feature or modality ablations.',features=.9),
 C('Label quality, data coverage, censoring, or sample weighting limits the training signal.','Inspect label distributions, event indicators, data provenance, and quality-stratified errors.',supervision=.9),
 C('Learning curves or controlled single-model experiments implicate capacity, objective, or optimization.','Inspect train/validation curves and model-family or head comparisons.',model=1),
 C('Correct aligned predictions from multiple sources show potentially complementary errors.','Inspect OOF provenance, standalone scores, residual correlations, and current blend ablations.',ensemble=1),
 C('Valid base predictions retain an observable calibration, granularity, or inference-view mismatch.','Inspect held-out calibration, target support, domain symmetries, and current post-processing ablations.',outputs=.9)])

used=set(LEAVES)
expected=set(A.values())-{'unassigned'}
assert used==expected,('missing leaf definitions',expected-used,'unused definitions',used-expected)
keyids={}; nodes={}
def identify(n,path):
 n['id']=path;keyids[n['_key']]=path
 for i,c in enumerate(n['children'],1):identify(c,f'{path}.{i}')
identify(root,'T')
def finish(n):
 key=n.pop('_key')
 if n['children']:
  checks=DECISIONS[key]
  childids={c['id'] for c in n['children']}
  out=[]
  for c in checks:
   mapped={keyids[k]:v for k,v in c['pushes'].items()}
   assert set(mapped)<=childids,(key,c)
   out.append({**c,'pushes':mapped})
  assert out,key
  nodes[n['id']]={'groups':[{'under':'WHAT FITS THIS CASE?','checks':out}]}
 for c in n['children']:finish(c)
finish(root)
root['unassigned']=[{'item':X[n]['id'],'reason':'Configures notebook progress-bar rendering and registration; it changes presentation rather than predictive performance or experimental validity.'} for n,c in sorted(A.items()) if c=='unassigned']
OUT=BASE/'output'
(OUT/'tree.json').write_text(json.dumps(root,ensure_ascii=False,indent=2)+'\n')
(OUT/'desiderata.json').write_text(json.dumps({'nodes':nodes},ensure_ascii=False,indent=2)+'\n')
def countitems(n):return len(n.get('items',[]))+sum(countitems(c) for c in n['children'])
counts=[(c['id'],c['name'],countitems(c)) for c in root['children']]
notes='''# Clustering and interpretation

Read all items through indexed batches of general goals/actions, supplemented by context samples across action clusters and instance evidence for ambiguous cases. Placement follows the principal reusable intervention, not competition, expert, chronology, or incidental code terms. Repeated tests share a leaf even when the winning setting differed. Bundled rationales have one home; their subordinate edits are not duplicated.

The tree chooses the **next intervention**, not a complete workflow: sibling choices are alternative uses of the next experiment. Several may ultimately be useful, but there is no required traversal order. A leaf describes one reusable intervention or controlled comparison, not a claim that it always improves performance. All action leaves have data support; decision wording and diagnostic synthesis are editorial. Positive/negative weights are qualitative routing hints, not fitted probabilities or causal effect sizes. Checks use available data, code, artifacts, or earlier results; missing evidence is not a YES.

Uncertainty is greatest for bundled architecture/preprocessing changes, tiny public-score gains, and unpinned external checkpoints. Identical-code reruns can include artifact changes, so a score shift alone is not proof of stochastic noise. Rank transforms, folds, additional models, filtering, and discretization have conflicting outcomes; the tree retains controlled comparisons and regression paths. Monotone transformations cannot improve a standalone pure rank score without changing ties; their possible effects before blending are different. Local held-out evidence is preferred to repeatedly tuning on a tiny public leaderboard.

The broadest decisions are the root’s bottleneck selection and input-representation selection: independent causes can coexist, so they route the next action rather than identify an exclusive cause. “Recover the last validated configuration” and “Ablate or prune active members” pool many implementations because the decision and context recur. Training-family swaps and coherent multi-change baseline replacements have weaker attribution than single-factor probes. One progress-bar-only item is unassigned as bookkeeping.

## Items per top-level branch

'''
notes+='\n'.join(f'- {i} — {name}: {n}' for i,name,n in counts)
notes+='\n\nTotal: '+str(sum(n for _,_,n in counts))+' placed; '+str(len(root['unassigned']))+' unassigned. `validate_output.py` checks exact coverage, structure, references, and check schemas. `build_tree.py` records the reproducible index-to-leaf mapping.\n'
(OUT/'notes.md').write_text(notes)
print('Built',len(LEAVES),'leaves;',len(DECISIONS),'decisions')
