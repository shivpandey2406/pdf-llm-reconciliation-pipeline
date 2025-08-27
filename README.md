End-to-End PDF → LLM → Reconciliation Workflow
This project provides a full pipeline to process PDF trade documents, extract structured fields using an LLM, reconcile them against bookings, and generate a final summary report. The workflow is automated using a single script (run_end_to_end.sh) but can also be run step by step.


# Project Structure

RECONCILIATION/
│── data/
│   ├── Genel Energy.pdf             # Example input PDF
│   ├── Genel_Energy_Trades.json     # Example bookings JSON
│
│── src/
│   ├── parse_docs.py                # Step A: Parse PDF
│   ├── llm_extract.py               # Step B: Extract fields using LLM
│   ├── ingest_bookings.py           # Step C: Convert bookings JSON → CSV
│   ├── reconcile.py                 # Step D: Reconcile extracted vs bookings
│   ├── generate_report.py           # Step E: Generate Markdown report
│
│── tmp/                             # Stores intermediate + final outputs
│
│── requirements.txt                 # Python dependencies
│── .env                             # API key configuration
│── run_end_to_end.sh                # End-to-end workflow runner
│── README.md                        # Documentation

# Step 1: Environment Setup
Python Version: Python 3.9+ is recommended.
Install Dependencies: Run the following to install dependencies:
pip install -r requirements.txt
Requirements include: pandas, pdfplumber, python-dateutil, python-dotenv, openai, langchain-groq
API Key Setup: Create a .env file in the project root with your credentials:

GROQ_API_KEY="your_groq_api_key_here"

# Step 2: Configuration
- Input Files:
   - PDF document (e.g., data/Genel Energy.pdf)
   - Bookings JSON (e.g., data/Genel_Energy_Trades.json)
- Environment Variables:
   - GROQ_API_KEY (required for LLM extraction)
- Intermediate Outputs (in tmp/):
   - genel_text.json → Parsed text from PDF
   - genel_extracted.json → Fields extracted by LLM
   - genel_bookings.csv → Converted bookings data
   - genel_recon.csv → Reconciliation results
- Final Output:
   - genel_recon.md → Markdown summary report
# Step 3: Running the Workflow
Option A: Run Full Workflow Automatically
bash run_end_to_end.sh
This script executes the following steps sequentially:
Parse PDF → JSON:
python src/parse_docs.py "data/Genel Energy.pdf" tmp/genel_text.json
LLM Extract Fields → JSON:
python src/llm_extract.py tmp/genel_text.json tmp/genel_extracted.json
Convert Bookings JSON → CSV:
python src/ingest_bookings.py data/Genel_Energy_Trades.json tmp/genel_bookings.csv
Reconcile Extracted vs Bookings → CSV:
python src/reconcile.py tmp/genel_extracted.json tmp/genel_bookings.csv tmp/genel_recon.csv
Generate Markdown Report:
python src/generate_report.py tmp/genel_recon.csv tmp/genel_recon.md

# Example Input & Output
Input Files:
- data/Genel Energy.pdf (trade agreement)
- data/Genel_Energy_Trades.json (bookings data)
Final Output (tmp/genel_recon.md):
# Reconciliation Report

  Counterparty matches
  Trade date matches
  Commodity matches
  Quantity matches

**Summary:** All fields matched successfully.

# Summary
This pipeline enables you to:
1. Parse PDF trade documents into structured JSON.
2. Use LLMs to extract relevant fields.
3. Normalize bookings data into CSV format.
4. Reconcile extracted vs booked data.
5. Generate a human-readable summary report.

Run everything with:
bash run_end_to_end.sh
