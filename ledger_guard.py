#!/usr/bin/env python3
"""Ledger Guard: deterministic checker for stacked sales/event goal ledgers.

Reads a ledger CSV with columns:
  name,owner,period,amount,relation,parent,declared_total
relation is one of: additive | included | stretch
  - additive: counts toward the combined total
  - included: sits inside its parent entry; must never be added again
  - stretch:  an alternate version of its parent base entry; only one
              version may be the headline figure
declared_total (on any one row) is the combined total the documents print.

Exits 0 when every check passes, 1 with a plain-language report otherwise.
No network, no credentials, no writes outside stdout.
"""
import csv, sys
from collections import defaultdict

def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f) if r.get('name')]
    for r in rows:
        r['amount'] = float(r['amount'])
    return rows

def check(rows):
    problems, notes = [], []
    additive = [r for r in rows if r['relation'] == 'additive']
    total = sum(r['amount'] for r in additive)
    declared = next((float(r['declared_total']) for r in rows if r.get('declared_total')), None)
    if declared is None:
        problems.append("No declared_total found: documents have no combined total to verify against.")
    elif abs(total - declared) > 0.005:
        problems.append(f"Additive entries sum to {total:,.2f} but the declared combined total is {declared:,.2f} (difference {total-declared:+,.2f}).")
    else:
        notes.append(f"Additive sum matches declared total: {declared:,.2f}.")
    names = {r['name'] for r in rows}
    for r in rows:
        if r['relation'] in ('included', 'stretch'):
            if not r.get('parent'):
                problems.append(f"'{r['name']}' is marked {r['relation']} but names no parent entry.")
            elif r['parent'] not in names:
                problems.append(f"'{r['name']}' points at parent '{r['parent']}', which is not in the ledger.")
            elif r in additive:
                problems.append(f"'{r['name']}' is both {r['relation']} and additive: double-count risk.")
    by_parent = defaultdict(list)
    for r in rows:
        if r['relation'] == 'stretch':
            by_parent[r['parent']].append(r['name'])
    for parent, stretches in by_parent.items():
        notes.append(f"Base '{parent}' has stretch version(s): {', '.join(stretches)} — print only one as the headline.")
    dupes = [n for n, c in ((n, sum(1 for r in rows if r['name'] == n)) for n in names) if c > 1]
    if dupes:
        problems.append(f"Duplicate entry names: {', '.join(sorted(dupes))}.")
    return problems, notes

def main(argv):
    if len(argv) != 2:
        print("usage: ledger_guard.py <ledger.csv>"); return 2
    rows = load(argv[1])
    problems, notes = check(rows)
    for n in notes: print(f"OK  {n}")
    for p in problems: print(f"FAIL {p}")
    print(f"\n{len(rows)} entries checked, {len(problems)} problem(s).")
    return 1 if problems else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
