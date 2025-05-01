from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import ElectionFraudDetectionResponse, ElectionFraudDetectionRequest
import pandas as pd
from model import stacked_model_predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validate_vote/", response_model=ElectionFraudDetectionResponse)
def validate_vote(data: ElectionFraudDetectionRequest):
    try:
        fraud_pred = stacked_model_predict(data)
        if fraud_pred:
            return ElectionFraudDetectionResponse(
                Address=fraud_pred['Address'],
                is_fraud=fraud_pred['is_fraud']
            )
        else:
            raise HTTPException(status_code=400, detail="Prediction failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))