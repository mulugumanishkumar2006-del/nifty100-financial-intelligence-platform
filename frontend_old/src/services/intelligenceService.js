import axios from "axios";

// =========================================
// Base API URL
// =========================================

const API = "http://127.0.0.1:8000/api";

// =========================================
// Get All Companies
// =========================================

export async function getCompanies() {
  const response = await axios.get(
    `${API}/companies`
  );
  return response.data;
}

// =========================================
// AI Health Score
// =========================================

export async function getHealthScore(companyId) {
  const response = await axios.get(
    `${API}/intelligence/health-score/${companyId}`
  );
  return response.data;
}

// =========================================
// AI Recommendation
// =========================================

export async function getRecommendation(companyId) {
  const response = await axios.get(
    `${API}/intelligence/recommendation/${companyId}`
  );
  return response.data;
}

// =========================================
// AI Financial Summary
// =========================================

export async function getAISummary(companyId) {
  const response = await axios.get(
    `${API}/intelligence/summary/${companyId}`
  );
  return response.data;
}

// =========================================
// Get All AI Data Together
// =========================================

export async function getAIAnalysis(companyId) {
  try {
    const [
      health,
      recommendation,
      summary,
    ] = await Promise.all([
      getHealthScore(companyId),
      getRecommendation(companyId),
      getAISummary(companyId),
    ]);

    return {
      health,
      recommendation,
      summary,
    };
  } catch (error) {
    console.error(
      "AI Analysis Error:",
      error
    );
    throw error;
  }
}