import os, json
from langchain_groq import ChatGroq
from typing import Dict
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or GROQ_API_KEY.strip() == "":
    print("ERROR: GROQ_API_KEY not found or empty. Check your .env file or environment variables.")
    exit(1)

PROMPT_TEMPLATE = """
You are given a bond term-sheet text. Extract the following fields as JSON:
ISIN, Issuer, Parent, IssueDate (YYYY-MM-DD if present), SettlementDate,
MaturityDate, CouponRatePercent, CouponFrequency, Currency, IssueAmount, Notional,
IssuePricePercent, NominalAmountPerBond, DayCountFraction, BusinessDayConvention,
BusinessDayLocation, InterestPaymentDates (first if present), MinimumSubscription

Return ONLY valid JSON with these keys. Use null if value not found.
Input text:
\"\"\"{document_text}\"\"\"
"""

MAX_CHARS = 16000  # ~8000 tokens, adjust as needed

def call_groq_extract(document_text: str) -> Dict:
    if len(document_text) > MAX_CHARS:
        print(f"WARNING: Input text too long ({len(document_text)} chars), truncating to {MAX_CHARS} chars.")
        document_text = document_text[:MAX_CHARS]
    prompt = PROMPT_TEMPLATE.format(document_text=document_text)
    chat = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )
    try:
        resp = chat.invoke(prompt)
        content = resp.content if hasattr(resp, "content") else str(resp)
        try:
            return json.loads(content)
        except Exception:
            import re
            m = re.search(r"(\{.*\})", content, re.S)
            if m:
                return json.loads(m.group(1))
            raise
    except Exception as e:
        print("Groq API call failed:", e)
        exit(2)

if __name__ == "__main__":
    import sys
    docfile = sys.argv[1]
    outjson = sys.argv[2]
    doc = json.load(open(docfile, encoding="utf-8"))
    extracted = call_groq_extract(doc["text"])
    json.dump(extracted, open(outjson, "w", encoding="utf-8"), indent=2)
    print("extracted ->", outjson)