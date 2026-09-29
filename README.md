# PRISM Theme 02 / Report 1
Two-stage Gemini engine: conservative enrichment, issue extraction, context-grounded plan generation, Pydantic validation, latency/token metadata.

Install: `python -m pip install -r requirements.txt`. Configure `.env` with GEMINI_API_KEY and GEMINI_MODEL; never commit `.env`.

Integration:
`from llm_engine import troubleshoot`
`result = troubleshoot("Battery drains", retrieved_context=[{"source_id":"KB-1","approved_steps":["verified step"],"deeplink":"exact catalog URI"}])`

Use only Person 2's approved retrieval records. IDs accepted: source_id/scenario_id/id. Stage 2 skips if context is empty. Returned IDs must be present in context; deeplinks must exactly match a supplied context value. This is not a replacement for Person 3's authoritative deeplink validator. `estimated_cost_usd` remains null until billing/pricing is verified. The 20 prompts in tests/test_cases.json are a manual evaluation set; unit tests do not establish live accuracy.
