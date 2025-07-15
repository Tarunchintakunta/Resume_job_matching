from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pymongo import MongoClient

from app.core.config import settings
from app.api.endpoints import resumes, jobs, matches, match, advanced_matches, nlp_analysis

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS - Allow ALL origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Use config value for allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.DATABASE_NAME]
    
    # Ensure collections exist
    collection_names = app.mongodb.list_collection_names()
    if "resumes" not in collection_names:
        app.mongodb.create_collection("resumes")
    if "jobs" not in collection_names:
        app.mongodb.create_collection("jobs")
    if "matches" not in collection_names:
        app.mongodb.create_collection("matches")
    
    # Create indexes
    app.mongodb.resumes.create_index("id", unique=True)
    app.mongodb.jobs.create_index("id", unique=True)
    app.mongodb.matches.create_index([("job_id", 1), ("resume_id", 1)], unique=True)
    
    print("Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("MongoDB connection closed")

# Include routers
app.include_router(resumes.router, prefix=f"{settings.API_V1_STR}/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])
app.include_router(matches.router, prefix=f"{settings.API_V1_STR}/matches", tags=["matches"])
app.include_router(match.router, prefix=f"{settings.API_V1_STR}", tags=["evaluation"])
app.include_router(advanced_matches.router, prefix=f"{settings.API_V1_STR}/advanced", tags=["advanced-matching"])
app.include_router(nlp_analysis.router, prefix=f"{settings.API_V1_STR}/nlp", tags=["nlp-analysis"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Resume-Job Matching API",
        "documentation": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    # Run the application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)