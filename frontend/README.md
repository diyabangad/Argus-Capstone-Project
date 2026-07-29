# ARGUS Dashboard

## Run locally

Start the backend from the repository root:

```powershell
cd backend
uvicorn app.main:app --reload
```

In a second terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

The Vite development server proxies `/api` and `/mock` requests to the
FastAPI backend at `http://127.0.0.1:8000`.
