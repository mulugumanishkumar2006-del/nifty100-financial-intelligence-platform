from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import traceback

from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices,
    intelligence,
)

from app.utils import CustomJSONEncoder, clean_value


# ==========================================
# Custom JSON Response
# ==========================================

class APIJSONResponse(JSONResponse):
    def render(self, content):
        cleaned_content = clean_value(content)

        return json.dumps(
            cleaned_content,
            ensure_ascii=False,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


# ==========================================
# FastAPI App
# ==========================================

app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    version="1.0.0",
    description="Financial Intelligence Platform for NIFTY100 Companies",
    default_response_class=APIJSONResponse,
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Global Exception Handler
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    error_detail = {
        "error": str(exc),
        "type": exc.__class__.__name__,
        "path": request.url.path,
        "method": request.method,
    }

    try:
        error_detail["traceback"] = traceback.format_exc()
    except Exception:
        pass

    return APIJSONResponse(
        status_code=500,
        content={"detail": error_detail},
    )


# ==========================================
# Routers
# ==========================================

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
    tags=["Intelligence"],
)


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "message": "NIFTY100 Financial Intelligence API",
        "version": "1.0.0",
        "status": "Running",
        "documentation": "/docs",
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "NIFTY100 Financial Intelligence API",
    }