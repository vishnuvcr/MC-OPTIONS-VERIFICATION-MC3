from __future__ import annotations

from datetime import datetime
from pathlib import Path
from html import escape

from .store import read_jsonl, open_positions

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site"


def _load() -> dict:
    signals = read_jsonl("signals.jsonl")
    events = read_jsonl("events.jsonl")
    positions = open_positions()
    valid_signals = [s for s in signals if s.get("prospective_valid")]
    trades = [s for s in valid_signals if s.get("trade")]
    pnl = [
        e.get("pnl_rupees_net_estimate", e.get("pnl_rupees"))
        for e in events
        if e.get("event_type") == "MARK"
        and isinstance(e.get("pnl_rupees_net_estimate", e.get("pnl_rupees")), (int, float))
    ]
    return {
        "signals": signals,
        "events": events,
        "positions": positions,
        "valid_signals": valid_signals,
        "trades": trades,
        "pnl": pnl,
    }


def build() -> None:
    d = _load()
    OUT.mkdir(parents=True, exist_ok=True)

    signal_count = len(d["signals"])
    valid_count = len(d["valid_signals"])
    trade_count = len(d["trades"])
    open_count = len(d["positions"])
    last_pnl = d["pnl"][-1] if d["pnl"] else 0.0
    closed = [e for e in d["events"] if e.get("event_type") == "CLOSE"]
    realised = sum(float(e.get("realized_pnl_rupees_net", e.get("realized_pnl_rupees", 0))) for e in closed)

    rows = []
    for s in reversed(d["signals"][-120:]):
        ev = s.get("mc_ev_points")
        ev_text = f"{float(ev):,.2f}" if isinstance(ev, (int, float)) else ""
        strikes = s.get("strikes") or {}
        strike_text = " / ".join(
            f"{k.replace('_',' ')}={v:g}" for k, v in strikes.items()
        ) if strikes else "—"
        rows.append(
            "<tr>"
            f"<td>{escape(str(s.get('scan_date','')))}</td>"
            f"<td><b>{escape(str(s.get('underlying','')))}</b></td>"
            f"<td>{escape(str(s.get('expiry','')))}</td>"
            f"<td>{escape(str(s.get('status','')))}</td>"
            f"<td>{'ON' if s.get('gate') else 'OFF'}</td>"
            f"<td>{escape(ev_text)}</td>"
            f"<td>{escape(strike_text)}</td>"
            f"<td>{'PAPER' if s.get('trade') else '—'}</td>"
            f"<td>{escape(str(s.get('reason','')))}</td>"
            "</tr>"
        )

    trade_rows = []
    for pid, p in d["positions"].items():
        last = p.get("last_mark", {})
        last_pnl = last.get("pnl_rupees_net_estimate", last.get("pnl_rupees")) if last else None
        pnl_text = f"₹{float(last_pnl):,.0f}" if isinstance(last_pnl, (int, float)) else "—"
        trade_rows.append(
            "<tr>"
            f"<td>{escape(pid)}</td>"
            f"<td>{escape(str(p.get('underlying','')))}</td>"
            f"<td>{escape(str(p.get('expiry','')))}</td>"
            f"<td>OPEN</td>"
            f"<td>{escape(pnl_text)}</td>"
            f"<td>{escape(str(p.get('strikes',{})))}</td>"
            "</tr>"
        )

    css = """
    :root{--bg:#070b13;--panel:#111827;--panel2:#0d1422;--ink:#edf4ff;--muted:#91a3bf;--accent:#64e1c6;--line:#24334b;--warn:#f3c969}
    *{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% 0%,#12203a 0,#070b13 44%,#05070d 100%);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
    .wrap{max-width:1380px;margin:0 auto;padding:28px}.hero{display:flex;justify-content:space-between;gap:30px;align-items:flex-end;margin-bottom:26px}
    h1{font-size:42px;line-height:1.05;margin:8px 0 10px;letter-spacing:-.03em}.sub{color:var(--muted);max-width:900px;line-height:1.55}
    .pill{display:inline-flex;align-items:center;gap:7px;padding:7px 11px;border:1px solid #285146;border-radius:999px;color:var(--accent);background:#0a1716;font-size:12px;font-weight:700;letter-spacing:.06em}
    .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:16px 0}.card{background:linear-gradient(180deg,rgba(17,24,39,.96),rgba(13,20,34,.96));border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 14px 40px rgba(0,0,0,.22)}
    .k{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.09em}.v{font-size:28px;font-weight:800;margin-top:7px}.small{font-size:12px;color:var(--muted);line-height:1.55}
    table{width:100%;border-collapse:collapse;font-size:12px}.table-wrap{overflow:auto}.panel{margin-top:16px}.panel h2{margin:0 0 13px;font-size:18px}
    th,td{padding:10px 9px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{color:var(--muted);font-weight:650;position:sticky;top:0;background:var(--panel)}
    .foot{margin-top:24px;color:var(--muted);font-size:12px;line-height:1.7}.nav a{color:var(--accent);text-decoration:none;margin-right:16px}
    .banner{background:#19170d;border:1px solid #4a3f1d;color:#e8d8a4;border-radius:16px;padding:14px 16px;margin-top:16px}
    @media(max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}.hero{flex-direction:column;align-items:flex-start}}@media(max-width:580px){.grid{grid-template-columns:1fr}.wrap{padding:16px}h1{font-size:31px}}
    """

    generated = datetime.utcnow().isoformat() + "Z"
    banner = (
        "Paper-only: this module never sends live orders. "
        "Prospective statistics count only records explicitly marked prospective_valid=true."
    )

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BATMAN PAPER TRADE</title><style>{css}</style></head>
<body><div class="wrap">
<div class="hero">
  <div>
    <div class="pill">PROSPECTIVE VALIDATION · PAPER ONLY</div>
    <h1>BATMAN PAPER TRADE</h1>
    <div class="sub">Frozen MC-RQ6-v1 validation for NIFTY and SENSEX. D3 signals, gate decisions, paper entries, repeated live marks, costs, data-source provenance and exceptions are retained as an append-only research record.</div>
  </div>
  <div class="small">Generated {escape(generated)}</div>
