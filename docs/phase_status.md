# Phase status

## Completed so far
- Data preprocessing pipeline and unified dataset generation
- Shared feature columns for supplier reliability, price anomaly, delay probability, and delivery deviation
- SQLite feature-store population
- Module A anomaly model training
- Module B delay-risk classifier and regressor training
- FastAPI endpoints for price risk, delay risk, remediation, and summary

## Remaining follow-up ideas
- Add PostgreSQL support for a more production-like demo
- Expand the remediation layer into a fuller optimization engine
- Add chatbot tool-calling and RAG support
