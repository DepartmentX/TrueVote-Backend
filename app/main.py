from fastapi import FastAPI
from app.routes.predict_route import router as predict_router

app = FastAPI()

app.include_router(predict_router)

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
