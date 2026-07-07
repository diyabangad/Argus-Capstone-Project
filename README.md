# 🔱 ARGUS
### Autonomous Risk & Governance for Unified Supply Chain

> "See the risk before it becomes a loss."

An AI-powered Procurement & Supply Chain Risk Intelligence Platform built for enterprise ERP ecosystems (SAP Ariba / S/4HANA).

## Modules
- **Module A** — Price & Invoice Anomaly Detection
- **Module B** — Supply Chain Disruption Prediction
- **Argus Assistant** — Conversational chatbot with live ML tool-calling

## Tech Stack
- Backend: FastAPI + Python
- ML: Scikit-learn, XGBoost, LightGBM, Prophet
- Frontend: React + Tailwind + Recharts
- Chatbot: LLM + RAG + LangChain
- Database: PostgreSQL
- Deployment: Docker + Render

## Data engineering and feature store
- Run the preprocessing pipeline with:
  - `/home/codespace/.python/current/bin/python backend/ml/prepare_procurement_logistics_dataset.py`
- This creates cleaned procurement, cleaned logistics, synthetic procurement, and unified datasets in backend/data/processed.
- The SQLite demo feature store is populated with the unified data via backend/app/load_feature_store.py.

## Module A and Module B
- Module A trains an Isolation Forest model for price anomaly detection.
- Module B trains a delay-risk classifier and regressor for disruption prediction.
- Model artifacts are stored in backend/ml/models.

## Backend API
- Start the API with:
  - `/home/codespace/.python/current/bin/python -m uvicorn app.main:app --reload`
- Available endpoints include:
  - `/api/price-risk`
  - `/api/delay-risk`
  - `/api/remediation`
  - `/api/summary`

## Quick smoke test
- Run:
  - `/home/codespace/.python/current/bin/python -m pytest -q tests/test_api.py`
- This verifies the core API flow and remediation logic.

## Team
Built for Neovatic Capstone Project
