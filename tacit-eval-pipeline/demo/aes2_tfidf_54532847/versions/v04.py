# %% [1]
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import cohen_kappa_score
import gc

# %% [2]
train = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv")

# %% [3] markdown
# # Evaluation

# %% [4]
train_X, test_X, train_y, test_y = train_test_split(train[['full_text']], train['score'], test_size=0.3)

print(f"train shape: {train_X.shape}, test shape: {test_X.shape}")

# %% [5]
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3), 
    lowercase=False, 
    sublinear_tf=True, 
    analyzer='word',
    strip_accents='unicode',
    stop_words='english'
)

tf_train = vectorizer.fit_transform(train_X['full_text'])
tf_test = vectorizer.transform(test_X['full_text'])

# %% [6]
"""
loss{‘hinge’, ‘log_loss’, ‘modified_huber’, ‘squared_hinge’, ‘perceptron’, ‘squared_error’, ‘huber’, ‘epsilon_insensitive’, ‘squared_epsilon_insensitive’}, default=’hinge’
The loss function to be used.

‘hinge’ gives a linear SVM.

‘log_loss’ gives logistic regression, a probabilistic classifier.

‘modified_huber’ is another smooth loss that brings tolerance to outliers as well as probability estimates.

‘squared_hinge’ is like hinge but is quadratically penalized.

‘perceptron’ is the linear loss used by the perceptron algorithm.

The other losses, ‘squared_error’, ‘huber’, ‘epsilon_insensitive’ and ‘squared_epsilon_insensitive’ are designed for regression but can be useful in classification as well; see SGDRegressor for a description.

"""

from sklearn.calibration import CalibratedClassifierCV

def init_model():
    clf_sgd = SGDClassifier(max_iter=8000, tol=1e-4, loss="modified_huber") 
    clf_sgd2 = CalibratedClassifierCV(SGDClassifier(max_iter=8000, tol=1e-4, loss="hinge"), cv=3, method='sigmoid')
    clf_sgd3 = SGDClassifier(max_iter=8000, tol=2e-4, loss="log_loss")
#     clf_nb = MultinomialNB(alpha=0.02)

    ensemble = VotingClassifier(
        estimators=[
            ('sgd', clf_sgd), # 0.572
            ('sgd2', clf_sgd2), # 0.576
            ('sgd3', clf_sgd3),  # 0.580
#             ('nb', clf_nb),  # 0.413
#             ('lr', clf_lr)
        ],
        voting='soft', 
        weights=[0.4, 0.5, 0.1],
        n_jobs=-1)
    return ensemble

# %% [7]
model = init_model()
model.fit(tf_train, train_y)
gc.collect()
preds = np.argmax(model.predict_proba(tf_test), axis=1) + 1

kappa_score = cohen_kappa_score(test_y, preds, weights='quadratic')
print("validation kappa score:", kappa_score)

# %% [8] markdown
# # Train

# %% [9]
test = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

# %% [10]
tf_train = vectorizer.fit_transform(train['full_text'])
tf_test = vectorizer.transform(test['full_text'])

# %% [11]
model = init_model()
model.fit(tf_train, train['score'])

print(gc.collect())
preds = np.argmax(model.predict_proba(tf_test), axis=1) + 1

# %% [12]
sub['score'] = preds
sub.to_csv('submission.csv', index=False)
display(sub.head())
