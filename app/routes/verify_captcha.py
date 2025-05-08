from fastapi import APIRouter
from fastapi import HTTPException
from app.schemas.recaptcha_response import CaptchaRequest
import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Use reCAPTCHA secret key in .env file
SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

router = APIRouter()

@router.post("/verify-captcha")
async def verify_captcha(data: CaptchaRequest):
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": SECRET_KEY,
            "response": data.token
        }
    )
    result = response.json()
    return result