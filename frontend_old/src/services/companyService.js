import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// ============================
// Get All Companies
// ============================

export const getCompanies = async () => {
  const response = await axios.get(`${API}/companies`);
  return response.data;
};

// ============================
// Get Single Company
// ============================

export const getCompany = async (id) => {
  const response = await axios.get(`${API}/companies/${id}`);
  return response.data;
};

// ============================
// Dashboard
// ============================

export const getDashboard = async () => {
  const response = await axios.get(`${API}/analytics/dashboard`);
  return response.data;
};

// ============================
// Top Revenue
// ============================

export const getTopRevenue = async () => {
  const response = await axios.get(`${API}/analytics/top-revenue`);
  return response.data;
};

// ============================
// Top Profit
// ============================

export const getTopProfit = async () => {
  const response = await axios.get(`${API}/analytics/top-profit`);
  return response.data;
};

// ============================
// Sector Distribution
// ============================

export const getSectorDistribution = async () => {
  const response = await axios.get(
    `${API}/analytics/sector-distribution`
  );
  return response.data;
};

// ============================
// Latest Financial Year
// ============================

export const getLatestYear = async () => {
  const response = await axios.get(
    `${API}/analytics/latest-year`
  );
  return response.data;
};