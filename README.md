# Smart Guided Troubleshooting Engine

> **Samsung PRISM Generative AI Hackathon 3rd Edition (2026--27) ---
> Theme 02**\
> **Team:** `Srm_Devlopers`

A modular AI-assisted troubleshooting engine that converts vague
mobile-device complaints into **structured, grounded, validated, and
actionable troubleshooting workflows**.

------------------------------------------------------------------------

## Project Demo

🎥 **Project Demonstration Video:**  
https://youtu.be/n5QUuWbuMSo

📊 **Project Presentation (PPT):**
https://docs.google.com/presentation/d/10cpphCCZq6MkWp0kPXvpW0UZncM1uKrT/edit?usp=sharing&ouid=100383858190968814876&rtpof=true&sd=true

# Overview

The system accepts natural-language complaints such as:

-   `My phone is getting very hot`
-   `Battery is dying so fast`
-   `My Wi-Fi keeps disconnecting`

It combines query understanding, approved knowledge retrieval, grounded
plan generation, deterministic deeplink validation, action ordering,
fast-path caching, a FastAPI REST API, and a React/TypeScript frontend.

### Core principle

> **Generative AI handles understanding; deterministic validation
> handles execution.**

------------------------------------------------------------------------

## Problem Statement

Mobile users normally describe device problems using vague or colloquial
language. A generic chatbot may misunderstand the symptom, invent
unsupported steps, or provide invalid Settings paths.

This project separates **understanding** from **execution validation**:

``` text
User Complaint
      ↓
Fast-Path Cache
      ↓
Problem Understanding
      ↓
Knowledge Retrieval
      ↓
Grounded Plan Generation
      ↓
Deeplink Validation + Action Ordering
      ↓
Cache Write
      ↓
REST Response
      ↓
Interactive React UI
```

------------------------------------------------------------------------

## Key Features

-   Natural-language troubleshooting
-   Gemini-assisted problem understanding
-   Query enrichment and normalization
-   FAISS semantic retrieval
-   Token-overlap retrieval fallback
-   Grounded plan generation
-   Catalog-backed deeplink validation
-   Anti-hallucination deeplink protection
-   `critical → auto → manual` action ordering
-   Manual-action deeplink removal
-   SHA-256 fast-path cache
-   1-hour cache TTL
-   Request/trace ID support
-   FastAPI REST API
-   Interactive troubleshooting checklist
-   Real-time step completion progress
-   Samsung One UI-inspired frontend
-   Docker and Docker Compose
-   Automated backend tests

------------------------------------------------------------------------

# Architecture

``` text
                         ┌──────────────────────────┐
                         │       Web Browser         │
                         │ React + TypeScript + Vite │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │       FastAPI API         │
                         │      backend/main.py      │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │       Orchestrator        │
                         │ services/orchestrator.py  │
                         └────────────┬─────────────┘
                                      │
              ┌───────────────────────┼────────────────────┐
              ▼                       ▼                    ▼
        ┌───────────┐          ┌─────────────┐      ┌─────────────┐
        │ FastPath  │          │ Person 1    │      │ Person 2    │
        │ Cache     │          │ Gemini /    │      │ Retrieval   │
        │           │          │ Enrichment  │      │ FAISS / KB  │
        └───────────┘          └──────┬──────┘      └──────┬──────┘
                                      └──────────┬───────────┘
                                                 ▼
                                         ┌──────────────┐
                                         │ Grounded     │
                                         │ Plan         │
                                         └──────┬───────┘
                                                ▼
                                         ┌──────────────┐
                                         │ Person 3     │
                                         │ Validation + │
                                         │ Deeplinks    │
                                         └──────┬───────┘
                                                ▼
                                         ┌──────────────┐
                                         │ Canonical    │
                                         │ Response     │
                                         └──────┬───────┘
                                                ▼
                                         ┌──────────────┐
                                         │ React UI     │
                                         └──────────────┘
```

------------------------------------------------------------------------

# End-to-End Request Flow

For:

``` text
My phone is getting very hot
```

