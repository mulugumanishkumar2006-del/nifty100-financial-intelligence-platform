import axios from "axios";

const API = "http://127.0.0.1:8000/api";

export const getRevenueRanking = async () => {
  try {
    const response = await axios.get(
      `${API}/analytics/revenue-ranking`
    );

    return response.data;
  } catch (error) {
    console.error("Revenue Ranking Error:", error);
    return [];
  }
};

export const getProfitRanking = async () => {
  try {
    const response = await axios.get(
      `${API}/analytics/profit-ranking`
    );

    return response.data;
  } catch (error) {
    console.error("Profit Ranking Error:", error);
    return [];
  }
};

export const getSectorAnalytics = async () => {
  try {
    const response = await axios.get(
      `${API}/analytics/sector-performance`
    );

    return response.data;
  } catch (error) {
    console.error("Sector Analytics Error:", error);
    return [];
  }
};

export const getCompanyComparison = async (
  company1,
  company2
) => {
  try {
    const response = await axios.get(
      `${API}/analytics/company-comparison`,
      {
        params: {
          company1,
          company2,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Comparison Error:", error);
    return null;
  }
};

export const getFinancialTrend = async (company) => {
  try {
    const response = await axios.get(
      `${API}/analytics/financial-trend`,
      {
        params: {
          company,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Trend Error:", error);
    return [];
  }
};