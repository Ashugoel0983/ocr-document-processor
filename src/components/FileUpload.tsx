"use client";

import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';

interface FileUploadProps {
  onUploadComplete: (data: any, fileUrl: string) => void;
  onError: (error: string) => void;
  onLoadingChange: (loading: boolean) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  onUploadComplete, 
  onError, 
  onLoadingChange 
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const validateFile = (file: File): boolean => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!allowedTypes.includes(file.type)) {
      onError('Unsupported file type. Please upload a PDF, JPEG, or PNG file.');
      return false;
    }

    if (file.size > maxSize) {
      onError('File size too large. Please upload a file smaller than 10MB.');
      return false;
    }

    return true;
  };

  const handleFileChange = (file: File) => {
    if (!validateFile(file)) return;
    setSelectedFile(file);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileChange(file);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileChange(file);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) return;

    onLoadingChange(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8001/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed.');
      }

      const data = await response.json();
      const fileUrl = URL.createObjectURL(selectedFile);
      onUploadComplete(data, fileUrl);
      
    } catch (error: any) {
      onError(error.message || 'An error occurred during upload.');
    } finally {
      onLoadingChange(false);
    }
  };

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div className="space-y-4">
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive 
                ? 'border-primary bg-primary/5' 
                : 'border-muted-foreground/25 hover:border-muted-foreground/50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="space-y-2">
              <p className="text-lg font-medium">
                {selectedFile ? selectedFile.name : 'Drop your document here'}
              </p>
              <p className="text-muted-foreground">
                or click to browse files
              </p>
              <p className="text-sm text-muted-foreground">
                Supports PDF, JPEG, PNG files up to 10MB
              </p>
            </div>
            
            <Input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={handleInputChange}
              className="mt-4 cursor-pointer"
            />
          </div>

          {selectedFile && (
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div>
                <p className="font-medium">{selectedFile.name}</p>
                <p className="text-sm text-muted-foreground">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <Button onClick={uploadFile} className="ml-4">
                Process Document
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FileUpload;
