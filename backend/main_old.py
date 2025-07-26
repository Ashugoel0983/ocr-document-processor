from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
import json
from pathlib import Path
import utils
import gemini_client

app = FastAPI(title="OCR Document Processor", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for file processing
TEMP_DIR = Path("./temp")
TEMP_DIR.mkdir(exist_ok=True)

# Load document classification config
CONFIG_PATH = Path("./config.json")
try:
    with open(CONFIG_PATH) as f:
        CLASSIFICATION_CONFIG = json.load(f)
except FileNotFoundError:
    # Default configuration if file doesn't exist
    CLASSIFICATION_CONFIG = {
        "Invoice": ["Invoice Number", "Total", "Date", "Due", "Bill", "Amount"],
        "Bank Statement": ["Account Number", "Transaction", "Balance", "Statement", "Bank", "Deposit"],
        "Contract": ["Parties", "Agreement", "Effective Date", "Terms", "Contract", "Party"]
    }

@app.get("/")
async def root():
    return {"message": "OCR Document Processor API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "OCR Document Processor"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a document file (PDF or image) for OCR and structured data extraction.
    
    Returns:
    - document_type: Classified document type based on keyword matching
    - keyword_matches: Count of keywords found for each document type
    - structured_data: AI-extracted structured information based on document type
    """
    
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file.content_type}. Allowed types: PDF, JPEG, PNG"
        )
    
    # Validate file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum allowed size is 10MB."
        )
    
    # Generate unique filename and save temporarily
    file_extension = Path(file.filename or "document").suffix
    filename = f"{uuid.uuid4()}{file_extension}"
    file_location = TEMP_DIR / filename
    
    try:
        # Save uploaded file
        with open(file_location, "wb") as f_out:
            shutil.copyfileobj(file.file, f_out)
        
        # Process OCR to extract text
        try:
            ocr_text = utils.process_ocr(str(file_location))
            if not ocr_text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="OCR processing failed: No text could be extracted from the document."
                )
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"OCR processing failed: {str(e)}"
            )
        
        # Classify document based on keywords
        try:
            classification = utils.classify_document(ocr_text, CLASSIFICATION_CONFIG)
            doc_type = classification.get("document_type", "Unknown")
            keyword_counts = classification.get("keyword_counts", {})
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Document classification failed: {str(e)}"
            )
        
        # Extract structured data using Gemini API
        try:
            structured_data = await gemini_client.extract_structured_data(doc_type, ocr_text)
        except Exception as e:
            # If Gemini API fails, return basic extraction with error note
            structured_data = {
                "error": f"AI extraction failed: {str(e)}",
                "raw_text_preview": ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text
            }
        
        # Prepare response
        result = {
            "document_type": doc_type,
            "keyword_matches": keyword_counts,
            "structured_data": structured_data,
            "processing_info": {
                "file_name": file.filename,
                "file_size": file.size,
                "text_length": len(ocr_text)
            }
        }
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if file_location.exists():
            try:
                file_location.unlink()
            except Exception:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
