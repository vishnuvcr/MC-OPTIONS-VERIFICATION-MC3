from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from html import escape

from .store import read_jsonl, open_positions

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"site"


def _load() -> dict:
    signals=read_jsonl("signals.jsonl")
    events=read_jsonl("events.jsonl")
    positions=open_positions()
    trades=[s for s in signals if s.get("trade")]
    pnl=[e.get("pnl_rupees") for e in events if e.get("event_type")=="MARK" and isinstance(e.get("pnl_rupees"),(int,float))]
    return {"signals":signals,"events":events,"positions":positions,"trades":trades,"pnl":pnl}


def build() -> None:
    d=_load()
    OUT.mkdir(parents=True,exist_ok=True)
    open_count=len(d["positions"])
    signal_count=len(d["signals"])
    trade_count=len(d["trades"])
    last_pnl=d["pnl"][-1] if d["pnl"] else 0
    closed=[e for e in d["events"] if e.get("event_type")=="CLOSE"]
    realised=sum(float(e.get("realized_pnl_rupees",0)) for e in closed)

    rows=[]
    for s in reversed(d["signals"][-100:]):
        rows.append(
            "<tr>"
            f"<td>{escape(str(s.get('scan_date','')))}</td>"
            f"<td><b>{escape(str(s.get('underlying','')))}</b></td>"
            f"<td>{escape(str(s.get('expiry','')))}</td>"
            f"<td>{escape(str(s.get('status','')))}</td>"
            f"<td>{'ON' if s.get('gate') else 'OFF'}</td>"
            f"<td>{escape(f'{float(s.get("mc_ev_points")):,.2f}' if isinstance(s.get('mc_ev_points'),(int,float)) else '')}</td>"
            f"<td>{'PAPER TRADE' if s.get('trade') else '—'}</td>"
            f"<td>{escape(str(s.get('reason','')))}</td>"
            "</tr>"
        )

    trade_rows=[]
    for pid,p in d["positions"].items():
        last=p.get("last_mark",{})
        trade_rows.append(
            "<tr>"
            f"<td>{escape(pid)}</td><td>{escape(p['underlying'])}</td><td>{escape(p['expiry'])}</td>"
            f"<td>OPEN</td><td>{escape(f'{float(last.get("pnl_rupees",0)):,.2f}' if last else '—')}</td>"
            "</tr>"
        )

    css="""
    :root{--bg:#0b1020;--panel:#121a2b;--ink:#eaf1ff;--muted:#9fb0ca;--accent:#55d6be;--line:#25314a}
    *{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#09101c,#0f172a);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
    .wrap{max-width:1250px;margin:0 auto;padding:32px}.hero{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;margin-bottom:28px}
    h1{font-size:38px;margin:0 0 8px}.sub{color:var(--muted);max-width:780px;line-height:1.5}.pill{display:inline-block;padding:7px 10px;border:1px solid var(--line);border-radius:999px;color:var(--accent);font-size:12px}
    .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}.card{background:rgba(18,26,43,.86);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 12px 36px rgba(0,0,0,.18)}
    .k{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}.v{font-size:28px;font-weight:750;margin-top:7px}.small{font-size:12px;color:var(--muted)}
    table{width:100%;border-collapse:collapse;font-size:13px}.table-wrap{overflow:auto}.panel{margin-top:18px}.panel h2{margin:0 0 14px;font-size:19px}
    th,td{padding:10px 9px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{color:var(--muted);font-weight:600}
    .foot{margin-top:28px;color:var(--muted);font-size:12px;line-height:1.6}.nav a{color:var(--accent);text-decoration:none;margin-right:16px}
    @media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.hero{flex-direction:column;align-items:flex-start}}@media(max-width:560px){.grid{grid-template-columns:1fr}.wrap{padding:18px}h1{font-size:30px}}
    """
    html=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BATMAN PAPER TRADE</title><style>{css}</style></head>
<body><div class="wrap">
<div class="hero"><div><div class="pill">PROSPECTIVE VALIDATION • PAPER ONLY</div><h1>BATMAN PAPER TRADE</h1>
<div class="sub">Frozen MC-RQ6-v1 validation for NIFTY and SENSEX. Every scan is retained, every gated trade becomes paper-only, and open positions are marked from live prices without submitting broker orders.</div></div>
<div class="small">Generated {escape(datetime.utcnow().isoformat())} UTC</div></div>
<div class="grid">
<div class="card"><div class="k">Signals logged</div><div class="v">{signal_count}</div></div>
<div class="card"><div class="k">Paper trades</div><div class="v">{trade_count}</div></div>
<div class="card"><div class="k">Open positions</div><div class="v">{open_count}</div></div>
<div class="card"><div class="k">Latest MTM</div><div class="v">₹{last_pnl:,.0f}</div></div>
</div>
<div class="grid">
<div class="card"><div class="k">Realised P&L</div><div class="v">₹{realised:,.0f}</div></div>
<div class="card"><div class="k">Strategy</div><div class="v">P20/P35/P65/P80</div><div class="small">+1 / -2 / +1 / -2</div></div>
<div class="card"><div class="k">MC</div><div class="v">756 × 5,000</div><div class="small">seed 756 • 3 sessions</div></div>
<div class="card"><div class="k">Slippage</div><div class="v">2 pts/leg</div><div class="small">research primary friction</div></div>
</div>
<div class="panel card"><h2>Signal ledger</h2><div class="table-wrap"><table><thead><tr><th>Date</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Gate</th><th>MC-EV</th><th>Trade</th><th>Reason</th></tr></thead><tbody>{''.join(rows) or '<tr><td colspan="8">No signals recorded yet.</td></tr>'}</tbody></table></div></div>
<div class="panel card"><h2>Open paper positions</h2><div class="table-wrap"><table><thead><tr><th>Position</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Latest MTM</th></tr></thead><tbody>{''.join(trade_rows) or '<tr><td colspan="5">No open positions.</td></tr>'}</tbody></table></div></div>
<div class="panel card"><h2>Data discipline</h2><div class="small">No synthetic prices are used. Missing or unauthenticated market data produces an explicit DATA_UNAVAILABLE outcome. GitHub Actions timestamps are recorded as actual observations. No live order endpoint is called by this module.</div></div>
<div class="foot nav"><a href="https://github.com/vishnuvcr/MC-OPTIONS-VERIFICATION-MC3/tree/main/data/paper">Raw logs</a><a href="https://github.com/vishnuvcr/MC-OPTIONS-VERIFICATION-MC3/blob/main/research/prospective_validation/PROTOCOL.md">Protocol</a><a href="https://www.nseindia.com/option-chain">NSE option chain</a><a href="https://developer.paytmmoney.com/">Paytm Money API</a></div>
</div></body></html>"""
    (OUT/"index.html").write_text(html,encoding="utf-8")


if __name__=="__main__":
    build()
