# %% [markdown]
# # Imports and configs

# %%
import importlib.util, subprocess, sys
if importlib.util.find_spec("lifelines") is None:
    for w in ["autograd-1.7.0-py3-none-any.whl", "autograd-gamma-0.5.0.tar.gz", "interface_meta-1.3.0-py3-none-any.whl",
              "formulaic-1.0.2-py3-none-any.whl", "lifelines-0.30.0-py3-none-any.whl"]:
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", f"/kaggle/input/pip-install-lifelines/{w}"])

# %%
from lightgbm import LGBMRegressor, early_stopping, log_evaluation
from catboost import CatBoostRegressor, Pool
from xgboost import XGBRegressor
from sklearn.model_selection import KFold
from lifelines import KaplanMeierFitter
from sklearn.base import clone
from scipy.stats import rankdata 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import shutil
import optuna
import json
import glob
import os
import gc

warnings.filterwarnings("ignore")

# %%
class CFG:
    train_path = "/kaggle/input/equity-post-HCT-survival-predictions/train.csv"
    test_path = "/kaggle/input/equity-post-HCT-survival-predictions/test.csv"
    sample_sub_path = "/kaggle/input/equity-post-HCT-survival-predictions/sample_submission.csv"

    n_folds = 10
    seed = 42

# %% [markdown]
# # Loading data

# %%
train = pd.read_csv(CFG.train_path)
test = pd.read_csv(CFG.test_path)

# %%
cat_cols = train.select_dtypes("object").columns.tolist()

train[cat_cols] = train[cat_cols].astype("category")
test[cat_cols] = test[cat_cols].astype("category")

# %%
def transform_survival_probability(df, time_col='efs_time', event_col='efs'):
    kmf = KaplanMeierFitter()
    kmf.fit(df[time_col], df[event_col])
    y = kmf.survival_function_at_times(df[time_col]).values
    return y
    
train["y"] = transform_survival_probability(train, time_col='efs_time', event_col='efs')

# %%
X = train.drop(["efs", "efs_time", "y", "ID"], axis=1)
y = train[["efs", "efs_time", "y", "race_group", "ID"]]

X_test = test.drop("ID", axis=1)

# %% [markdown]
# # Data preprocessing

# %% [markdown]
# # Training base models

# %%
"""
To evaluate the equitable prediction of transplant survival outcomes,
we use the concordance index (C-index) between a series of event
times and a predicted score across each race group.
 
It represents the global assessment of the model discrimination power:
this is the model’s ability to correctly provide a reliable ranking
of the survival times based on the individual risk scores.
 
The concordance index is a value between 0 and 1 where:
 
0.5 is the expected result from random predictions,
1.0 is perfect concordance (with no censoring, otherwise <1.0),
0.0 is perfect anti-concordance (with no censoring, otherwise >0.0)

"""

import pandas as pd
import pandas.api.types
import numpy as np
from lifelines.utils import concordance_index

class ParticipantVisibleError(Exception):
    pass


