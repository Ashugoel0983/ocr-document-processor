"use client";

import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

interface JSONViewerProps {
  jsonData: any;
}

const JSONViewer: React.FC<JSONViewerProps> = ({ jsonData }) => {
  const downloadJSON = () => {
    if (!jsonData) return;
    
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { 
      type: 'application/json' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `extraction-result-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!jsonData) {
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
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
                />
              </svg>
            </div>
            <p className="text-muted-foreground">No extraction results</p>
            <p className="text-sm text-muted-foreground">
              Process a document to see structured data extraction results
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Document Type and Classification Summary */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Document Classification</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">Detected Type:</span>
            <Badge variant="default" className="text-sm">
              {jsonData.document_type || 'Unknown'}
            </Badge>
          </div>
          
          {jsonData.keyword_matches && (
            <div className="space-y-2">
              <span className="text-sm font-medium">Keyword Matches:</span>
              <div className="grid grid-cols-1 gap-2">
                {Object.entries(jsonData.keyword_matches).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground">{type}:</span>
                    <Badge variant="outline" className="text-xs">
                      {String(count)} matches
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Structured Data */}
      <Card className="flex-1">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg">Extracted Data</CardTitle>
            <Button 
              onClick={downloadJSON}
              variant="outline"
              size="sm"
            >
              Download JSON
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="bg-muted rounded-lg p-4 max-h-64 overflow-auto">
            <pre className="text-sm whitespace-pre-wrap font-mono">
              {JSON.stringify(jsonData.structured_data || jsonData, null, 2)}
            </pre>
          </div>
        </CardContent>
      </Card>

      {/* Raw JSON View */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Complete Response</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-muted rounded-lg p-4 max-h-48 overflow-auto">
            <pre className="text-xs whitespace-pre-wrap font-mono text-muted-foreground">
              {JSON.stringify(jsonData, null, 2)}
            </pre>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default JSONViewer;
