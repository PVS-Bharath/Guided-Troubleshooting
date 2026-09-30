"""Conservative complaint normalization without adding symptoms."""

import re


def enrich_query(raw_complaint: str) -> dict:
    if not isinstance(raw_complaint, str):
        raise TypeError("raw_complaint must be a string")

    original = re.sub(r"\s+", " ", raw_complaint).strip()

    if not original:
        return {
            "original_complaint": "",
            "enriched_query": "",
            "is_empty": True,
        }

    enriched = original.lower()

    replacements = [
        (r"\b(dying|going down|running out)\s+so\s+fast\b",
         "draining quickly"),
        (r"\bgetting\s+too\s+hot\b", "overheating"),
        (r"\b(feels|feeling)\s+too\s+hot\b", "overheating"),
        (r"\b(blinking|blinks)\b", "flickering"),
        (r"\bwon't\s+charge\b", "not charging"),
        (r"\bdoesn't\s+charge\b", "not charging"),
        (r"\bdoes\s+not\s+charge\b", "not charging"),
    ]

    for pattern, replacement in replacements:
        enriched = re.sub(pattern, replacement, enriched, flags=re.I)

    enriched = re.sub(
        r"^(my\s+)?(samsung\s+)?phone\s+",
        "phone ",
        enriched,
        flags=re.I,
    )

    return {
        "original_complaint": original,
        "enriched_query": enriched.strip(),
        "is_empty": False,
    }