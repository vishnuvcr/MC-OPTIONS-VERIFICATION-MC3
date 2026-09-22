from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from .store import open_positions, read_jsonl

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site"

CSS = r"""
:root{--bg:#060a12;--panel:#0f1725;--panel2:#0b1220;--ink:#eef4ff;--muted:#91a1bb;--accent:#67e5c3;--line:#233149;--warn:#f3cf6a;--bad:#ef8c8c}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:radial-gradient(circle at 15% 0%,#13213a 0,#070b12 48%,#05070c 100%);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
a{color:var(--accent);text-decoration:none}.wrap{max-width:1450px;margin:auto;padding:28px}
.top{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:22px}.brand{font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--accent)}
h1{font-size:40px;line-height:1.05;letter-spacing:-.04em;margin:7px 0 9px}h2{font-size:18px;margin:0 0 12px}.sub{color:var(--muted);line-height:1.55;max-width:950px}
.nav{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}.nav a{border:1px solid var(--line);background:#0a111d;padding:8px 11px;border-radius:999px;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:linear-gradient(180deg,rgba(15,23,37,.97),rgba(10,17,29,.97));border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 16px 40px rgba(0,0,0,.2);margin-top:14px}
.k{color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:.09em}.v{font-size:29px;font-weight:800;margin-top:7px}.small{font-size:12px;color:var(--muted);line-height:1.6}
.badge{display:inline-block;padding:5px 8px;border-radius:999px;border:1px solid var(--line);font-size:11px}
.badge.ok{color:var(--accent);border-color:#245844}.badge.warn{color:var(--warn);border-color:#54481c}.badge.bad{color:var(--bad);border-color:#5c2c2c}
.table{overflow:auto}.table table{width:100%;border-collapse:collapse;font-size:12px}.table th,.table td{padding:9px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}.table th{color:var(--muted);font-weight:700;position:sticky;top:0;background:var(--panel)}
.code{background:#070c15;border:1px solid var(--line);border-radius:12px;padding:14px;overflow:auto;color:#cde8dd;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;line-height:1.55}
.footer{margin:22px 0 8px;color:var(--muted);font-size:12px;line-height:1.6}.hero-banner{border:1px solid #4f4118;background:#17150b;color:#e7d69b;border-radius:15px;padding:13px 15px;margin:15px 0}
@media(max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}.top{flex-direction:column;align-items:flex-start}}@media(max-width:560px){.grid{grid-template-columns:1fr}.wrap{padding:16px}h1{font-size:31px}}
"""

NAV = """
<div class="nav">
<a href="index.html">Dashboard</a>
<a href="signals.html">Signals</a>
<a href="trades.html">Trades & MTM</a>
<a href="events.html">Events</a>
<a href="errors.html">Errors & Runs</a>
<a href="methodology.html">Frozen Method</a>
<a href="https://github.com/vishnuvcr/MC-OPTIONS-VERIFICATION-MC3/tree/main/data/paper">Raw records</a>
</div>
"""

def _load():
    return {
        "signals": read_jsonl("signals.jsonl"),
        "events": read_jsonl("events.jsonl"),
        "errors": read_jsonl("errors.jsonl"),
        "runs": read_jsonl("runs.jsonl"),
        "positions": open_positions(),
    }

