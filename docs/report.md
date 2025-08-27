Title: LLM-powered Term-Sheet Reconciliation — Implementation Summary
Author: [Shiv Pandey]
Date: [date]

Objective
Automate reconciliation between unstructured bond term-sheets and structured booking extracts by using Python for parsing, an LLM for field extraction, and programmatic comparison logic to produce actionable reconciliation outputs.

Architecture & Workflow
1. PDF/Text extraction — pdfplumber to convert term sheet PDFs to raw text (script: src/parse_docs.py).
2. LLM extraction — programmatically submit raw text to an LLM via API (src/llm_extract.py). Output: canonical JSON fields (ISIN, Coupon, Maturity, IssueAmount, IssuePrice, etc.).
3. Booking ingest — parse CSV/JSON booking extracts with pandas (src/ingest_bookings.py).
4. Reconciliation engine — compare LLM-extracted fields to booking records (match by ISIN). Rules:
   - Dates: normalized to ISO format; exact match required by default.
   - Numeric: absolute/relative tolerance (configurable); mismatch flagged if outside tolerance.
   - Strings: case-insensitive trimmed equality.
5. Outputs — reconciliation table CSV, Markdown summary, and optional HTML.

LLM/API integration
- The project is written to be agnostic to provider. Example integration uses OpenAI API (openai Python package).
- The prompt asks the model to output ONLY JSON with specific keys to keep parsing robust.
- Alternative: use Hugging Face inference endpoint or Cohere if preferred (swap the client in src/llm_extract.py).

Field extraction design & mapping
- Canonical fields: ISIN, Issuer, Parent, IssueDate, SettlementDate, MaturityDate, CouponRatePercent, CouponFrequency, Currency, Notional/IssueAmount, IssuePricePercent, NominalAmountPerBond, DayCountFraction, BusinessDayConvention, InterestPaymentDates, MinimumSubscription.
- Booking fields are normalized to the same names before comparing (bookings with different field names are mapped via utils).

Assumptions & Challenges
- Term sheets are human-written and may have inconsistent phrasing; LLM helps convert variations to canonical fields.
- Accuracy depends on LLM prompt and quality of extracted text; noisy OCR increases errors — high-quality PDF text extraction (or OCR pre-step) recommended for scanned PDFs.
- Tolerances: dates are strict by default; numeric comparisons use configurable tolerances in src/utils.py.

Reproducibility & Testing
- All sample term-sheets and booking extracts included in sample_data/ (Genel and IDBI files). Run the example commands in README to reproduce.
- Unit tests (optional) can be added to assert extraction outputs and reconciliation against known mismatches.

Production suggestions
- Deploy LLM calls behind rate-limiter and robust retry/backoff.
- Add structured logging, monitoring, and CI tests (GitHub Actions) to validate end-to-end on PRs.
- Containerize (Dockerfile) and provide an infra/helm chart for k8s deployment if needed.

Contact
For questions or to request a feature (e.g., fuzzy matching, auto-triage rules), contact: [your email]
