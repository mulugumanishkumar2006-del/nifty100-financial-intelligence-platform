from fastapi import FastAPI

from app.routers import (
    company,
    analytics,
    financial_ratios,
    sectors,
    stock_prices
)

app = FastAPI(
    title="NIFTY100 Financial Intelligence API",
    version="1.0.0"
)

app.include_router(
    company.router,
    prefix="/companies",
    tags=["Companies"]
)

app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

app.include_router(
    financial_ratios.router,
    prefix="/financial-ratios",
    tags=["Financial Ratios"]
)

app.include_router(
    sectors.router,
    prefix="/sectors",
    tags=["Sectors"]
)

app.include_router(
    stock_prices.router,
    prefix="/stock-prices",
    tags=["Stock Prices"]
)


@app.get("/")
def home():

    return {

        "message": "NIFTY100 Financial Intelligence API",

        "version": "1.0.0",

        "status": "Running"

    }