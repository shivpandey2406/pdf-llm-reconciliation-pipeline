# A: parse PDFs
python src/parse_docs.py "data/Genel Energy.pdf" tmp/genel_text.json

# B: call LLM to extract fields (uses the parsed text as input)
python src/llm_extract.py tmp/genel_text.json tmp/genel_extracted.json

# C: convert booking json to csv
python src/ingest_bookings.py data/Genel_Energy_Trades.json tmp/genel_bookings.csv

# D: reconcile
python src/reconcile.py tmp/genel_extracted.json tmp/genel_bookings.csv tmp/genel_recon.csv

# E: summary report
python src/generate_report.py tmp/genel_recon.csv tmp/genel_recon.md



