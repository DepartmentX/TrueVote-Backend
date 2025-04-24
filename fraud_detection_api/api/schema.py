from pydantic import BaseModel, Field

class ElectionFraudDetectionResponse(BaseModel):
    Address: str
    is_fraud: bool

    class Config:
        from_attributes = True


class ElectionFraudDetectionRequest(BaseModel):
    Address: str
    Time_Diff_between_first_and_last_Mins: float = Field(..., alias="Time Diff between first and last (Mins)")
    Face_Attempts: int = Field(..., alias="Face Attempts")
    Detected_As_a_Robot_At_Least_Once: int = Field(..., alias="Detected As a Robot At Least Once")
    Face_Match_Percentage: float = Field(..., alias="Face Match Percentage")
    Liveness_Score_of_The_Face: float = Field(..., alias="Liveness Score of The Face")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True