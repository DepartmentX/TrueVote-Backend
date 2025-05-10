from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.image_preprocess import preprocess_image_from_path
import os
from typing import Optional
import aiofiles
import uuid
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, BotoCoreError
import face_recognition
from app.utils.image_preprocess import preprocess_image_from_path
from app.models.model import predict

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

async def register_user(
    db: Session,
    wallet_address: str,
    first_name: str,
    last_name: str,
    email: str,
    biometric_image: UploadFile
) -> User:
    try:
        print(f"Registering user with wallet address: {wallet_address}")
        # Check if user already exists
        existing_user = db.query(User).filter(User.wallet_address == wallet_address).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this wallet address already exists")

        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Save file temporarily
        temp_filename = f"temp_{uuid.uuid4()}.png"
        try:
            async with aiofiles.open(temp_filename, 'wb') as out_file:
                content = await biometric_image.read()
                await out_file.write(content)

            # Upload to S3
            s3_key = f"biometrics/{uuid.uuid4()}.png"
            with open(temp_filename, "rb") as file_data:
                print(f"Uploading {temp_filename} to S3 bucket {S3_BUCKET_NAME} with key {s3_key}")
                s3_client.upload_fileobj(file_data, S3_BUCKET_NAME, s3_key)
                print(f"Uploaded {temp_filename} to S3 bucket {S3_BUCKET_NAME} with key {s3_key}")
            # Optional: Generate public URL
            s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"


            new_user = User(
                wallet_address=wallet_address,
                first_name=first_name,
                last_name=last_name,
                email=email,
                biometric_image_url=s3_url  # If you add this column to your User model
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    except (BotoCoreError, NoCredentialsError) as aws_error:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"AWS error: {str(aws_error)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def biometric_image_verify(
    db: Session,
    wallet_address: str,
    biometric_image: UploadFile
) -> dict:
    try:
        # Check if user exists
        user = db.query(User).filter(User.wallet_address == wallet_address).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        stored_image_url = user.biometric_image_url
        if not stored_image_url:
            raise HTTPException(status_code=404, detail="Biometric image not found for the user")

        stored_temp_filename = f"stored_temp_{uuid.uuid4()}.png"
        uploaded_temp_filename = f"uploaded_temp_{uuid.uuid4()}.png"

        try:
            # Download the stored image from S3
            s3_key = stored_image_url.split(f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/")[-1]
            s3_client.download_file(S3_BUCKET_NAME, s3_key, stored_temp_filename)

            # Save the uploaded image temporarily
            async with aiofiles.open(uploaded_temp_filename, 'wb') as out_file:
                content = await biometric_image.read()
                await out_file.write(content)

            # Preprocess both images
            preprocessed_stored = stored_temp_filename  # Ensure this is a file path
            preprocessed_uploaded = uploaded_temp_filename  # Ensure this is a file path

            # Compare the images
            comparison_result = compare_faces(preprocessed_stored, preprocessed_uploaded)

            if comparison_result['error']:
                raise HTTPException(status_code=400, detail=comparison_result['error'])

            check_spoofing_result = await check_spoofing(uploaded_temp_filename)

            if check_spoofing_result['label'] == "Spoof":
                raise HTTPException(status_code=400, detail="Spoofing detected")
            
            return {
                "wallet_address": wallet_address,
                "is_match": comparison_result['is_match'],
                "face_match_score": comparison_result['distance'],
                "spoofing_score": check_spoofing_result['prediction'],
            }

        finally:
            # Clean up the temporary files
            for file in [stored_temp_filename, uploaded_temp_filename]:
                if os.path.exists(file):
                    os.remove(file)

    except HTTPException as http_err:
        raise http_err  # Propagate HTTPException
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
def compare_faces(img_path1, img_path2, threshold=0.6):
    try:
        # Load images and extract face encodings
        img1 = face_recognition.load_image_file(img_path1)
        img2 = face_recognition.load_image_file(img_path2)

        enc1 = face_recognition.face_encodings(img1)
        enc2 = face_recognition.face_encodings(img2)

        # Check if faces are found in both images
        if not enc1 or not enc2:
            return {
                'distance': None,
                'is_match': False,
                'error': 'Face not found in one or both images'
            }

        # Calculate the face distance and compare
        distance = float(face_recognition.face_distance([enc1[0]], enc2[0])[0])  # Convert to Python float
        is_match = bool(distance < threshold)  # Convert to Python bool
        print(f"Distance: {distance}, Is Match: {is_match}")
        return {
            'distance': distance,
            'is_match': is_match,
            'error': None
        }

    except Exception as e:
        return {
            'distance': None,
            'is_match': False,
            'error': f"Error during face comparison: {str(e)}"
        }
    

async def get_user_by_wallet(db: Session, wallet_address: str) -> Optional[User]:
    return db.query(User).filter(User.wallet_address == wallet_address).first()



async def check_spoofing(image_path: str) -> dict:
    img_array = preprocess_image_from_path(image_path)
    prediction, label = predict(img_array)
    return {"prediction": float(prediction), "label": label}
