# Hybrid Crop Recommender (Production Split)

This project converts the notebook workflow into a structured production setup:

- `backend/`: FastAPI API + training pipeline + model artifacts
- `frontend/`: React UI (Vite)

## Quick Start

### 1) Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m train.train --data "C:\Users\jitendra kumar\Downloads\Sanchinta\Crop_recommendation.csv"
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend expects API at `http://127.0.0.1:8000`.

## Deploy (Render)

- Deploy backend as a web service using `backend/` root.
- Deploy frontend as static site (or web service), set `VITE_API_BASE_URL` to backend URL.
