"""
Main Application

NIFTY100 Financial Intelligence Platform
"""

import json
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.routers.comparison_router import router as comparison_router
from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices,
    intelligence,
    charts,
)

from app.utils import CustomJSONEncoder, clean_value


# ==========================================================
# Custom JSON Response
# ==========================================================

class APIJSONResponse(JSONResponse):
    def render(self, content):
        cleaned_content = clean_value(content)

        return json.dumps(
            cleaned_content,
            ensure_ascii=False,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    description="AI Powered Financial Intelligence Platform for NIFTY100 Companies",
    version="1.0.0",
    default_response_class=APIJSONResponse,
    contact={
        "name": "Mulugu Maneesh Kumar",
        "email": "your-email@example.com",
    },
    license_info={
        "name": "MIT License",
    },
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Startup / Shutdown
# ==========================================================

@app.on_event("startup")
async def startup_event():
    print("✅ NIFTY100 Financial Intelligence API Started")


@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 API Shutdown")


# ==========================================================
# Validation Error Handler
# ==========================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return APIJSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )


# ==========================================================
# Global Exception Handler
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    error = {
        "error": str(exc),
        "type": exc.__class__.__name__,
        "path": request.url.path,
        "method": request.method,
    }

    try:
        error["traceback"] = traceback.format_exc()
    except Exception:
        pass

    return APIJSONResponse(
        status_code=500,
        content={
            "detail": error
        },
    )


# ==========================================================
# Register Routers
# ==========================================================

app.include_router(
    company.router,
    prefix="/api",
    tags=["Companies"],
)

app.include_router(
    analytics.router,
    prefix="/api",
    tags=["Analytics"],
)

app.include_router(
    financial_ratios.router,
    prefix="/api",
    tags=["Financial Ratios"],
)

app.include_router(
    sectors.router,
    prefix="/api",
    tags=["Sectors"],
)

app.include_router(
    stock_prices.router,
    prefix="/api",
    tags=["Stock Prices"],
)

app.include_router(
    intelligence.router,
    prefix="/api",
    tags=["AI Intelligence"],
)

app.include_router(
    charts.router,
    prefix="/api",
    tags=["Charts"],
)
app.include_router(
    comparison_router,
    prefix="/api"
)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def home():
    return {
        "project": "NIFTY100 Financial Intelligence Platform",
        "version": "1.0.0",
        "status": "Running",
        "documentation": "/docs",
        "health": "/health",
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "api": "NIFTY100 Financial Intelligence API",
        "version": "1.0.0",
    }


# ==========================================================
# API Information
# ==========================================================

@app.get("/api-info")
def api_info():
    return {
        "backend": "FastAPI",
        "database": "SQLite",
        "frontend": "React",
        "modules": [
            "Dashboard",
            "Companies",
            "Financial Ratios",
            "Stock Prices",
            "Sector Analytics",
            "AI Intelligence",
            "Charts",
        ],
    }