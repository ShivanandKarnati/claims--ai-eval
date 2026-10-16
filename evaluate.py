"""Runs the golden set and writes results/report.md - the numbers you put in your README.

Usage:
    python evaluate.py
    python evaluate.py --model llama3.2:1b      # compare a different model
    python evaluate.py --temperature 0.8        # see how randomness hurts
"""
import argparse
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from app import MODEL, extract_claim, parse_claim
from eval_utils import FIELDS, amount_is_grounded, field_matches, load_golden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--temperature", type=float, default=0.0)
    args = ap.parse_args()

    golden = load_golden()
    correct = {f: 0 for f in FIELDS}
    schema_ok = hallucinations = 0
    mistakes = []

    for case in golden:
        raw = extract_claim(case["note"], model=args.model, temperature=args.temperature)
        try:
            claim = parse_claim(raw)
            schema_ok += 1
        except ValidationError:
            mistakes.append((case["id"], "ALL", "valid JSON", raw[:60]))
            continue
        if not amount_is_grounded(case["note"], claim.estimated_amount):
            hallucinations += 1
        for f in FIELDS:
            exp, got = case["expected"][f], getattr(claim, f)
            if field_matches(f, exp, got):
                correct[f] += 1
            else:
                mistakes.append((case["id"], f, exp, got))
        print(f"{case['id']} done")

    n = len(golden)
    overall = sum(correct.values()) / (n * len(FIELDS))
    lines = [
        f"# Evaluation report",
        f"Model: `{args.model}` | temperature: {args.temperature} | cases: {n} | "
        f"run: {datetime.now():%Y-%m-%d %H:%M}",
        "",
        "| Metric | Result |", "|---|---|",
        f"| Overall field accuracy | {overall:.0%} |",
        f"| Valid schema | {schema_ok}/{n} |",
        f"| Hallucinated amounts | {hallucinations} |",
        *[f"| {f} accuracy | {correct[f] / n:.0%} |" for f in FIELDS],
        "", "## Mistakes", "| Case | Field | Expected | Got |", "|---|---|---|---|",
        *[f"| {cid} | {f} | {e} | {g} |" for cid, f, e, g in mistakes],
    ]
    out = Path("results") / f"report_{args.model.replace(':', '_')}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:12]))
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
