from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.controllers.user_controller import register_user, get_user_by_wallet, get_user_by_email
from app.utils.database import get_db
from typing import Optional
from pydantic import BaseModel, EmailStr

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
    user = await register_user(
        db=db,
        wallet_address=wallet_address,
        first_name=first_name,
        last_name=last_name,
        email=email,
        biometric_image=biometric_image
    )
    return user

@router.get("/wallet/{wallet_address}", response_model=UserResponse)
async def get_user_wallet(
    wallet_address: str,
    db: Session = Depends(get_db)
):
    """
    Get user details by wallet address
    """
    user = await get_user_by_wallet(db, wallet_address)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Get user details by email
    """
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 