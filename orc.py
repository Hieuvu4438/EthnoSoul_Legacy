import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pdf2image
import cv2
import numpy as np
from pathlib import Path
from typing import Union, List
import sys
import shutil

import shutil, os, subprocess

print("=== OCR REQUEST DEBUG ===")
print("REQ python:", sys.executable)
print("REQ pdftoppm:", shutil.which("pdftoppm"))
print("REQ pdfinfo:", shutil.which("pdfinfo"))
print("REQ PATH:", os.environ["PATH"])


class OCRProcessor:
    SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"}
    SUPPORTED_PDF_FORMAT = ".pdf"

    def __init__(self, language: str = "khm", use_preprocessing: bool = True):
        self.language = language
        self.use_preprocessing = use_preprocessing
        self._validate_tesseract()

    def _validate_tesseract(self):
        pytesseract.get_tesseract_version()

    def _is_image(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_IMAGE_FORMATS

    def _is_pdf(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == self.SUPPORTED_PDF_FORMAT

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        if not self.use_preprocessing:
            return image

        img = np.array(image)
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)

        img = Image.fromarray(denoised)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        img = ImageEnhance.Contrast(img).enhance(1.5)
        return img

    def _ocr_image(self, image: Image.Image) -> str:
        pre = self._preprocess_image(image)
        return pytesseract.image_to_string(pre, lang=self.language, config="--oem 3 --psm 6")

    def _process_pdf(self, file_path: Path) -> str:
        images = pdf2image.convert_from_path(str(file_path), dpi=300, poppler_path="/nix/store/zmpjl7jgxgdsxmb5aga82h5g844llb29-poppler-utils-25.07.0/bin")
        return "\n\n--- Page Break ---\n\n".join(self._ocr_image(img) for img in images)

    def _process_image(self, file_path: Path) -> str:
        img = Image.open(file_path)
        return self._ocr_image(img)

    def process_file(self, file_path: Union[str, Path]) -> str:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(file_path)

        if self._is_pdf(p):
            return self._process_pdf(p)
        if self._is_image(p):
            return self._process_image(p)
        raise ValueError("Unsupported format")
