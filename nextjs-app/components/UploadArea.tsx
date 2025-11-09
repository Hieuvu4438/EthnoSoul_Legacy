'use client';

import React, { useState, useRef } from 'react';

interface UploadAreaProps {
  onFileSelect: (file: File) => void;
  isProcessing: boolean;
}

export default function UploadArea({ onFileSelect, isProcessing }: UploadAreaProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setIsDragging(true);
    }
  };

  const handleDragOut = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      onFileSelect(file);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      onFileSelect(file);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handlePaste = async (e: React.ClipboardEvent) => {
    const items = e.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        const file = items[i].getAsFile();
        if (file) {
          onFileSelect(file);
        }
      }
    }
  };

  return (
    <div
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onPaste={handlePaste}
      className={`relative border-3 border-dashed rounded-2xl p-16 text-center transition-all ${
        isDragging
          ? 'border-primary bg-primary/10 scale-105'
          : 'border-gray-300 bg-white'
      } ${isProcessing ? 'opacity-50 pointer-events-none' : ''}`}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".jpg,.jpeg,.png,.gif,.jfif,.heic,.pdf"
        onChange={handleFileInput}
        className="hidden"
        disabled={isProcessing}
      />

      <div className="flex flex-col items-center space-y-6">
        <div className="w-24 h-24 gradient-primary rounded-3xl flex items-center justify-center shadow-lg">
          <svg className="w-12 h-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>

        <div>
          <h3 className="text-2xl font-semibold text-gray-800 mb-3">
            Kéo thả tài liệu vào đây
          </h3>
          <p className="text-gray-600 text-base mb-2">
            hoặc nhấn nút bên dưới để chọn file
          </p>
          <p className="text-sm text-gray-500">
            Hỗ trợ: JPG, PNG, PDF, HEIC (Tối đa 10MB)
          </p>
        </div>

        <button
          onClick={handleBrowseClick}
          disabled={isProcessing}
          className="px-10 py-4 gradient-primary text-white font-semibold text-lg rounded-xl hover:opacity-90 transition-all disabled:opacity-50 shadow-lg transform hover:scale-105"
        >
          Chọn tài liệu từ máy
        </button>
      </div>
    </div>
  );
}