1.  React submits `POST /api/troubleshoot`.
2.  FastAPI validates the request.
3.  The orchestrator checks the SHA-256 fast-path cache.
4.  Person 1 normalizes the complaint into a diagnostic concept.
5.  Person 2 retrieves approved troubleshooting knowledge.
6.  Person 1 generates a plan grounded in retrieved context.
7.  Person 3 validates deeplinks against `data/deeplinks.json`.
8.  Actions are ordered `critical → auto → manual`.
9.  Manual actions have `deeplink = None`.
10. The validated result is cached and returned to the frontend.
11. React displays the diagnosis, actions, checklist, progress, trace
    ID, and Settings shortcut.

If no grounded retrieval context exists, the planning layer can return
`no_grounded_solution` instead of inventing a solution.

------------------------------------------------------------------------

# Repository Structure

``` text
Guided-Troubleshooting/
├── .env.example
├── .gitignore
├── cache.py
├── deeplink_mapper.py
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── test_person3.py
├── validator.py
│
├── backend/
│   ├── Dockerfile
│   ├── llm_engine.py
│   ├── main.py
│   ├── models.py
│   ├── query_enrichment.py
│   ├── requirements.txt
│   ├── adapters/
│   │   ├── gemini_ai.py
│   │   ├── interfaces.py
│   │   ├── mock_ai.py
│   │   ├── mock_deeplink.py
│   │   ├── mock_retrieval.py
│   │   ├── person3_deeplink.py
│   │   └── retrieval_adapter.py
│   ├── prompts/
│   │   ├── stage1_problem_understanding.txt
│   │   └── stage2_troubleshooting.txt
│   ├── schemas/
│   │   └── troubleshooting.py
│   └── services/
│       └── orchestrator.py
│
├── data/
│   └── deeplinks.json
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── styles.css
│       ├── types.ts
│       └── components/
│
├── retrieval_module/
│   ├── main.py
│   ├── data/
│   │   ├── faiss.index
│   │   ├── index.py
│   │   ├── preprocess.py
│   │   └── raw_knowledge_base.json
│   ├── services/
│   │   └── retrieval.py
│   ├── src/
│   │   ├── preprocessor.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   └── tests/
│
├── schemas/
│   └── troubleshooting.py
│
└── tests/
    ├── test_cases.json
    ├── test_engine.py
    ├── test_query_enrichment.py
    ├── test_validation.py
    └── backend/
        ├── conftest.py
        ├── test_errors.py
        ├── test_health.py
        └── test_troubleshoot.py
```

------------------------------------------------------------------------

# Team Responsibilities

  --------------------------------------------------------------------------
  Person                  Responsibility          Main Components
  ----------------------- ----------------------- --------------------------
  Person 1                LLM / AI Engine         `backend/llm_engine.py`,
                                                  `query_enrichment.py`,
                                                  `prompts/`

  Person 2                Retrieval               `retrieval_module/`

  Person 3                Deeplink Validation +   `validator.py`,
                          Cache                   `deeplink_mapper.py`,
                                                  `cache.py`,
                                                  `data/deeplinks.json`

  Person 4                REST API + Frontend +   `backend/main.py`,
                          Integration             `orchestrator.py`,
                                                  adapters, `frontend/`,
                                                  integration tests
  --------------------------------------------------------------------------

Integrated branch:

``` text
person4-integration
```

------------------------------------------------------------------------

# Person 1 --- LLM / Gemini

Main files:

``` text
backend/llm_engine.py
backend/query_enrichment.py
backend/adapters/gemini_ai.py
backend/prompts/
```

### Stage 1 --- Problem Understanding

The engine:

1.  receives the complaint,
2.  applies deterministic enrichment,
3.  optionally calls Gemini,
4.  parses structured output.

### Stage 2 --- Grounded Planning

The planner receives retrieved context and creates structured actions
based on approved records.

### Fallback

If Gemini is unavailable, deterministic fallback behavior allows local
testing to continue.

------------------------------------------------------------------------

# Person 2 --- Retrieval

The retrieval stack is:

``` text
Knowledge Base
     ↓
Preprocessing
     ↓
SentenceTransformer
     ↓
all-MiniLM-L6-v2
     ↓
384-d embeddings
     ↓
FAISS IndexFlatIP
     ↓
Top-K results
```

The integration adapter attempts semantic retrieval first.

If the required vector dependencies are unavailable, it falls back to
token-overlap matching over the approved knowledge base.

The currently audited knowledge base contains:

``` text
KB_BATTERY_OVERHEAT
KB_NET_WIFI_RESET
```

