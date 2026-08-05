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

from app.utils import CustomJSONEncoder, clean_value

# Routers
from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices,
    intelligence,
    charts,
)

from app.routers.comparison_router import router as comparison_router
from app.routers.company_insight_router import router as company_insight_router

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
# FastAPI App
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
    print("✅ API Started")


@app.on_event("shutdown")
async def shutdown():
    print("🛑 API Shutdown")


# ==========================================================
# Validation Error
# ==========================================================

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):

    return APIJSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
        },
    )


# ==========================================================
# Global Error
# ==========================================================

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):

    return APIJSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
            "traceback": traceback.format_exc(),
        },
    )

# ==========================================================
# Register Routers
# ==========================================================

app.include_router(company.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(financial_ratios.router, prefix="/api")
app.include_router(sectors.router, prefix="/api")
app.include_router(stock_prices.router, prefix="/api")
app.include_router(intelligence.router, prefix="/api")
app.include_router(charts.router, prefix="/api")
app.include_router(comparison_router, prefix="/api")
app.include_router(company_insight_router, prefix="/api")

# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():
    return {
        "project": "NIFTY100 Financial Intelligence Platform",
        "status": "Running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api-info")
def api_info():
    return {
        "backend": "FastAPI",
        "frontend": "React",
        "database": "SQLite",
    }