# Prospective paper-trade data

This directory is the append-only prospective record.

- signals.jsonl — every scheduled/manual scan result;
- events.jsonl — OPEN / MARK / CLOSE events;
- errors.jsonl — errors and unavailable data;
- runs.jsonl — run-level provenance;
- snapshots/ — D3/live source snapshots when material to the signal;
- config_snapshot.json — frozen strategy/data rules.

Do not hand-edit these records during prospective validation.
