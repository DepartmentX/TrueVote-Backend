from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from schema import ElectionFraudDetectionResponse
import pandas as pd
from model import stacked_model_predict

app = APIRouter()

@app.get("/validate_vote/{data}", response_model=ElectionFraudDetectionResponse)
def validate_vote(data):
    fraud_pred = stacked_model_predict(data)
    if fraud_pred:
        return ElectionFraudDetectionResponse(Address=fraud_pred['Address'], is_fraud=fraud_pred['is_fraud'])
    else:
        raise ValueError("Invalid data format or prediction failed.")
    

print(validate_vote({
  "Address": "0x3f5CE5FBFe3E9af3971dD833D26BA9b5C936f0bE",
  "Time Diff between first and last (Mins)": 12,
  "Face Attempts": 5,
  "Detected As a Robot At Least Once": 0,
  "Face Match Percentage": 94.2,
  "Liveness Score of The Face": 0.93
}))