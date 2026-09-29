from llm_engine import plan
from schemas.troubleshooting import Stage1
def s():return Stage1(issues=["battery drain"],intent="troubleshoot",device_context={},confidence="high",needs_clarification=False)
def test_empty_context_safe():
 p,m=plan(s(),[]);assert p.status=="no_grounded_solution" and p.actions==[] and m["skipped"]
def test_context_needs_id():
 p,_=plan(s(),[{"steps":["not trusted"]}]);assert p.status=="no_grounded_solution"
