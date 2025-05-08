from pydantic import BaseModel

class CaptchaRequest(BaseModel):
    token: str