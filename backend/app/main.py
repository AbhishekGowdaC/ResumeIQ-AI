from fastapi import FastAPI
from app.api.users import router as user_router

from app.database.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ResumeIQ AI",
    description="AI-powered Resume Screening Platform",
    version="1.0.0"
)
app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to ResumeIQ AI",
        "version" : "1.0.0"
    }
@app.get("/health")
def health():
    return {
        "status":"healthy"
    }

@app.get("/developer")
def developer():
    return {
        "name":"Abhishek Gowda C",
        "project":"ResumeIQ AI",
        "day":1
    }