from typing import List, Dict, Any

class MockRetrievalEngine:
    """Development mock for the knowledge retrieval component.
    Receives enriched data from MockAIEngine and returns a static list of candidate actions.
    MARKED AS DEVELOPMENT/MOCK – replace with real retrieval implementation.
    """
    def retrieve(self, enriched_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # For any input, return a single candidate action dict
        return [
            {
                "actionName": "Battery",
                "description": "It will help reduce battery usage",
                "steps": ["Open Settings", "Select Battery", "Check battery usage"],
                "deeplink": "settings://battery",
                "category": "manual",
            }
        ]
