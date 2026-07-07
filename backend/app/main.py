from datetime import datetime

from fastapi import FastAPI

from app.routers.mock_risk import router as mock_risk_router
from app.routers.risk import router as risk_router

app = FastAPI(
    title="ARGUS — Autonomous Risk & Governance for Unified Supply Chain",
    description="AI-powered Procurement & Supply Chain Risk Intelligence Platform built for SAP Ariba / S4HANA ecosystems",
    version="1.0.0"
)
app.include_router(mock_risk_router)
app.include_router(risk_router)

@app.get("/")
def root():
    return {
        "platform": "ARGUS",
        "tagline": "See the risk before it becomes a loss",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "modules": {
            "module_a_price_anomaly": "ready",
            "module_b_disruption_risk": "ready",
            "argus_chatbot": "ready"
        },
        "datasets": {
            "procurement_kpi": "loaded",
            "logistics": "loaded"
        }
    }

@app.get("/modules")
def modules():
    return {
        "module_a": {
            "name": "Price & Invoice Anomaly Detection",
            "model": "Isolation Forest + Autoencoder",
            "status": "in development"
        },
        "module_b": {
            "name": "Supply Chain Disruption Prediction",
            "model": "XGBoost / LightGBM",
            "status": "in development"
        },
        "optimization": {
            "name": "Remediation & Optimization Engine",
            "model": "Greedy Constraint Optimizer",
            "status": "in development"
        },
        "chatbot": {
            "name": "Argus Assistant",
            "model": "LLM + RAG + Tool Calling",
            "status": "in development"
        }
    }
