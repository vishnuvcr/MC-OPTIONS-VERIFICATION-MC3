from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CAL=ROOT/"data"/"paper"/"calendars"
CAL.mkdir(parents=True,exist_ok=True)

# Exchange-authenticated 2026 holiday cache. Updated from official exchange
# calendars before the current prospective window.
DEFAULT_2026={
    # Exchange-specific derivatives calendars for 2026.
    # NIFTY source: NSE F&O holiday circular NSE/FAOP/71777.
    # SENSEX source: current BSE equity/equity-derivatives holiday calendar.
    "NIFTY":[
        "2026-01-15","2026-01-26","2026-03-03","2026-03-26","2026-03-31",
        "2026-04-03","2026-04-14","2026-05-01","2026-05-28",
        "2026-06-26","2026-09-14","2026-10-02","2026-10-20",
        "2026-11-10","2026-11-24","2026-12-25"
    ],
    "SENSEX":[
        "2026-01-15","2026-01-26","2026-03-03","2026-03-26",
        "2026-03-31","2026-04-03","2026-04-14","2026-05-01",
        "2026-05-28","2026-06-26","2026-09-14","2026-10-02",
        "2026-10-20","2026-11-10","2026-11-24","2026-12-25"
    ]
}


def holidays(exchange: str, year: int) -> set[date]:
    p=CAL/f"{exchange}_{year}.json"
    if p.exists():
        data=json.loads(p.read_text(encoding="utf-8"))
    elif year==2026 and exchange in DEFAULT_2026:
        data=DEFAULT_2026[exchange]
        p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    else:
        raise RuntimeError(f"no cached {exchange} holiday calendar for {year}; fail-closed to avoid a wrong D3")
    return {date.fromisoformat(x) for x in data}
