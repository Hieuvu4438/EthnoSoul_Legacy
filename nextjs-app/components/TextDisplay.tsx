'use client';

import React from 'react';

interface TextDisplayProps {
  text: string;
  filename: string;
}

export default function TextDisplay({ text, filename }: TextDisplayProps) {
  const handleDownload = () => {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename.replace(/\.[^/.]+$/, '')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mt-12 space-y-6">
      <div className="bg-gradient-to-r from-primary to-secondary rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
              <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white">Chuyển đổi thành công!</h3>
              <p className="text-white/90 text-sm mt-1">{filename}</p>
            </div>
          </div>
          
          <button
            onClick={handleDownload}
            className="flex items-center space-x-2 px-6 py-3 bg-white text-primary font-semibold rounded-xl hover:shadow-xl transition-all"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>Tải xuống .txt</span>
          </button>
        </div>
      </div>

      <div className="bg-white border-2 border-gray-200 rounded-2xl p-8 shadow-lg">
        <div className="flex items-center gap-3 mb-5 pb-4 border-b-2 border-gray-100">
          <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="font-semibold text-gray-800 text-lg">Nội dung văn bản</span>
        </div>
        <div className="max-h-[500px] overflow-y-auto">
          <pre className="whitespace-pre-wrap font-sans text-gray-800 text-base leading-relaxed">
            {text}
          </pre>
        </div>
      </div>

      <div className="flex justify-center gap-4">
        <button 
          onClick={() => navigator.clipboard.writeText(text)}
          className="px-6 py-3 bg-light border-2 border-primary text-primary font-medium rounded-xl hover:bg-primary hover:text-white transition-all"
        >
          Sao chép văn bản
        </button>
      </div>
    </div>
  );
}
