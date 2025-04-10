# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import upload, extract, health
from .db.database import init_database

# Create FastAPI application
app = FastAPI(
    title="Document Extraction Service",
    description="Service for uploading and extracting document information",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(extract.router, prefix="/api/extract", tags=["Extract"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_database()