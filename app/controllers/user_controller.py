from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.image_preprocess import preprocess_image_from_path
import os
from typing import Optional
import aiofiles
import uuid
import zlib  # Add this import for compression

async def register_user(
    db: Session,
    wallet_address: str,
    first_name: str,
    last_name: str,
    email: str,
    biometric_image: UploadFile
) -> User:
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.wallet_address == wallet_address).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this wallet address already exists")

        # Check if email is already registered
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create temporary file for biometric image
        temp_filename = f"temp_{uuid.uuid4()}.png"
        try:
            # Save uploaded file temporarily
            async with aiofiles.open(temp_filename, 'wb') as out_file:
                content = await biometric_image.read()
                await out_file.write(content)

            # Process the image
            img_array = preprocess_image_from_path(temp_filename)
            
            # Compress the biometric data before storing
            compressed_data = zlib.compress(img_array.tobytes())
            
            # Create new user
            new_user = User(
                wallet_address=wallet_address,
                first_name=first_name,
                last_name=last_name,
                email=email,
                biometric_data=compressed_data  # Store compressed data
            )

            # Add to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_by_wallet(db: Session, wallet_address: str) -> Optional[User]:
    return db.query(User).filter(User.wallet_address == wallet_address).first()

async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first() 