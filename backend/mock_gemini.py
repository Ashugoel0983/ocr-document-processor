import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Mock extraction field mappings for different document types
MOCK_EXTRACTION_RESULTS = {
    "Invoice": {
        "extracted_data": {
            "invoice_number": "INV-2024-001",
            "invoice_date": "2024-01-15",
            "due_date": "2024-02-15",
            "total_amount": "$1,350.00",
            "subtotal": "$1,250.00",
            "tax_amount": "$100.00",
            "vendor_name": "ABC Company",
            "customer_name": "John Smith"
        },
        "confidence": "high",
        "notes": "Mock extraction - successfully identified invoice fields"
    },
    "Bank Statement": {
        "extracted_data": {
            "account_number": "****1234",
            "account_holder_name": "John Smith",
            "statement_period": "January 2024",
            "opening_balance": "$2,500.00",
            "closing_balance": "$3,200.00",
            "bank_name": "Sample Bank"
        },
        "confidence": "high",
        "notes": "Mock extraction - successfully identified bank statement fields"
    },
    "Contract": {
        "extracted_data": {
            "contract_title": "Service Agreement",
            "parties_involved": ["ABC Company", "John Smith"],
            "effective_date": "2024-01-15",
            "contract_value": "$5,000.00",
            "key_terms": "Monthly service agreement"
        },
        "confidence": "high",
        "notes": "Mock extraction - successfully identified contract fields"
    },
    "Unknown": {
        "extracted_data": {
            "document_title": "Unknown Document",
            "key_information": "Unable to classify document type",
            "text_preview": "Document content preview..."
        },
        "confidence": "low",
        "notes": "Mock extraction - document type could not be determined"
    }
}

async def extract_structured_data(doc_type: str, ocr_text: str) -> Dict[str, Any]:
    """
    Mock structured data extraction that returns predefined results based on document type.
    
    Args:
        doc_type: Type of document (Invoice, Bank Statement, Contract, etc.)
        ocr_text: Raw text extracted from OCR
        
    Returns:
        Dictionary containing mock structured data
    """
    try:
        logger.info(f"Mock extraction for document type: {doc_type}")
        
        # Get mock result based on document type
        mock_result = MOCK_EXTRACTION_RESULTS.get(doc_type, MOCK_EXTRACTION_RESULTS["Unknown"])
        
        # Add some dynamic content based on OCR text
        if "invoice" in ocr_text.lower():
            # Try to extract invoice number from OCR text
            lines = ocr_text.split('\n')
            for line in lines:
                if 'invoice number' in line.lower() or 'inv-' in line.lower():
                    # Extract potential invoice number
                    parts = line.split()
                    for part in parts:
                        if 'INV-' in part.upper():
                            mock_result["extracted_data"]["invoice_number"] = part
                            break
        
        # Add OCR text preview to the result
        mock_result["extracted_data"]["ocr_text_preview"] = ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text
        
        logger.info(f"Mock extraction completed for {doc_type}")
        return mock_result
        
    except Exception as e:
        logger.error(f"Mock extraction failed: {str(e)}")
        return {
            "extracted_data": {
                "error": f"Mock extraction failed: {str(e)}",
                "document_type": doc_type,
                "text_preview": ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text
            },
            "confidence": "low",
            "notes": "Mock extraction failed, returning raw text preview"
        }