def score(solution: pd.DataFrame, submission: pd.DataFrame, row_id_column_name: str) -> float:
    """
    >>> import pandas as pd
    >>> row_id_column_name = "id"
    >>> y_pred = {'prediction': {0: 1.0, 1: 0.0, 2: 1.0}}
    >>> y_pred = pd.DataFrame(y_pred)
    >>> y_pred.insert(0, row_id_column_name, range(len(y_pred)))
    >>> y_true = { 'efs': {0: 1.0, 1: 0.0, 2: 0.0}, 'efs_time': {0: 25.1234,1: 250.1234,2: 2500.1234}, 'race_group': {0: 'race_group_1', 1: 'race_group_1', 2: 'race_group_1'}}
    >>> y_true = pd.DataFrame(y_true)
    >>> y_true.insert(0, row_id_column_name, range(len(y_true)))
    >>> score(y_true.copy(), y_pred.copy(), row_id_column_name)
    0.75
    """
    
    del solution[row_id_column_name]
    del submission[row_id_column_name]
    
    event_label = 'efs'
    interval_label = 'efs_time'
    prediction_label = 'prediction'
    for col in submission.columns:
        if not pandas.api.types.is_numeric_dtype(submission[col]):
            raise ParticipantVisibleError(f'Submission column {col} must be a number')
    # Merging solution and submission dfs on ID
    merged_df = pd.concat([solution, submission], axis=1)
    merged_df.reset_index(inplace=True)
    merged_df_race_dict = dict(merged_df.groupby(['race_group']).groups)
    metric_list = []
    for race in merged_df_race_dict.keys():
        # Retrieving values from y_test based on index
        indices = sorted(merged_df_race_dict[race])
        merged_df_race = merged_df.iloc[indices]
        # Calculate the concordance index
        c_index_race = concordance_index(
                        merged_df_race[interval_label],
                        -merged_df_race[prediction_label],
                        merged_df_race[event_label])
        metric_list.append(c_index_race)
    return float(np.mean(metric_list)-np.sqrt(np.var(metric_list)))

# %%
class Trainer:
    def __init__(self, model, config=CFG):
        self.model = model
        self.config = config
        
    def train(self, X, y, X_test):       
        print(f"Training {self.model.__class__.__name__}\n")
                
        scores = []
        oof_preds = np.zeros(X.shape[0])
        test_preds = np.zeros(X_test.shape[0])
        
        split = KFold(n_splits=self.config.n_folds, random_state=self.config.seed, shuffle=True).split(X, y)
        for fold_idx, (train_idx, val_idx) in enumerate(split):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            y_preds, temp_test_preds, m = self._fit_predict(fold_idx, X_train, y_train, X_val, y_val, X_test)
            oof_preds[val_idx] = y_preds
            test_preds += temp_test_preds / self.config.n_folds
            scores.append(m)
            
            del X_train, y_train, X_val, y_val, y_preds, temp_test_preds
            gc.collect() 

        oof_preds_df = pd.DataFrame({"ID": y.ID, "prediction": oof_preds})            
        overall_score = score(y.copy(), oof_preds_df, "ID")
        average_score = np.mean(scores)
        
        print(f"\n------ Overall Score: {overall_score:.6f} - Average Score: {average_score:.6f}")
        
        return oof_preds, test_preds, scores
            
    def _fit_predict(self, fold_idx, X_train, y_train, X_val, y_val, X_test):
        if isinstance(self.model, LGBMRegressor):
            y_preds, test_preds = self._fit_lightgbm(X_train, y_train, X_val, y_val, X_test)
        elif isinstance(self.model, XGBRegressor):
            y_preds, test_preds = self._fit_xgboost(X_train, y_train, X_val, y_val, X_test)
        elif isinstance(self.model, CatBoostRegressor):
            y_preds, test_preds = self._fit_catboost(X_train, y_train, X_val, y_val, X_test)
        else:
            model = clone(self.model)
            model.fit(X_train, y_train["y"])
            y_preds = model.predict(X_val)
            test_preds = model.predict(X_test)

        y_preds_df = pd.DataFrame({"ID": y_val.ID, "prediction": y_preds})
        m = score(y_val.copy(), y_preds_df, "ID")
        
        if isinstance(self.model, (CatBoostRegressor, LGBMRegressor, XGBRegressor)):
            print(f"\n--- Fold {fold_idx + 1} - Score: {m:.6f}\n\n")
        else:
            print(f"--- Fold {fold_idx + 1} - Score: {m:.6f}")
            
        return y_preds, test_preds, m
        
    def _fit_lightgbm(self, X_train, y_train, X_val, y_val, X_test):
        model = clone(self.model)
        model.fit(
            X_train, 
            y_train["y"], 
            eval_set=[(X_val, y_val["y"])], 
            callbacks=[
                log_evaluation(period=200), 
                early_stopping(stopping_rounds=100)
            ]
        )
        
        y_preds = model.predict(X_val)
        test_preds = model.predict(X_test)
        del model
        
        return y_preds, test_preds
    
    def _fit_xgboost(self, X_train, y_train, X_val, y_val, X_test):
        model = clone(self.model)
        model.fit(
                X_train, 
                y_train["y"], 
                eval_set=[(X_val, y_val["y"])], 
                verbose=200
            )
        
        y_preds = model.predict(X_val)
        test_preds = model.predict(X_test)
        del model
        
        return y_preds, test_preds
    
    def _fit_catboost(self, X_train, y_train, X_val, y_val, X_test):
        model = clone(self.model)

        cat_cols = X_train.select_dtypes(include="category").columns.tolist()
        X_train, X_val, X_test = [d.copy() for d in (X_train, X_val, X_test)]
        for d in (X_train, X_val, X_test):
            d[cat_cols] = d[cat_cols].astype(str)
        if len(cat_cols) > 0:
            train_pool = Pool(X_train, y_train["y"], cat_features=cat_cols)
            val_pool = Pool(X_val, y_val["y"], cat_features=cat_cols)
            test_pool = Pool(X_test, cat_features=cat_cols)
        else:
            train_pool = Pool(X_train, y_train["y"])
            val_pool = Pool(X_val, y_val["y"])
            test_pool = Pool(X_test)

        model.fit(
            X=train_pool, 
            eval_set=val_pool, 
            verbose=200, 
            early_stopping_rounds=100,
            use_best_model=True
        )
        
        y_preds = model.predict(val_pool)
        test_preds = model.predict(test_pool)
        del model
        
        return y_preds, test_preds

