from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data"/"paper"


def ensure_dirs() -> None:
    (DATA/"snapshots").mkdir(parents=True,exist_ok=True)


def now_utc() -> str:
    return datetime.utcnow().isoformat()+"Z"


def append_jsonl(name: str, record: dict[str,Any]) -> None:
    ensure_dirs()
    p=DATA/name
    with p.open("a",encoding="utf-8") as f:
        f.write(json.dumps(record,ensure_ascii=False,sort_keys=True,default=str)+"\n")


def read_jsonl(name: str) -> list[dict[str,Any]]:
    p=DATA/name
    if not p.exists():
        return []
    out=[]
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def write_snapshot(snapshot_name: str, payload: dict[str,Any]) -> str:
    ensure_dirs()
    ts=datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe=snapshot_name.replace("/","_").replace(" ","_")
    p=DATA/"snapshots"/f"{safe}_{ts}.json"
    p.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,default=str,indent=2),encoding="utf-8")
    return str(p.relative_to(ROOT))


def open_positions() -> dict[str,dict[str,Any]]:
    events=read_jsonl("events.jsonl")
    state={}
    for e in events:
        pid=e.get("position_id")
        if not pid: continue
        typ=e.get("event_type")
        if typ=="OPEN":
            state[pid]=e.get("position",{})
        elif typ=="CLOSE":
            state.pop(pid,None)
        elif typ=="MARK" and pid in state:
            state[pid]["last_mark"]=e
    return state
