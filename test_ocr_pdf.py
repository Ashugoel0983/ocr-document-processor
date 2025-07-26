import sys
sys.path.insert(0, './backend')

from utils_fixed import process_ocr

pdf_path = "105.pdf"

try:
    text = process_ocr(pdf_path)
    print(f"Extracted text from PDF ({pdf_path}):\\n{text[:500]}...")
except Exception as e:
    print(f"Failed to extract text from PDF: {e}")