------------------------------------------------------------------------

# Person 3 --- Deeplink Validation

Approved deeplinks are stored in:

``` text
data/deeplinks.json
```

Current catalog categories include battery, display, device care, and
Wi-Fi Settings destinations.

Validation rules:

1.  Candidate deeplinks must exist in the approved catalog.
2.  Unverified URLs are rejected or remapped.
3.  Manual actions must have no deeplink.
4.  Actions are sorted:

``` text
critical → auto → manual
```

This deterministic layer prevents arbitrary LLM-generated URLs from
reaching the final response.

------------------------------------------------------------------------

# Fast-Path Cache

Implemented in:

``` text
cache.py
```

Key:

``` text
SHA256(query.lower().strip())
```

Properties:

-   in-memory
-   1-hour default TTL
-   hit/miss metrics
-   expired entries removed on access
-   validated responses can bypass downstream processing

For production-scale deployment, this can be replaced by a distributed
cache such as Redis.

------------------------------------------------------------------------

# REST API

## Health

``` http
GET /health
```

``` json
{
  "status": "ok"
}
```

## Troubleshooting

``` http
POST /troubleshoot
```

Request:

``` json
{
  "query": "My phone is getting very hot",
  "request_id": "optional-trace-id"
}
```

Response contains:

``` text
request_id
query
goal
actions[]
cached
latency_ms
metadata
```

Each action can contain:

``` text
actionName
description
steps[]
deeplink
category
is_mock
```

### Error responses

-   `422` --- invalid request
-   `502` --- downstream adapter failure

------------------------------------------------------------------------

# Frontend

Technology:

-   React 19
-   TypeScript
-   Vite
-   Axios

Major components:

  Component                 Purpose
  ------------------------- ------------------------------------
  `Header.tsx`              Samsung/Galaxy diagnostic branding
  `TroubleshootInput.tsx`   Complaint input and sample queries
  `EmptyState.tsx`          Initial diagnostic cards
  `LoadingState.tsx`        Diagnostic loading experience
  `ErrorState.tsx`          Error and retry UI
  `ResultDisplay.tsx`       Diagnosis and actions
  `StepList.tsx`            Interactive checklist and progress

The UI provides:

-   natural-language input,
-   quick sample complaints,
-   diagnostic loading state,
-   structured result cards,
-   action categories,
-   interactive step completion,
-   progress tracking,
-   trace ID copy,
-   validated Settings shortcuts.

------------------------------------------------------------------------

# Frontend ↔ Backend

Development flow:

``` text
React :5173
    │
    │ /api/*
    ▼
Vite Proxy
    │
    ▼
FastAPI :8000
```

Frontend endpoint:

``` text
POST /api/troubleshoot
```

Backend endpoint:

``` text
POST /troubleshoot
```

------------------------------------------------------------------------

# Data and Schemas

## Deeplink Catalog

``` text
data/deeplinks.json
```

## Knowledge Base

``` text
retrieval_module/data/raw_knowledge_base.json
```

## FAISS Index

``` text
retrieval_module/data/faiss.index
```

### API request

``` text
TroubleshootRequest
├── query: string
└── request_id: optional string
```

### API response

``` text
TroubleshootResponse
├── request_id
├── query
├── goal
├── actions
├── cached
├── latency_ms
└── metadata
```

------------------------------------------------------------------------

# Technology Stack

  Layer                Technology
  -------------------- -------------------------
  Frontend             React 19
  Language             TypeScript
  Build                Vite
  HTTP                 Axios
  Backend              FastAPI
  Runtime              Python 3.13
  ASGI                 Uvicorn
  Validation           Pydantic v2
  LLM                  Google GenAI / Gemini
  Embeddings           SentenceTransformers
  Vector Search        FAISS CPU
  Embedding Model      `all-MiniLM-L6-v2`
  Testing              Pytest
  Containerization     Docker / Docker Compose
  Frontend Container   Nginx

------------------------------------------------------------------------

# Environment Variables

Create `.env` from `.env.example`.

  Variable                      Purpose
  ----------------------------- --------------------------
  `GEMINI_API_KEY`              Gemini authentication
  `GEMINI_MODEL`                Primary Gemini model
  `GEMINI_FALLBACK_MODELS`      Optional fallback models
  `GEMINI_MAX_ATTEMPTS`         Retry limit
  `GEMINI_RETRY_BASE_SECONDS`   Retry backoff
  `ENVIRONMENT`                 Runtime environment

