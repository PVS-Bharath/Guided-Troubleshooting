import pytest
from query_enrichment import enrich_query
@pytest.mark.parametrize("x,y",[("My phone battery is dying so fast","phone battery is draining quickly"),("phone getting too hot","phone overheating"),("screen blinking","screen flickering"),("phone won't charge","phone not charging"),(" ","")])
def test_normalize(x,y):
 r=enrich_query(x);assert ("" if r["is_empty"] else r["enriched_query"])==y
def test_type():
 with pytest.raises(TypeError):enrich_query(None)
