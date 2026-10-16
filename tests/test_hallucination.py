"""4. Hallucination test: the model must not invent dollar amounts that aren't in the note."""
import pytest

from eval_utils import amount_is_grounded, load_golden

CASES = load_golden()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_amount_is_grounded_in_note(case, parsed):
    claim = parsed[case["id"]]
    if claim is None:
        pytest.skip("Output failed schema validation (covered by test_schema)")
    assert amount_is_grounded(case["note"], claim.estimated_amount), (
        f"Model returned ${claim.estimated_amount}, which does not appear in the note"
    )
    if case["expected"]["estimated_amount"] is None:
        assert claim.estimated_amount is None, "Note has no amount, but the model invented one"
