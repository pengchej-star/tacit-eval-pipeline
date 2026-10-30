# %% [markdown]
# ## Import Libraries

# %%
import pandas as pd
import numpy as np
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score

# %%
# os.remove("/kaggle/working/submission.csv")
# os.remove("/kaggle/working/state.db")

# %% [markdown]
# ## Data exploration

# %%
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

# display datasets

train_df1 = pd.read_csv('/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv')

# %%
train_df1['score'].dtypes

# %%
train_df1.head(10)

# %%
train_df1['score'].value_counts()

# %%
submission = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
submission

# %%


# %% [markdown]
# ## Data Cleaning

# %%
train_df1['full_text'] = train_df1['full_text'].map(lambda x: re.sub('\n',' ',str(x)))

train_df1['full_text'] = train_df1['full_text'].map(lambda x: re.sub(r'[^\w\s]','',str(x)))  

train_df1['full_text'] = train_df1['full_text'].str.lower()  

train_df1['full_text'] = train_df1['full_text'].str.replace(r'\d+', '', regex=True) 

# %%
test_df1 = pd.read_csv('/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv')

# %%
test_df1['full_text'] = test_df1['full_text'].map(lambda x: re.sub('\n',' ',str(x)))

test_df1['full_text'] = test_df1['full_text'].map(lambda x: re.sub(r'[^\w\s]','',str(x)))

test_df1['full_text'] = test_df1['full_text'].str.lower()

test_df1['full_text'] = test_df1['full_text'].str.replace(r'\d+', '', regex=True) 

# %%
essay_id_test_df1 = test_df1['essay_id']  

# %%
type(essay_id_test_df1)

# %%
essay_id_test_df1

# %% [markdown]
# ## Splitting data into training and testing sets

# %%
x = train_df1[['full_text', 'essay_id']]  
y = train_df1.iloc[:, 2:8] 

# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=123)  

# %%
y_train['score'].value_counts()

# %%
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

# %% [markdown]
# ## Instantiate TF-IDF VEctorizer 

# %%
text_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='ascii',
    analyzer='word',
    token_pattern=r'\w+',  
    ngram_range=(1,2),
    max_features=100000,
    min_df=5)

# %%
X_train_features = text_vectorizer.fit_transform(X_train['full_text'])

# %% [markdown]
# ## Train features into a Ridge regressor (score treated as ordinal/continuous)

# %%
from sklearn.linear_model import Ridge

#transform the test features to sparse matrix
test_features = text_vectorizer.transform(X_test['full_text'])

clf = Ridge(alpha=1.0)
clf.fit(X_train_features, y_train['score'])  
y_pred = np.clip(np.round(clf.predict(test_features)), 1, 6).astype(int)  

# %% [markdown]
# ## Model Evaluation

# %%
print(confusion_matrix(y_test['score'], y_pred))

# %%
print(classification_report(y_test['score'], y_pred))

# %%
kappa = cohen_kappa_score(y_test['score'], y_pred, weights='quadratic')  
print('Cohen\'s kappa score: ', kappa)  

# %% [markdown]
# ## Predict test features using the trained classifier (clf)

# %%
# selected_rows = train_df1.loc[train_df1['essay_id'].isin(essay_id_test_df1)]

# selected_y_test = test_df1.loc[selected_rows.index] 

# sr_word_features = text_vectorizer.transform(selected_rows['full_text'])

st_features = text_vectorizer.transform(test_df1['full_text'])

# clf = make_pipeline(MaxAbsScaler(), SVC(C=2.0, kernel='rbf', gamma='scale', decision_function_shape='ovr', random_state=123, tol=1e-5, shrinking=True, verbose=True, break_ties=True))

# clf.fit(sr_word_features, selected_rows['score'])

test_predictions = np.clip(np.round(clf.predict(st_features)), 1, 6).astype(int)

# %% [markdown]
# ## Save submission into a CSV file

# %%
submission = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
submission['score'] = test_predictions
submission.to_csv("submission.csv", index=False)
print(submission.head())

# %%
submission.dtypes
