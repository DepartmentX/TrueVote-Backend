from fastapi import FastAPI
from schema import ElectionFraudDetectionResponse, ElectionFraudDetectionRequest
import pandas as pd
from model import stacked_model_predict

app = FastAPI()

@app.post("/validate_vote/", response_model=ElectionFraudDetectionResponse)
def validate_vote(data: ElectionFraudDetectionRequest):
    fraud_pred = stacked_model_predict(data)
    if fraud_pred:
        return ElectionFraudDetectionResponse(Address=fraud_pred['Address'], is_fraud=fraud_pred['is_fraud'])
    else:
        raise ValueError("Invalid data format or prediction failed.")
    

# Test the API endpoint

data_dict = {
  "Address": "0x3f5CE5FBFe3E9af3971dD833D26BA9b5C936f0bE",
  "Time Diff between first and last (Mins)": 12.0,
  "Face Attempts": 2,
  "Detected As a Robot At Least Once": 0,
  "Face Match Percentage": 94.2,
  "Liveness Score of The Face": 0.93
}

data = ElectionFraudDetectionRequest(**data_dict)


    
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.post("/validate_vote/", json=data_dict)
print(response.json())

