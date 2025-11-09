# Text Detection OCR Application

## Cấu trúc Project

```
text_detection/
├── main.py                 # OCR processor core
├── api.py                  # Flask API backend
├── requirements_api.txt    # Python dependencies
├── nextjs-app/            # Next.js frontend
│   ├── app/
│   │   ├── page.tsx       # Main page
│   │   ├── layout.tsx     # Root layout
│   │   ├── globals.css    # Global styles
│   │   └── api/
│   │       └── ocr/
│   │           └── route.ts  # API route
│   ├── components/
│   │   ├── UploadArea.tsx    # Upload component
│   │   └── TextDisplay.tsx   # Text display component
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
```

## Cài đặt và Chạy

### 1. Backend (Python Flask)

```bash
# Cài đặt dependencies
cd text_detection
pip install -r requirements_api.txt

# Chạy Flask API
python api.py
```

API sẽ chạy tại: http://localhost:5000

### 2. Frontend (Next.js)

```bash
# Di chuyển vào thư mục Next.js
cd nextjs-app

# Cài đặt dependencies
npm install

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

## Tính năng

- ✅ Upload file (JPG, PNG, GIF, JFIF, HEIC, PDF)
- ✅ Drag & Drop
- ✅ Paste from clipboard
- ✅ OCR text extraction (Khmer language support)
- ✅ Display extracted text
- ✅ Download as .txt file
- ✅ Responsive UI với Tailwind CSS

## API Endpoints

### POST /api/ocr
Upload file và nhận văn bản đã trích xuất

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (binary)

**Response:**
```json
{
  "success": true,
  "text": "Extracted text...",
  "filename": "document.pdf"
}
```

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 18+
- Tesseract OCR (phải được cài đặt trên hệ thống)
- Poppler (cho xử lý PDF)
