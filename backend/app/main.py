from fastapi import FastAPI

app = FastAPI(title="ARGUS API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "ARGUS is running ✅"}

@app.get("/health")
def health():
    return {"status": "ok", "modules": ["price_anomaly", "disruption_risk", "chatbot"]}
