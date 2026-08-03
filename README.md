# 🔱 ARGUS
### Autonomous Risk & Governance for Unified Supply Chain

> "See the risk before it becomes a loss."

ARGUS is an AI-powered procurement and supply chain risk intelligence platform designed for enterprise ERP ecosystems such as SAP Ariba and S/4HANA.

## What is implemented
- End-to-end data preprocessing and unified feature generation
- Trained anomaly and disruption-risk ML models
- FastAPI backend with risk, remediation, automation, and chatbot endpoints
- React + Tailwind frontend dashboard
- Docker-based local deployment setup

## Tech Stack
- Backend: FastAPI + Python
- ML: scikit-learn, joblib, pandas
- Frontend: React + Vite + Tailwind
- Chatbot: lightweight rule-based assistant endpoint
- Database: SQLite demo feature store
- Deployment: Docker + Docker Compose

## Run locally
### With Docker
```bash
docker compose up --build
```

This starts:
- Backend on http://localhost:8000
- Frontend on http://localhost:5173

### Without Docker
```bash
cd backend
source ../.venv/bin/activate
python app/init_db.py
python app/load_feature_store.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal:
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Core API endpoints
- /api/price-risk
- /api/delay-risk
- /api/remediation
- /api/automation/payload
- /api/automation/webhook
- /api/chatbot/ask
- /api/summary

## Tests
```bash
source .venv/bin/activate
pytest -q tests/test_api.py
```

## Team
Built for the ARGUS capstone project
