from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class TroubleshootRequest(BaseModel):
    """Request payload for /troubleshoot"""
    query: str = Field(..., min_length=1, description="User problem description")
    request_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Optional request identifier for tracing")

class ActionStep(BaseModel):
    """Single action recommended by the system (development mock)"""
    actionName: str
    description: str
    steps: List[str]
    deeplink: Optional[str] = None  # Development only – not official Samsung deeplink
    category: Optional[str] = None
    is_mock: bool = True  # Development/mock indicator

class TroubleshootResponse(BaseModel):
    """Response payload for /troubleshoot (development mock)"""
    request_id: str
    query: str
    goal: str
    actions: List[ActionStep]
    # MARK: Development mock response – replace with official schema when available
