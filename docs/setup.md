# Setup

## Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn backend.main:app --reload
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Docker services

```powershell
docker compose up -d postgres kafka kafka-ui
```

