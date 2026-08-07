const BASE_URL = "http://127.0.0.1:8000";

// ======================================================
// Helper
// ======================================================

async function fetchJSON(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`
    );
  }

  return await response.json();
}

// ======================================================
// Dashboard
// ======================================================

export async function getDashboard() {
  return await fetchJSON("/api/dashboard");
}

// ======================================================
// Latest Financial Year
// ======================================================

export async function getLatestYear() {
  return await fetchJSON("/api/latest-year");
}

// ======================================================
// Top Revenue Company
// ======================================================

export async function getTopRevenue() {
  return await fetchJSON("/api/top-revenue");
}

// ======================================================
// Top Profit Company
// ======================================================

export async function getTopProfit() {
  return await fetchJSON("/api/top-profit");
}

// ======================================================
// Sector Distribution
// ======================================================

export async function getSectorDistribution() {
  return await fetchJSON("/api/sector-distribution");
}