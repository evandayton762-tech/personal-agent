"""Cost ledger for recording token and dollar usage.

Writes entries to a JSONL file and provides aggregated totals for the current day.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any


LEDGER_PATH = os.path.join("memory", "cost_ledger.jsonl")


@dataclass
class LedgerEntry:
    task_id: str
    step_id: str
    in_tokens: int
    out_tokens: int
    usd: float
    ts: str  # ISO timestamp


class CostLedger:
    def __init__(self, ledger_path: str = LEDGER_PATH):
        self.ledger_path = ledger_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)

    def append(self, task_id: str, step_id: str, in_tokens: int, out_tokens: int, usd: float) -> None:
        """Append a new ledger entry as a JSONL line."""
        entry = LedgerEntry(
            task_id=task_id,
            step_id=step_id,
            in_tokens=in_tokens,
            out_tokens=out_tokens,
            usd=usd,
            ts=datetime.now(timezone.utc).isoformat(),
        )
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

    def totals_today(self) -> Dict[str, Any]:
        """Return aggregated token and USD totals for the current UTC date."""
        totals = {
            "in_tokens": 0,
            "out_tokens": 0,
            "usd": 0.0,
        }
        today = datetime.now(timezone.utc).date()
        if not os.path.exists(self.ledger_path):
            return totals
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
                ts = record.get("ts")
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts).astimezone(timezone.utc)
                    except ValueError:
                        continue
                    if dt.date() != today:
                        continue
                totals["in_tokens"] += record.get("in_tokens", 0)
                totals["out_tokens"] += record.get("out_tokens", 0)
                totals["usd"] += record.get("usd", 0.0)
        return totals