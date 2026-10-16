"""Shared helpers for the tests and the evaluation report."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
FIELDS = ["incident_date", "loss_type", "estimated_amount", "at_fault", "severity"]


def load_golden():
    return json.loads((ROOT / "data" / "golden.json").read_text(encoding="utf-8"))


def field_matches(field, expected, actual):
    """Exact match, except amounts are allowed to differ by under $1."""
    if field == "estimated_amount":
        if expected is None or actual is None:
            return expected is None and actual is None
        return abs(float(expected) - float(actual)) < 1
    return expected == actual


def amount_is_grounded(note, amount):
    """Hallucination check: a non-null amount must actually appear in the note text."""
    if amount is None:
        return True
    text = re.sub(r"[,$]", "", note)
    candidates = {f"{amount:.0f}", f"{amount:.2f}"}
    return any(c in text for c in candidates)
