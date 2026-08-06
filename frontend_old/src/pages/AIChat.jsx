import { useState, useRef, useEffect } from "react";
import Layout from "../components/Layout";
import axios from "axios";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };

  async function askAI() {
    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/chat/",
        {
          question: currentQuestion,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: res.data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "Unable to generate response.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askAI();
    }
  }

  return (
    <Layout>
      <div
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
          padding: "30px",
        }}
      >
        <h1
          style={{
            marginBottom: "8px",
          }}
        >
          🤖 AI Financial Assistant
        </h1>

        <p
          style={{
            color: "#64748b",
            marginBottom: "25px",
          }}
        >
          Ask anything about NIFTY100 companies.
        </p>

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
          {messages.length === 0 && (
            <div
              style={{
                textAlign: "center",
                color: "#94a3b8",
                marginTop: "150px",
              }}
            >
              <h2>👋 Welcome</h2>

              <p>
                Ask questions like:
              </p>

              <ul
                style={{
                  listStyle: "none",
                  padding: 0,
                }}
              >
                <li>Should I invest in TCS?</li>
                <li>Tell me about Reliance.</li>
                <li>Compare Infosys and Wipro.</li>
              </ul>
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                justifyContent:
                  msg.type === "user"
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "18px",
              }}
            >
              <div
                style={{
                  maxWidth: "75%",
                  padding: "15px",
                  borderRadius: "15px",
                  background:
                    msg.type === "user"
                      ? "#2563eb"
                      : "#f1f5f9",
                  color:
                    msg.type === "user"
                      ? "#fff"
                      : "#111827",
                  lineHeight: "1.7",
                  whiteSpace: "pre-wrap",
                }}
              >
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div
              style={{
                display: "flex",
                justifyContent: "flex-start",
              }}
            >
              <div
                style={{
                  background: "#f1f5f9",
                  padding: "15px",
                  borderRadius: "15px",
                }}
              >
                🤖 Thinking...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div
          style={{
            display: "flex",
            gap: "15px",
          }}
        >
          <textarea
            rows={3}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about NIFTY100 companies..."
            style={{
              flex: 1,
              padding: "15px",
              borderRadius: "12px",
              border: "1px solid #CBD5E1",
              fontSize: "16px",
              resize: "none",
            }}
          />

          <button
            onClick={askAI}
            disabled={loading}
            style={{
              width: "150px",
              border: "none",
              borderRadius: "12px",
              background: "#2563eb",
              color: "#fff",
              fontWeight: "600",
              cursor: "pointer",
              fontSize: "16px",
            }}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </Layout>
  );
}

export default AIChat;