</div>

<div class="banner">{escape(banner)}</div>

<div class="grid">
  <div class="card"><div class="k">All signals logged</div><div class="v">{signal_count}</div><div class="small">includes NOT_D3 / diagnostics / errors</div></div>
  <div class="card"><div class="k">Valid prospective signals</div><div class="v">{valid_count}</div><div class="small">eligible for validation statistics</div></div>
  <div class="card"><div class="k">Paper trades</div><div class="v">{trade_count}</div><div class="small">gate ON + executable legs</div></div>
  <div class="card"><div class="k">Open positions</div><div class="v">{open_count}</div><div class="small">marked from live quotes</div></div>
</div>

<div class="grid">
  <div class="card"><div class="k">Latest net-estimate MTM</div><div class="v">₹{last_pnl:,.0f}</div><div class="small">entry-cost adjusted estimate</div></div>
  <div class="card"><div class="k">Realised net P&amp;L</div><div class="v">₹{realised:,.0f}</div><div class="small">closed paper positions</div></div>
  <div class="card"><div class="k">MC control</div><div class="v">756 × 5,000</div><div class="small">seed 756 · 3 sessions</div></div>
  <div class="card"><div class="k">Primary slippage</div><div class="v">2 pts/leg</div><div class="small">locked research convention</div></div>
</div>

<div class="panel card"><h2>Signal ledger</h2>
<div class="table-wrap"><table><thead><tr>
<th>Date</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Gate</th><th>MC-EV</th><th>Strikes</th><th>Trade</th><th>Reason</th>
</tr></thead><tbody>{''.join(rows) or '<tr><td colspan="9">No signals recorded yet.</td></tr>'}</tbody></table></div></div>

<div class="panel card"><h2>Open paper positions</h2>
<div class="table-wrap"><table><thead><tr><th>Position</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Latest net-est. MTM</th><th>Strikes</th></tr></thead>
<tbody>{''.join(trade_rows) or '<tr><td colspan="6">No open positions.</td></tr>'}</tbody></table></div></div>

<div class="panel card"><h2>Frozen strategy</h2>
<div class="small">+1 P35 PE · −2 P20 PE · +1 P65 CE · −2 P80 CE · gross MC-EV &gt; 0 gate · 09:30 IST target · expiry exit · no live order submission. Missing/unavailable market data causes a logged DATA_UNAVAILABLE outcome rather than synthetic prices.</div></div>

<div class="foot nav">
<a href="https://github.com/vishnuvcr/MC-OPTIONS-VERIFICATION-MC3/tree/main/data/paper">Raw logs</a>
<a href="https://github.com/vishnuvcr/MC-OPTIONS-VERIFICATION-MC3/blob/main/research/prospective_validation/PROTOCOL.md">Protocol</a>
<a href="https://www.nseindia.com/option-chain">NSE option chain</a>
<a href="https://developer.paytmmoney.com/">Paytm Money API</a>
</div>
</div></body></html>"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
