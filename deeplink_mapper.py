import json
import os
from typing import Dict, Optional

class DeeplinkMapper:
    def __init__(self, catalog_path: str = None):
        if catalog_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            catalog_path = os.path.join(base_dir, "data", "deeplinks.json")
            
        self.catalog_path = catalog_path
        self.catalog: Dict[str, str] = {}
        self.load_catalog()

    def load_catalog(self):
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"Authoritative deeplink catalog not found: {self.catalog_path}")

        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    name = item.get("name") or item.get("target")
                    url = item.get("deeplink") or item.get("url")
                    if name and url:
                        self.catalog[name.lower().strip()] = url.strip()
            elif isinstance(data, dict):
                for k, v in data.items():
                    self.catalog[k.lower().strip()] = v.strip()

        if not self.catalog:
            raise ValueError(f"Authoritative deeplink catalog is empty or invalid: {self.catalog_path}")

    def map_action(self, action_name: str, hint: Optional[str] = None) -> Optional[str]:
        if hint and hint.lower().strip() in self.catalog:
            return self.catalog[hint.lower().strip()]

        action_clean = action_name.lower().strip()
        for key, deeplink in self.catalog.items():
            if key in action_clean or action_clean in key:
                return deeplink
        
        return None