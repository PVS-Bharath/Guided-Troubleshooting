# PERSON 4 IMPLEMENTATION GUIDE — INTEGRATION, API & FRONTEND
**Samsung PRISM Generative AI Hackathon 3rd Edition 2026–27**  
**Theme 02 — Smart Guided Troubleshooting Engine**  
**Team:** Srm_Devlopers  
**Role:** Person 4 — REST API + Frontend + Integration  
**Workspace:** `C:\vs\test\Guided-Troubleshooting`

---

## 1. Responsibilities of Person 4

Person 4 is responsible for:
1. REST API implementation with FastAPI (`GET /health`, `POST /troubleshoot`).
2. Central orchestration layer connecting all 4 team components.
3. Stable interface/adapter definitions (`AIEngine`, `RetrievalEngine`, `DeeplinkValidator`).
4. Working development mocks to unblock frontend and integration testing.
5. Modern, clean React + TypeScript frontend with Vite proxy.
6. Comprehensive test suite (`pytest`, `httpx`, `TestClient`).
7. Docker configuration and container readiness.
8. System-level error handling, logging, and documentation.

---

## 2. Architecture & Pipeline

```
User Query (e.g. "My phone is getting very hot")
    │
    ▼
Frontend (React + TypeScript)
    │
    ▼ POST /api/troubleshoot (Vite Proxy on port 5173)
FastAPI Backend (port 8000)
    │
    ▼ POST /troubleshoot
Orchestrator (backend/services/orchestrator.py)
    │
    ├── Step 1: AI Engine Adapter (backend/adapters/interfaces.py -> AIEngine)
    │           enrich(query) -> Returns normalized problem & intent
    │
    ├── Step 2: Retrieval Adapter (backend/adapters/interfaces.py -> RetrievalEngine)
    │           retrieve(enriched_data) -> Returns candidate actions from knowledge base
    │
    └── Step 3: Deeplink/Validation Adapter (backend/adapters/interfaces.py -> DeeplinkValidator)
                validate_and_map(candidates) -> Validates deeplinks & enforces catalog ordering
    │
    ▼
Final Validated Troubleshooting JSON
    │
    ▼
Frontend Display (Actions, Steps, Deeplink with Mock Warning)
```

---

## 3. Directory Layout

```
C:\vs\test\Guided-Troubleshooting/
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app with CORS & dependency injection
│   ├── models.py                # Pydantic schemas (TroubleshootRequest, ActionStep, TroubleshootResponse)
│   ├── requirements.txt         # Dependencies
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── interfaces.py        # Protocol classes for Person 1, 2, and 3
│   │   ├── mock_ai.py           # MockAIEngine implementation
│   │   ├── mock_retrieval.py    # MockRetrievalEngine implementation
│   │   └── mock_deeplink.py     # MockDeeplinkValidator implementation
│   └── services/
│       ├── __init__.py
│       └── orchestrator.py      # Core orchestration service coordinating adapters
├── frontend/
│   ├── index.html               # Vite HTML entry point
│   ├── package.json             # NPM configuration
│   ├── tsconfig.json            # TypeScript configuration
│   ├── vite.config.ts           # Dev server config & proxy
│   └── src/
│       ├── main.tsx             # React DOM root
│       ├── App.tsx              # Application layout & state
│       ├── types.ts             # TypeScript data contracts
│       ├── styles.css           # Styling
│       └── components/
│           ├── LoadingSpinner.tsx
│           └── ResultDisplay.tsx
├── tests/
│   ├── __init__.py
│   └── backend/
│       ├── __init__.py
│       ├── conftest.py          # Pytest setup and FastAPI TestClient fixture
│       ├── test_health.py       # Health check test (200 status)
│       ├── test_troubleshoot.py # Main workflow, request ID, actions, mock tag test
│       └── test_errors.py       # 422 validation and 502 simulated adapter failure tests
├── docs/
│   ├── PERSON4_ANALYSIS.md
│   └── PERSON4_IMPLEMENTATION.md
├── pytest.ini
└── README.md
```

---

## 4. Adapter Architecture & How Teammates Connect

The orchestrator depends purely on the `Protocol` classes defined in `backend/adapters/interfaces.py`:

```python
class AIEngine(Protocol):
    def enrich(self, query: str) -> Dict[str, Any]: ...

class RetrievalEngine(Protocol):
    def retrieve(self, enriched_data: Dict[str, Any]) -> List[Dict[str, Any]]: ...

class DeeplinkValidator(Protocol):
    def validate_and_map(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]: ...
```

### When Teammates Deliver Real Modules:
1. **Person 1 (AI / LLM):**
   - Create `backend/adapters/real_ai.py` implementing `AIEngine.enrich(query: str)`.
   - Update `get_orchestrator()` in `backend/main.py`:
     ```python
     from .adapters.real_ai import RealAIEngine
     ai_engine = RealAIEngine()
     ```
2. **Person 2 (Knowledge / Retrieval):**
   - Create `backend/adapters/real_retrieval.py` implementing `RetrievalEngine.retrieve(enriched_data)`.
   - Update `get_orchestrator()` in `backend/main.py`:
     ```python
     from .adapters.real_retrieval import RealRetrievalEngine
     retrieval_engine = RealRetrievalEngine()
     ```
3. **Person 3 (Deeplink / Validation / Fast-Path Cache):**
   - Create `backend/adapters/real_deeplink.py` implementing `DeeplinkValidator.validate_and_map(candidates)`.
   - Update `get_orchestrator()` in `backend/main.py`:
     ```python
     from .adapters.real_deeplink import RealDeeplinkValidator
     deeplink_validator = RealDeeplinkValidator()
     ```

**Zero changes to the API route (`/troubleshoot`) or the frontend are needed.**

---

## 5. How to Run Backend

```powershell
cd C:\vs\test\Guided-Troubleshooting

# Activate virtual environment
.\backend\venv\Scripts\activate

# Start backend using python module syntax (preserving relative package imports)
python -m uvicorn backend.main:app --reload --port 8000
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## 6. How to Run Frontend

```powershell
cd C:\vs\test\Guided-Troubleshooting\frontend

# Install dependencies (already installed)
npm install

# Start Vite dev server
npm run dev
```

- Frontend URL: [http://localhost:5173](http://localhost:5173)

---

## 7. How to Run Tests

```powershell
cd C:\vs\test\Guided-Troubleshooting

# Run all backend tests with verbose output
.\backend\venv\Scripts\pytest.exe tests/backend -v

# Or quiet mode
.\backend\venv\Scripts\pytest.exe -q
```

---

## 8. Current Limitations

1. **Official Theme 02 Assets Missing:** Official `schema.py`, `queries.json`, `siis_responses.json`, and `deeplinks.json` have not yet been provided in the workspace.
2. **Development Mock Responses:** The response data (`goal`, `Battery` action, `settings://battery`) are strictly temporary development placeholders and clearly tagged as mocks.
3. **Deeplink Validation:** Deeplink validity will be enforced strictly once Person 3 provides the verified Samsung Settings deeplink catalog.
