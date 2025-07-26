# OCR Document Processor

A full-stack application for processing documents with OCR (Optical Character Recognition) and AI-powered structured data extraction. The application uses React/Next.js for the frontend, FastAPI for the backend, Tesseract for OCR processing, and Google Gemini AI for intelligent data extraction.

## Features

- **Document Upload**: Support for PDF and image files (JPEG, PNG)
- **OCR Processing**: Extract text from documents using Tesseract OCR
- **Document Classification**: Automatically classify documents as Invoice, Bank Statement, Contract, or Unknown
- **AI-Powered Extraction**: Use Google Gemini AI to extract structured data based on document type
- **Two-Pane Interface**: 
  - Left pane: Document preview
  - Right pane: Structured JSON results with download capability
- **Modern UI**: Clean, responsive design using Tailwind CSS and shadcn/ui components

## Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend      │ ◄──────────────► │   Backend       │
│   (Next.js)     │                 │   (FastAPI)     │
│                 │                 │                 │
│ • File Upload   │                 │ • OCR Processing│
│ • PDF Viewer    │                 │ • Classification│
│ • JSON Display  │                 │ • AI Extraction │
└─────────────────┘                 └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   External APIs │
                                    │                 │
                                    │ • Tesseract OCR │
                                    │ • Google Gemini │
                                    └─────────────────┘
```

## Prerequisites

### System Requirements
- Node.js 18+ and npm
- Python 3.8+
- Tesseract OCR

### Installing Tesseract OCR

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

#### macOS:
```bash
brew install tesseract
```

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Verify installation: `tesseract --version`

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ocr-document-processor
```

### 2. Frontend Setup
```bash
# Install frontend dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:8000`

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

The backend API will be available at `http://localhost:8001`

## Configuration

### Google Gemini AI Setup
The application uses Google Gemini AI for structured data extraction. The service account credentials are already configured in the code, but you can update them in `backend/gemini_client.py` if needed.

### Document Classification
Document types and their keywords can be customized in `backend/config.json`:

```json
{
  "Invoice": ["Invoice Number", "Total", "Date", "Due", ...],
  "Bank Statement": ["Account Number", "Transaction", "Balance", ...],
  "Contract": ["Parties", "Agreement", "Effective Date", ...]
}
```

## Usage

1. **Start both servers**:
   - Frontend: `npm run dev` (port 8000)
   - Backend: `python backend/main.py` (port 8001)

2. **Upload a document**:
   - Drag and drop or click to select a PDF or image file
   - Click "Process Document"

3. **View results**:
   - Left pane: Document preview
   - Right pane: Classification results and structured data
   - Download JSON results using the download button

## API Endpoints

### Backend API (http://localhost:8001)

#### `POST /upload`
Upload and process a document file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or image)

**Response:**
```json
{
  "document_type": "Invoice",
  "keyword_matches": {
    "Invoice": 5,
    "Bank Statement": 0,
    "Contract": 1
  },
  "structured_data": {
    "extracted_data": {
      "invoice_number": "INV-2024-001",
      "total_amount": "$1,250.00",
      "due_date": "2024-02-15"
    },
    "confidence": "high"
  },
  "processing_info": {
    "file_name": "invoice.pdf",
    "file_size": 245760,
    "text_length": 1024
  }
}
```

#### `GET /health`
Health check endpoint.

#### `GET /`
API status and information.

## Project Structure

```
ocr-document-processor/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Main application page
│   │   └── globals.css         # Global styles
│   └── components/
│       ├── FileUpload.tsx      # File upload component
│       ├── PDFViewer.tsx       # Document preview component
│       ├── JSONViewer.tsx      # Results display component
│       └── ui/                 # shadcn/ui components
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── utils.py                # OCR and classification utilities
│   ├── gemini_client.py        # Google Gemini AI integration
│   ├── config.json             # Document classification config
│   ├── requirements.txt        # Python dependencies
│   └── temp/                   # Temporary file storage
├── package.json                # Node.js dependencies
└── README.md                   # This file
```

## Supported Document Types

### Invoice
**Extracted Fields:**
- Invoice number, date, due date
- Total amount, subtotal, tax amount
- Vendor and customer information
- Line items

### Bank Statement
**Extracted Fields:**
- Account number and holder name
- Statement period and balances
- Transaction details
- Bank information

### Contract
**Extracted Fields:**
- Contract title and parties
- Effective and expiration dates
- Key terms and conditions
- Signatures and governing law

### Unknown Documents
**Extracted Fields:**
- General document information
- Key dates and amounts
- Mentioned parties or entities

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types or sizes
- OCR processing failures
- AI API errors
- Network connectivity issues
- File system errors

## Development

### Frontend Development
```bash
