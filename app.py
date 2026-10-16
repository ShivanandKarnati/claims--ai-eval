"""Claim intake extractor: turns a free-text insurance claim note into structured fields
using a local LLM (Ollama)."""
import os
from typing import Literal, Optional

import ollama
from pydantic import BaseModel, Field

MODEL = os.getenv("CLAIMS_MODEL", "llama3.2:3b")


class Claim(BaseModel):
    incident_date: Optional[str] = Field(None, description="YYYY-MM-DD, or null if no date is given")
    loss_type: Literal["auto_collision", "water_damage", "fire", "theft", "other"]
    estimated_amount: Optional[float] = Field(None, description="Dollar amount, or null if none is stated")
    at_fault: Literal["insured", "other_party", "unknown"]
    severity: Literal["low", "medium", "high"]


SYSTEM_PROMPT = """You are an insurance claims intake assistant.
Read the claim note and return ONLY a JSON object with these fields:

- incident_date: the date of the incident as YYYY-MM-DD. null if no date is given.
- loss_type: one of "auto_collision", "water_damage", "fire", "theft", "other".
- estimated_amount: the total dollar amount as a number (no $ or commas).
  null if no amount is mentioned. Never guess an amount.
- at_fault:
    "insured" if the policyholder, or someone driving their vehicle / in their household, caused it;
    "other_party" if another named or described person caused it (including a thief or a neighbor);
    "unknown" if nobody is said to be responsible.
- severity:
    "high" if anyone was injured OR the amount is over 10000;
    "medium" if the amount is 1000 to 10000, or if there is no amount and no injury;
    "low" if the amount is under 1000.
"""


def extract_claim(note: str, model: str = MODEL, temperature: float = 0.0) -> str:
    """Send one claim note to the model and return its raw JSON text."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": note},
        ],
        format=Claim.model_json_schema(),  # structured output: forces JSON in this shape
        options={"temperature": temperature, "seed": 42},
    )
    return response["message"]["content"]


def parse_claim(raw: str) -> Claim:
    """Validate raw model output against the schema (raises if invalid)."""
    return Claim.model_validate_json(raw)


if __name__ == "__main__":
    sample = "Rear-ended at a red light on 2026-03-14, other driver was cited. Bumper damage, estimate $2,400."
    raw = extract_claim(sample)
    print(raw)
    print(parse_claim(raw))
