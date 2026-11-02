"""
rf_testpo — create a test Bringans purchase order in Cin7 for one item.

Default is a dry run: looks the item up and prints the PO payload, creates nothing.

    python rf_testpo.py                     # dry run, TAM87062 x1
    python rf_testpo.py --live              # really creates the PO in Cin7
    python rf_testpo.py --code TAM87062 --qty 2 --live

The PO is real — void it in Cin7 once you're done with it.
"""
import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv
from supabase import create_client

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_ROOT / ".env")

SUPABASE_URL    = os.getenv("SUPABASE_URL")
SUPABASE_KEY    = os.getenv("SUPABASE_KEY")
CIN7_ACCOUNT_ID = os.getenv("CIN7_ACCOUNT_ID")
CIN7_API_KEY    = os.getenv("CIN7_API_KEY")

CIN7_MEMBER_ID = 5226  # Trevor Bringans Ltd
CIN7_PO_URL    = "https://api.cin7.com/api/v1/PurchaseOrders/"


def cin7_headers():
    credentials = base64.b64encode(f"{CIN7_ACCOUNT_ID}:{CIN7_API_KEY}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }


def lookup_item(supabase, code):
    resp = supabase.table("product_summary") \
        .select("code, cost_nzd") \
        .eq("code", code) \
        .execute()
    return resp.data[0] if resp.data else None


def main():
    parser = argparse.ArgumentParser(description="Create a test Bringans PO in Cin7")
    parser.add_argument("--code", default="TAM87062", help="Cin7 product code")
    parser.add_argument("--qty",  type=int, default=1)
    parser.add_argument("--live", action="store_true", help="actually create the PO")
    args = parser.parse_args()

    missing = [k for k, v in {"SUPABASE_URL": SUPABASE_URL, "SUPABASE_KEY": SUPABASE_KEY,
                              "CIN7_ACCOUNT_ID": CIN7_ACCOUNT_ID, "CIN7_API_KEY": CIN7_API_KEY}.items() if not v]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    item = lookup_item(supabase, args.code)
    if not item:
        sys.exit(f"{args.code} not found in product_summary")

    cost = float(item["cost_nzd"] or 0)
    print(f"{args.code} x{args.qty} @ ${cost:.2f}")

    payload = [{
        "memberId":                 CIN7_MEMBER_ID,
        "currencyCode":             "NZD",
        "taxStatus":                "Excl",
        "supplierInvoiceReference": "TEST - rf_testpo",
        "internalComments":         f"TEST PO from rf_testpo {datetime.now():%d/%m/%Y %H:%M} - void me",
        "lineItems": [{"code": args.code, "qty": args.qty, "unitPrice": cost}],
    }]

    if not args.live:
        print("Dry run - PO not created. Payload:")
        print(json.dumps(payload, indent=2))
        return

    resp = httpx.post(CIN7_PO_URL, headers=cin7_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    result = resp.json()
    first = result[0] if isinstance(result, list) else result
    if str(first.get("success", "")).lower() == "true":
        print(f"Cin7 PO created: {first.get('code')} (id {first.get('id')})")
    else:
        sys.exit(f"Cin7 PO failed: {first.get('message') or result}")


if __name__ == "__main__":
    main()
