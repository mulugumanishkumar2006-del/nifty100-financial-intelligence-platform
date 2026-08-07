import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";

import Layout from "../components/Layout";
import { askAI } from "../services/aiChatService";

function AIChat() {
  const [searchParams] = useSearchParams();

  const companyId = searchParams.get("company");
  const companyName =
    searchParams.get("name") || "NIFTY100 Companies";

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // ==========================================================
  // Auto Scroll
  // ==========================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // ==========================================================
  // Initial Message
  // ==========================================================

  useEffect(() => {
    if (companyId) {
      setMessages([
        {
          type: "ai",
          text: `👋 I'm ready to help you analyze ${companyName}.

You can ask about:
• Financial performance
• Growth
• Risk
• Profitability
• Valuation
• Investment considerations`,
        },
      ]);
    }
  }, [companyId, companyName]);

  // ==========================================================
  // Ask AI
  // ==========================================================

  async function handleAskAI() {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    let finalQuestion = trimmedQuestion;

    // Add company context when coming from Company Details
    if (companyId) {
      finalQuestion = `
Company ID: ${companyId}
Company Name: ${companyName}

User Question:
${trimmedQuestion}

Answer specifically in the context of this company.
`;
    }

    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await askAI(finalQuestion);

      setMessages((previous) => [
        ...previous,
        {
          type: "ai",
          text:
            response?.answer ||
            response?.response ||
            response?.message ||
            "The AI service returned an empty response.",
        },
      ]);
    } catch (error) {
      console.error("AI Chat Error:", error);

      setMessages((previous) => [
        ...previous,
        {
          type: "ai",
          text:
            error.message ||
            "Unable to generate an AI response. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // ==========================================================
  // Keyboard Handler
  // ==========================================================

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskAI();
    }
  }

  // ==========================================================
  // Clear Chat
  // ==========================================================

  function clearChat() {
    setMessages([]);

    if (companyId) {
      setMessages([
        {
          type: "ai",
          text: `Chat cleared.

Ask me anything about ${companyName}.`,
        },
      ]);
    }
  }

  // ==========================================================
  // Render
  // ==========================================================

  return (
    <Layout>
      <div
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
          padding: "30px",
        }}
      >
        {/* Header */}

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "8px",
          }}
        >
          <div>
            <h1
              style={{
                margin: 0,
              }}
            >
              🤖 AI Financial Assistant
            </h1>

            <p
              style={{
                color: "#64748b",
                marginTop: "8px",
              }}
            >
              {companyId
                ? `Analyzing ${companyName}`
                : "Ask anything about NIFTY100 companies."}
            </p>
          </div>

          {messages.length > 0 && (
            <button
              onClick={clearChat}
              style={{
                padding: "10px 16px",
                border: "1px solid #cbd5e1",
                borderRadius: "10px",
                background: "#ffffff",
                cursor: "pointer",
                fontWeight: "600",
                color: "#475569",
              }}
            >
              Clear Chat
            </button>
          )}
        </div>

        {/* Company Context */}

        {companyId && (
          <div
            style={{
              background:
                "linear-gradient(135deg,#eff6ff,#dbeafe)",
              border: "1px solid #bfdbfe",
              borderRadius: "12px",
              padding: "14px 18px",
              margin: "20px 0",
              color: "#1e40af",
            }}
          >
            <strong>📊 Company Context</strong>

            <div
              style={{
                marginTop: "5px",
                fontSize: "14px",
              }}
            >
              {companyName} · ID: {companyId}
            </div>
          </div>
        )}

        {/* Chat Window */}

        <div
          style={{
            background: "#ffffff",
            borderRadius: "15px",
            boxShadow: "0 10px 25px rgba(0,0,0,.08)",
            height: "500px",
            overflowY: "auto",
            padding: "20px",
            marginBottom: "20px",
          }}
        >
          {/* Empty State */}

          {messages.length === 0 && (
            <div
              style={{
                textAlign: "center",
                color: "#94a3b8",
                marginTop: "130px",
              }}
            >
              <div
                style={{
                  fontSize: "50px",
                  marginBottom: "15px",
                }}
              >
                🤖
              </div>

              <h2
                style={{
                  color: "#334155",
                }}
              >
                AI Financial Assistant
              </h2>

              <p>
                Ask a question to begin your financial analysis.
              </p>

              <div
                style={{
                  marginTop: "20px",
                  lineHeight: "2",
                }}
              >
                <div>💰 What is the company's financial performance?</div>
                <div>📈 What are its growth prospects?</div>
                <div>⚠️ What are the major risks?</div>
              </div>
            </div>
          )}

          {/* Messages */}

          {messages.map((message, index) => (
            <div
              key={`${message.type}-${index}`}
              style={{
                display: "flex",
                justifyContent:
                  message.type === "user"
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "18px",
              }}
            >
              <div
                style={{
                  maxWidth: "75%",
                  padding: "15px 18px",
                  borderRadius: "15px",

                  background:
                    message.type === "user"
                      ? "#2563eb"
                      : "#f1f5f9",

                  color:
                    message.type === "user"
                      ? "#ffffff"
                      : "#111827",

                  lineHeight: "1.7",
                  whiteSpace: "pre-wrap",
                }}
              >
                {message.text}
              </div>
            </div>
          ))}

          {/* Loading */}

          {loading && (
            <div
              style={{
                display: "flex",
                justifyContent: "flex-start",
                marginBottom: "18px",
              }}
            >
              <div
                style={{
                  background: "#f1f5f9",
                  padding: "15px 18px",
                  borderRadius: "15px",
                  color: "#475569",
                }}
              >
                🤖 Thinking...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}

        <div
          style={{
            display: "flex",
            gap: "15px",
          }}
        >
          <textarea
            rows={3}
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
            placeholder={
              companyId
                ? `Ask anything about ${companyName}...`
                : "Ask anything about NIFTY100 companies..."
            }
            style={{
              flex: 1,
              padding: "15px",
              borderRadius: "12px",
              border: "1px solid #cbd5e1",
              fontSize: "16px",
              resize: "none",
              outline: "none",
            }}
          />

          <button
            onClick={handleAskAI}
            disabled={loading || !question.trim()}
            style={{
              width: "150px",
              border: "none",
              borderRadius: "12px",

              background:
                loading || !question.trim()
                  ? "#94a3b8"
                  : "#2563eb",

              color: "#ffffff",
              fontWeight: "600",
              cursor:
                loading || !question.trim()
                  ? "not-allowed"
                  : "pointer",

              fontSize: "16px",
            }}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>

        {/* Hint */}

        <p
          style={{
            textAlign: "center",
            color: "#94a3b8",
            fontSize: "12px",
            marginTop: "12px",
          }}
        >
          Press Enter to send · Shift + Enter for a new line
        </p>
      </div>
    </Layout>
  );
}

export default AIChat;