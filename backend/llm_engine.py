"""
Samsung PRISM - Smart Guided Troubleshooting Engine.

Stage 1: Understand complaint using Gemini.
Stage 2: Generate a plan only from supplied approved context.

Resilience:
- Configurable primary and fallback Gemini models via .env
- Retries transient 429/5xx/network errors with exponential backoff
- Explicit stage/provider failure metadata
- Conservative schema-valid fallback responses
- Never fabricates approved actions or deeplinks
"""

import json
import os
import random
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from pydantic import ValidationError

from query_enrichment import enrich_query
from schemas.troubleshooting import Stage1, Plan

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Example:
# GEMINI_MODEL=your-primary-model-id
# GEMINI_FALLBACK_MODELS=verified-backup-id,another-verified-id
MODEL = os.getenv("GEMINI_MODEL", "").strip()
FALLBACK_MODELS = [
    item.strip()
    for item in os.getenv("GEMINI_FALLBACK_MODELS", "").split(",")
    if item.strip()
]
MAX_ATTEMPTS = max(1, int(os.getenv("GEMINI_MAX_ATTEMPTS", "3")))
RETRY_BASE_SECONDS = max(0.1, float(os.getenv("GEMINI_RETRY_BASE_SECONDS", "1")))
CLIENT = None


class GeminiRequestError(RuntimeError):
    """Provider request failed after retry/model fallback attempts."""

    def __init__(self, message: str, attempts: list[dict[str, Any]]):
        super().__init__(message)
        self.attempts = attempts


def get_client():
    global CLIENT
    if CLIENT is None:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_api_key_here":
            raise RuntimeError("GEMINI_API_KEY is missing or is still a placeholder in .env.")
        CLIENT = genai.Client(api_key=api_key)
    return CLIENT


def _model_candidates():
    # Preserve order and remove duplicates. Do not guess model names.
    candidates = ([MODEL] if MODEL else []) + FALLBACK_MODELS
    return list(dict.fromkeys(candidates))


def _is_retryable(exc: Exception) -> bool:
    """Identify common transient provider/network failures."""
    text = f"{type(exc).__name__}: {exc}".lower()
    retry_markers = (
        "503", "unavailable", "overloaded", "high demand",
        "429", "resource_exhausted", "rate limit", "too many requests",
        "500", "502", "504", "internal server error",
        "deadline exceeded", "temporarily", "connection reset",
        "connection error", "timed out", "timeout",
    )
    return any(marker in text for marker in retry_markers)


def _call_gemini(prompt_file: str, payload: dict[str, Any]):
    """Try configured models; retry transient failures with exponential backoff."""
    prompt_path = ROOT / "prompts" / prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    candidates = _model_candidates()
    if not candidates:
        raise RuntimeError(
            "No Gemini model configured. Set GEMINI_MODEL in .env to a model "
            "ID available to your API key."
        )

    prompt = prompt_path.read_text(encoding="utf-8")
    request_text = (
        prompt
        + "\n\nReturn only valid JSON. Do not use Markdown.\n"
        + "INPUT_JSON:\n"
        + json.dumps(payload, ensure_ascii=False)
    )

    attempts_log: list[dict[str, Any]] = []
    started_all = time.perf_counter()
    last_error: Exception | None = None

    for model_index, model_name in enumerate(candidates):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            started = time.perf_counter()
            try:
                response = get_client().models.generate_content(
                    model=model_name,
                    contents=request_text,
                    config={
                        "response_mime_type": "application/json",
                        "temperature": 0.1,
                    },
                )
                elapsed_ms = round((time.perf_counter() - started) * 1000, 2)

                if not response.text:
                    raise RuntimeError("Gemini returned an empty response.")

                try:
                    data = json.loads(response.text)
                except json.JSONDecodeError as exc:
                    raise RuntimeError("Gemini returned invalid JSON.") from exc

                usage = getattr(response, "usage_metadata", None)
                metrics = {
                    "success": True,
                    "model": model_name,
                    "fallback_model_used": model_index > 0,
                    "attempts": attempts_log + [{
                        "model": model_name,
                        "attempt": attempt,
                        "success": True,
                        "latency_ms": elapsed_ms,
                    }],
                    "latency_ms": round((time.perf_counter() - started_all) * 1000, 2),
                    "prompt_tokens": getattr(usage, "prompt_token_count", None) if usage else None,
                    "output_tokens": getattr(usage, "candidates_token_count", None) if usage else None,
                }
                return data, metrics

            except Exception as exc:
                last_error = exc
                retryable = _is_retryable(exc)
                attempts_log.append({
                    "model": model_name,
                    "attempt": attempt,
                    "success": False,
                    "retryable": retryable,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                })

                # Don't waste retries on likely permanent errors.
                if not retryable:
                    break

                if attempt < MAX_ATTEMPTS:
                    delay = RETRY_BASE_SECONDS * (2 ** (attempt - 1))
                    delay += random.uniform(0, min(0.5, delay * 0.25))
                    time.sleep(delay)

        # Move to next configured model after this model's attempts fail.

    message = str(last_error) if last_error else "No configured model could be called."
    raise GeminiRequestError(message, attempts_log)


