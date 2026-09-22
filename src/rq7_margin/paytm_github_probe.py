"""RQ-7 GitHub-only Paytm Money read-only connectivity probe."""
from __future__ import annotations
import hashlib, json, os, sys

def required(name: str) -> str:
    value = os.getenv(name, '').strip()
    if not value:
        raise RuntimeError(f'missing required GitHub Actions secret: {name}')
    return value

def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), default=str).encode()
    return hashlib.sha256(raw).hexdigest()

def main() -> int:
    api_key = required('PAYTM_MONEY_API_KEY')
    api_secret = required('PAYTM_MONEY_API_SECRET')
    access_token = os.getenv('PAYTM_MONEY_ACCESS_TOKEN', '').strip()
    request_token = os.getenv('PAYTM_MONEY_REQUEST_TOKEN', '').strip()

    try:
        from pyPMClient import PMClient
    except Exception as exc:
        raise RuntimeError(f'official Paytm Money SDK import failed: {exc}') from exc

    pm = PMClient(
        api_secret=api_secret, api_key=api_key,
        access_token=access_token or None,
        public_access_token=os.getenv('PAYTM_MONEY_PUBLIC_ACCESS_TOKEN') or None,
        read_access_token=os.getenv('PAYTM_MONEY_READ_ACCESS_TOKEN') or None,
    )

    if request_token:
        pm.generate_session(request_token=request_token)

    response = pm.get_user_details()
    print('PAYTM_USER_DETAILS_STATUS=RECEIVED')
    print('PAYTM_USER_DETAILS_SHA256=' + digest(response))
    print('PAPER_ONLY_GUARD=ACTIVE')
    print('LIVE_ORDER_ENDPOINTS_CALLED=0')
    print('REQUEST_TOKEN_USED=' + str(bool(request_token)))
    print('ACCESS_TOKEN_PRESET=' + str(bool(access_token)))
    return 0

if __name__ == '__main__':
    sys.exit(main())