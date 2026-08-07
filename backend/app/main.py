"""
Main Application

NIFTY100 Financial Intelligence Platform
"""

import json
import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.utils import CustomJSONEncoder, clean_value


# ==========================================================
# Routers
# ==========================================================

from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices,
    intelligence,
    charts,
)

from app.routers.comparison_router import (
    router as comparison_router,
)

from app.routers.company_insight_router import (
    router as company_insight_router,
)

from app.routers.ai_insights_router import (
    router as ai_router,
)

from app.routers.chat_router import (
    router as chat_router,
)

# Day 23 - AI Stock Recommendations
from app.routers.recommendation_router import (
    router as recommendation_router,
)


# ==========================================================
# Custom JSON Response
# ==========================================================

class APIJSONResponse(JSONResponse):

    def render(self, content):
        cleaned = clean_value(content)

        return json.dumps(
            cleaned,
            ensure_ascii=False,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    description="AI Powered Financial Intelligence Platform",
    version="1.0.0",
    default_response_class=APIJSONResponse,
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
# Startup
# ==========================================================

@app.on_event("startup")
async def startup():
    print(
        "✅ NIFTY100 Financial Intelligence API Started"
    )


# ==========================================================
# Shutdown
# ==========================================================

@app.on_event("shutdown")
async def shutdown():
    print("🛑 API Shutdown")


# ==========================================================
# Validation Error Handler
# ==========================================================

@app.exception_handler(RequestValidationError)
async def validation_handler(
    request: Request,
    exc: RequestValidationError,
):

    return APIJSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "path": request.url.path,
            "method": request.method,
        },
    )


# ==========================================================
# Global Exception Handler
# ==========================================================

@app.exception_handler(Exception)
async def exception_handler(
    request: Request,
    exc: Exception,
):

    return APIJSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc(),
        },
    )


# ==========================================================
# Register Routers
# ==========================================================

# ----------------------------------------------------------
# Companies
# ----------------------------------------------------------

app.include_router(
    company.router,
    prefix="/api",
    tags=["Companies"],
)


# ----------------------------------------------------------
# Analytics
# ----------------------------------------------------------

app.include_router(
    analytics.router,
    prefix="/api",
    tags=["Analytics"],
)


# ----------------------------------------------------------
# Financial Ratios
# ----------------------------------------------------------

app.include_router(
    financial_ratios.router,
    prefix="/api",
    tags=["Financial Ratios"],
)


# ----------------------------------------------------------
# Sectors
# ----------------------------------------------------------

app.include_router(
    sectors.router,
    prefix="/api",
    tags=["Sectors"],
)


# ----------------------------------------------------------
# Stock Prices
# ----------------------------------------------------------

app.include_router(
    stock_prices.router,
    prefix="/api",
    tags=["Stock Prices"],
)


# ----------------------------------------------------------
# AI Intelligence
# ----------------------------------------------------------

app.include_router(
    intelligence.router,
    prefix="/api",
    tags=["AI Intelligence"],
)


# ----------------------------------------------------------
# Charts
# ----------------------------------------------------------

app.include_router(
    charts.router,
    prefix="/api",
    tags=["Charts"],
)


# ----------------------------------------------------------
# Company Comparison
# ----------------------------------------------------------

app.include_router(
    comparison_router,
    prefix="/api",
    tags=["Company Comparison"],
)


# ----------------------------------------------------------
# Company Insights
# ----------------------------------------------------------

app.include_router(
    company_insight_router,
    prefix="/api",
    tags=["Company Insights"],
)


# ----------------------------------------------------------
# AI Insights
# ----------------------------------------------------------

app.include_router(
    ai_router,
    prefix="/api",
    tags=["AI Insights"],
)


# ----------------------------------------------------------
# AI Chat
# ----------------------------------------------------------

app.include_router(
    chat_router,
    prefix="/api",
    tags=["AI Chat"],
)


# ----------------------------------------------------------
# AI Stock Recommendations
# Day 23
# ----------------------------------------------------------

app.include_router(
    recommendation_router,
    prefix="/api",
    tags=["AI Stock Recommendations"],
)


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def home():

    return {
        "project": "NIFTY100 Financial Intelligence Platform",
        "status": "Running",
        "version": "1.0.0",
        "docs": "/docs",
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
        "frontend": "React",
        "database": "SQLite",

        "modules": [
            "Dashboard",
            "Companies",
            "Financial Ratios",
            "Stock Prices",
            "Sector Analytics",
            "Company Comparison",
            "Company Insights",
            "AI Intelligence",
            "AI Insights",
            "AI Chat",
            "AI Stock Recommendations",
            "Charts",
        ],
    }