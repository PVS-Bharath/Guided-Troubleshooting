import pytest
from pydantic import ValidationError
from schemas.troubleshooting import Plan
def test_schema_rejects_extra():
 with pytest.raises(ValidationError):Plan.model_validate({"title":"x","score":0,"actions":[],"status":"ok","extra":1})
def test_score_bounds():
 with pytest.raises(ValidationError):Plan.model_validate({"title":"x","score":2,"actions":[],"status":"ok"})
