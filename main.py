from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
import logging

from app.config import settings
from app.db.session import engine
from app.utils.exceptions import AppException
from app.api.v1 import patients, providers, appointments, visits, analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting Healthcare Appointment System...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[-1]}")  # Hide credentials
    
    yield
    
    logger.info("Shutting down Healthcare Appointment System...")
    await engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="Healthcare Appointment & Patient Flow System",
    description="""
    A production-grade healthcare management system for scheduling appointments,
    managing patient records, and tracking provider availability.
    
    ## Features
    
    * **Double-booking Prevention**: Database-level constraints prevent scheduling conflicts
    * **Provider Scheduling**: Flexible availability management
    * **Visit Tracking**: Complete medical visit documentation
    * **Analytics**: Utilization reports, no-show tracking, and performance metrics
    * **Audit Logging**: Complete audit trail for all sensitive operations
    
    ## Technical Highlights
    
    * PostgreSQL with advanced constraints (EXCLUDE, CHECK)
    * ACID transactions with proper isolation levels
    * RESTful API design
    * Comprehensive validation and error handling
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(providers.router, prefix="/api/v1/providers", tags=["Providers"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(visits.router, prefix="/api/v1/visits", tags=["Visits"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": {
                "error": exc.error_code,
                "message": exc.message
            }
        }
    )


@app.exception_handler(IntegrityError)
async def db_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")
    
    # Parse error for user-friendly message
    error_msg = str(exc.orig).lower()
    
    if "unique" in error_msg:
        detail = "A record with this information already exists"
    elif "foreign key" in error_msg:
        detail = "Referenced record does not exist"
    elif "check constraint" in error_msg:
        detail = "Data validation failed"
    elif "exclude" in error_msg:
        detail = "This operation conflicts with existing data"
    else:
        detail = "Database constraint violation"
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": {
                "error": "DATA_INTEGRITY_ERROR",
                "message": detail
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Healthcare Appointment & Patient Flow System API",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "patients": "/api/v1/patients",
            "providers": "/api/v1/providers",
            "appointments": "/api/v1/appointments",
            "visits": "/api/v1/visits",
            "analytics": "/api/v1/analytics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "healthcare-api",
        "version": "1.0.0"
    }


# Optional: Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response

