from fastapi import FastAPI
app = FastAPI(
    title="ResumeIQ AI",
    description="AI-powered Resume Screening Platform",
    version="1.0.0"
)
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