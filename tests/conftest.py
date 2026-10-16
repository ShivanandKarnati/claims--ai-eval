"""Runs the model once per golden case and shares the results with every test (keeps runs fast)."""
import pytest
from pydantic import ValidationError

from app import extract_claim, parse_claim
from eval_utils import load_golden


@pytest.fixture(scope="session")
def golden():
    return load_golden()


@pytest.fixture(scope="session")
def raw_outputs(golden):
    return {case["id"]: extract_claim(case["note"]) for case in golden}


@pytest.fixture(scope="session")
def parsed(raw_outputs):
    """id -> Claim, or None if the model's output failed schema validation."""
    result = {}
    for case_id, raw in raw_outputs.items():
        try:
            result[case_id] = parse_claim(raw)
        except ValidationError:
            result[case_id] = None
    return result
