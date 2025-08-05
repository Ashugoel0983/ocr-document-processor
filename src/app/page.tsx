"use client";

import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import PDFViewer from '../components/PDFViewer';
import JSONViewer from '../components/JSONViewer';

interface DocumentData {
  document_type: string;
  keyword_matches: Record<string, number>;
  structured_data: any;
}

const Page = () => {
  const [documentData, setDocumentData] = useState<DocumentData | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleUploadComplete = (data: DocumentData, fileUrl: string) => {
    setDocumentData(data);
    setPdfUrl(fileUrl);
    setError('');
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setDocumentData(null);
    setPdfUrl('');
  };

  const handleLoadingChange = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  return (
    <div className="min-h-screen flex flex-col p-6 bg-background text-foreground">
      <div className="max-w-7xl mx-auto w-full">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">OCR Document Processor</h1>
          <p className="text-muted-foreground text-lg">
            Upload PDF or image documents for AI-powered text extraction and structured data analysis
          </p>
        </header>

        <FileUpload 
          onUploadComplete={handleUploadComplete} 
          onError={handleError}
          onLoadingChange={handleLoadingChange}
        />

        {error && (
          <div className="mt-4 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-destructive font-medium">Error: {error}</p>
          </div>
        )}

        {loading && (
          <div className="mt-4 p-4 bg-muted rounded-lg">
            <p className="text-muted-foreground">Processing document... This may take a few moments.</p>
          </div>
        )}

        <div className="flex flex-col lg:flex-row mt-8 gap-6">
          <div className="flex-1 border border-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Document Preview</h2>
            <PDFViewer fileUrl={pdfUrl} />
          </div>
          
          <div className="flex-1 border border-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Extraction Results</h2>
            <JSONViewer jsonData={documentData} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Page;
