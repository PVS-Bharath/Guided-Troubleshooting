import time
from typing import List, Dict, Any, Optional

from ..models import TroubleshootResponse, ActionStep
from schemas.troubleshooting import TroubleshootingResponse as P3Response, Action as P3Action


class Orchestrator:
    """Orchestrates the end-to-end guided troubleshooting pipeline:
    1. Fast-Path Cache check (Person 3)
    2. Stage 1 Query Enrichment & Problem Understanding (Person 1)
    3. Approved Context Retrieval (Person 2)
    4. Stage 2 Structured Troubleshooting Plan Generation (Person 1)
    5. Deeplink Catalog Validation & Action Ordering (Person 3)
    6. Fast-Path Cache storage & Canonical API Response delivery (Person 4)
    """

    def __init__(self, ai_engine: Any, retrieval_engine: Any, deeplink_validator: Any):
        self.ai_engine = ai_engine
        self.retrieval_engine = retrieval_engine
        self.deeplink_validator = deeplink_validator
        self.cache = getattr(deeplink_validator, "cache", None)

    def process(self, query: str, request_id: str) -> TroubleshootResponse:
        start_time = time.perf_counter()

        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")

        clean_query = query.strip()

        # Step 1: Fast-Path Cache Check
        if self.cache is not None:
            cached = self.cache.get(clean_query)
            if cached is not None:
                total_latency = round((time.perf_counter() - start_time) * 1000, 2)
                actions = [
                    ActionStep(
                        actionName=act.actionName,
                        description=act.description,
                        steps=act.steps,
                        deeplink=act.deeplink,
                        category=act.category,
                        is_mock=False,
                    )
                    for act in cached.actions
                ]
                return TroubleshootResponse(
                    request_id=request_id,
                    query=clean_query,
                    goal=cached.goal,
                    actions=actions,
                    cached=True,
                    latency_ms=total_latency,
                    metadata={"source": "fast_path_cache"},
                )

        # Step 2: Person 1 Stage 1 - Problem Understanding & Enrichment
        if hasattr(self.ai_engine, "understand"):
            stage1_result, stage1_metrics = self.ai_engine.understand(clean_query)
        elif hasattr(self.ai_engine, "enrich"):
            from schemas.troubleshooting import Stage1
            enriched = self.ai_engine.enrich(clean_query)
            stage1_result = Stage1(issues=[clean_query])
            stage1_metrics = {"enrichment": {"enriched_query": enriched if isinstance(enriched, str) else clean_query}}
        else:
            raise RuntimeError("AI Engine does not support understand or enrich.")

        # Determine search term from Stage 1 output
        search_query = clean_query
        if hasattr(stage1_result, "issues") and stage1_result.issues:
            search_query = stage1_result.issues[0]
        elif isinstance(stage1_metrics, dict):
            enrichment = stage1_metrics.get("enrichment", {})
            if isinstance(enrichment, dict) and enrichment.get("enriched_query"):
                search_query = enrichment["enriched_query"]

        # Step 3: Person 2 - Retrieval of approved troubleshooting context
        retrieved_context = []
        if hasattr(self.retrieval_engine, "retrieve"):
            retrieved_context = self.retrieval_engine.retrieve(search_query)
        elif hasattr(self.retrieval_engine, "search"):
            search_res = self.retrieval_engine.search(search_query)
            retrieved_context = search_res.get("candidates", [])

        # Step 4: Person 1 Stage 2 - Structured Plan Generation from approved context
        if hasattr(self.ai_engine, "plan"):
            stage2_result, stage2_metrics = self.ai_engine.plan(stage1_result, retrieved_context)
            if hasattr(stage2_result, "model_dump"):
                plan_dict = stage2_result.model_dump()
            else:
                plan_dict = dict(getattr(stage2_result, "__dict__", {}))
        else:
            plan_dict = {
                "title": "Troubleshooting steps for your issue",
                "actions": retrieved_context,
            }

        candidate_actions = plan_dict.get("actions", [])

        # Step 5: Person 3 - Deeplink catalog validation & action ordering
        final_actions = self.deeplink_validator.validate_and_map(candidate_actions)

        # Convert to ActionStep models
        actions: List[ActionStep] = []
        p3_actions: List[P3Action] = []
        for act in final_actions:
            step = ActionStep(
                actionName=act.get("actionName", ""),
                description=act.get("description", ""),
                steps=act.get("steps", []),
                deeplink=act.get("deeplink"),
                category=act.get("category"),
                is_mock=act.get("is_mock", False),
            )
            actions.append(step)
            p3_actions.append(P3Action(
                actionName=step.actionName,
                description=step.description,
                category=step.category or "manual",
                steps=step.steps,
                deeplink=step.deeplink,
            ))

        goal = plan_dict.get("title") or "Resolve device issue"
        total_latency = round((time.perf_counter() - start_time) * 1000, 2)

        # Step 6: Store in Fast-Path Cache (Person 3)
        if self.cache is not None:
            cache_payload = P3Response(
                query=clean_query,
                goal=goal,
                actions=p3_actions,
                cached=False,
                latency_ms=total_latency,
            )
            self.cache.set(clean_query, cache_payload)

        return TroubleshootResponse(
            request_id=request_id,
            query=clean_query,
            goal=goal,
            actions=actions,
            cached=False,
            latency_ms=total_latency,
            metadata={
                "intent": getattr(stage1_result, "intent", "troubleshoot"),
                "candidates_retrieved": len(retrieved_context),
                "actions_ordered": len(actions),
            },
        )
