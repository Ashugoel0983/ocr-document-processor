import pytesseract
from PIL import Image
import pdf2image
import os
import logging
from typing import Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_ocr_on_image(image: Image.Image, source_info: str = "") -> str:
    """
    Process OCR on a PIL Image with multiple fallback methods.
    
    Args:
        image: PIL Image object
        source_info: Information about the source (for logging)
        
    Returns:
        Extracted text as string
    """
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Try multiple OCR configurations
    configs = [
        ('--oem 3 --psm 3', 'PSM 3 (automatic page segmentation)'),
        ('--oem 3 --psm 6', 'PSM 6 (single uniform block)'),
        ('--oem 3 --psm 1', 'PSM 1 (automatic with OSD)'),
        ('', 'basic (no specific config)')
    ]
    
    for config, description in configs:
        try:
            if config:
                text = pytesseract.image_to_string(image, config=config)
            else:
                text = pytesseract.image_to_string(image)
            
            logger.info(f"OCR attempt with {description} {source_info}: '{repr(text[:100])}' (length: {len(text)})")
            
            # If we got meaningful text, return it
            if text.strip() and len(text.strip()) > 2:
                logger.info(f"Successfully extracted text with {description}")
                return text.strip()
                
        except Exception as e:
            logger.warning(f"OCR attempt with {description} failed: {str(e)}")
            continue
    
    # If all methods failed, return empty string
    logger.warning(f"All OCR methods failed for {source_info}")
    return ""

def process_ocr(file_path: str) -> str:
    """
    Extract text from PDF or image file using Tesseract OCR.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Extracted text as string
        
    Raises:
        Exception: If OCR processing fails
    """
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    
    text = ""
    file_path_lower = file_path.lower()
    
    try:
        if file_path_lower.endswith(".pdf"):
            logger.info(f"Processing PDF file: {file_path}")
            # Convert PDF pages to images and extract text
            try:
                pages = pdf2image.convert_from_path(
                    file_path,
                    dpi=300,  # Higher DPI for better OCR accuracy
                    first_page=1,
                    last_page=5  # Limit to first 5 pages for performance
                )
                
                if not pages:
                    raise Exception("No pages found in PDF")
                
                logger.info(f"Successfully converted PDF to {len(pages)} page(s)")
                
                for i, page in enumerate(pages):
                    logger.info(f"Processing page {i+1}/{len(pages)}")
                    
                    # Use the improved OCR processing
                    page_text = process_ocr_on_image(page, f"from PDF page {i+1}")
                    
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n{page_text}"
                    else:
                        logger.warning(f"No text extracted from page {i+1}")
                    
            except Exception as e:
                raise Exception(f"PDF processing failed: {str(e)}")
                
        elif file_path_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            logger.info(f"Processing image file: {file_path}")
            try:
                # Open and process image
                image = Image.open(file_path)
                logger.info(f"Image loaded: mode={image.mode}, size={image.size}")
                
                # Use the improved OCR processing
                text = process_ocr_on_image(image, f"from image file")
                
            except Exception as e:
                raise Exception(f"Image processing failed: {str(e)}")
        else:
            raise Exception(f"Unsupported file format: {file_path}")
        
        # Clean up extracted text
        text = text.strip()
        if not text or len(text) < 3:
            raise Exception("No meaningful text could be extracted from the document")
            
        logger.info(f"Successfully extracted {len(text)} characters of text")
        return text
        
    except Exception as e:
        logger.error(f"OCR processing failed for {file_path}: {str(e)}")
        raise

def classify_document(text: str, config: Dict[str, list]) -> Dict[str, Any]:
    """
    Classify document type based on keyword matching.
    
    Args:
        text: Extracted text from OCR
        config: Dictionary mapping document types to keyword lists
        
    Returns:
        Dictionary containing document_type and keyword_counts
    """
    if not text or not text.strip():
        return {
            "document_type": "Unknown",
            "keyword_counts": {},
            "confidence": 0.0
        }
    
    text_lower = text.lower()
    keyword_counts = {}
    total_keywords = 0
    
    # Count keyword occurrences for each document type
    for doc_type, keywords in config.items():
        count = 0
        matched_keywords = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            keyword_count = text_lower.count(keyword_lower)
            count += keyword_count
            total_keywords += len(keywords)
            
            if keyword_count > 0:
                matched_keywords.append(keyword)
        
        keyword_counts[doc_type] = {
            "count": count,
            "matched_keywords": matched_keywords,
            "total_possible": len(keywords)
        }
    
    # Determine document type with highest keyword count
    if not keyword_counts:
        document_type = "Unknown"
        confidence = 0.0
    else:
        # Find the document type with the highest count
        best_match = max(keyword_counts.items(), key=lambda x: x[1]["count"])
        document_type = best_match[0]
        best_count = best_match[1]["count"]
        
        # Calculate confidence based on keyword matches
        if total_keywords > 0:
            confidence = min(best_count / max(1, len(config[document_type])), 1.0)
        else:
            confidence = 0.0
        
        # If no keywords found, classify as Unknown
        if best_count == 0:
            document_type = "Unknown"
    
    logger.info(f"Document classified as: {document_type} (confidence: {confidence:.2f})")
    
    return {
        "document_type": document_type,
        "keyword_counts": {k: v["count"] for k, v in keyword_counts.items()},
        "detailed_matches": keyword_counts,
        "confidence": confidence
    }

def validate_tesseract_installation():
    """
    Validate that Tesseract is properly installed and accessible.
    
    Returns:
        bool: True if Tesseract is available, False otherwise
    """
    try:
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.error(f"Tesseract not found or not properly installed: {str(e)}")
        return False

def validate_pdf2image_installation():
    """
    Validate that pdf2image and poppler are properly installed.
    
    Returns:
        bool: True if pdf2image is available, False otherwise
    """
    try:
        # Try to import pdf2image
        import pdf2image
        logger.info("pdf2image is available")
        return True
    except ImportError as e:
        logger.error(f"pdf2image not found: {str(e)}")
        return False

# Validate installations on module import
if not validate_tesseract_installation():
    logger.warning("Tesseract OCR is not properly installed. OCR functionality may not work.")

if not validate_pdf2image_installation():
    logger.warning("pdf2image is not properly installed. PDF processing may not work.")
