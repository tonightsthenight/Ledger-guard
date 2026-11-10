# Ledger Guard

Deterministic checker for stacked goal ledgers — the decks, one-sheets and
forms built from one set of figures, where a window total quietly gets added
on top of the day total it already sits inside.

## What it does

Registers one Hermes tool, `ledger_guard_check`, which verifies a ledger CSV
with columns `name, owner, period, amount, relation, parent, declared_total`:

- `additive` entries count toward the combined total
- `included` entries sit inside a parent entry and must never be added again
- `stretch` entries are alternate versions of a parent base entry; only one
  version may be the headline figure
- `declared_total` (on any one row) is the combined total the documents print

The tool checks that additive entries sum exactly to the declared total,
flags included/stretch entries with a missing or unknown parent, flags
duplicate entry names, and lists base entries that have stretch versions.
It accepts either a file path or inline CSV text and returns a JSON verdict:
`{ok, entries_checked, problems, notes, summary}`.

This is code, not a prompt: the same input always gives the same verdict,
which is the point — a language model should not be the thing checking
its own arithmetic.

## Disclosure (per Hermes catalog rule 13)

- No network calls. No credentials. No shell commands. No background processes.
- No telemetry. No self-updating code; updates ship as new commits only.
- Reads only the ledger file the user passes it (or CSV text supplied in the
  tool call); writes nothing.
- Pure Python standard library; no third-party dependencies.

## Try it standalone

The checker also runs outside Hermes:

```
python3 ledger_guard.py sample-ledger.csv
```

Exit code 0 means every check passed; 1 prints a plain-language report.

## Layout

```
plugin.yaml      manifest (name, version, provides_tools, requires_hermes)
__init__.py      registration — register(ctx) wires one tool
schemas.py       the tool schema the LLM reads
tools.py         handlers (args dict in, JSON string out)
ledger_guard.py  the tested checker core (load / check), vendored unchanged
sample-ledger.csv  example ledger used in the tests
```

## License

MIT
