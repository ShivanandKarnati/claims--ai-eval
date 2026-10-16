"""1. Schema / contract test: every output must be valid JSON with the right fields and types."""
import pytest

from app import parse_claim
from eval_utils import load_golden

CASE_IDS = [c["id"] for c in load_golden()]


@pytest.mark.parametrize("case_id", CASE_IDS)
def test_output_matches_schema(case_id, raw_outputs):
    parse_claim(raw_outputs[case_id])  # raises ValidationError -> test fails
