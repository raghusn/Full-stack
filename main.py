import json
import os
from io import StringIO
from typing import Optional, Any

import mlflow
from fastapi import FastAPI
from mlflow.deployments.cli import predictions_to_json
from mlflow.pyfunc.scoring_server import infer_and_parse_json_input
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository
from pydantic import BaseModel

# tested comments
#requirements databricks host in env , databricks token in mlflow

#add endpoint for rebuild
#init model's on server load
#checking security for endpoints
#container deployment


class Body(BaseModel):
    dataframe_records: list


mlflow.set_tracking_uri("databricks")

model_name = "VisitorFormSubmission"
model_stage = "Staging" # Should be either ‘Staging’ or ‘Production’

os.makedirs("model", exist_ok=True)
os.makedirs("model/VisitorFormSubmission", exist_ok=True)

app = FastAPI()
ml_model = None
input_schema: Optional[Any]


@app.get("/")
async def root():
    return {"message": "Model Api"}


def init():
    
    local_path = ModelsArtifactRepository(f'models:/{model_name}/{model_stage}').download_artifacts("", dst_path="../model/VisitorFormSubmission")
    
    global ml_model
    ml_model = mlflow.pyfunc.load_model(local_path)
    print(ml_model)
    global input_schema
    input_schema = ml_model.metadata.get_input_schema()
    #print(input_schema)


@app.post("/Model/")
async def predict(raw_data: list):
    if ml_model is None:
        init()

    json_data = json.dumps(raw_data)
    json_data = json.loads(json_data)
    
    predictions = ml_model.predict(json_data)
    print(predictions)
    result = StringIO()
    predictions_to_json(predictions, result)
    return result.getvalue()
