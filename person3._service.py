from deeplink_mapper import DeeplinkMapper
from validator import ResponseValidator
from cache import FastPathCache
from schemas.troubleshooting import TroubleshootingResponse

class Person3Engine:
    def __init__(self, catalog_path: str = None):
        self.mapper = DeeplinkMapper(catalog_path)
        self.validator = ResponseValidator(self.mapper)
        self.cache = FastPathCache()

    def check_cache(self, query: str):
        return self.cache.get(query)

    def process_and_cache(self, response: TroubleshootingResponse) -> TroubleshootingResponse:
        valid_actions, warnings = self.validator.validate_and_order_actions(response.actions)
        response.actions = valid_actions
        self.cache.set(response.query, response)
        return response