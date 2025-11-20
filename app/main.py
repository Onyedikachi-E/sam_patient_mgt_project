from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .routes import router as patient_art_router


# ============================================
# FASTAPI APPLICATION
# ============================================

app = FastAPI(
    title="Patient ART Management System",
    description="This is for the management of patient data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ============================================
# MIDDLEWARE CONFIGURATION
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# ROOT ENDPOINTS
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Patient ART Management System",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

app.include_router(patient_art_router, prefix="/app/v1", tags=["Patient Art Data Management"])



if __name__ == "__main__":    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )