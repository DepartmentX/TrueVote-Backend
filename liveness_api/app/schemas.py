from pydantic import BaseModel

class PredictionResponse(BaseModel):
    prediction: float
    label: str