**Never commit real API keys.**

------------------------------------------------------------------------

# Local Setup

## Prerequisites

-   Python 3.13
-   Node.js
-   npm
-   Git
-   Docker Desktop (optional)
-   Gemini API key (optional for fallback mode)

## Clone

``` powershell
git clone https://github.com/PVS-Bharath/Guided-Troubleshooting.git
cd Guided-Troubleshooting
```

## Python environment

``` powershell
python -m venv backendenv
.\backend\env\Scripts\Activate.ps1
```

## Install dependencies

``` powershell
.\backend\env\Scripts\pip.exe install -r requirements.txt
.\backend\env\Scripts\pip.exe install -r backendequirements.txt
```

## Configure environment

``` powershell
Copy-Item .env.example .env
```

Add the Gemini key to `.env` if live Gemini generation is required.

------------------------------------------------------------------------

# Run Backend

From project root:

``` powershell
.\backend\env\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

``` text
http://localhost:8000/docs
http://localhost:8000/health
```

------------------------------------------------------------------------

# Run Frontend

Open a second terminal:

``` powershell
cd frontend
npm install
npm run dev
```

Open:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# Run Tests

From repository root:

``` powershell
.\backend\env\Scripts\pytest.exe -q
```

Backend integration tests:

``` powershell
.\backend\env\Scripts\pytest.exe tests/backend -v
```

Person 3:

``` powershell
.\backend\env\Scripts\pytest.exe test_person3.py -v
```

The audited run reported:

``` text
12 passed
```

------------------------------------------------------------------------

# Frontend Production Build

``` powershell
npm --prefix frontend run build
```

The audited build completed successfully with zero build errors.

------------------------------------------------------------------------

# Docker

``` powershell
docker compose up --build
```

Services:

``` text
Frontend → http://localhost:5173
Backend  → http://localhost:8000
```

Stop:

``` powershell
docker compose down
```

------------------------------------------------------------------------

# Security

### Secret isolation

`.env` and key files are excluded through `.gitignore`.

### Deeplink protection

Every deeplink is checked against the approved catalog.

### Manual action protection

Manual actions cannot expose Settings deeplinks.

### Input validation

FastAPI/Pydantic validates the incoming query.

### CORS

CORS is permissive for local/hackathon use. Production deployment should
restrict allowed origins.

------------------------------------------------------------------------

# Testing Strategy

The project tests:

-   API health
-   valid troubleshooting requests
-   request validation
-   malformed JSON
-   AI adapter failure
-   retrieval adapter failure
-   validator failure
-   action structure
-   deeplink validation
-   cache hits
-   request ID preservation
-   query enrichment
-   schema constraints
-   score bounds
-   Person 3 ordering and anti-hallucination behavior

------------------------------------------------------------------------

# Implemented Features

-   [x] FastAPI REST API
-   [x] `/health`
-   [x] `/troubleshoot`
-   [x] Pydantic schemas
-   [x] Request tracing
-   [x] Query enrichment
-   [x] Gemini integration
-   [x] Deterministic Gemini fallback
-   [x] FAISS retrieval path
-   [x] Retrieval fallback
-   [x] Grounded plan generation
-   [x] Deeplink catalog validation
-   [x] Anti-hallucination deeplink guardrail
-   [x] Critical/auto/manual ordering
-   [x] Manual deeplink stripping
-   [x] Fast-path cache
-   [x] React frontend
-   [x] Interactive checklist
-   [x] Progress tracking
-   [x] Docker configuration
-   [x] Automated tests

------------------------------------------------------------------------

# Current Limitations

### Limited knowledge base

The audited knowledge base currently contains two comprehensive
scenarios:

``` text
KB_BATTERY_OVERHEAT
KB_NET_WIFI_RESET
```

### Static deeplinks

Current Settings shortcuts target static destinations.

### No multi-turn clarification UI

The schemas support clarification-related information, but the current
frontend does not implement a full conversational clarification loop.

### In-memory cache

The cache is process-local.

### Production hardening

Production deployment would require stricter CORS, HTTPS/reverse proxy
configuration, and production secret management.

------------------------------------------------------------------------

# Future Improvements

1.  Expand the approved troubleshooting knowledge base.
2.  Add additional device symptom categories.
3.  Add dynamic deeplink parameters.
4.  Implement multi-turn clarification.
5.  Replace local cache with Redis for distributed deployments.
6.  Add production authentication and authorization.
7.  Restrict CORS to trusted domains.
8.  Add richer retrieval evaluation and monitoring.
9.  Add structured telemetry.
10. Add production reverse proxy and HTTPS.

------------------------------------------------------------------------

# Beginner Explanation

Suppose a user types:

> **My phone is getting very hot**

The system:

1.  Checks whether the same problem is already cached.
2.  Understands the complaint.
3.  Searches approved troubleshooting knowledge.
4.  Creates a grounded troubleshooting plan.
5.  Checks every Settings shortcut against the approved catalog.
6.  Orders the actions.
7.  Displays the result as an interactive checklist.

The important difference is that the system does not simply ask an LLM
to invent a troubleshooting answer.

------------------------------------------------------------------------

# Engineering Explanation

The system is a modular RAG pipeline:

``` text
React
  ↓
