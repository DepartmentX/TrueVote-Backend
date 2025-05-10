from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.controllers.user_controller import register_user,biometric_image_verify, get_user_by_wallet
from app.utils.database import get_db
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from fastapi import Response

router = APIRouter(prefix="/api/users", tags=["users"])

class UserResponse(BaseModel):
    wallet_address: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse)
async def register(
    response: Response,
    wallet_address: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    biometric_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Register a new user with their details and biometric data
    """
    print(f"Registering user with wallet address: {wallet_address}")
    user = await register_user(
        db=db,
        wallet_address=wallet_address,
        first_name=first_name,
        last_name=last_name,
        email=email,
        biometric_image=biometric_image,
    )
    response.set_cookie(key="wallet_address", value=wallet_address, httponly=True)

    return user


class LoginRequest(BaseModel):
    address: str

@router.post("/login", response_model=UserResponse)
async def login(
    login_request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login a user with their wallet address
    """
    user = await get_user_by_wallet(
        db=db,
        wallet_address=login_request.address,
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    response.set_cookie(key="wallet_address", value=login_request.address, httponly=True)
    return user


@router.post("/biometric_auth", response_model=dict)
async def biometric_auth(
    wallet_address: str = Form(...),
    biometric_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    print(f"Biometric authentication for wallet address: {wallet_address}")
    print(f"Biometric image: {biometric_image.filename}")
    result = await biometric_image_verify(
        db=db,
        wallet_address=wallet_address,
        biometric_image=biometric_image
    )
    return result

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("wallet_address", path="/")
    return {"message": "Logged out"}
