"""Central Paytm Money read-only Python client for MC3/RQ-7."""
from __future__ import annotations
import hashlib, json, os
from typing import Any
from pyPMClient import PMClient

class PaytmMoneyReadOnlyClient:
    """Authenticated client with no order methods exposed."""
    def __init__(self) -> None:
        api_key=os.getenv("PAYTM_MONEY_API_KEY","").strip()
        api_secret=os.getenv("PAYTM_MONEY_API_SECRET","").strip()
        if not api_key or not api_secret:
            raise RuntimeError("PAYTM_MONEY_API_KEY and PAYTM_MONEY_API_SECRET are required")
        self._client=PMClient(
            api_secret=api_secret, api_key=api_key,
            access_token=os.getenv("PAYTM_MONEY_ACCESS_TOKEN") or None,
            public_access_token=os.getenv("PAYTM_MONEY_PUBLIC_ACCESS_TOKEN") or None,
            read_access_token=os.getenv("PAYTM_MONEY_READ_ACCESS_TOKEN") or None,
        )
        request_token=os.getenv("PAYTM_MONEY_REQUEST_TOKEN","").strip()
        if request_token:
            self._client.generate_session(request_token=request_token)
    def user_details(self) -> Any:
        return self._client.get_user_details()
    @staticmethod
    def response_sha256(value: Any) -> str:
        raw=json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()
        return hashlib.sha256(raw).hexdigest()
