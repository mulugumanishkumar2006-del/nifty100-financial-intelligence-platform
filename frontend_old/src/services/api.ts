import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;

// ==========================
// Dashboard
// ==========================

export const getDashboard = () =>
  api.get("/dashboard");

// ==========================
// Companies
// ==========================

export const getCompanies = () =>
  api.get("/companies");

export const getCompany = (id: string) =>
  api.get(`/companies/${id}`);

// ==========================
// Analytics
// ==========================

export const getRevenueRanking = () =>
  api.get("/revenue-ranking");

export const getProfitRanking = () =>
  api.get("/profit-ranking");

// ==========================
// Financial Ratios
// ==========================

export const getFinancialRatios = () =>
  api.get("/financial-ratios");

export const getCompanyRatios = (id: string) =>
  api.get(`/financial-ratios/company/${id}`);

// ==========================
// Stock Prices
// ==========================

export const getStockPrices = () =>
  api.get("/stock-prices");

export const getLatestPrice = (id: string) =>
  api.get(`/stock-prices/latest/${id}`);

// ==========================
// AI Intelligence
// ==========================

export const getHealthScore = (id: string) =>
  api.get(`/intelligence/health-score/${id}`);

export const getRecommendation = (id: string) =>
  api.get(`/intelligence/recommendation/${id}`);

export const getAISummary = (id: string) =>
  api.get(`/intelligence/summary/${id}`);

// ==========================
// Charts
// ==========================

export const getRevenueTrend = (id: string) =>
  api.get(`/charts/revenue/${id}`);

export const getROETrend = (id: string) =>
  api.get(`/charts/roe/${id}`);

export const getMarketCap = () =>
  api.get("/charts/market-cap");

export const getSectorDistribution = () =>
  api.get("/charts/sector-distribution");

export const getStockHistory = (id: string) =>
  api.get(`/charts/stock-history/${id}`);