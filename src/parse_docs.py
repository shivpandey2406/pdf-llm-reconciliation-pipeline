# src/parse_docs.py
import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    from os.path import exists
    if not exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

if __name__ == "__main__":
    import sys, json
    # Join all arguments except the last one for the PDF path
    if len(sys.argv) < 3:
        print("Usage: python src/parse_docs.py <pdf_path> <output_json>")
        sys.exit(1)
    pdf = " ".join(sys.argv[1:-1])
    out = sys.argv[-1]  # output json file path to store document text
    doc_text = extract_text_from_pdf(pdf)
    # Ensure output directory exists
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps({"filename": pdf, "text": doc_text}, indent=2))
    print("wrote", out)
