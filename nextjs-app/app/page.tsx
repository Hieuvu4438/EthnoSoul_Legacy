'use client';

import { useState } from 'react';
import UploadArea from '@/components/UploadArea';
import TextDisplay from '@/components/TextDisplay';
import './globals.css';

export default function Home() {
  const [extractedText, setExtractedText] = useState<string>('');
  const [filename, setFilename] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string>('');

  const handleFileSelect = async (file: File) => {
    setIsProcessing(true);
    setError('');
    setExtractedText('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/ocr', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to process file');
      }

      setExtractedText(data.text);
      setFilename(file.name);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-light/95 backdrop-blur-sm shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-primary">EthnoSoul Legacy</h1>
            <div className="hidden md:flex space-x-8">
              <a href="#home" className="text-gray-600 hover:text-primary transition-colors font-medium">Trang chủ</a>
              <a href="#features" className="text-gray-600 hover:text-primary transition-colors font-medium">Khám phá</a>
              <a href="#ocr" className="text-gray-600 hover:text-primary transition-colors font-medium">Khóa học</a>
              <a href="#ocr" className="text-gray-600 hover:text-primary transition-colors font-medium">Từ điển</a>
              <a href="#ocr" className="text-gray-600 hover:text-primary transition-colors font-medium">Thư viện</a>
            </div>
            <div className="flex items-center space-x-3">
              <button className="px-4 py-2 text-gray-700 hover:text-primary transition-colors font-medium">
                Đăng nhập
              </button>
              <button className="px-5 py-2 gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity font-medium shadow-md">
                Đăng kí
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="relative h-screen flex items-center justify-center pt-16">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: 'url(https://consosukien.vn/pic/News/xoa-mu-chu-cho-tre-em-dan-toc-thieu-so-va-mien-nui-1.jpg)',
          }}
        >
          <div className="absolute inset-0 hero-overlay"></div>
        </div>

        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Bảo Tồn Chữ Viết<br />Lưu Giữ Di Sản
          </h2>
          <p className="text-xl md:text-2xl text-white/95 mb-10 font-light">
            Số hóa tài liệu - Gìn giữ từng dòng chữ quý giá của dân tộc cho thế hệ mai sau
          </p>
          <a 
            href="#ocr"
            className="inline-block bg-white text-primary font-semibold px-10 py-4 rounded-full hover:shadow-2xl transition-all transform hover:scale-105 text-lg"
          >
            Bắt đầu ngay →
          </a>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-gradient-to-b from-white to-light">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <span className="text-primary font-semibold text-sm uppercase tracking-wider">Tính năng</span>
            <h3 className="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-5">
              Công nghệ bảo tồn di sản văn hóa
            </h3>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Ứng dụng trí tuệ nhân tạo để số hóa, lưu giữ và lan tòa những giá trị tri thức dân tộc
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
            {/* Feature 1 */}
            <div className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2">
              <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4">
                Nhận dạng chính xác
              </h4>
              <p className="text-gray-600 leading-relaxed">
                Công nghệ AI thông minh nhận diện và chuyển đổi chữ viết cổ, tài liệu phai mờ thành văn bản số với độ chính xác cao
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2">
              <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4">
                Bảo tồn di sản
              </h4>
              <p className="text-gray-600 leading-relaxed">
                Số hóa nhanh chóng sách cũ, tài liệu lịch sử, giúp bảo tồn tri thức cho thế hệ tương lai
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2">
              <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4">
                Dễ dàng chia sẻ
              </h4>
              <p className="text-gray-600 leading-relaxed">
                Chuyển đổi thành văn bản điện tử, dễ dàng lưu trữ, tìm kiếm và chia sẻ kiến thức đến mọi người
              </p>
            </div>
          </div>

          {/* Additional Feature with Image */}
          <div className="mt-20 bg-white rounded-3xl shadow-2xl overflow-hidden">
            <div className="grid md:grid-cols-2 gap-0">
              <div className="p-12 flex flex-col justify-center">
                <span className="text-primary font-semibold text-sm uppercase tracking-wider mb-3">Sứ mệnh</span>
                <h4 className="text-3xl font-bold text-gray-900 mb-6">
                  Gìn giữ di sản văn hóa dân tộc
                </h4>
                <ul className="space-y-4">
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-700">Số hóa sách giáo khoa, tài liệu học tập cho học sinh vùng cao</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-700">Bảo tồn tài liệu lịch sử, văn hóa dân tộc thiểu số</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-6 h-6 text-primary mr-3 flex-shrink-0 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-700">Hỗ trợ tiếng Việt và tiếng Khmer - Lan tỏa tri thức đến mọi miền</span>
                  </li>
                </ul>
              </div>
              <div className="relative h-80 md:h-auto">
                <img 
                  src="https://consosukien.vn/pic/News/xoa-mu-chu-cho-tre-em-dan-toc-thieu-so-va-mien-nui-1.jpg"
                  alt="Students learning"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* OCR Section */}
      <section id="ocr" className="py-24 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-primary font-semibold text-sm uppercase tracking-wider">Công cụ số hóa</span>
            <h3 className="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-5">
              Chuyển đổi tài liệu thành văn bản số
            </h3>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Bắt đầu hành trình số hóa - Mỗi tài liệu được lưu giữ là một phần di sản được bảo tồn
            </p>
          </div>

          <div className="bg-gradient-to-br from-light to-white rounded-3xl p-10 shadow-2xl border border-primary/10">
            <UploadArea onFileSelect={handleFileSelect} isProcessing={isProcessing} />

            {isProcessing && (
              <div className="mt-12 text-center">
                <div className="inline-block relative">
                  <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary border-t-transparent"></div>
                </div>
                <p className="mt-6 text-lg text-gray-700 font-medium">Đang xử lý tài liệu của bạn...</p>
                <p className="mt-2 text-sm text-gray-500">Vui lòng chờ trong giây lát</p>
              </div>
            )}

            {error && (
              <div className="mt-12 bg-red-50 border-l-4 border-red-500 rounded-lg p-6 shadow-md">
                <div className="flex items-start">
                  <svg className="w-6 h-6 text-red-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <p className="font-semibold text-red-800 text-lg">Có lỗi xảy ra</p>
                    <p className="text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {extractedText && !isProcessing && (
              <TextDisplay text={extractedText} filename={filename} />
            )}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1f2937] text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            {/* Column 1 - About */}
            <div>
              <h3 className="text-2xl font-bold text-primary mb-4">EthnoSoul Legacy</h3>
              <p className="text-gray-400 text-sm mb-6">
                Get started now! try our product
              </p>
              <div className="flex">
                <input
                  type="email"
                  placeholder="Enter your email here"
                  className="flex-1 px-4 py-2 rounded-l-full bg-gray-800 border border-gray-700 focus:outline-none focus:border-primary text-sm"
                />
                <button className="px-6 py-2 bg-primary hover:bg-secondary rounded-r-full transition-colors">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Column 2 */}
            <div>
              <h4 className="font-semibold text-white mb-4">Về Dịch Án</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">Giới thiệu về chúng tôi</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Số người & Tầm nhìn</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Đội ngũ LuminousForge</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Liên hệ hợp tác</a></li>
              </ul>
            </div>

            {/* Column 3 */}
            <div>
              <h4 className="font-semibold text-white mb-4">Khám Phá</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">Lộ trình phát triển</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Khóa học liên quan hệ</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Kho lưu giải thưởng</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Mạng cho đối tác giáo dục</a></li>
              </ul>
            </div>

            {/* Column 4 */}
            <div>
              <h4 className="font-semibold text-white mb-4">Cộng Đồng</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">Tham gia cộng đồng</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Đóng góp cho dự án</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Báo cáo lỗi và vướng mắc</a></li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400">
            <p>&copy; 2025 EthnoSoul Legacy by LuminousForge. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="hover:text-primary transition-colors">Terms and Conditions</a>
              <a href="#" className="hover:text-primary transition-colors">Privacy Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
