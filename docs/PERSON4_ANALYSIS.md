# PERSON 4 ANALYSIS — SMART GUIDED TROUBLESHOOTING ENGINE
**Samsung PRISM Generative AI Hackathon 3rd Edition 2026–27**  
**Theme 02 — Smart Guided Troubleshooting Engine**  
**Team:** Srm_Devlopers  
**Role:** Person 4 — REST API + Frontend + Integration  
**Workspace:** `C:\vs\test\Guided-Troubleshooting`

---

## A. Existing Project Structure

```
Guided-Troubleshooting/
├── .pytest_cache/
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # Pydantic request/response schemas (mock development models)
│   ├── requirements.txt         # Backend Python dependencies
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── interfaces.py        # Protocol definitions (AIEngine, RetrievalEngine, DeeplinkValidator)
│   │   ├── mock_ai.py           # MockAIEngine (Development mock)
│   │   ├── mock_retrieval.py    # MockRetrievalEngine (Development mock)
│   │   └── mock_deeplink.py     # MockDeeplinkValidator (Development mock)
│   └── services/
│       ├── __init__.py
│       └── orchestrator.py      # Core orchestration service
├── frontend/
│   ├── index.html               # React mount root
│   ├── package.json             # React, Vite, Axios dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   ├── vite.config.ts           # Vite server + /api proxy to http://127.0.0.1:8000
│   └── src/
│       ├── main.tsx             # Application bootstrap
│       ├── App.tsx              # Main UI component
│       ├── types.ts             # Shared frontend TypeScript interfaces
│       ├── styles.css           # Styling
│       └── components/
│           ├── LoadingSpinner.tsx
│           └── ResultDisplay.tsx
├── tests/
│   ├── __init__.py
│   └── backend/
│       ├── __init__.py
│       ├── conftest.py          # TestClient fixture and sys.path resolution
│       ├── test_health.py       # Health check tests
│       ├── test_troubleshoot.py # Main pipeline & response tests
│       └── test_errors.py       # 422 & 502 error handling tests
└── pytest.ini                   # Pytest configuration
```

---

## B. Official Theme 02 Input/Output Contract Status

- The official Theme 02 starter assets (`schema.py`, `queries.json`, `siis_responses.json`, `deeplinks.json`, `samples/`) are **not yet supplied in this workspace**.
- Until they are provided, we strictly follow the **no-hallucination rule**:
  - We do NOT fabricate fake official files.
  - We do NOT invent official Samsung deeplinks (`settings://battery` is strictly a development mock placeholder and clearly marked as such in UI, code, and response models).
  - All mock adapters and models are explicitly labelled with `DEVELOPMENT/MOCK`.
  - When `schema.py` is supplied, `backend/models.py`, `frontend/src/types.ts`, `orchestrator.py`, and `tests/` will be cleanly updated to match the official contract.

---

## C. Existing Components (Person 4 Scope)

| Component | Technology | Status | Details |
|---|---|---|---|
| REST API | FastAPI | Working | Implements `GET /health` and `POST /troubleshoot` |
| Serialization | Pydantic v2 | Working | Request validation, UUID `request_id`, mock response |
| Orchestration | Python Service | Working | Calls AI -> Retrieval -> DeeplinkValidator in sequence |
| Adapter Interfaces | `typing.Protocol` | Working | Decoupled contracts for Persons 1, 2, and 3 |
| Development Mocks | Python Classes | Working | `MockAIEngine`, `MockRetrievalEngine`, `MockDeeplinkValidator` |
| Web Frontend | React + Vite + TS | Working | Proxy configured for `/api/*` -> `http://127.0.0.1:8000` |
| Test Suite | pytest + httpx | Working | 11 automated backend tests passing |

---

## D. Missing Components (To Be Provided by Teammates)

1. **Person 1 — AI / LLM Engine:**
   - Query enrichment, intent/goal extraction, two-stage LLM processing.
2. **Person 2 — Knowledge / Retrieval:**
   - Preprocessed official knowledge dataset, semantic vector search, knowledge ranking.
3. **Person 3 — Deeplink / Validation / Fast-Path Cache:**
   - Official Samsung Settings deeplink catalog, validation rules, fast-path semantic cache.
4. **Official Theme 02 Starter Assets:**
   - Official `schema.py`, `queries.json`, `siis_responses.json`, `deeplinks.json`.

---

## E. Expected Interfaces for Teammates

### Person 1: AI / LLM Engine
- **Method:** `enrich(query: str) -> Dict[str, Any]`
- **Input:** Raw user string (e.g. `"My phone is getting very hot"`).
- **Output:** Enriched problem metadata (normalized query, detected intent, goal).

### Person 2: Knowledge / Retrieval
- **Method:** `retrieve(enriched_data: Dict[str, Any]) -> List[Dict[str, Any]]`
- **Input:** Enriched dictionary from Person 1.
- **Output:** Ranked candidate troubleshooting actions and instructions from official knowledge base.

### Person 3: Deeplink / Validation / Fast-Path Cache
- **Method:** `validate_and_map(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]`
- **Input:** Candidate actions from Person 2.
- **Output:** Validated, ordered actions with verified official Samsung Settings deeplinks and cache indicators.

---

## F. Proposed API Endpoints

1. `GET /health`
   - Response: `{"status": "ok"}`
2. `POST /troubleshoot`
   - Request: `{"query": "My phone is getting very hot", "request_id": "optional-uuid"}`
   - Response: `{"request_id": "...", "query": "...", "goal": "...", "actions": [...]}`

---

## G. Proposed Frontend Flow

1. User enters natural language complaint into text field.
2. User clicks "Troubleshoot" (or presses Enter).
3. UI transitions to loading state (`loading=true`).
4. Axios issues `POST /api/troubleshoot` (routed by Vite proxy to FastAPI backend).
5. FastAPI validates payload and triggers `Orchestrator.process()`.
6. Orchestrator coordinates adapter pipeline.
7. Result renders:
   - Query and Goal header.
   - Recommended actions list with ordered steps.
   - Deeplink button clearly tagged as development mock.
8. Errors (validation 422 or server 502) render friendly error alert with no stack trace leak.

---

## H. Integration Risks & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Official schema differs from current mock | Models break | `models.py` and `types.ts` are isolated; update schemas upon receiving `schema.py` |
| Teammate module latency | High end-to-end response time | Asynchronous calls, timeout wrappers, semantic cache integration |
| Teammate module exception | 500 unhandled crash | Handled by Orchestrator error boundary; returns clean 502 with log detail |
| Deeplink hallucination | Invalid user instructions | Person 3 catalog validation enforces strict whitelist |
