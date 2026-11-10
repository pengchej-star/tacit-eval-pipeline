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
import random
import gc

# %% [2]
SEED = 1124
SUBMIT = True
EVALUATE = True
SGD_ITER = 15000
CV = 3

def seed_everything(seed=1111):
    random.seed(seed)
    np.random.seed(seed)

seed_everything(SEED)

# %% [3]
data = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv")

# %% [4] markdown
# # Train & Evaluation

# %% [5]
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3), 
    lowercase=False, 
    sublinear_tf=True, 
    analyzer='word',
    strip_accents='unicode',
#     stop_words='english'
)

tf_data = vectorizer.fit_transform(data['full_text'])

# %% [6]
def init_model(iterations):
    clf_sgd = SGDClassifier(max_iter=iterations, tol=1e-4, loss="modified_huber") 
    clf_sgd2 = CalibratedClassifierCV(SGDClassifier(max_iter=iterations, tol=1e-4, loss="hinge"), cv=3, method='sigmoid')
    clf_sgd3 = SGDClassifier(max_iter=iterations, tol=1e-4, loss="log_loss")
#     clf_nb = MultinomialNB(alpha=0.02)

    ensemble = VotingClassifier(
        estimators=[
            ('sgd', clf_sgd), 
            ('sgd2', clf_sgd2),
            ('sgd3', clf_sgd3),
        ],
        voting='soft', 
        weights=[0.4, 0.5, 0.1],
        n_jobs=-1)
    return ensemble

# %% [7]
%%time

# huber-sgd-10,000 => train: 0.611992 | test: 0.556
# huber+hinge+log_loss-10,000 => train: 0.6209 | test: 0.579
# 0.627078
if EVALUATE:
    metrics = pd.DataFrame(np.zeros((1, CV)), columns=[f'kappa_{i}' for i in range(1, CV+1)])
    kf = KFold(n_splits=CV, random_state=SEED, shuffle=True)

    for i, (train_idx, val_idx) in enumerate(kf.split(tf_data)):
        print("Training fold", i+1)
        train_X = tf_data[train_idx]
        train_y = data['score'].iloc[train_idx]
        val_X = tf_data[val_idx]
        val_y = data['score'].iloc[val_idx]

        model = init_model(SGD_ITER)
        model.fit(train_X, train_y)
        preds = np.argmax(model.predict_proba(val_X), axis=1) + 1

        kappa_score = cohen_kappa_score(val_y, preds, weights='quadratic')
        metrics.loc[0, f'kappa_{i+1}'] = kappa_score
    metrics['kappa_mean'] = metrics.mean(axis=1)
    display(metrics)

# %% [8] markdown
# # Inference

# %% [9]
test = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

# use test data for tokenizer
data_full = pd.concat([test[['full_text']], data[['full_text']]])
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3), 
    lowercase=False, 
    sublinear_tf=True, 
    analyzer='word',
    strip_accents='unicode'
)

vectorizer = vectorizer.fit(data_full['full_text'])

# %% [10]
if SUBMIT:
    print("Online submission")
    tf_test = vectorizer.transform(test['full_text'])
    model = init_model(SGD_ITER)
    model.fit(tf_data, data['score'])

    print(gc.collect())
    preds = np.argmax(model.predict_proba(tf_test), axis=1) + 1
    
    sub['score'] = preds
    sub.to_csv('submission.csv', index=False)
    display(sub.head())
