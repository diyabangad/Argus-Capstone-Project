# 🔱 ARGUS
### Autonomous Risk & Governance for Unified Supply Chain
> *"See the risk before it becomes a loss."*

Built for the **Neovatic Capstone Project**, ARGUS is an AI-powered Procurement & Supply Chain Risk Intelligence Platform built for ERP ecosystems such as SAP Ariba and SAP S/4HANA.

ARGUS unifies procurement and logistics data into a shared feature store, applies risk models for pricing anomalies and delivery disruption, and delivers remediation and automation outputs via backend APIs and a React dashboard.

---

## What ARGUS includes
- End-to-end data ingestion and unified feature store creation
- Price anomaly risk scoring using isolation forest based ML
- Delay risk prediction using classification and regression models
- Remediation recommendation engine for high-risk POs
- Automation payload generation and webhook simulation
- React + Tailwind dashboard for live risk visibility
- Lightweight CLI chatbot assistant powered by backend APIs
- Docker Compose deployment for local end-to-end demos

---

## Live Demo 

<img width="1600" height="734" alt="image" src="https://github.com/user-attachments/assets/d5aa40b5-5c88-4290-9176-d3d068d9131b" />

<img width="1600" height="723" alt="image" src="https://github.com/user-attachments/assets/3263fea6-6b6c-4af0-b26b-b9ab71f8e407" />

<img width="1600" height="510" alt="image" src="https://github.com/user-attachments/assets/d16ac8e4-5ddd-436e-978d-9178b4c3692a" />

---

## Tech stack
- Backend: FastAPI + Python 3.12
- Database: SQLite demo feature store
- ML: scikit-learn, XGBoost, pandas, joblib
- Frontend: React + Vite + Tailwind CSS
- Automation / webhook: JSON payload generation
- Chatbot: rule-based CLI assistant interfacing with the backend
- Deployment: Docker + Docker Compose

---

## Key capabilities
- High-risk purchase order discovery
- Supplier risk profile analytics
- Price anomaly and delay probability scoring
- Remediation advice for procurement decision-making
- SAP-style automation payloads for RPA / integration engines
- Live dashboard with KPI cards and risk tables
- CLI assistant for natural-language risk queries

---

## Project structure

```
Argus-Capstone-Project/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entrypoint and API router registration
│   │   ├── routers/                   # API route handlers
│   │   ├── models/                    # SQLAlchemy ORM models
│   │   ├── schemas/                   # Pydantic request/response schemas
│   │   └── core/                      # Config and database connection
│   ├── data/
│   │   ├── raw/                       # Original procurement and logistics source files
│   │   └── processed/                 # Cleaned unified datasets for the feature store
│   └── ml/                           # Model training scripts and saved joblib artifacts
├── chatbot/                           # CLI assistant client for backend APIs
├── docs/                              # Architecture, phase status, and documentation notes
├── frontend/                          # React dashboard application
├── docker-compose.yml                # Local Docker orchestration
├── start.sh                          # Backend startup script with initialization checks
└── README.md                       # Project documentation
```

---

## Data and model artifacts
- `backend/data/processed/unified_procurement_logistics.csv` is the main unified dataset used by the feature store.
- `backend/ml/models/module_a_isolation_forest.joblib` is the price anomaly model.
- `backend/ml/models/module_b_delay_classifier.joblib` and `backend/ml/models/module_b_delay_regressor.joblib` power delay forecasting.
- Training and preprocessing artifacts are available in `backend/ml/` and the associated notebooks.

---

## Running ARGUS locally

### Option 1: Docker Compose

```bash
git clone https://github.com/diyabangad/Argus-Capstone-Project.git
cd Argus-Capstone-Project
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Option 2: Local development

```bash
cd Argus-Capstone-Project/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/init_db.py
python app/load_feature_store.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In a second terminal:

```bash
cd Argus-Capstone-Project/frontend
npm install
npm run dev -- --host 0.0.0.0
```

### Backend quick-start script

```bash
chmod +x start.sh
./start.sh
```

This helper script initializes the SQLite database, loads the feature store, and starts the FastAPI backend only if it is not already running.

---

## Backend API endpoints

### Risk and model endpoints
- `GET /api/price-risk?po_id=<PO_ID>` — returns price anomaly score and risk flag.
- `GET /api/delay-risk?po_id=<PO_ID>` — returns delay probability and predicted delay days.
- `POST /api/remediation` — returns remediation advice for a purchase order.
- `POST /api/automation/payload` — builds a structured SAP-style automation payload.
- `POST /api/automation/webhook` — simulates webhook ingestion for automation payloads.
- `POST /api/chatbot/ask` — generates an assistant response from a message.
- `GET /api/summary` — returns aggregate dataset risk metrics.

### Feature-store endpoints
- `GET /api/high-risk-purchase-orders` — returns active high-risk POs from SQLite.
- `GET /api/vendor-risk-profile/{supplier_name}` — returns supplier risk profile and scores.
- `GET /api/summary` — returns feature-store summary metrics.

### Mock risk endpoint
- `GET /mock/risk-summary` — returns demo risk records for vendor/category filtering.

---

## Frontend dashboard
The React dashboard is built with Vite and Tailwind CSS. It includes:
- KPI cards for average anomaly and delay risk
- Vendor risk profile selection and summary
- High-risk purchase order table
- Automation payload panel for PO action simulation

The frontend proxies `/api` requests to the backend and displays live risk data from the SQLite feature store.

---

## Chatbot assistant
The chatbot CLI in `chatbot/chatbot.py` demonstrates conversational interaction with ARGUS using backend APIs. It supports:
- high-risk order queries
- vendor risk profile requests
- summary and overview responses

This assistant is rule-driven and illustrates how ARGUS can support natural-language risk triage.

---

## Tests
Run backend API tests with:

```bash
cd Argus-Capstone-Project
source backend/.venv/bin/activate
pytest -q tests/test_api.py
```

The test suite validates the core risk endpoints and ensures backend behavior is stable.

---

## Presentation flow
1. Start the backend and verify health: `GET http://localhost:8000/health`
2. Open the dashboard at `http://localhost:5173`
3. Show high-risk POs and vendor profiles
4. Demonstrate automation payload generation and webhook simulation
5. Run the chatbot assistant for a live query
6. Explain the data flow from CSV ingestion to risk scoring and remediation

---

## Value proposition
ARGUS helps procurement and supply chain teams:
- identify price anomalies before approval
- predict delivery disruption risk ahead of execution
- recommend remediation actions for procurement decisions
- deliver structured outputs suitable for SAP / RPA automation
- present a unified view of supplier risk and high-risk orders

---

## Notes
- The current demo uses SQLite and local model artifacts for fast presentation.
- The backend architecture is designed for easy extension to enterprise data sources.
- Docker Compose provides a reproducible local deployment path.

---

## Credits
Built by **Team ARGUS** for the Neovatic Capstone Project.
