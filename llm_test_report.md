# LLM Engine Test / Accuracy Report

## Samsung PRISM 2026–27 — Theme 02: Smart Guided Troubleshooting Engine

**Owner:** Dinesh  
**Module:** AI / LLM Engine (Report 1)  
**Model:** Gemini 3.6 Flash  
**Architecture:** Query Enrichment → Stage 1 Problem Understanding → Approved/Retrieved Context → Grounded Stage 2 Plan → Schema Validation

## 1. Purpose

This report evaluates the AI/LLM engine against the required complaint categories: simple, vague, paraphrased, multi-issue, and unsupported/unknown complaints.

Evaluation checks:
- Correct issue identification and query enrichment
- Multi-issue preservation
- Grounded troubleshooting actions
- Schema-valid JSON
- Source ID traceability
- No fabricated Settings deeplinks
- Safe clarification/no-grounded-solution behavior
- Latency and token metrics

> The current local demo uses approved battery records (`BATTERY_001`–`BATTERY_003`) as temporary context. Full retrieval integration is supplied by the team's retrieval component. Therefore, scenarios without corresponding approved/retrieved context should be marked **Integration Pending**, not falsely marked PASS.

## 2. How to Run

From the project root with the virtual environment activated:

```powershell
python run_engine.py
```

Enter a complaint when prompted, for example:

```text
Phone battery draining quickly
```

The program prints structured JSON.

For supported complaints with approved context, verify:
- `status` is `ok`
- `actions` is non-empty
- every grounded action has `source_ids`
- `deeplink` is either verified or `null`

For unsupported/unknown complaints, safe results include:
- `needs_clarification`
- `no_grounded_solution`

The engine must not invent troubleshooting actions or Settings deeplinks when approved context is unavailable.

## 3. Evaluation Rules

A test is **PASS** when applicable criteria are satisfied:
1. The main issue is correctly identified.
2. Vague/paraphrased wording is normalized without adding unsupported symptoms.
3. Every issue in a multi-issue complaint is preserved.
4. Actions come from approved/retrieved context.
5. Output follows the agreed JSON/schema.
6. Grounded actions have source IDs.
7. Unverified deeplinks are not fabricated.
8. Unknown complaints do not receive invented troubleshooting.
9. Latency is recorded.

A test is **FAIL** if the engine silently drops an issue, invents an unsupported action/deeplink, produces invalid schema output, or gives a grounded solution without approved/retrieved context.

A test is **Integration Pending** when the required knowledge is not yet available in the current demo context.

## 4. Required 20-Test Evaluation Set

| # | Complaint | Category | Expected behavior | Current status |
|---|---|---|---|---|
| 1 | Phone battery draining quickly | Simple | Identify battery drain and return grounded battery actions | **PASS — verified** |
| 2 | My phone gets very hot | Simple | Identify overheating and return approved overheating actions | Integration Pending |
| 3 | My screen keeps flickering | Simple | Identify screen flicker and return approved display actions | Integration Pending |
| 4 | My battery drains quickly and my phone gets very hot | Multi-issue | Preserve both battery and overheating issues | Integration Pending |
| 5 | My battery is dying really fast | Paraphrase | Normalize to battery-drain intent | Integration Pending |
| 6 | The battery percentage drops very quickly | Paraphrase | Identify battery-drain intent | Integration Pending |
| 7 | My phone loses power even when I barely use it | Paraphrase | Identify abnormal battery drain | Integration Pending |
| 8 | The battery doesn't last through the day anymore | Vague/Paraphrase | Identify battery-drain complaint without inventing symptoms | Integration Pending |
| 9 | Device becomes unusually warm during use | Paraphrase | Identify overheating | Integration Pending |
| 10 | My phone is overheating while charging | Specific | Identify overheating/charging complaint | Integration Pending |
| 11 | Display flashes randomly | Paraphrase | Identify screen flicker | Integration Pending |
| 12 | The screen keeps blinking on and off | Paraphrase | Identify screen flicker | Integration Pending |
| 13 | Battery drains quickly and screen flickers | Multi-issue | Preserve both issues | Integration Pending |
| 14 | Phone overheats and battery drops very fast | Multi-issue | Preserve overheating + battery drain | Integration Pending |
| 15 | My display is unstable and the phone gets hot | Multi-issue | Preserve screen + overheating issues | Integration Pending |
| 16 | Something is wrong with my battery | Vague | Clarify or safely identify battery-related intent | Integration Pending |
| 17 | My phone is behaving strangely | Vague | Ask for clarification rather than inventing a diagnosis | Integration Pending |
| 18 | My device has a problem | Unsupported/Vague | Ask for more information | Integration Pending |
| 19 | The phone is acting weird after an update | Vague/Unsupported | Clarify unless approved context supports it | Integration Pending |
| 20 | The camera takes pictures differently | Unsupported | Do not invent troubleshooting; clarify/no grounded solution | Integration Pending |

## 5. Verified Test #1 — Battery Drain

### Input

```text
Phone battery draining quickly
```

### Observed result

- `status: ok`
- Issue: `battery draining quickly`
- Three grounded actions
- `BATTERY_001`
- `BATTERY_002`
- `BATTERY_003`
- Schema-valid structured output
- Stage 2 latency: `0 ms`

Actions returned:
1. Check battery usage
2. Review battery-saving settings
3. Check battery condition

**Result: PASS**

## 6. How to Evaluate Each Test

Run:

```powershell
python run_engine.py
```

and enter each complaint individually.

### Simple / paraphrase tests

Check that the issue is normalized correctly and that no unsupported symptoms are added.

### Multi-issue tests

For example:

```text
My battery drains quickly and my phone gets very hot
```

Verify that both problems remain represented.

**FAIL:** only battery drain is retained and overheating is silently removed.

### Unknown tests

For example:

```text
The camera takes pictures differently
```

If there is no approved context, the engine must not fabricate troubleshooting actions. `needs_clarification` or `no_grounded_solution` is acceptable.

## 7. Metrics

The engine records:
- Stage 1 latency
- Stage 2 latency
- Total latency
- Prompt tokens
- Output tokens
- Success/fallback status

Example observed Stage 1 metrics from the battery test:

```text
latency_ms: 55866.76
prompt_tokens: 109
output_tokens: 49
```

### Cost

The current implementation reports:

```json
"estimated_cost_usd": null
```

This means a verified provider pricing calculation is not configured yet. Do **not** invent a cost value. Token counts are retained so cost can be calculated once the applicable Gemini pricing configuration is available.

## 8. Current Evaluation Summary

| Metric | Result |
|---|---|
| Required test cases defined | 20 |
| Battery simple case | PASS |
| Paraphrase coverage | Defined; retrieval integration pending |
| Multi-issue coverage | Defined; retrieval integration pending |
| Unknown/unsupported coverage | Defined; retrieval integration pending |
| JSON/schema validation | Implemented |
| Grounding/source IDs | Implemented |
| Unsupported deeplink protection | Implemented |
| Latency measurement | Implemented |
| Token measurement | Implemented |
| Verified cost/query value | Pending |
| Full retrieval dataset integration | Team integration pending |

## 9. Conclusion

The current AI/LLM engine successfully demonstrates the core Report 1 pipeline using approved battery troubleshooting context.

The 20-case evaluation set covers the required simple, vague, paraphrased, multi-issue and unsupported complaint categories. Full PASS/FAIL scoring for the remaining scenarios should be completed after the retrieval component supplies the corresponding approved knowledge records.

The engine avoids unsupported troubleshooting actions and fabricated Settings deeplinks while returning structured, schema-compatible output with source traceability.
