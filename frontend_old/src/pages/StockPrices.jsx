import { useEffect, useMemo, useState } from "react";

import Layout from "../components/Layout";

import StockOverview from "../components/stock/StockOverview";
import StockStats from "../components/stock/StockStats";

import LinePriceChart from "../components/charts/LinePriceChart";
import VolumeBarChart from "../components/charts/VolumeBarChart";
import PriceLineChart from "../components/charts/PriceLineChart";
import PriceAreaChart from "../components/charts/PriceAreaChart";
import MarketSharePieChart from "../components/charts/MarketSharePieChart";
import ChangeBarChart from "../components/charts/ChangeBarChart";

import { getStockPrices } from "../services/stockService";

function StockPrices() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("company");

  useEffect(() => {
    loadStocks();
  }, []);

  async function loadStocks() {
    try {
      setLoading(true);
      setError("");

      const data = await getStockPrices();

      const formatted = (data || []).map((item) => ({
        id: item.id,

        company:
          item.company_name ||
          "Unknown",

        price: Number(
          item.close_price ??
          item.close ??
          item.current_price ??
          item.price ??
          0
        ),

        change: Number(
          item.change_percentage ??
          item.change ??
          0
        ),

        high52: Number(
          item.high_price ??
          item.high_52 ??
          item.high ??
          0
        ),

        low52: Number(
          item.low_price ??
          item.low_52 ??
          item.low ??
          0
        ),

        volume: Number(
          item.volume ?? 0
        ),

        date: item.date,

        open: Number(
          item.open_price ?? 0
        ),

        adjustedClose: Number(
          item.adjusted_close ?? 0
        )
      }));

      setStocks(formatted);
    } catch (error) {
      console.error("Stock Loading Error:", error);
      setError("Failed to load stock prices. Please check your network or try again.");
    } finally {
      setLoading(false);
    }
  }

  const filteredStocks = useMemo(() => {
    return [...stocks]
      .filter((stock) =>
        stock.company?.toLowerCase().includes(search.toLowerCase())
      )
      .sort((a, b) => {
        switch (sortBy) {
          case "price":
            return b.price - a.price;
          case "change":
            return b.change - a.change;
          case "volume":
            return b.volume - a.volume;
          default:
            return a.company.localeCompare(b.company);
        }
      });
  }, [stocks, search, sortBy]);

  const highestPrice = filteredStocks.length
    ? Math.max(...filteredStocks.map((s) => s.price))
    : 0;

  const averagePrice = filteredStocks.length
    ? (
        filteredStocks.reduce((sum, s) => sum + s.price, 0) /
        filteredStocks.length
      ).toFixed(2)
    : 0;

  const marketSummary = useMemo(() => {
    if (!filteredStocks.length) {
      return {
        topGainer: null,
        topLoser: null,
        totalVolume: 0,
      };
    }

    const topGainer = filteredStocks.reduce((a, b) =>
      a.change > b.change ? a : b
    );

    const topLoser = filteredStocks.reduce((a, b) =>
      a.change < b.change ? a : b
    );

    const totalVolume = filteredStocks.reduce(
      (sum, stock) => sum + stock.volume,
      0
    );

    return {
      topGainer,
      topLoser,
      totalVolume,
    };
  }, [filteredStocks]);

  if (loading && stocks.length === 0) {
    return (
      <Layout>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "400px",
            gap: "16px",
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              border: "5px solid #e5e7eb",
              borderTop: "5px solid #2563eb",
              borderRadius: "50%",
              animation: "spin 1s linear infinite",
            }}
          />
          <style>
            {`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}
          </style>
          <h2 style={{ color: "#4b5563", fontSize: "18px", fontWeight: "600", margin: 0 }}>
            Loading Stock Prices...
          </h2>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* HEADER SECTION */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "25px",
        }}
      >
        <h1 style={{ fontSize: "28px", fontWeight: "700", margin: 0 }}>
          📈 Real-Time Stock Prices
        </h1>
        <button
          onClick={loadStocks}
          disabled={loading}
          style={{
            padding: "14px 24px",
            background: "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: "12px",
            cursor: loading ? "not-allowed" : "pointer",
            fontWeight: "700",
            fontSize: "15px",
            transition: "0.3s",
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "Loading..." : "🔄 Refresh Data"}
        </button>
      </div>

      {/* ERROR DISPLAY BANNER */}
      {error && (
        <div
          style={{
            padding: "16px 20px",
            marginBottom: "20px",
            background: "#fef2f2",
            border: "1px solid #fca5a5",
            borderRadius: "12px",
            color: "#991b1b",
            fontWeight: "600",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span>⚠️ {error}</span>
          <button
            onClick={loadStocks}
            style={{
              padding: "8px 16px",
              background: "#dc2626",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "600",
            }}
          >
            Retry
          </button>
        </div>
      )}

      {/* OVERVIEW & STATS */}
      <StockOverview stocks={filteredStocks} />
      
      <div style={{ marginTop: "35px" }}>
        <PriceLineChart stocks={filteredStocks} />
      </div>

      <StockStats
        highestPrice={highestPrice}
        averagePrice={averagePrice}
        totalVolume={marketSummary.totalVolume}
      />

      {/* CHARTS */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(450px, 1fr))",
          gap: "20px",
          margin: "25px 0",
        }}
      >
        <LinePriceChart data={filteredStocks} />
        <VolumeBarChart data={filteredStocks} />
      </div>

      <div style={{ marginTop: "30px" }}>
        <PriceAreaChart stocks={filteredStocks} />
      </div>

      <div style={{ marginTop: "30px" }}>
        <MarketSharePieChart stocks={filteredStocks} />
      </div>

      <div style={{ marginTop: "30px" }}>
        <ChangeBarChart stocks={filteredStocks} />
      </div>

      {/* SEARCH & SORT */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
          marginBottom: "25px",
        }}
      >
        <input
          type="text"
          placeholder="🔍 Search Company..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            minWidth: "300px",
            padding: "14px",
            borderRadius: "12px",
            border: "1px solid #d1d5db",
            fontSize: "15px",
            outline: "none",
          }}
        />

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{
            padding: "14px",
            borderRadius: "12px",
            border: "1px solid #d1d5db",
            background: "#fff",
            fontSize: "15px",
            minWidth: "180px",
            cursor: "pointer",
          }}
        >
          <option value="company">Company</option>
          <option value="price">Price</option>
          <option value="change">Daily Change</option>
          <option value="volume">Volume</option>
        </select>
      </div>

      <p
        style={{
          color: "#6b7280",
          marginBottom: "15px",
          fontWeight: "600",
        }}
      >
        Showing {filteredStocks.length} Companies
      </p>

      {/* STOCK TABLE */}
      <div
        style={{
          background: "#ffffff",
          borderRadius: "12px",
          overflowX: "auto",
          boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr
              style={{
                background: "#2563eb",
                color: "#fff",
                height: "60px",
              }}
            >
              <th style={{ padding: "14px" }}>Company</th>
              <th>Current Price</th>
              <th>Daily Change</th>
              <th>52W High</th>
              <th>52W Low</th>
              <th>Volume</th>
            </tr>
          </thead>

          <tbody>
            {filteredStocks.length === 0 ? (
              <tr>
                <td
                  colSpan="6"
                  style={{
                    padding: "50px",
                    textAlign: "center",
                    color: "#6b7280",
                    fontSize: "18px",
                  }}
                >
                  No stock data found.
                </td>
              </tr>
            ) : (
              filteredStocks.map((stock, index) => (
                <tr
                  key={stock.id || index}
                  style={{
                    background:
                      index % 2 === 0 ? "#ffffff" : "#f9fafb",
                    borderBottom: "1px solid #e5e7eb",
                    textAlign: "center",
                    transition: "all 0.25s ease",
                    cursor: "pointer",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "#eff6ff";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background =
                      index % 2 === 0 ? "#ffffff" : "#f9fafb";
                  }}
                >
                  <td
                    style={{
                      padding: "16px",
                      fontWeight: "600",
                      color: "#111827",
                    }}
                  >
                    {stock.company}
                  </td>

                  <td
                    style={{
                      fontWeight: "600",
                      color: "#2563eb",
                    }}
                  >
                    ₹ {stock.price.toLocaleString()}
                  </td>

                  <td
                    style={{
                      color:
                        stock.change >= 0 ? "#16a34a" : "#dc2626",
                      fontWeight: "700",
                    }}
                  >
                    {stock.change > 0 ? "+" : ""}
                    {stock.change.toFixed(2)}%
                  </td>

                  <td
                    style={{
                      color: "#16a34a",
                      fontWeight: "600",
                    }}
                  >
                    ₹ {stock.high52.toLocaleString()}
                  </td>

                  <td
                    style={{
                      color: "#dc2626",
                      fontWeight: "600",
                    }}
                  >
                    ₹ {stock.low52.toLocaleString()}
                  </td>

                  <td
                    style={{
                      color: "#7c3aed",
                      fontWeight: "600",
                    }}
                  >
                    {stock.volume.toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* MARKET SUMMARY */}
      <div
        style={{
          marginTop: "35px",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
          gap: "20px",
        }}
      >
        <SummaryCard
          title="📈 Top Gainer"
          value={
            marketSummary.topGainer
              ? `${marketSummary.topGainer.company} (+${marketSummary.topGainer.change.toFixed(2)}%)`
              : "-"
          }
          color="#16a34a"
        />

        <SummaryCard
          title="📉 Top Loser"
          value={
            marketSummary.topLoser
              ? `${marketSummary.topLoser.company} (${marketSummary.topLoser.change.toFixed(2)}%)`
              : "-"
          }
          color="#dc2626"
        />

        <SummaryCard
          title="📊 Total Volume"
          value={marketSummary.totalVolume.toLocaleString()}
          color="#2563eb"
        />

        <SummaryCard
          title="💹 Highest Price"
          value={`₹ ${highestPrice.toLocaleString()}`}
          color="#7c3aed"
        />
      </div>

      {/* DASHBOARD FOOTER */}
      <div
        style={{
          marginTop: "40px",
          padding: "20px",
          textAlign: "center",
          color: "#6b7280",
          borderTop: "1px solid #e5e7eb",
        }}
      >
        Showing {filteredStocks.length} companies • Data refreshed from NIFTY100 Financial Intelligence API
      </div>
    </Layout>
  );
}

/* ===========================================================
   Summary Card Component
=========================================================== */

function SummaryCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "22px",
        borderRadius: "12px",
        borderLeft: `6px solid ${color}`,
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
      }}
    >
      <h4
        style={{
          color: "#6b7280",
          marginBottom: "12px",
        }}
      >
        {title}
      </h4>

      <h2
        style={{
          margin: 0,
          color,
          fontSize: "28px",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default StockPrices;