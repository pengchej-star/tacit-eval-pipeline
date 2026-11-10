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
    strip_accents='unicode'
)

tf_train = vectorizer.fit_transform(train_X['full_text'])
tf_test = vectorizer.transform(test_X['full_text'])

# %% [6]
def init_model():
#     clf = LogisticRegression(solver='liblinear', C=0.5)
    sgd_model = SGDClassifier(max_iter=10000, tol=1e-4, loss="modified_huber") 

    ensemble = VotingClassifier(
        estimators=[
            ('sgd', sgd_model)
        ],
        voting='soft', 
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
