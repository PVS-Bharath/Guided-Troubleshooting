from typing import List, Tuple
from schemas.troubleshooting import Action
from deeplink_mapper import DeeplinkMapper

CATEGORY_ORDER = {"critical": 0, "auto": 1, "manual": 2}

class ResponseValidator:
    def __init__(self, mapper: DeeplinkMapper):
        self.mapper = mapper

    def validate_and_order_actions(self, actions: List[Action]) -> Tuple[List[Action], List[str]]:
        validated_actions = []
        warnings = []

        for action in actions:
            mapped_url = self.mapper.map_action(action.actionName)

            if action.deeplink:
                if action.deeplink not in self.mapper.catalog.values():
                    warnings.append(f"Rejected unverified/hallucinated URL: {action.deeplink}")
                    action.deeplink = mapped_url
            else:
                action.deeplink = mapped_url

            category_clean = action.category.lower().strip() if action.category else "manual"
            if category_clean not in CATEGORY_ORDER:
                action.category = "manual"
            else:
                action.category = category_clean

            # Manual actions must not receive actionable deeplinks
            if action.category == "manual":
                action.deeplink = None

            validated_actions.append(action)

        validated_actions.sort(key=lambda a: CATEGORY_ORDER.get(a.category, 3))
        return validated_actions, warnings