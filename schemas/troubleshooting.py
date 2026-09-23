from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class Action(BaseModel):
    actionName: str
    description: str
    category: str = Field(default="manual", description="auto | critical | manual")
    steps: List[str] = Field(default_factory=list)
    deeplink: Optional[str] = None
    source_ids: Optional[List[str]] = None

class Stage1(BaseModel):
    issues: List[str] = Field(default_factory=list)
    intent: Optional[str] = "troubleshoot"
    device_context: Dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[str] = "medium"
    needs_clarification: bool = False
    clarification_question: Optional[str] = None

class Plan(BaseModel):
    title: str = "Troubleshooting plan"
    score: float = Field(default=0.8, ge=0, le=1)
    actions: List[Action] = Field(default_factory=list)
    status: Literal["ok", "needs_clarification", "no_grounded_solution"] = "ok"
    issues: List[str] = Field(default_factory=list)
    clarification_question: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TroubleshootingResponse(BaseModel):
    query: str
    goal: str
    actions: List[Action]
    cached: bool = False
    latency_ms: Optional[float] = None