# src/ingest_bookings.py
import json, pandas as pd
from pathlib import Path

def load_bookings(path):
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if p.suffix.lower() == ".json":
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            return pd.json_normalize(data["trades"])
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {p}:\n{e}")
            raise
    elif p.suffix.lower() in [".csv"]:
        return pd.read_csv(p)
    else:
        raise ValueError("unsupported format")
    
if __name__=="__main__":
    import sys
    df = load_bookings(sys.argv[1])
    df.to_csv(sys.argv[2], index=False)
    print("wrote", sys.argv[2])
