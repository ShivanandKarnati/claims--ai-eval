"""2. Accuracy test: AI output isn't pass/fail per case, so we measure accuracy and gate on a threshold."""
import os

from eval_utils import FIELDS, field_matches

THRESHOLD = float(os.getenv("ACCURACY_THRESHOLD", "0.80"))


def test_field_accuracy_meets_threshold(golden, parsed):
    correct = {f: 0 for f in FIELDS}
    for case in golden:
        claim = parsed[case["id"]]
        for f in FIELDS:
            if claim is not None and field_matches(f, case["expected"][f], getattr(claim, f)):
                correct[f] += 1

    n = len(golden)
    print("\nPer-field accuracy:")
    for f in FIELDS:
        print(f"  {f:<18} {correct[f] / n:.0%}")
    overall = sum(correct.values()) / (n * len(FIELDS))
    print(f"  {'OVERALL':<18} {overall:.0%}  (threshold {THRESHOLD:.0%})")

    assert overall >= THRESHOLD, f"Overall accuracy {overall:.0%} is below {THRESHOLD:.0%}"
