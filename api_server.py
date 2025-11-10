from flask import Flask, request, jsonify
from flask_cors import CORS
from main import OCRProcessor
import os
import sys
from pathlib import Path
from werkzeug.utils import secure_filename
import shutil
from pathlib import Path


# Tìm poppler path động
def find_poppler_path():
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        return str(Path(pdftoppm).parent)
    return None


# Set PATH cho Nix
extra_paths = [
    "/run/current-system/sw/bin",
    os.path.expanduser("~/.nix-profile/bin"),
]

for p in extra_paths:
    if p not in os.environ["PATH"]:
        os.environ["PATH"] += f":{p}"

# Verify poppler
print("=== POPPLER CHECK ===")
print("pdftoppm:", shutil.which("pdftoppm"))
print("pdfinfo:", shutil.which("pdfinfo"))
print("Poppler path:", find_poppler_path())

app = Flask(__name__)


CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "https://*.vercel.app",  # Cho phép tất cả Vercel subdomains
                "https://your-domain.com",  # Thêm domain chính thức sau
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": False,
        }
    },
)

UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "pdf", "heic", "jfif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


import shutil, os

print("PYTHON:", sys.executable)
print("pdftoppm:", shutil.which("pdftoppm"))
print("pdfinfo:", shutil.which("pdfinfo"))
print("PATH:", os.environ["PATH"])


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "OCR API", "version": "1.0.0"}), 200


@app.route("/api/ocr", methods=["POST"])
def process_ocr():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File format not supported"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)

        processor = OCRProcessor(language="khm", use_preprocessing=True)
        extracted_text = processor.process_file(filepath)

        os.remove(filepath)

        return jsonify({"success": True, "text": extracted_text, "filename": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    pass


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
