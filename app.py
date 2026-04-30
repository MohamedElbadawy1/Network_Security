import sys
import os
import fastapi
import pymongo

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline
from NetworkSecurity.utlis.main_utils.utils import load_object
from NetworkSecurity.utlis.ml_utils.model.estimator import NetworkModel

from NetworkSecurity.Constants.training_pipeline import( DATA_INGESTION_COLLECTION_NAME,
                                                         DATA_INGESTION_DATABASE_NAME)

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training Is Sucessfull")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request:Request, file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_models/preprocessor.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor, final_model)
        logging.info(df.head())
        y_pred = network_model.predict(df)
        logging.info(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(index=False, classes='table table-striped')
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=table_html)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)