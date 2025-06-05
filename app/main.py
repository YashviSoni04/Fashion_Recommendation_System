from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os


from .config import settings
from .models import FashionRequest, FashionResponse, ErrorResponse
from .services import FashionRecommendationService

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Global service instance
fashion_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global fashion_service
    try:
        settings.validate_settings()
        fashion_service = FashionRecommendationService()
        logger.info("Application startup completed")
        yield
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
    # Shutdown
    logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

@app.get("/ui", response_class=HTMLResponse, tags=["Frontend"])
async def frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get service
def get_fashion_service():
    if fashion_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    return fashion_service

# ENDPOINTS

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Fashion Recommendation API is running!",
        "version": settings.API_VERSION,
        "status": "healthy",
        "timestamp": time.time()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "fashion-recommendation-api",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "timestamp": time.time()
    }

@app.post("/recommend", response_model=FashionResponse, tags=["Recommendations"])
async def get_fashion_recommendations(
    request: FashionRequest,
    service: FashionRecommendationService = Depends(get_fashion_service)
):
    """
    Get personalized fashion recommendations
    """
    try:
        result = await service.get_recommendations(request)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=500, 
                detail=result.get("message", "Internal server error")
            )
        
        return FashionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /recommend: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/fashion-types", tags=["Reference"])
async def get_fashion_types():
    """Get available fashion types"""
    from .models import FashionType
    return {
        "fashion_types": [item.value for item in FashionType],
        "description": "Available fashion/occasion types"
    }

@app.get("/sizes", tags=["Reference"])
async def get_sizes():
    """Get available sizes"""
    from .models import SizeCategory
    return {
        "sizes": [item.value for item in SizeCategory],
        "description": "Available clothing sizes"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )