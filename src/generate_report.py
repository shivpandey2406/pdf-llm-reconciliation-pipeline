import pandas as pd, sys, os
from pandas.errors import EmptyDataError

csv_path = sys.argv[1]
out_md = sys.argv[2]

if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    with open(out_md, "w") as f:
        f.write("# Reconciliation Summary\n\n")
        f.write("No data available in the input CSV file.\n")
    print("wrote", out_md)
    sys.exit(0)

try:
    df = pd.read_csv(csv_path)
except EmptyDataError:
    with open(out_md, "w") as f:
        f.write("# Reconciliation Summary\n\n")
        f.write("No data available in the input CSV file.\n")
    print("wrote", out_md)
    sys.exit(0)

with open(out_md,"w") as f:
    f.write("# Reconciliation Summary\n\n")
    total = len(df)
    mismatches = df[df["Status"]!="MATCH"]
    f.write(f"- Total checks: {total}\n- Mismatches: {len(mismatches)}\n\n")
    if not mismatches.empty:
        f.write("## Mismatch details\n\n")
        for _,r in mismatches.iterrows():
            f.write(f"- ISIN {r['ISIN']}: Field `{r['Field']}` term='{r['TermValue']}' booking='{r['BookingValue']}'\n")
print("wrote", out_md)