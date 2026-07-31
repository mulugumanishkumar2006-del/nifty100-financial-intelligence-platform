# 📈 NIFTY100 Financial Intelligence Platform

> A full-stack financial analytics platform for analyzing NIFTY100 companies using FastAPI, React, SQLite, and AI-powered insights.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 🚀 Project Overview

The **NIFTY100 Financial Intelligence Platform** is an end-to-end financial analytics application designed to analyze Indian stock market companies.

The platform combines:

- Financial Statements
- Stock Price Analysis
- Financial Ratios
- Sector Analytics
- Company Comparison
- Interactive Dashboard
- AI-powered Financial Intelligence (In Progress)

The objective is to provide investors, students, analysts, and recruiters with an intelligent financial analysis platform.

---

# ✨ Features

## 📊 Dashboard

- Executive Dashboard
- KPI Cards
- Revenue Analytics
- Profit Analytics
- Sector Distribution
- Market Summary

---

## 🏢 Company Module

- Company Directory
- Company Search
- Company Details
- Company Financial Summary

---

## 💹 Stock Price Module

- Latest Stock Prices
- Company Price History
- Search Companies
- Sorting
- Market Overview
- Top Gainers
- Top Losers
- Volume Analysis

---

## 📈 Financial Ratios

- ROE
- ROCE
- EPS
- Debt Equity Ratio
- Current Ratio
- P/E Ratio
- Company-wise Ratios

---

## 🏭 Sector Analytics

- Sector Summary
- Financial Distribution
- Company Count
- Revenue Distribution

---

## 🤖 AI Intelligence (Coming Soon)

- AI Company Health Score
- Buy / Hold / Sell Recommendation
- Risk Analysis
- AI Financial Summary
- Company Ranking
- Portfolio Suggestions

---

# 🛠 Tech Stack

## Frontend

- React.js
- JavaScript
- Axios
- CSS

---

## Backend

- FastAPI
- Python
- Pandas
- SQLite

---

## Database

- SQLite

---

## Data Processing

- Pandas
- NumPy

---

# 📂 Project Structure

```
NIFTY100-Financial-Intelligence/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   └── database/
│       └── nifty100.db
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│
├── data/
│
├── README.md
│
└── requirements.txt
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/nifty100-financial-intelligence.git
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

Swagger Docs

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 📡 API Endpoints

## Companies

```
GET /api/companies
```

```
GET /api/company/{id}
```

---

## Stock Prices

```
GET /api/stock-prices
```

```
GET /api/stock-prices/company/{id}
```

```
GET /api/stock-prices/latest/{id}
```

---

## Financial Ratios

```
GET /api/financial-ratios
```

```
GET /api/financial-ratios/company/{id}
```

---

## Sector Analytics

```
GET /api/sectors/summary
```

```
GET /api/sectors/financial
```

---

## Dashboard

```
GET /api/dashboard
```

---

# 📊 Current Modules

- ✅ Dashboard
- ✅ Companies
- ✅ Stock Prices
- ✅ Financial Ratios
- ✅ Sector Analytics
- 🚧 AI Intelligence
- 🚧 Company Comparison
- 🚧 Stock Forecasting

---

# 📌 Roadmap

## Phase 1

- Database Design
- ETL Pipeline
- API Development

✅ Completed

---

## Phase 2

- React Dashboard
- Company Module
- Stock Module

✅ Completed

---

## Phase 3

- AI Intelligence
- Company Health Score
- Recommendation Engine

🚧 In Progress

---

## Phase 4

- Authentication
- Portfolio Tracking
- Watchlist
- News Analysis

🔜 Planned

---
#
```
Dashboard

Company Module

Stock Prices

Financial Ratios

Sector Analytics

AI Intelligence
```

---

# 🎯 Learning Outcomes

This project demonstrates:

- Full Stack Development
- REST API Design
- Database Management
- Financial Data Analysis
- React Development
- FastAPI Backend
- Data Visualization
- Software Architecture

---

# 🚀 Future Enhancements

- Machine Learning Price Prediction
- AI Chat Assistant
- Portfolio Optimization
- News Sentiment Analysis
- Technical Indicators
- Candlestick Charts
- PDF Reports
- Excel Export
- Cloud Deployment

---

# 👨‍💻 Author

**Mulugu Maneesh Kumar**

B.Tech CSE (AI & ML)

Sir Padampat Singhania University

GitHub:
https://github.com/mulugumanishkumar2006-del



---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📜 License

This project is licensed under the MIT License.