FastAPI
  ↓
Dependency-injected Orchestrator
  ↓
FastPathCache
  ↓
Problem Understanding
  ↓
Retrieval Adapter
  ↓
Grounded Plan Generation
  ↓
Deterministic Deeplink Validation
  ↓
Canonical Pydantic Response
  ↓
React Rendering
```

The adapter layer provides separation between:

``` text
AIEngine
RetrievalEngine
DeeplinkValidator
```

This allows real components and test doubles to be swapped without
rewriting the API layer.

The validation stage is intentionally deterministic: an LLM-generated
URL is not trusted simply because it looks valid.

------------------------------------------------------------------------

# Intended vs Actual Architecture

  Component          Intended                    Actual
  ------------------ --------------------------- ------------------------------
  REST API           FastAPI                     FastAPI
  Schemas            Pydantic                    Pydantic v2
  Frontend           React + TypeScript + Vite   React 19 + TypeScript + Vite
  Understanding      AI + enrichment             Implemented
  Retrieval          Semantic KB retrieval       FAISS + fallback
  Planning           Grounded generation         Implemented
  Deeplinks          Catalog validation          Implemented
  Ordering           Critical → Auto → Manual    Implemented
  Manual deeplinks   None                        Implemented
  Cache              Fast path                   SHA-256 in-memory
  Containers         Docker                      Docker + Compose

------------------------------------------------------------------------

# Git Workflow

Team branches:

``` text
person1-llm-engine
        │
person-2-retrieval
        │
person3-deeplink-integration
        │
        ▼
person4-integration
        │
        ▼
main
```

Each person develops on their own branch. The integration branch
combines the components and is tested before final merge into `main`.

------------------------------------------------------------------------

# Project Status

Based on the technical audit:

  Area                  Status
  --------------------- ---------------------------
  Architecture          Integrated
  Backend               Implemented
  Frontend              Implemented
  Retrieval             Implemented with fallback
  Deeplink validation   Implemented
  Fast-path cache       Implemented
  Docker                Configured
  Backend tests         Passing in audited run
  Frontend build        Passing in audited run
  Knowledge base        Limited / expandable
  Gemini                Configuration-dependent

------------------------------------------------------------------------

# Hackathon Value Proposition

The project is designed as more than a generic chatbot.

Its controlled pipeline is:

``` text
Vague Complaint
      ↓
AI Understanding
      ↓
Approved Knowledge Retrieval
      ↓
Grounded Plan
      ↓
Deterministic Validation
      ↓
Verified Action
      ↓
Interactive Guidance
```

This combines the flexibility of generative AI for understanding
natural-language complaints with deterministic safeguards for the final
troubleshooting actions and Settings shortcuts.

------------------------------------------------------------------------

## Team

**Team:** `Srm_Devlopers`

**Project:** Smart Guided Troubleshooting Engine

**Hackathon:** Samsung PRISM Generative AI Hackathon 3rd Edition
(2026--27)

**Theme:** Theme 02 --- Smart Guided Troubleshooting Engine

------------------------------------------------------------------------

## License

This is a hackathon project. Add the final project-specific license if
required by the team or submission rules.
