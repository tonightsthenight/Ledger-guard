"""Tool handlers — the code that runs when the LLM calls each tool.

The checking logic itself lives in ledger_guard.py, vendored unchanged from
the tested standalone checker; these handlers only adapt its load()/check()
functions to the Hermes tool surface (args dict in, JSON string out).
"""

import csv
import io
import json

from . import ledger_guard


def _report(rows, problems, notes):
    return {
        "ok": not problems,
        "entries_checked": len(rows),
        "problems": problems,
        "notes": notes,
        "summary": (
            f"{len(rows)} entries checked, {len(problems)} problem(s)."
        ),
    }


def ledger_guard_check(args: dict, **kwargs) -> str:
    """Run the ledger consistency check. Always returns a JSON string."""
    path = (args.get("path") or "").strip()
    csv_text = args.get("csv_text") or ""
    try:
        if csv_text.strip():
            rows = [
                r
                for r in csv.DictReader(io.StringIO(csv_text))
                if r.get("name")
            ]
            for r in rows:
                r["amount"] = float(r["amount"])
        elif path:
            rows = ledger_guard.load(path)
        else:
            return json.dumps(
                {"error": "Provide either 'path' or 'csv_text'."}
            )
        problems, notes = ledger_guard.check(rows)
        return json.dumps(_report(rows, problems, notes))
    except FileNotFoundError:
        return json.dumps({"error": f"Ledger file not found: {path}"})
    except Exception as e:  # handlers never raise; errors go back as JSON
        return json.dumps({"error": f"Ledger check failed: {e}"})