def _layout(title: str, subtitle: str, body: str) -> str:
    now = datetime.utcnow().isoformat() + "Z"
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · BATMAN PAPER TRADE</title><style>{CSS}</style></head><body><div class="wrap">
<div class="top"><div><div class="brand">BATMAN PAPER TRADE · PROSPECTIVE VALIDATION</div><h1>{escape(title)}</h1><div class="sub">{escape(subtitle)}</div></div><div class="small">Generated {escape(now)}</div></div>
{NAV}
{body}
<div class="footer">Paper-only operational layer. No live broker orders are submitted. Prospective statistics include only records explicitly marked <span class="badge ok">prospective_valid=true</span>.</div>
</div></body></html>"""

def _fmt_money(x):
    return f"₹{float(x):,.0f}"

def _signal_rows(signals):
    rows=[]
    for s in reversed(signals[-200:]):
        ev=s.get("mc_ev_points")
        gate=s.get("gate")
        trade=s.get("trade")
        rows.append(
            "<tr>"
            f"<td>{escape(str(s.get('scan_date','')))}</td><td>{escape(str(s.get('observed_timestamp_ist','')))}</td>"
            f"<td>{escape(str(s.get('underlying','')))}</td><td>{escape(str(s.get('expiry','')))}</td>"
            f"<td>{escape(str(s.get('status','')))}</td><td>{'ON' if gate else 'OFF'}</td>"
            f"<td>{escape(f'{float(ev):,.2f}' if isinstance(ev,(int,float)) else '—')}</td>"
            f"<td>{'PAPER' if trade else '—'}</td><td>{escape(str(s.get('reason','')))}</td>"
            "</tr>"
        )
    return "".join(rows) or "<tr><td colspan='9'>No signal records yet.</td></tr>"

def build() -> None:
    d=_load()
    signals=d["signals"]; events=d["events"]; errors=d["errors"]; runs=d["runs"]; positions=d["positions"]
    valid=[s for s in signals if s.get("prospective_valid")]
    trades=[s for s in valid if s.get("trade")]
    marks=[e for e in events if e.get("event_type")=="MARK"]
    closes=[e for e in events if e.get("event_type")=="CLOSE"]
    realised=sum(float(e.get("realized_pnl_rupees_net",0)) for e in closes)
    last_mark=marks[-1].get("pnl_rupees_net_estimate",0) if marks else 0

    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"style.css").write_text(CSS,encoding="utf-8")

    dashboard=f"""
<div class="hero-banner">The strategy is frozen at MC-RQ6-v1: 756 historical returns, 5,000 paths, seed 756, 3-session horizon, P20/P35/P65/P80, +1/-2/+1/-2, gross MC-EV &gt; 0 gate, 09:30 IST target, 2-point-per-leg primary slippage, paper-only execution.</div>
<div class="grid">
<div class="card"><div class="k">All signals</div><div class="v">{len(signals)}</div><div class="small">includes NOT_D3, diagnostics and errors</div></div>
<div class="card"><div class="k">Valid prospective</div><div class="v">{len(valid)}</div><div class="small">included in validation statistics</div></div>
<div class="card"><div class="k">Paper trades</div><div class="v">{len(trades)}</div><div class="small">gate ON + executable four-leg entry</div></div>
<div class="card"><div class="k">Open positions</div><div class="v">{len(positions)}</div><div class="small">live-marked positions</div></div>
</div>
<div class="grid">
<div class="card"><div class="k">Latest net-est. MTM</div><div class="v">{_fmt_money(last_mark)}</div><div class="small">gross MTM less recorded entry-cost estimate</div></div>
<div class="card"><div class="k">Realised net P&amp;L</div><div class="v">{_fmt_money(realised)}</div><div class="small">closed paper positions</div></div>
<div class="card"><div class="k">Live marks</div><div class="v">{len(marks)}</div><div class="small">10-minute event cadence while open</div></div>
<div class="card"><div class="k">Errors logged</div><div class="v">{len(errors)}</div><div class="small">never silently discarded</div></div>
</div>
<div class="card"><h2>Latest signals</h2><div class="table"><table><thead><tr><th>Date</th><th>Observed IST</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Gate</th><th>MC-EV</th><th>Trade</th><th>Reason</th></tr></thead><tbody>{_signal_rows(signals)}</tbody></table></div></div>
<div class="card"><h2>Open paper positions</h2><div class="table"><table><thead><tr><th>Position</th><th>Underlying</th><th>Expiry</th><th>Latest MTM</th><th>Strikes</th></tr></thead><tbody>
{''.join(
f"<tr><td>{escape(pid)}</td><td>{escape(str(p.get('underlying')))}</td><td>{escape(str(p.get('expiry')))}</td><td>{_fmt_money(p.get('last_mark',{}).get('pnl_rupees_net_estimate',0)) if p.get('last_mark') else '—'}</td><td>{escape(str(p.get('strikes',{})))}</td></tr>"
for pid,p in positions.items()
) or "<tr><td colspan='5'>No open paper positions.</td></tr>"}
</tbody></table></div></div>
"""
    (OUT/"index.html").write_text(_layout("Dashboard","Live operational view of the frozen BATMAN prospective validation harness.",dashboard),encoding="utf-8")

    signals_body=f"""<div class="card"><h2>Chronological signal ledger</h2><div class="table"><table><thead><tr><th>Date</th><th>Observed IST</th><th>Underlying</th><th>Expiry</th><th>Status</th><th>Gate</th><th>MC-EV</th><th>Trade</th><th>Reason</th></tr></thead><tbody>{_signal_rows(signals)}</tbody></table></div></div>"""
    (OUT/"signals.html").write_text(_layout("Signals","Every scheduled/manual scan is retained; only prospective_valid=true observations enter validation statistics.",signals_body),encoding="utf-8")

    trade_rows=[]
    for e in reversed(events):
        if e.get("event_type") in ("OPEN","CLOSE"):
            pos=e.get("position",{})
            trade_rows.append(
                f"<tr><td>{escape(str(e.get('timestamp_utc','')))}</td><td>{escape(str(e.get('event_type')))}</td><td>{escape(str(e.get('position_id','')))}</td><td>{escape(str(pos.get('underlying',e.get('underlying',''))))}</td><td>{escape(str(pos.get('expiry',e.get('expiry',''))))}</td><td>{_fmt_money(e.get('realized_pnl_rupees_net',0)) if e.get('event_type')=='CLOSE' else '—'}</td></tr>"
            )
    mark_rows=[]
    for e in reversed(marks[-300:]):
        mark_rows.append(
            f"<tr><td>{escape(str(e.get('timestamp_utc','')))}</td><td>{escape(str(e.get('underlying','')))}</td><td>{escape(str(e.get('expiry','')))}</td><td>{_fmt_money(e.get('pnl_rupees',0))}</td><td>{_fmt_money(e.get('pnl_rupees_net_estimate',0))}</td><td>{escape(str(e.get('data_source','')))}</td></tr>"
        )
    trades_body=f"""<div class="grid">
