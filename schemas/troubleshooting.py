from typing import List, Optional
from pydantic import BaseModel, Field

class Action(BaseModel):
    actionName: str
    description: str
    category: str = Field(..., description="auto | critical | manual")
    steps: List[str]
    deeplink: Optional[str] = None

class TroubleshootingResponse(BaseModel):
    query: str
    goal: str
    actions: List[Action]
    cached: bool = False
    latency_ms: Optional[float] = None