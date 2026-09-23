from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid

class TroubleshootRequest(BaseModel):
    """Request payload for /troubleshoot"""
    query: str = Field(..., min_length=1, description="User problem description")
    request_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Optional request identifier for tracing")

class ActionStep(BaseModel):
    """Single action recommended by the system"""
    actionName: str
    description: str
    steps: List[str] = Field(default_factory=list)
    deeplink: Optional[str] = None
    category: Optional[str] = None
    is_mock: bool = False  # Real integrated actions are False

class TroubleshootResponse(BaseModel):
    """Canonical response payload for /troubleshoot"""
    request_id: str
    query: str
    goal: str
    actions: List[ActionStep]
    cached: bool = False
    latency_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
