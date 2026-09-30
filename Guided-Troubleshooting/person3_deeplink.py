from typing import Any, List, Dict
from cache import FastPathCache
from deeplink_mapper import DeeplinkMapper
from validator import ResponseValidator
from schemas.troubleshooting import Action

class Person3DeeplinkValidator:
    """Adapter connecting Person 3's validation system to Person 4's API."""

    def __init__(self, catalog_path: str = None):
        self.mapper = DeeplinkMapper(catalog_path=catalog_path)
        self.validator = ResponseValidator(self.mapper)
        self.cache = FastPathCache()

    def validate_and_map(self, candidates: List[dict]) -> List[dict]:
        person3_actions = [
            Action(
                actionName=act.get("actionName", ""),
                description=act.get("description", ""),
                category=act.get("category") or "manual",
                steps=act.get("steps", []),
                deeplink=act.get("deeplink"),
            )
            for act in candidates
        ]

        ordered_actions, _warnings = self.validator.validate_and_order_actions(person3_actions)

        return [
            {
                "actionName": action.actionName,
                "description": action.description,
                "steps": action.steps,
                "deeplink": action.deeplink,
                "category": action.category,
                "is_mock": False,
            }
            for action in ordered_actions
        ]