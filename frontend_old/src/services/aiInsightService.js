import axios from "axios";

// ==========================================================
// Axios Instance
// ==========================================================

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/ai",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ==========================================================
// Error Handler
// ==========================================================

const handleError = (error, moduleName) => {
  console.error(`${moduleName} Error:`, error);

  if (error.response) {
    throw new Error(
      error.response.data.detail ||
      `${moduleName} request failed.`
    );
  }

  if (error.request) {
    throw new Error(
      "Unable to connect to the backend server."
    );
  }

  throw new Error(error.message);
};

// ==========================================================
// Complete AI Insights
// ==========================================================

export const getCompanyAIInsights = async (companyId) => {
  try {
    const response = await api.get(`/company/${companyId}`);
    return response.data;
  } catch (error) {
    handleError(error, "AI Insights");
  }
};

// ==========================================================
// Growth Analysis
// ==========================================================

export const getGrowthAnalysis = async (companyId) => {
  try {
    const response = await api.get(`/growth/${companyId}`);
    return response.data;
  } catch (error) {
    handleError(error, "Growth Analysis");
  }
};

// ==========================================================
// Risk Analysis
// ==========================================================

export const getRiskAnalysis = async (companyId) => {
  try {
    const response = await api.get(`/risk/${companyId}`);
    return response.data;
  } catch (error) {
    handleError(error, "Risk Analysis");
  }
};

// ==========================================================
// Investment Recommendation
// ==========================================================

export const getInvestmentRecommendation = async (companyId) => {
  try {
    const response = await api.get(`/recommendation/${companyId}`);
    return response.data;
  } catch (error) {
    handleError(error, "Investment Recommendation");
  }
};

// ==========================================================
// Load Everything Together
// ==========================================================

export const getCompleteAIReport = async (companyId) => {
  try {
    const [
      insights,
      growth,
      risk,
      recommendation,
    ] = await Promise.all([
      getCompanyAIInsights(companyId),
      getGrowthAnalysis(companyId),
      getRiskAnalysis(companyId),
      getInvestmentRecommendation(companyId),
    ]);

    return {
      insights,
      growth,
      risk,
      recommendation,
    };
  } catch (error) {
    console.error("Complete AI Report Error:", error);
    throw error;
  }
};