# %%
scores = {}
oof_preds = {}
test_preds = {}

# %%
xgb_model = XGBRegressor(
    enable_categorical=True,
    device="cuda",
    max_depth=3,
    learning_rate=0.02,
    n_estimators=2000,
    subsample=0.8,
    colsample_bytree=0.5,
    min_child_weight=80,
    early_stopping_rounds=200,
    random_state=42,
)
xgb_trainer = Trainer(xgb_model)
oof_preds["XGBoost"], test_preds["XGBoost"], scores["XGBoost"] = xgb_trainer.train(X, y, X_test)

# %%
cb_model = CatBoostRegressor(
    iterations=3000,
    learning_rate=0.05,
    depth=6,
    l2_leaf_reg=5,
    task_type="CPU",
    random_seed=42,
)
cb_trainer = Trainer(cb_model)
oof_preds["CatBoost"], test_preds["CatBoost"], scores["CatBoost"] = cb_trainer.train(X, y, X_test)

# %%
lgb_model = LGBMRegressor(
    n_estimators=3000,
    learning_rate=0.02,
    num_leaves=15,
    max_depth=4,
    min_child_samples=40,
    subsample=0.8,
    subsample_freq=1,
    colsample_bytree=0.5,
    reg_lambda=1.0,
    random_state=42,
    verbose=-1,
)
lgb_trainer = Trainer(lgb_model)
oof_preds["LightGBM"], test_preds["LightGBM"], scores["LightGBM"] = lgb_trainer.train(X, y, X_test)

# %% [markdown]
# # Ensembling

# %%
weights = {"XGBoost": 1.0, "CatBoost": 1.0, "LightGBM": 1.0}

oof_ens = sum(w * rankdata(oof_preds[k]) for k, w in weights.items())
test_ens = sum(w * rankdata(test_preds[k]) for k, w in weights.items())

for k in weights:
    print(f"{k}: {score(y.copy(), pd.DataFrame({'ID': y.ID, 'prediction': oof_preds[k]}), 'ID'):.6f}")
print(f"Ensemble: {score(y.copy(), pd.DataFrame({'ID': y.ID, 'prediction': oof_ens}), 'ID'):.6f}")

# %% [markdown]
# # Creating a submission file

# %%
sub = pd.read_csv(CFG.sample_sub_path)
sub.prediction = test_ens
sub.to_csv("submission.csv", index=False)
sub.head()
