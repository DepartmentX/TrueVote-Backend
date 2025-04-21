from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from schema import ElectionFraudDetectionResponse
from model import stacked_model_predict

app = APIRouter()

@app.get("/validate_vote/{data}", response_model=ElectionFraudDetectionResponse)
def validate_vote(data):
    fraud_pred = stacked_model_predict(data)
    if fraud_pred:
        return ElectionFraudDetectionResponse(Address=fraud_pred['Address'], is_fraud=fraud_pred['is_fraud'])
    else:
        raise ValueError("Invalid data format or prediction failed.")