<div class="card"><div class="k">Open</div><div class="v">{len(positions)}</div></div>
<div class="card"><div class="k">Closed</div><div class="v">{len(closes)}</div></div>
<div class="card"><div class="k">Realised net P&amp;L</div><div class="v">{_fmt_money(realised)}</div></div>
<div class="card"><div class="k">Latest MTM</div><div class="v">{_fmt_money(last_mark)}</div></div>
</div>
<div class="card"><h2>Paper trade lifecycle</h2><div class="table"><table><thead><tr><th>UTC</th><th>Event</th><th>Position</th><th>Underlying</th><th>Expiry</th><th>Realised net</th></tr></thead><tbody>{''.join(trade_rows) or '<tr><td colspan="6">No trade lifecycle events yet.</td></tr>'}</tbody></table></div></div>
<div class="card"><h2>Live MTM marks</h2><div class="table"><table><thead><tr><th>UTC</th><th>Underlying</th><th>Expiry</th><th>Gross MTM</th><th>Net-est. MTM</th><th>Data source</th></tr></thead><tbody>{''.join(mark_rows) or '<tr><td colspan="6">No marks yet.</td></tr>'}</tbody></table></div></div>
"""
    (OUT/"trades.html").write_text(_layout("Trades & MTM","Paper position lifecycle, repeated live marking, costs and expiry results.",trades_body),encoding="utf-8")

    event_rows=[]
    for e in reversed(events[-500:]):
        event_rows.append(
            f"<tr><td>{escape(str(e.get('timestamp_utc','')))}</td><td>{escape(str(e.get('event_type','')))}</td><td>{escape(str(e.get('position_id','')))}</td><td>{escape(str(e.get('underlying','')))}</td><td>{escape(str(e.get('expiry','')))}</td><td>{escape(str(e.get('reason','')))}</td></tr>"
        )
    runs_rows=[]
    for r in reversed(runs[-200:]):
        runs_rows.append(f"<tr><td>{escape(str(r.get('timestamp_utc','')))}</td><td>{escape(str(r.get('mode','')))}</td><td>{escape(str(r.get('status','')))}</td><td>{escape(str(r.get('repository_revision','')))}</td></tr>")
    events_body=f"""<div class="card"><h2>Event ledger</h2><div class="table"><table><thead><tr><th>UTC</th><th>Event</th><th>Position</th><th>Underlying</th><th>Expiry</th><th>Reason</th></tr></thead><tbody>{''.join(event_rows) or '<tr><td colspan="6">No events yet.</td></tr>'}</tbody></table></div></div>
