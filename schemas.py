"""Tool schemas — what the LLM sees."""

LEDGER_GUARD_CHECK = {
    "name": "ledger_guard_check",
    "description": (
        "Deterministically verify a stacked goal ledger CSV for double-counting "
        "and arithmetic errors. The CSV must have columns: name, owner, period, "
        "amount, relation, parent, declared_total. relation is one of: additive "
        "(counts toward the combined total), included (sits inside its parent "
        "entry and must never be added again), or stretch (an alternate version "
        "of its parent base entry; only one version may be the headline figure). "
        "declared_total (on any one row) is the combined total the documents "
        "print. The checker verifies that additive entries sum exactly to the "
        "declared total, flags included/stretch entries with a missing or "
        "unknown parent, flags duplicate entry names, and lists base entries "
        "that have stretch versions. Use this whenever a user shares a ledger, "
        "goal sheet, event plan, or any set of stacked figures whose parts are "
        "supposed to add up to a printed combined total — a language model "
        "should not be the thing checking its own arithmetic."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": (
                    "Path to the ledger CSV file to check "
                    "(e.g. '/home/user/ledgers/event-goals.csv')."
                ),
            },
            "csv_text": {
                "type": "string",
                "description": (
                    "Alternative to path: the ledger CSV content inline, with "
                    "the same columns. Use this when the user pasted the ledger "
                    "into the conversation instead of saving it as a file."
                ),
            },
        },
        "required": [],
    },
}
