"""3. Consistency test: the same input should give the same answer every time."""
import os

import pytest

from app import extract_claim, parse_claim
from eval_utils import load_golden

RUNS = 3
TEMPERATURE = float(os.getenv("CONSISTENCY_TEMPERATURE", "0.0"))  # try 0.8 to see it break
CASES = load_golden()[:5]


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_same_input_same_output(case):
    outputs = [parse_claim(extract_claim(case["note"], temperature=TEMPERATURE)).model_dump()
               for _ in range(RUNS)]
    assert all(o == outputs[0] for o in outputs), f"Outputs differed across runs: {outputs}"
