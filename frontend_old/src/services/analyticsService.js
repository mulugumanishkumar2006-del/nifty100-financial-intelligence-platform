import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// ======================================================
// Dashboard Summary
// ======================================================

export const getDashboard = async () => {
  try {
    const { data } = await axios.get(`${API}/dashboard`);
    return data;
  } catch (err) {
    console.error("Dashboard Error:", err);
    return {};
  }
};

// ======================================================
// Revenue Ranking
// ======================================================

export const getRevenueRanking = async () => {
  try {
    const { data } = await axios.get(`${API}/revenue-ranking`);
    return data;
  } catch (err) {
    console.error("Revenue Ranking Error:", err);
    return [];
  }
};

// ======================================================
// Profit Ranking
// ======================================================

export const getProfitRanking = async () => {
  try {
    const { data } = await axios.get(`${API}/profit-ranking`);
    return data;
  } catch (err) {
    console.error("Profit Ranking Error:", err);
    return [];
  }
};

// ======================================================
// Sector Distribution
// ======================================================

export const getSectorDistribution = async () => {
  try {
    const { data } = await axios.get(`${API}/sector-distribution`);
    return data;
  } catch (err) {
    console.error("Sector Distribution Error:", err);
    return [];
  }
};

// ======================================================
// Company Analytics
// ======================================================

export const getCompanyAnalytics = async (companyId) => {
  try {
    const { data } = await axios.get(`${API}/company/${companyId}`);
    return data;
  } catch (err) {
    console.error("Company Analytics Error:", err);
    return null;
  }
};

// ======================================================
// Revenue Trend Chart
// ======================================================

export const getRevenueTrend = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/charts/revenue/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Revenue Trend Error:", err);
    return [];
  }
};

// ======================================================
// ROE Trend Chart
// ======================================================

export const getROETrend = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/charts/roe/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("ROE Trend Error:", err);
    return [];
  }
};

// ======================================================
// Market Cap Chart
// ======================================================

export const getMarketCap = async () => {
  try {
    const { data } = await axios.get(
      `${API}/charts/market-cap`
    );
    return data;
  } catch (err) {
    console.error("Market Cap Error:", err);
    return [];
  }
};

// ======================================================
// Stock History
// ======================================================

export const getStockHistory = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/charts/stock-history/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Stock History Error:", err);
    return [];
  }
};