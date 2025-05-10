from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.verify_captcha import router as verify_captcha_router
from app.routes.detect_fraud import router as detect_fraud_router
  

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(verify_captcha_router)
app.include_router(detect_fraud_router)

#check if the database is connected
@app.get("/check-db")
async def check_db():
    try:
        from app.utils.database import engine
        from app.models.base import Base
        Base.metadata.create_all(bind=engine)
        return {"status": "Database connected successfully"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
