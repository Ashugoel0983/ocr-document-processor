"use client";

import React from 'react';
import { Card, CardContent } from './ui/card';

interface PDFViewerProps {
  fileUrl: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ fileUrl }) => {
  if (!fileUrl) {
    return (
      <Card className="h-96 flex items-center justify-center">
        <CardContent className="text-center">
          <div className="space-y-2">
            <div className="w-16 h-16 mx-auto bg-muted rounded-lg flex items-center justify-center">
              <svg 
                className="w-8 h-8 text-muted-foreground" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                />
              </svg>
            </div>
            <p className="text-muted-foreground">No document selected</p>
            <p className="text-sm text-muted-foreground">
              Upload a PDF or image file to preview it here
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const isPDF = fileUrl.toLowerCase().includes('.pdf') || fileUrl.startsWith('blob:') && fileUrl.includes('pdf');
  const isImage = /\.(jpg|jpeg|png|gif|webp)$/i.test(fileUrl) || fileUrl.startsWith('blob:');

  return (
    <Card className="h-96 overflow-hidden">
      <CardContent className="p-0 h-full">
        <div className="h-full overflow-auto">
          {isPDF ? (
            <div className="h-full">
              <object 
                data={fileUrl} 
                type="application/pdf" 
                width="100%" 
                height="100%"
                className="min-h-full"
              >
                <div className="flex items-center justify-center h-full p-4">
                  <div className="text-center space-y-2">
                    <p className="text-muted-foreground">PDF preview not available in this browser</p>
                    <a 
                      href={fileUrl} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      Open PDF in new tab
                    </a>
                  </div>
                </div>
              </object>
            </div>
          ) : isImage ? (
            <div className="flex items-center justify-center h-full p-4">
              <img 
                src={fileUrl} 
                alt="Document preview" 
                className="max-w-full max-h-full object-contain rounded"
              />
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center space-y-2">
                <p className="text-muted-foreground">Preview not available</p>
                <p className="text-sm text-muted-foreground">
                  Unsupported file format for preview
                </p>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default PDFViewer;
