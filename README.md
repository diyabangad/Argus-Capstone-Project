# 🔱 ARGUS
### Autonomous Risk & Governance for Unified Supply Chain
> *"See the risk before it becomes a loss."*

Built for **Neovatic** Capstone Project — An AI-powered Procurement & Supply Chain Risk Intelligence Platform designed for SAP Ariba / S/4HANA enterprise ecosystems.

---

## 🚨 The Problem
Enterprises using ERP systems like SAP discover pricing fraud and delivery delays **only after they happen** — causing financial leakage and operational disruption. There is no unified system that proactively flags these risks before a PO is finalized or a shipment fails.

---

## ✅ Our Solution
ARGUS is a unified AI platform with two intelligence engines sharing one vendor risk backbone:
- **Proactively flags** pricing anomalies and fake invoices before approval
- **Predicts** supply chain disruptions 5+ days before they occur
- **Recommends** corrective actions — renegotiation targets or alternate vendor rerouting
- **Converses** — a plain-English chatbot that queries live ML models on demand
- **Integrates** — outputs clean JSON payloads ready for SAP / RPA automation triggers

---

## 🧠 Modules

| Module | Description | Models Used |
|---|---|---|
| **Module A** | Price & Invoice Anomaly Detection | Isolation Forest, Autoencoder, Prophet |
| **Module B** | Supply Chain Disruption Prediction | XGBoost, LightGBM, Random Forest |
| **Optimizer** | Remediation & Vendor Re-routing Engine | Greedy Constraint Optimizer |
| **Argus Assistant** | Conversational AI Chatbot | LLM + RAG + Tool Calling |

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────┐
│              DATA INGESTION LAYER                     │
│    Procurement KPI Dataset + Logistics Dataset        │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│              SHARED FEATURE STORE                     │
│   Vendor Reliability Score · Price Volatility Index   │
│   Lead Time History  · Material Scarcity Index        │
└────────────┬─────────────────────┬───────────────────┘
             │                     │
             ▼                     ▼
┌─────────────────────┐  ┌─────────────────────────────┐
│      MODULE A       │  │         MODULE B             │
│    Price & Invoice  │  │   Supply Chain Disruption    │
│   Anomaly Detection │  │      Delay Classifier        │
└──────────┬──────────┘  └────────────┬────────────────┘
           │                          │
           └────────────┬─────────────┘
                        ▼
┌──────────────────────────────────────────────────────┐
│        OPTIMIZATION & REMEDIATION ENGINE              │
│  Renegotiation Target · Alternate Vendor Reroute      │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                  DELIVERY LAYER                       │
│  React Dashboard · Argus Chatbot · FastAPI Endpoint   │
└──────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Python 3.11 |
| ML — Anomaly Detection | Scikit-learn (Isolation Forest), Keras (Autoencoder) |
| ML — Forecasting | Prophet, ARIMA |
| ML — Disruption | XGBoost, LightGBM |
| Optimization | OR-Tools / Greedy Constraint Programming |
| Frontend Dashboard | React + Tailwind CSS + Recharts |
| Chatbot | LLM (Claude/GPT) + LangChain + RAG + ChromaDB |
| Database | PostgreSQL |
| Deployment | Docker + Render |

---

## 📁 Project Structure
argus-capstone/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── routers/          # API route handlers
│   │   ├── models/           # ML model loaders
│   │   ├── schemas/          # Pydantic schemas
│   │   └── core/             # Config & DB connection
│   ├── ml/
│   │   ├── module_a_price_anomaly/    # Anomaly detection notebooks & scripts
│   │   ├── module_b_disruption/       # Delay prediction notebooks & scripts
│   │   └── optimization/              # Remediation engine
│   └── data/
│       ├── raw/              # Original datasets
│       └── processed/        # Cleaned & engineered datasets
├── frontend/                 # React dashboard
├── chatbot/                  # Argus Assistant (RAG + tool calling)
├── docs/                     # Architecture & documentation
├── .env.example              # Environment variable template
└── README.md
---

## 📊 Datasets

| Dataset | Source | Purpose |
|---|---|---|
| Procurement KPI Analysis | Kaggle (shahriarkabir) | Module A — price anomaly, invoice risk |
| Logistics & Supply Chain | Kaggle (datasetengineer) | Module B — delay prediction, disruption risk |

---

## 🤖 Argus Assistant — Chatbot Capabilities

| User Query | Action |
|---|---|
| "Show high risk invoices this week" | Queries risk DB, returns flagged table |
| "Why is invoice INV-4521 flagged?" | SHAP explanation in plain English |
| "What should I pay for steel next month?" | Prophet forecast + renegotiation price |
| "Is PO-1190 at risk of delay?" | Module B classifier → probability + days |
| "Summarize this month's procurement risk" | Executive summary across both modules |

---

## 💡 Why ARGUS for Neovatic

| Neovatic Focus Area | ARGUS Alignment |
|---|---|
| SAP Ariba / S4HANA | Output payloads simulate SAP integration triggers |
| Hyper-Automation / RPA | JSON API output ready for RPA bot consumption |
| Manufacturing & Chemicals | Vendor + material-level risk profiling |
| Data Science & AI | End-to-end ML pipeline from raw data to actionable insight |

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/diyabangad/Argus-Capstone-Project.git
cd Argus-Capstone-Project

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload
# API live at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## 📈 Project Status

| Component | Status |
|---|---|
| Project Structure | ✅ Complete |
| Dataset Ingestion | ✅ Complete |
| EDA & Feature Engineering | 🟡 In Progress |
| Module A — Price Anomaly | 🟡 In Progress |
| Module B — Disruption Risk | 🟡 In Progress |
| Optimization Engine | 🔴 Upcoming |
| React Dashboard | 🔴 Upcoming |
| Argus Chatbot | 🔴 Upcoming |
| Deployment | 🔴 Upcoming |

---

## 👥 Team
Built by **Team ARGUS** for **Neovatic Capstone 2025**

*Powered by Python · FastAPI · React · LangChain · XGBoost · Prophet*
EOF
