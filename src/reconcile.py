# src/reconcile.py
import pandas as pd, json
from dateutil.parser import parse as parse_dt
from pathlib import Path
import re

NUM_TOLERANCE = 1e-6

def normalize_date(s):
    if s is None: return None
    try:
        return parse_dt(s).date().isoformat()
    except Exception:
        return str(s)

def compare_values(left, right, field):
    # dates normalized
    if left is None and right is None: return ("MATCH", left, right)
    if field.lower().endswith("date") or "date" in field.lower():
        a = normalize_date(left); b = normalize_date(right)
        return ("MATCH" if a==b else "MISMATCH", a, b)
    # numeric
    try:
        la = float(left); ra = float(right)
        return ("MATCH" if abs(la-ra) <= max(1e-6, abs(ra)*1e-6) else "MISMATCH", la, ra)
    except Exception:
        # string compare case-insensitive trimmed
        a = (str(left).strip().lower() if left is not None else None)
        b = (str(right).strip().lower() if right is not None else None)
        return ("MATCH" if a==b else "MISMATCH", left, right)

def reconcile_one(term_fields: dict, booking_df: pd.DataFrame):
    # find bookings matching ISIN
    isin = term_fields.get("ISIN") or term_fields.get("isin")
    # Use pandas str.replace for the DataFrame column, and re.sub for the single value
    isin_clean = re.sub(r'[^A-Za-z0-9]', '', str(isin)).upper()
    matches = booking_df[
        booking_df["ISIN"].str.replace(r'[^A-Za-z0-9]', '', regex=True).str.upper() == isin_clean
    ]
    results=[]
    fields_to_check = ["ISIN","Issuer","Parent","IssueDate","SettlementDate","MaturityDate","CouponRatePercent","CouponFrequency","Currency","IssueAmount","Notional","IssuePricePercent","NominalAmountPerBond","DayCountFraction"]
    if matches.empty:
        results.append({"Field":"ISIN","Status":"MISSING_BOOKING","TermValue":isin,"BookingValue":None})
        return results
    # use first match for field comparisons (or iterate all)
    booking = matches.iloc[0].to_dict()
    for f in fields_to_check:
        status,left,right = compare_values(term_fields.get(f), booking.get(f), f)
        results.append({"Field":f,"Status":status,"TermValue":left,"BookingValue":right})
    return results

if __name__ == "__main__":
    import sys
    from pathlib import Path

    term_json_path = Path(sys.argv[1]).resolve()
    booking_csv_path = Path(sys.argv[2]).resolve()
    out_csv_path = Path(sys.argv[3]).resolve()

    if not term_json_path.exists():
        print(f"ERROR: File not found: {term_json_path}")
        sys.exit(1)
    if not booking_csv_path.exists():
        print(f"ERROR: File not found: {booking_csv_path}")
        sys.exit(1)

    term_json = json.load(open(term_json_path, encoding="utf-8"))
    # Ensure term_json is a list of dicts
    if isinstance(term_json, dict):
        term_json = [term_json]
    elif isinstance(term_json, list):
        pass
    else:
        raise ValueError("Input JSON must be a dict or list of dicts.")

    booking_df = pd.read_csv(booking_csv_path)
    recon_rows = []
    for term_fields in term_json:
        if not isinstance(term_fields, dict):
            print("WARNING: Skipping non-dict entry in term_json:", term_fields)
            continue
        result = reconcile_one(term_fields, booking_df)
        recon_rows.extend(result)

    if recon_rows:
     pd.DataFrame(recon_rows).to_csv(out_csv_path, index=False)
     print("reconciliation saved ->", out_csv_path)
    else:
     print("No reconciliation results found. CSV will be empty.")
     pd.DataFrame(columns=["ISIN", "Field", "TermValue", "BookingValue", "Status"]).to_csv(out_csv_path, index=False)