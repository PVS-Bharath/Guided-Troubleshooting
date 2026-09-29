from typing import Literal
from pydantic import BaseModel,Field,ConfigDict
class Strict(BaseModel):
 model_config=ConfigDict(extra="forbid")
class Stage1(Strict):
 issues:list[str]=Field(min_length=1)
 intent:Literal["troubleshoot","information","clarification"]
 device_context:dict[str,str]={}
 confidence:Literal["low","medium","high"]
 needs_clarification:bool
 clarification_question:str|None=None
class Action(Strict):
 actionName:str
 description:str
 category:Literal["auto","critical","manual"]
 steps:list[str]=Field(min_length=1)
 deeplink:str|None=None
 source_ids:list[str]=Field(min_length=1)
class Plan(Strict):
 title:str
 score:float=Field(ge=0,le=1)
 actions:list[Action]
 status:Literal["ok","needs_clarification","no_grounded_solution"]
 issues:list[str]=[]
 clarification_question:str|None=None
 metadata:dict[str,object]={}
