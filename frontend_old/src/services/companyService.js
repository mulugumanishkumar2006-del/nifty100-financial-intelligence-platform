import axios from "axios";

const API = "http://127.0.0.1:8000/api";

// ======================================================
// Companies
// ======================================================

export const getCompanies = async () => {
  try {
    const { data } = await axios.get(`${API}/companies`);
    return data;
  } catch (err) {
    console.error("Companies Error:", err);
    return [];
  }
};

export const getCompany = async (companyId) => {
  try {
    const { data } = await axios.get(`${API}/companies/${companyId}`);
    return data;
  } catch (err) {
    console.error("Company Error:", err);
    return null;
  }
};

// ======================================================
// Financial Ratios
// ======================================================

export const getCompanyRatios = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/financial-ratios/company/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Financial Ratios Error:", err);
    return [];
  }
};

export const getTopROE = async (limit = 10) => {
  try {
    const { data } = await axios.get(
      `${API}/financial-ratios/top-roe?limit=${limit}`
    );
    return data;
  } catch (err) {
    console.error("Top ROE Error:", err);
    return [];
  }
};

export const getTopAssetTurnover = async (limit = 10) => {
  try {
    const { data } = await axios.get(
      `${API}/financial-ratios/top-asset-turnover?limit=${limit}`
    );
    return data;
  } catch (err) {
    console.error("Asset Turnover Error:", err);
    return [];
  }
};

// ======================================================
// Sectors
// ======================================================

export const getSectors = async () => {
  try {
    const { data } = await axios.get(`${API}/sectors`);
    return data;
  } catch (err) {
    console.error("Sector Error:", err);
    return [];
  }
};

export const getSectorSummary = async () => {
  try {
    const { data } = await axios.get(`${API}/sectors/summary`);
    return data;
  } catch (err) {
    console.error("Sector Summary Error:", err);
    return [];
  }
};

export const getCompaniesBySector = async (sector) => {
  try {
    const { data } = await axios.get(`${API}/sectors/${sector}`);
    return data;
  } catch (err) {
    console.error("Companies By Sector Error:", err);
    return [];
  }
};

// ======================================================
// Stock Prices
// ======================================================

export const getLatestStockPrices = async (limit = 100) => {
  try {
    const { data } = await axios.get(
      `${API}/stock-prices?limit=${limit}`
    );
    return data;
  } catch (err) {
    console.error("Latest Stock Prices Error:", err);
    return [];
  }
};

export const getCompanyStockHistory = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/stock-prices/company/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Company Stock History Error:", err);
    return [];
  }
};

export const getLatestStockPrice = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/stock-prices/latest/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Latest Stock Price Error:", err);
    return {};
  }
};

// ======================================================
// AI Intelligence (Existing)
// ======================================================

export const getHealthScore = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/intelligence/health-score/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Health Score Error:", err);
    return null;
  }
};

export const getRecommendation = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/intelligence/recommendation/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Recommendation Error:", err);
    return null;
  }
};

export const getAISummary = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/intelligence/summary/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("AI Summary Error:", err);
    return null;
  }
};

// ======================================================
// Day 21 - AI Insights
// ======================================================

export const getAIInsights = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/ai/company/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("AI Insights Error:", err);
    return null;
  }
};

export const getGrowthAnalysis = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/ai/growth/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Growth Analysis Error:", err);
    return null;
  }
};

export const getRiskAnalysis = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/ai/risk/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Risk Analysis Error:", err);
    return null;
  }
};

export const getAIRecommendation = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/ai/recommendation/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("AI Recommendation Error:", err);
    return null;
  }
};

// ======================================================
// Charts
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

export const getMarketCapChart = async () => {
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

export const getSectorDistributionChart = async () => {
  try {
    const { data } = await axios.get(
      `${API}/charts/sector-distribution`
    );
    return data;
  } catch (err) {
    console.error("Sector Distribution Chart Error:", err);
    return [];
  }
};

export const getStockHistoryChart = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/charts/stock-history/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Stock History Chart Error:", err);
    return [];
  }
};

// ======================================================
// Peer Comparison
// ======================================================

export const getPeerComparison = async (companyId) => {
  try {
    const { data } = await axios.get(
      `${API}/comparison/peer-comparison/${companyId}`
    );
    return data;
  } catch (err) {
    console.error("Peer Comparison Error:", err);
    return [];
  }
};

// ======================================================
// Company Comparison
// ======================================================

export const compareCompanies = async (company1, company2) => {
  try {
    const { data } = await axios.get(
      `${API}/comparison`,
      {
        params: {
          company1,
          company2,
        },
      }
    );

    return data;
  } catch (err) {
    console.error("Company Comparison Error:", err);
    return [];
  }
};