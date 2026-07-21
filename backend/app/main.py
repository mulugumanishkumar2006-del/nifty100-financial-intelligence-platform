from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

import json
import math
import traceback

from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices,
)
from app.utils import CustomJSONEncoder, clean_value


# Custom JSON response with NaN handling
class APIJSONResponse(JSONResponse):
    def render(self, content):
        # Clean the content before encoding
        cleaned_content = clean_value(content)
        return json.dumps(
            cleaned_content,
            ensure_ascii=False,
            indent=None,
            separators=(",", ":"),
            cls=CustomJSONEncoder,
        ).encode("utf-8")


app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    version="1.0.0",
    description="Financial Intelligence Platform for NIFTY 100 Companies",
    default_response_class=APIJSONResponse
)

# Enable CORS for dashboard and frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for database errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    error_detail = {
        "error": str(exc),
        "type": exc.__class__.__name__,
        "path": str(request.url.path),
        "method": request.method
    }
    
    # Only include traceback in development
    try:
        error_detail["traceback"] = traceback.format_exc()
    except:
        pass
    
    return APIJSONResponse(
        status_code=500,
        content={"detail": error_detail}
    )


# Register Routers with prefixes
app.include_router(company.router, prefix="/api", tags=["Companies"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(financial_ratios.router, prefix="/api", tags=["Financial Ratios"])
app.include_router(sectors.router, prefix="/api", tags=["Sectors"])
app.include_router(stock_prices.router, prefix="/api", tags=["Stock Prices"])


@app.get("/")
def home():
    return {
        "message": "NIFTY100 Financial Intelligence API",
        "version": "1.0.0",
        "status": "Running"
    }