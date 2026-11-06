# %% [1]
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import cohen_kappa_score
from sklearn.calibration import CalibratedClassifierCV
import gc

# %% [2]
SEED = 1124
ONLINE = True
CV = 3

# %% [3]
data = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv")

# %% [4] markdown
# # Evaluation

# %% [5]
def init_model():
    clf_sgd = SGDClassifier(max_iter=10000, tol=1e-4, loss="modified_huber") 
#     clf_sgd2 = CalibratedClassifierCV(SGDClassifier(max_iter=8000, tol=1e-4, loss="hinge"), cv=3, method='sigmoid')
#     clf_sgd3 = SGDClassifier(max_iter=8000, tol=2e-4, loss="log_loss")
#     clf_nb = MultinomialNB(alpha=0.02)

    ensemble = VotingClassifier(
        estimators=[
            ('sgd', clf_sgd), # 0.572
#             ('sgd2', clf_sgd2), # 0.576
#             ('sgd3', clf_sgd3),  # 0.580
#             ('nb', clf_nb),  # 0.413
#             ('lr', clf_lr)
        ],
        voting='soft', 
#         weights=[0.4, 0.5, 0.1],
        n_jobs=-1)
    return ensemble

# %% [6]
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3), 
    lowercase=False, 
    sublinear_tf=True, 
    analyzer='word',
    strip_accents='unicode',
#     stop_words='english'
)

tf_data = vectorizer.fit_transform(data['full_text'])

# %% [7]
%%time
if not ONLINE:
    metrics = pd.DataFrame(np.zeros((1, CV)), columns=[f'kappa_{i}' for i in range(1, CV+1)])
    kf = KFold(n_splits=CV)

    for i, (train_idx, val_idx) in enumerate(kf.split(tf_data)):
        print("Training fold", i+1)
        train_X = tf_data[train_idx]
        train_y = data['score'].iloc[train_idx]
        val_X = tf_data[val_idx]
        val_y = data['score'].iloc[val_idx]

        model = init_model()
        model.fit(train_X, train_y)
        preds = np.argmax(model.predict_proba(val_X), axis=1) + 1

        kappa_score = cohen_kappa_score(val_y, preds, weights='quadratic')
        metrics.loc[0, f'kappa_{i+1}'] = kappa_score
    metrics['kappa_mean'] = metrics.mean(axis=1)
    display(metrics)

# %% [8] markdown
# # Train

# %% [9]
test = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

# %% [10]
if ONLINE:
    print("Online submission")
    tf_test = vectorizer.transform(test['full_text'])
    model = init_model()
    model.fit(tf_data, data['score'])

    print(gc.collect())
    preds = np.argmax(model.predict_proba(tf_test), axis=1) + 1
    
    sub['score'] = preds
    sub.to_csv('submission.csv', index=False)
    display(sub.head())
