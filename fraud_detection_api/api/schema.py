from pydantic import BaseModel

class ElectionFraudDetectionResponse(BaseModel):
    Address: str
    is_fraud: bool

    class Config:
        from_attributes = True