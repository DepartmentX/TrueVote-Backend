from fastapi import APIRouter
from app.controllers.predict_controller import test_predict
from app.schemas.prediction_response import PredictionResponse

router = APIRouter()

@router.get("/predict", response_model=PredictionResponse)
async def predict():
    return await test_predict()
