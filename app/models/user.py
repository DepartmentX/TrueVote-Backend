from sqlalchemy import Column, String, LargeBinary
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    # Primary key - MetaMask address
    wallet_address = Column(String(150), primary_key=True, index=True)
    
    # User details
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    
    # Biometric data stored as binary
    biometric_image_url = Column(String(100), nullable=True)


    def __repr__(self):
        return f"<User(wallet_address='{self.wallet_address}', email='{self.email}')>" 