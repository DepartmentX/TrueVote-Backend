import requests
import os

BASE_URL = "http://localhost:8000/api/users"

def test_registration():
    # Test data
    data = {
        "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    
    # Test image path - replace with your actual image path
    image_path = "path/to/your/test/image.png"
    
    # Prepare files
    files = {
        "biometric_image": ("image.png", open(image_path, "rb"), "image/png")
    }
    
    # Make request
    response = requests.post(f"{BASE_URL}/register", data=data, files=files)
    print("Registration Response:", response.json())
    return response.json()

def test_get_user_by_wallet(wallet_address):
    response = requests.get(f"{BASE_URL}/wallet/{wallet_address}")
    print("Get User by Wallet Response:", response.json())
    return response.json()

def test_get_user_by_email(email):
    response = requests.get(f"{BASE_URL}/email/{email}")
    print("Get User by Email Response:", response.json())
    return response.json()

if __name__ == "__main__":
    # Test registration
    user_data = test_registration()
    
    # Test get by wallet
    test_get_user_by_wallet(user_data["wallet_address"])
    
    # Test get by email
    test_get_user_by_email(user_data["email"]) 