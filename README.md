# Claims AI Evaluation Suite

A QA framework for testing an LLM feature that pulls structured data out of free-text insurance claim notes.

AI output isn't deterministic, so ordinary `expected == actual` tests aren't enough. This project tests the model the way an AI QA team would: against a **golden dataset**, with **accuracy thresholds**, **consistency checks**, **hallucination detection**, and a **CI quality gate** that blocks a release when quality drops.

## Results

<!-- Paste the table from results/report_*.md here after you run evaluate.py -->

| Metric | llama3.2:3b |
|---|---|
| Overall field accuracy | _fill in_ |
| Valid schema | _fill in_ |
| Hallucinated amounts | _fill in_ |
| Consistent across 3 runs (temp 0) | _fill in_ |

**Key finding:** _fill in, e.g. "the model struggled with notes that had no dollar amount; it invented one in 2 of 3 cases."_

## What's tested

| Test | Why it matters for an AI feature |
|---|---|
| `test_schema.py` | Output always matches the contract that downstream systems rely on (Pydantic) |
| `test_accuracy.py` | Per-field accuracy against 20 hand-labeled claims; fails below 80% |
| `test_consistency.py` | The same claim gives the same answer every time |
| `test_hallucination.py` | The model never invents a dollar amount that isn't in the note |
| `.github/workflows/ai-eval.yml` | Runs everything in CI, so a prompt or model change can't lower quality unnoticed |

The golden set includes deliberately messy notes (typos, missing dates, missing amounts, ambiguous fault) because that's where AI features fail in production.

## Run it

```bash
# 1. Install Ollama (https://ollama.com) and pull a free local model
ollama pull llama3.2:3b

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the tests
pytest -v -s

# 4. Generate the evaluation report
python evaluate.py
python evaluate.py --model llama3.2:1b   # compare models
```

## What I'd add next
- **Bias checks:** swap names and zip codes and confirm the severity doesn't change
- **Robustness:** auto-generate typo and paraphrase variants of each golden case
- **Drift monitoring:** track accuracy over time as real claim language changes
- **Tooling:** run the same evaluations in promptfoo or DeepEval
- **UI layer:** a small web form with Cypress end-to-end tests

## Stack
Python · Ollama (local LLM) · Pydantic · pytest · GitHub Actions