<div class="card"><h2>Workflow run ledger</h2><div class="table"><table><thead><tr><th>UTC</th><th>Mode</th><th>Status</th><th>Revision</th></tr></thead><tbody>{''.join(runs_rows) or '<tr><td colspan="4">No runs yet.</td></tr>'}</tbody></table></div></div>"""
    (OUT/"events.html").write_text(_layout("Events","Append-only event and workflow-run history used to reconstruct the prospective record.",events_body),encoding="utf-8")

    error_rows=[]
    for e in reversed(errors[-300:]):
        error_rows.append(f"<tr><td>{escape(str(e.get('timestamp_utc','')))}</td><td>{escape(str(e.get('mode','')))}</td><td>{escape(str(e.get('underlying','')))}</td><td>{escape(str(e.get('error_type','')))}</td><td>{escape(str(e.get('message','')))}</td></tr>")
    errors_body=f"""<div class="grid"><div class="card"><div class="k">Logged errors</div><div class="v">{len(errors)}</div></div><div class="card"><div class="k">Provider discipline</div><div class="v">Fail closed</div><div class="small">No synthetic live prices</div></div></div>
<div class="card"><h2>Errors</h2><div class="table"><table><thead><tr><th>UTC</th><th>Mode</th><th>Underlying</th><th>Type</th><th>Message</th></tr></thead><tbody>{''.join(error_rows) or '<tr><td colspan="5">No runtime errors recorded.</td></tr>'}</tbody></table></div></div>"""
    (OUT/"errors.html").write_text(_layout("Errors & Runs","Runtime failures, unavailable data and workflow provenance are retained rather than suppressed.",errors_body),encoding="utf-8")

    method_body="""<div class="card"><h2>Frozen control</h2><div class="code">MC-RQ6-v1
Historical window: final 756 finite daily log returns strictly before D3
Paths: 5,000
Seed: 756
Horizon: 3 trading sessions
Quantiles: P20 / P35 / P65 / P80
Portfolio: +1 P35 PE / -2 P20 PE / +1 P65 CE / -2 P80 CE
Gate: gross MC-EV &gt; 0
Signal target: 09:30 IST
Primary slippage: 2 points per execution leg
Exit: expiry settlement
Mode: PAPER ONLY</div></div>
<div class="card"><h2>Prospective acceptance</h2><div class="small">A prospective signal requires attributable expiry/D3, a valid 09:30 operational observation window, a source snapshot, all four tradable strikes, calculable MC-EV and executable paper prices. Manual force_today runs are diagnostics only.</div></div>
<div class="card"><h2>Data sources</h2><div class="small">NIFTY option chain: official NSE public option-chain service. Historical daily index history is cached after retrieval under data/paper/market_cache. SENSEX option-chain validation uses a configured attributable adapter and fails closed when unavailable. Paytm Money brokerage is configurable through PAYTM_MONEY_BROKERAGE_PER_ORDER; no live order API is called.</div></div>"""
    (OUT/"methodology.html").write_text(_layout("Frozen Method","Exact operational rules, data discipline and cost conventions for the paper-validation harness.",method_body),encoding="utf-8")

if __name__ == "__main__":
    build()
