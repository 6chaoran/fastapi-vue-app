# FastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
# Model
import pickle
import numpy as np
import pandas as pd
import lightgbm as lgb
from utils import encode_cat_variables

# load encoder
with open('./saved_model/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)
# load model
model = lgb.Booster(model_file='./saved_model/model.txt')
fnames = model.feature_name()

# data model of predictors
class TitanicFeature(BaseModel):
    Age: int = Field(..., example=20)
    Pclass: int = Field(..., example=1)
    Sex: str = Field(..., example='male')
    SibSp: int = Field(..., example=1)
    Parch: int = Field(..., example=1)
    Fare: float = Field(..., example=120)
    Embarked: str = Field(..., example='S')


app = FastAPI()

# vue app URL
# load ui from app.html


@app.get("/app")
def read_index():
    return FileResponse("./app.html")

# POST method for model prediction


@app.post("/predict")
async def predict(payload: TitanicFeature):
    input_df = pd.DataFrame([payload.dict()])
    input_df_encoded, _ = encode_cat_variables(input_df, list(le.keys()), le)
    score = model.predict(input_df_encoded)[0]
    shap_values = model.predict(input_df_encoded, pred_contrib=True)[0]
    # remove the last term - bias
    shap_values = shap_values[:-1]
    # desc sort SHAP variables by absolute value
    shap_values = shap_values[np.argsort(-np.abs(shap_values))]
    shap_values = [
        {"name": fnames[i], "value": np.round(v, 4)} for i, v in enumerate(shap_values)
    ]
    return {
        'score': score,
        'shap_values': shap_values
    }
