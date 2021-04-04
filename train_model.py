import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import pickle
from utils import encode_cat_variables

fnames_cat = ['Pclass', 'Sex', 'Embarked']
fnames_num = ['Age', 'Fare', 'SibSp', 'Parch']
fnames = fnames_cat + fnames_num
data = pd.read_csv('./data/titanic.csv')
train, valid = train_test_split(data, stratify=data.Survived, train_size=0.7)

train, le = encode_cat_variables(train, fnames_cat)
valid, le = encode_cat_variables(valid, fnames_cat, le)

dtrain = lgb.Dataset(train[fnames].values, train.Survived)
dvalid = lgb.Dataset(valid[fnames].values, valid.Survived)

params = {
    'objective': 'binary',
    'eta': 0.1,
    'metric': 'auc'
}

model = lgb.train(params,
                  dtrain,
                  num_boost_round=100,
                  valid_sets=[dtrain, dvalid],
                  valid_names=['train', 'valid'],
                  feature_name=fnames,
                  categorical_feature=fnames_cat,
                  verbose_eval=10)

# save model & encoder
model.save_model(filename = "./saved_model/model.txt")
with open('./saved_model/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)