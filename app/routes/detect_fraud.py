from fastapi import APIRouter
from fastapi import HTTPException
from app.schemas.fraud_detection import ElectionFraudDetectionResponse, ElectionFraudDetectionRequest
import pandas as pd
from app.utils.model import stacked_model_predict

router = APIRouter()

@router.post("/validate_vote/", response_model=ElectionFraudDetectionResponse)
def validate_vote(data: ElectionFraudDetectionRequest):
    try:
        data = pd.DataFrame({
            "Address": [data.Address],
            "Time Diff between first and last (Mins)": [data.Time_Diff_between_first_and_last_Mins],
            "Face Attempts": [data.Face_Attempts],
            "Detected As a Robot At Least Once": [data.Detected_As_a_Robot_At_Least_Once],
            "Face Match Percentage": [data.Face_Match_Percentage],
            "Liveness Score of The Face": [data.Liveness_Score_of_The_Face]
        })

        print("Data received for prediction:", data, type(data))

        fraud_pred = stacked_model_predict(data)
        if fraud_pred:
            return ElectionFraudDetectionResponse(
                Address=fraud_pred['Address'][0],
                is_fraud=fraud_pred['is_fraud'][0]
            )
        else:
            raise HTTPException(status_code=400, detail="Prediction failed.")
        
    except Exception as e:
        print("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
