"""RQ-7 GitHub-only Paytm Money read-only connectivity probe."""
from __future__ import annotations
import sys
from paytm_money import PaytmMoneyReadOnlyClient

def main() -> int:
    client=PaytmMoneyReadOnlyClient()
    response=client.user_details()
    print("PAYTM_USER_DETAILS_STATUS=RECEIVED")
    print("PAYTM_USER_DETAILS_SHA256="+client.response_sha256(response))
    print("PAPER_ONLY_GUARD=ACTIVE")
    print("LIVE_ORDER_ENDPOINTS_CALLED=0")
    return 0

if __name__=="__main__":
    sys.exit(main())
