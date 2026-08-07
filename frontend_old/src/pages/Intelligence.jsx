import { useEffect, useRef, useState } from "react";
import Layout from "../components/Layout";
import { getCompanies } from "../services/companyService";
import {
  getCompanyAIInsights,
  getGrowthAnalysis,
  getRiskAnalysis,
  getInvestmentRecommendation,
} from "../services/aiInsightService";
import { askAI } from "../services/aiChatService";

function Intelligence() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");

  const [insights, setInsights] = useState(null);
  const [growth, setGrowth] = useState(null);
  const [risk, setRisk] = useState(null);
  const [recommendation, setRecommendation] = useState(null);

  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState([]);

  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [loadingInsights, setLoadingInsights] = useState(false);
  const [loadingChat, setLoadingChat] = useState(false);

  const chatEndRef = useRef(null);

  // ==========================================================
  // Load Companies
  // ==========================================================

  useEffect(() => {
    loadCompanies();
  }, []);

  // ==========================================================
  // Load AI Intelligence when company changes
  // ==========================================================

  useEffect(() => {
    if (companyId) {
      loadCompanyIntelligence(companyId);
    }
  }, [companyId]);

  // ==========================================================
  // Scroll Chat
  // ==========================================================

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [chatMessages, loadingChat]);

  // ==========================================================
  // Companies
  // ==========================================================

  async function loadCompanies() {
    try {
      setLoadingCompanies(true);

      const data = await getCompanies();

      setCompanies(data || []);

      if (data && data.length > 0) {
        setCompanyId(data[0].id);
      }
    } catch (error) {
      console.error("Companies Error:", error);
    } finally {
      setLoadingCompanies(false);
    }
  }

  // ==========================================================
  // Company AI Intelligence
  // ==========================================================

  async function loadCompanyIntelligence(id) {
    try {
      setLoadingInsights(true);

      const [
        companyInsights,
        growthData,
        riskData,
        recommendationData,
      ] = await Promise.all([
        getCompanyAIInsights(id),
        getGrowthAnalysis(id),
        getRiskAnalysis(id),
        getInvestmentRecommendation(id),
      ]);

      setInsights(companyInsights);
      setGrowth(growthData);
      setRisk(riskData);
      setRecommendation(recommendationData);

      // Reset chat when company changes
      setChatMessages([]);
      setQuestion("");
    } catch (error) {
      console.error(
        "Company Intelligence Error:",
        error
      );
    } finally {
      setLoadingInsights(false);
    }
  }

  // ==========================================================
  // Selected Company
  // ==========================================================

  const selectedCompany = companies.find(
    (company) => String(company.id) === String(companyId)
  );

  // ==========================================================
  // Ask AI about selected company
  // ==========================================================

  async function handleAskAI() {
    const currentQuestion = question.trim();

    if (!currentQuestion || loadingChat) {
      return;
    }

    const companyName =
      selectedCompany?.company_name || "this company";

    setChatMessages((previous) => [
      ...previous,
      {
        id: Date.now(),
        type: "user",
        text: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoadingChat(true);

    try {
      const contextualQuestion = `
You are analyzing ${companyName} from the NIFTY100 Financial Intelligence Platform.

Company ID: ${companyId}

Answer the user's question specifically in the context of this company.

User question:
${currentQuestion}
`;

      const response = await askAI(contextualQuestion);

      const answer =
        response?.answer ||
        response?.response ||
        response?.message ||
        "The AI returned an empty response.";

      setChatMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          type: "ai",
          text: answer,
        },
      ]);
    } catch (error) {
      console.error("Intelligence AI Chat Error:", error);

      setChatMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          type: "error",
          text:
            error.message ||
            "Unable to generate AI response.",
        },
      ]);
    } finally {
      setLoadingChat(false);
    }
  }

  // ==========================================================
  // Keyboard
  // ==========================================================

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskAI();
    }
  }

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <Layout>
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "30px",
        }}
      >
        {/* ==================================================
            Header
        ================================================== */}

        <div style={{ marginBottom: "25px" }}>
          <h1
            style={{
              margin: 0,
              color: "#0f172a",
            }}
          >
            🧠 NIFTY100 Intelligence
          </h1>

          <p
            style={{
              color: "#64748b",
              marginTop: "8px",
            }}
          >
            Analyze companies and ask AI questions
            using the same intelligence workspace.
          </p>
        </div>

        {/* ==================================================
            Company Selector
        ================================================== */}

        <div
          style={{
            background: "#ffffff",
            padding: "20px",
            borderRadius: "16px",
            border: "1px solid #e2e8f0",
            boxShadow:
              "0 8px 25px rgba(15,23,42,0.06)",
            marginBottom: "25px",
          }}
        >
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              fontWeight: "600",
              color: "#334155",
            }}
          >
            Select Company
          </label>

          <select
            value={companyId}
            onChange={(event) =>
              setCompanyId(event.target.value)
            }
            disabled={loadingCompanies}
            style={{
              width: "100%",
              maxWidth: "450px",
              padding: "12px",
              borderRadius: "10px",
              border: "1px solid #cbd5e1",
              fontSize: "15px",
              background: "#ffffff",
            }}
          >
            {companies.map((company) => (
              <option
                key={company.id}
                value={company.id}
              >
                {company.company_name}
              </option>
            ))}
          </select>
        </div>

        {/* ==================================================
            Selected Company
        ================================================== */}

        {selectedCompany && (
          <div
            style={{
              background:
                "linear-gradient(135deg,#eff6ff,#ffffff)",
              borderRadius: "16px",
              padding: "25px",
              marginBottom: "25px",
              border: "1px solid #bfdbfe",
            }}
          >
            <h2
              style={{
                margin: 0,
                color: "#1e3a8a",
              }}
            >
              {selectedCompany.company_name}
            </h2>

            <p
              style={{
                color: "#64748b",
                marginBottom: 0,
              }}
            >
              AI-powered financial intelligence
            </p>
          </div>
        )}

        {/* ==================================================
            AI Analysis Cards
        ================================================== */}

        {loadingInsights ? (
          <div
            style={{
              background: "#ffffff",
              padding: "30px",
              borderRadius: "16px",
              textAlign: "center",
              color: "#64748b",
              marginBottom: "25px",
            }}
          >
            🤖 Loading company intelligence...
          </div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(250px,1fr))",
              gap: "18px",
              marginBottom: "25px",
            }}
          >
            <InsightCard
              title="Growth Analysis"
              value={
                growth?.growth_analysis ||
                growth?.analysis ||
                "No growth analysis available."
              }
              color="#16a34a"
            />

            <InsightCard
              title="Risk Analysis"
              value={
                risk?.risk_analysis ||
                risk?.analysis ||
                "No risk analysis available."
              }
              color="#dc2626"
            />

            <InsightCard
              title="Recommendation"
              value={
                recommendation?.recommendation ||
                recommendation?.analysis ||
                "No recommendation available."
              }
              color="#2563eb"
            />
          </div>
        )}

        {/* ==================================================
            Complete AI Insights
        ================================================== */}

        {insights && (
          <div
            style={{
              background: "#ffffff",
              borderRadius: "16px",
              padding: "25px",
              border: "1px solid #e2e8f0",
              boxShadow:
                "0 8px 25px rgba(15,23,42,0.06)",
              marginBottom: "25px",
            }}
          >
            <h2
              style={{
                marginTop: 0,
                color: "#0f172a",
              }}
            >
              📊 Company Intelligence
            </h2>

            <pre
              style={{
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                color: "#475569",
                lineHeight: "1.7",
                fontSize: "14px",
                margin: 0,
              }}
            >
              {JSON.stringify(
                insights,
                null,
                2
              )}
            </pre>
          </div>
        )}

        {/* ==================================================
            AI Chat
        ================================================== */}

        <div
          style={{
            background: "#ffffff",
            borderRadius: "16px",
            border: "1px solid #e2e8f0",
            boxShadow:
              "0 10px 30px rgba(15,23,42,0.08)",
            overflow: "hidden",
          }}
        >
          {/* Chat Header */}

          <div
            style={{
              padding: "20px 25px",
              borderBottom:
                "1px solid #e2e8f0",
              background: "#f8fafc",
            }}
          >
            <h2
              style={{
                margin: 0,
                color: "#0f172a",
              }}
            >
              🤖 Ask AI About{" "}
              {selectedCompany?.company_name ||
                "the Company"}
            </h2>

            <p
              style={{
                color: "#64748b",
                marginBottom: 0,
              }}
            >
              Ask follow-up questions using the
              selected company's intelligence.
            </p>
          </div>

          {/* Chat Messages */}

          <div
            style={{
              height: "400px",
              overflowY: "auto",
              padding: "25px",
            }}
          >
            {chatMessages.length === 0 && (
              <div
                style={{
                  textAlign: "center",
                  marginTop: "100px",
                  color: "#94a3b8",
                }}
              >
                <div
                  style={{
                    fontSize: "42px",
                    marginBottom: "10px",
                  }}
                >
                  💬
                </div>

                <h3
                  style={{
                    color: "#475569",
                  }}
                >
                  Ask a financial question
                </h3>

                <p>
                  Example: "What are the major risks
                  for this company?"
                </p>
              </div>
            )}

            {chatMessages.map((message) => {
              const isUser =
                message.type === "user";
              const isError =
                message.type === "error";

              return (
                <div
                  key={message.id}
                  style={{
                    display: "flex",
                    justifyContent: isUser
                      ? "flex-end"
                      : "flex-start",
                    marginBottom: "16px",
                  }}
                >
                  <div
                    style={{
                      maxWidth: "75%",
                      padding: "14px 17px",
                      borderRadius: isUser
                        ? "16px 16px 4px 16px"
                        : "16px 16px 16px 4px",
                      background: isUser
                        ? "#2563eb"
                        : isError
                        ? "#fef2f2"
                        : "#f1f5f9",
                      color: isUser
                        ? "#ffffff"
                        : isError
                        ? "#b91c1c"
                        : "#1e293b",
                      lineHeight: "1.7",
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                    }}
                  >
                    {!isUser && (
                      <div
                        style={{
                          fontSize: "12px",
                          fontWeight: "700",
                          marginBottom: "5px",
                        }}
                      >
                        {isError
                          ? "⚠️ AI Assistant"
                          : "🤖 AI Assistant"}
                      </div>
                    )}

                    {message.text}
                  </div>
                </div>
              );
            })}

            {loadingChat && (
              <div
                style={{
                  display: "flex",
                  justifyContent: "flex-start",
                }}
              >
                <div
                  style={{
                    background: "#f1f5f9",
                    padding: "14px 17px",
                    borderRadius:
                      "16px 16px 16px 4px",
                    color: "#64748b",
                  }}
                >
                  🤖 Analyzing...
                </div>
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* Chat Input */}

          <div
            style={{
              padding: "18px",
              borderTop:
                "1px solid #e2e8f0",
              display: "flex",
              gap: "12px",
            }}
          >
            <textarea
              rows={3}
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              onKeyDown={handleKeyDown}
              disabled={loadingChat}
              placeholder={`Ask about ${selectedCompany?.company_name || "this company"}...`}
              style={{
                flex: 1,
                resize: "none",
                padding: "13px",
                borderRadius: "10px",
                border:
                  "1px solid #cbd5e1",
                fontSize: "14px",
                lineHeight: "1.5",
                outline: "none",
              }}
            />

            <button
              onClick={handleAskAI}
              disabled={
                loadingChat ||
                !question.trim()
              }
              style={{
                width: "120px",
                border: "none",
                borderRadius: "10px",
                background:
                  loadingChat ||
                  !question.trim()
                    ? "#94a3b8"
                    : "#2563eb",
                color: "#ffffff",
                fontWeight: "600",
                cursor:
                  loadingChat ||
                  !question.trim()
                    ? "not-allowed"
                    : "pointer",
              }}
            >
              {loadingChat
                ? "Thinking..."
                : "Ask AI"}
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}

// ==========================================================
// Insight Card
// ==========================================================

function InsightCard({
  title,
  value,
  color,
}) {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "15px",
        padding: "22px",
        borderTop: `5px solid ${color}`,
        boxShadow:
          "0 8px 20px rgba(15,23,42,0.07)",
      }}
    >
      <h3
        style={{
          color: "#64748b",
          marginTop: 0,
          marginBottom: "12px",
          fontSize: "15px",
        }}
      >
        {title}
      </h3>

      <p
        style={{
          margin: 0,
          color: "#334155",
          lineHeight: "1.6",
          fontSize: "14px",
        }}
      >
        {typeof value === "object"
          ? JSON.stringify(value, null, 2)
          : value}
      </p>
    </div>
  );
}

export default Intelligence;