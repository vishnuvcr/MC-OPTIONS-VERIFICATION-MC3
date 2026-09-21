from __future__ import annotations

import argparse

from .engine import scan, mark
from .site import build


def main() -> None:
    p=argparse.ArgumentParser(prog="batman-paper-trade")
    sub=p.add_subparsers(dest="cmd",required=True)
    for name in ("scan","mark"):
        s=sub.add_parser(name)
        s.add_argument("--underlying",choices=["NIFTY","SENSEX","BOTH"],default="BOTH")
        if name=="scan":
            s.add_argument("--force-today",action="store_true")
    sub.add_parser("site")
    a=p.parse_args()
    if a.cmd=="scan":
        scan(a.underlying,a.force_today)
    elif a.cmd=="mark":
        mark(a.underlying)
    else:
        build()


if __name__=="__main__":
    main()
