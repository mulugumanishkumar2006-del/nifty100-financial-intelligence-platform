import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// ==========================================
// Rankings (Required by Dashboard)
// ==========================================

export const getRevenueRanking = async () => {
  try {
    const response = await axios.get(`${API}/analytics/revenue-ranking`);
    return response.data;
  } catch (error) {
    console.error("Revenue Ranking Error:", error);
    return [];
  }
};

export const getProfitRanking = async () => {
  try {
    const response = await axios.get(`${API}/analytics/profit-ranking`);
    return response.data;
  } catch (error) {
    console.error("Profit Ranking Error:", error);
    return [];
  }
};

// ==========================================
// Revenue & Profit Trends
// ==========================================

export const getRevenueTrend = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/analytics/revenue-trend/${companyId}`
    );
    return response.data;
  } catch (error) {
    console.error("Revenue Trend Error:", error);
    return [];
  }
};

export const getProfitTrend = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/analytics/profit-trend/${companyId}`
    );
    return response.data;
  } catch (error) {
    console.error("Profit Trend Error:", error);
    return [];
  }
};

// ==========================================
// Stock History
// ==========================================

export const getStockHistory = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/stock-history/${companyId}`
    );
    return response.data;
  } catch (error) {
    console.error("Stock History Error:", error);
    return [];
  }
};

// ==========================================
// Market Cap
// ==========================================

export const getMarketCap = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/companies/${companyId}`
    );
    return response.data;
  } catch (error) {
    console.error("Market Cap Error:", error);
    return null;
  }
};

// ==========================================
// Financial Ratios
// ==========================================

export const getFinancialRatios = async (companyId) => {
  try {
    const response = await axios.get(
      `${API}/financial-ratios/${companyId}`
    );
    return response.data;
  } catch (error) {
    console.error("Financial Ratios Error:", error);
    return null;
  }
};