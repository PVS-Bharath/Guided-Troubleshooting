# Smart Guided Troubleshooting Engine
**Samsung PRISM Generative AI Hackathon 3rd Edition 2026–27**  
**Theme 02 — Smart Guided Troubleshooting Engine**  
**Team:** Srm_Devlopers  
**Person 4:** REST API + Frontend + Integration  

---

## 1. Project Overview

The Smart Guided Troubleshooting Engine takes a natural-language mobile device complaint (e.g., *"My phone is getting very hot"* or *"Wi-Fi drops frequently"*) and generates structured, ordered, actionable troubleshooting steps with verified Samsung Settings deeplinks.

This repository hosts the **Person 4 Integration Layer**, connecting:
- **Person 1:** AI / LLM Engine (Intent extraction & Query enrichment)
- **Person 2:** Knowledge / Semantic Retrieval (Knowledge lookup & Ranking)
- **Person 3:** Deeplink / Validation / Fast-Path Cache (Catalog verification & Caching)
- **Person 4:** REST API + Frontend + Integration

---

## 2. Architecture & Pipeline

```
User Complaint (Browser)
       │
       ▼
React + TypeScript Frontend (http://localhost:5173)
       │
       ▼ POST /api/troubleshoot (Proxied)
FastAPI Backend (http://localhost:8000/troubleshoot)
       │
       ▼
Orchestration Service (Dependency Injected)
       ├── AI Engine Adapter (enrich)
       ├── Retrieval Adapter (retrieve)
       └── Deeplink & Validation Adapter (validate_and_map)
       │
       ▼
Validated Troubleshooting Response JSON
```

---

## 3. Technology Stack

- **Backend:** Python 3.13+, FastAPI, Pydantic v2, Uvicorn
- **Frontend:** React 19, TypeScript 5.8, Vite 8, Axios
- **Testing:** Pytest 9, HTTPX 0.28, FastAPI TestClient

---

## 4. Quick Start

### Backend Startup

```powershell
cd C:\vs\test\Guided-Troubleshooting

# Activate virtual environment
.\backend\venv\Scripts\activate

# Install requirements (if not already installed)
pip install -r backend\requirements.txt

# Run backend (from repository root)
python -m uvicorn backend.main:app --reload --port 8000
```

- Health Check: `GET http://localhost:8000/health`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`

### Frontend Startup

```powershell
cd C:\vs\test\Guided-Troubleshooting\frontend

# Install dependencies (if not already installed)
npm install

# Run Vite dev server
npm run dev
```

- Open in browser: `http://localhost:5173`

---

## 5. Running Automated Tests

From the project root:

```powershell
cd C:\vs\test\Guided-Troubleshooting

# Run verbose test suite
.\backend\venv\Scripts\pytest.exe tests/backend -v

# Run quiet mode
.\backend\venv\Scripts\pytest.exe -q
```

All 11 tests covering health, request validation, response payload structure, mock deeplink tags, custom trace IDs, and adapter error propagation (502 status) pass.

---

## 6. API Reference

### `GET /health`
- **Response (200 OK):**
  ```json
  {
    "status": "ok"
  }
  ```

### `POST /troubleshoot`
- **Request Body:**
  ```json
  {
    "query": "My phone is getting very hot",
    "request_id": "optional-custom-uuid"
  }
  ```
- **Response (200 OK — Development Mock):**
  ```json
  {
    "request_id": "c1f7b889-16f5-4d2c-80b6-12c5ff21db28",
    "query": "My phone is getting very hot",
    "goal": "Reduce device overheating",
    "actions": [
      {
        "actionName": "Battery",
        "description": "It will help reduce battery usage",
        "steps": [
          "Open Settings",
          "Select Battery",
          "Check battery usage"
        ],
        "deeplink": "settings://battery",
        "category": "manual",
        "is_mock": true
      }
    ]
  }
  ```

---

## 7. Development Mock Notice

> [!IMPORTANT]
> The current actions, steps, and `settings://battery` URL are **temporary development mocks**. They are NOT official Samsung data or official Samsung deeplinks. The UI explicitly flags them as development mocks. When official Theme 02 assets (`schema.py`, `deeplinks.json`, etc.) are delivered, real adapters will replace these placeholders.

---

## 8. Integration for Persons 1, 2, and 3

The orchestrator in `backend/services/orchestrator.py` communicates exclusively via the protocols in `backend/adapters/interfaces.py`:
- `AIEngine.enrich(query: str) -> Dict[str, Any]`
- `RetrievalEngine.retrieve(enriched_data: Dict[str, Any]) -> List[Dict[str, Any]]`
- `DeeplinkValidator.validate_and_map(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]`

To integrate:
1. Implement your real module following the corresponding protocol.
2. Replace the mock import in `backend/main.py` (`get_orchestrator`).
3. No changes to the REST API endpoints or frontend application will be needed.
