import axios from "axios";

const API = "http://127.0.0.1:8000/api/charts";

// Revenue Trend
export const getRevenueTrend = async (companyId) => {
  const { data } = await axios.get(`${API}/revenue/${companyId}`);
  return data;
};

// ROE Trend
export const getROETrend = async (companyId) => {
  const { data } = await axios.get(`${API}/roe/${companyId}`);
  return data;
};

// Market Cap
export const getMarketCap = async () => {
  const { data } = await axios.get(`${API}/market-cap`);
  return data;
};

// Sector Distribution
export const getSectorDistribution = async () => {
  const { data } = await axios.get(`${API}/sector-distribution`);
  return data;
};

// Stock Price History
export const getStockHistory = async (companyId) => {
  const { data } = await axios.get(`${API}/stock-history/${companyId}`);
  return data;
};