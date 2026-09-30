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

# Shared orchestrator singleton instance
_orchestrator_instance = None

def get_orchestrator() -> Orchestrator:
    global _orchestrator_instance
    if _orchestrator_instance is None:
        from .adapters.gemini_ai import GeminiAIEngine
        from .adapters.retrieval_adapter import Person2RetrievalEngine
        from .adapters.person3_deeplink import Person3DeeplinkValidator
        _orchestrator_instance = Orchestrator(
            ai_engine=GeminiAIEngine(),
            retrieval_engine=Person2RetrievalEngine(),
            deeplink_validator=Person3DeeplinkValidator(),
        )
    return _orchestrator_instance


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