def _field_names(model_class):
    return set(model_class.model_fields.keys())


def _safe_dict(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return {"device_type": value}
    return {}


def _normalize_confidence(value):
    if isinstance(value, str):
        value = value.strip().lower()
        if value in {"low", "medium", "high"}:
            return value
        try:
            value = float(value)
        except ValueError:
            return "medium"
    if isinstance(value, (int, float)):
        if value >= 0.75:
            return "high"
        if value >= 0.40:
            return "medium"
        return "low"
    return "medium"


def _normalize_stage1(data):
    if not isinstance(data, dict):
        raise ValueError("Stage 1 response must be a JSON object.")
    data = dict(data)
    if "device_context" in data:
        data["device_context"] = _safe_dict(data["device_context"])
    if "confidence" in data:
        data["confidence"] = _normalize_confidence(data["confidence"])
    allowed = _field_names(Stage1)
    return {key: value for key, value in data.items() if key in allowed}


def _fallback_stage1(complaint):
    """
    Build a conservative Stage1 instance. Validate when possible; use
    model_construct only as a last-resort schema-compatible emergency fallback.
    """
    fields = Stage1.model_fields
    values = {}
    for name, field in fields.items():
        if not field.is_required():
            if field.default_factory is not None:
                values[name] = field.default_factory()
            elif field.default is not None:
                values[name] = field.default

    safe_values = {
        "issues": [complaint],
        "device_context": {"device_type": "unknown"},
        "intent": "troubleshooting",
        "confidence": "low",
        "needs_clarification": True,
        "clarification_question": (
            "The AI service is currently unavailable. Please try again shortly "
            "or provide the device model and what changed before the issue began."
        ),
    }
    for key, value in safe_values.items():
        if key in fields:
            values[key] = value

    try:
        return Stage1.model_validate(values)
    except ValidationError:
        return Stage1.model_construct(**values)


def _fallback_plan(stage1_result, status, title):
    fields = Plan.model_fields
    values = {}
    for name, field in fields.items():
        if not field.is_required():
            if field.default_factory is not None:
                values[name] = field.default_factory()
            elif field.default is not None:
                values[name] = field.default

    candidates = {
        "title": title,
        "score": 0,
        "actions": [],
        "status": status,
        "issues": getattr(stage1_result, "issues", []),
        "clarification_question": getattr(
            stage1_result, "clarification_question", None
        ),
    }
    for key, value in candidates.items():
        if key in fields:
            values[key] = value

    try:
        return Plan.model_validate(values)
    except ValidationError:
        return Plan.model_construct(**values)


def _dump_model(model):
    try:
        return model.model_dump()
    except Exception:
        return dict(getattr(model, "__dict__", {}))


def understand(raw_complaint):
    enriched = enrich_query(raw_complaint)
    if enriched.get("is_empty"):
        raise ValueError("Please enter a complaint.")

    try:
        data, metrics = _call_gemini(
            "stage1_problem_understanding.txt",
            {
                "raw_complaint": enriched["original_complaint"],
                "enriched_query": enriched["enriched_query"],
            },
        )
        result = Stage1.model_validate(_normalize_stage1(data))
    except Exception as exc:
        result = _fallback_stage1(enriched["enriched_query"])
        attempts = exc.attempts if isinstance(exc, GeminiRequestError) else []
        metrics = {
            "success": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "fallback_used": True,
            "fallback_reason": "stage1_provider_or_validation_failure",
            "attempts": attempts,
            "latency_ms": None,
        }

    metrics["enrichment"] = enriched
    return result, metrics



def plan(stage1_result, retrieved_context=None):
    """Generate a schema-valid plan using supplied approved context."""

    context = []

    for item in retrieved_context or []:
        if not isinstance(item, dict):
            continue

        source_id = (
            item.get("source_id")
            or item.get("scenario_id")
            or item.get("id")
        )

        if isinstance(source_id, str) and source_id.strip():
            normalized = dict(item)
            normalized["source_id"] = source_id
            context.append(normalized)

    if (
        getattr(stage1_result, "needs_clarification", False)
        or getattr(stage1_result, "intent", "") == "clarification"
    ):
        return (
            _fallback_plan(
                stage1_result,
                "needs_clarification",
                "More information needed",
            ),
            {
                "success": True,
                "skipped": True,
                "reason": "clarification_required",
                "latency_ms": 0,
            },
        )

    if not context:
        return (
            _fallback_plan(
                stage1_result,
                "no_grounded_solution",
                "No verified troubleshooting data available",
            ),
            {
                "success": True,
                "skipped": True,
                "reason": "no_approved_context",
                "latency_ms": 0,
            },
        )

    # Build canonical actions from the supplied approved records.
    # This avoids asking the LLM to reconstruct action fields.
    approved_actions = []

    for item in context:
        required = (
            "actionName",
            "description",
            "category",
            "steps",
        )

        if not all(key in item for key in required):
            continue

        approved_actions.append({
            "actionName": item["actionName"],
            "description": item["description"],
            "category": item["category"],
            "steps": item["steps"],
            "deeplink": item.get("deeplink"),
            "source_ids": [item["source_id"]],
        })

    if not approved_actions:
        return (
            _fallback_plan(
                stage1_result,
                "no_grounded_solution",
                "No verified actions could be produced",
            ),
            {
                "success": False,
                "fallback_used": True,
                "reason": "context_missing_required_action_fields",
                "latency_ms": 0,
            },
        )

    # Deterministic fallback: return supplied approved actions.
    # This still works if Gemini is temporarily unavailable.
    try:
        result = Plan.model_validate({
            "title": "Troubleshooting steps for your issue",
            "score": 0.8,
            "actions": approved_actions,
            "status": "ok",
            "issues": getattr(stage1_result, "issues", []),
            "clarification_question": None,
            "metadata": {},
        })

        return result, {
            "success": True,
            "fallback_used": True,
            "fallback_reason": "deterministic_approved_context",
            "latency_ms": 0,
        }

    except ValidationError as exc:
        return (
            _fallback_plan(
                stage1_result,
                "no_grounded_solution",
                "Approved troubleshooting data failed validation",
            ),
            {
                "success": False,
                "fallback_used": True,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "latency_ms": 0,
            },
        )


def troubleshoot(raw_complaint, retrieved_context=None):
    started = time.perf_counter()
    stage1_result, stage1_metrics = understand(raw_complaint)
    stage2_result, stage2_metrics = plan(stage1_result, retrieved_context)
    output = _dump_model(stage2_result)

    metadata = {
        "model": MODEL or None,
        "fallback_models_configured": FALLBACK_MODELS,
        "stage1": stage1_metrics,
        "stage2": stage2_metrics,
        "total_latency_ms": round((time.perf_counter() - started) * 1000, 2),
        "estimated_cost_usd": None,
        "degraded": (
            not stage1_metrics.get("success", False)
            or not stage2_metrics.get("success", False)
        ),
    }
    if "metadata" in Plan.model_fields:
        output["metadata"] = metadata
    else:
        # Keep diagnostics visible even if the Plan schema has no metadata field.
        output["_diagnostics"] = metadata
    return output


if __name__ == "__main__":
    try:
        complaint = input("Describe your issue: ").strip()
        if not complaint:
            print(json.dumps({"error": "Please enter a complaint."}, indent=2))
        else:
            # Standalone run has no retrieval integration; therefore it will
            # intentionally return no_grounded_solution unless context is passed
            # by the application orchestrator.
            result = troubleshoot(complaint, retrieved_context=[])
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        print(json.dumps({
            "success": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "message": "Engine could not start. Check .env, dependencies, and prompt files.",
        }, indent=2, ensure_ascii=False))
