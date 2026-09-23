import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import TroubleshootRequest, TroubleshootResponse
from .services.orchestrator import Orchestrator

app = FastAPI(title="Smart Guided Troubleshooter", version="0.1.0")

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection – use real adapters in production, mocks for now
def get_orchestrator() -> Orchestrator:
    from .adapters.mock_ai import MockAIEngine
    from .adapters.mock_retrieval import MockRetrievalEngine
    from .adapters.mock_deeplink import MockDeeplinkValidator
    return Orchestrator(ai_engine=MockAIEngine(),
                       retrieval_engine=MockRetrievalEngine(),
                       deeplink_validator=MockDeeplinkValidator())

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/troubleshoot", response_model=TroubleshootResponse)
async def troubleshoot(request: TroubleshootRequest, orchestrator: Orchestrator = Depends(get_orchestrator)):
    try:
        response = orchestrator.process(request.query, request_id=request.request_id)
        return response
    except Exception as e:
        # Unexpected errors – return 502 Bad Gateway
        raise HTTPException(status_code=502, detail=str(e))
