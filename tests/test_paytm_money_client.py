import ast
from pathlib import Path

def test_paytm_client_has_no_order_methods():
    tree=ast.parse(Path("src/paytm_money/client.py").read_text())
    names={n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    forbidden={"place_order","modify_order","cancel_order","place_order_v2","modify_order_v2","cancel_order_v2"}
    assert names.isdisjoint(forbidden)
