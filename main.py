import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pdf2image
import cv2
import numpy as np
from pathlib import Path
from typing import Union, List
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

POPPLER_PATH = r'D:\PROJECTS\EthnoSoul Legacy\text_detection\Release-25.07.0-0\poppler-25.07.0\Library\bin'

class OCRProcessor:
    SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
    SUPPORTED_PDF_FORMAT = '.pdf'
    
    def __init__(self, language: str = 'khm', use_preprocessing: bool = True):
        self.language = language
        self.use_preprocessing = use_preprocessing
        self._validate_tesseract()
    
    def _validate_tesseract(self) -> None:
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract not found. Please install Tesseract OCR: {e}")
    
    def _is_image(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_IMAGE_FORMATS
    
    def _is_pdf(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == self.SUPPORTED_PDF_FORMAT
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        if not self.use_preprocessing:
            return image
        
        img_array = np.array(image)
        
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        thresh = cv2.adaptiveThreshold(
            blurred, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 2
        )
        
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        processed_image = Image.fromarray(denoised)
        
        enhancer = ImageEnhance.Sharpness(processed_image)
        processed_image = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Contrast(processed_image)
        processed_image = enhancer.enhance(1.5)
        
        return processed_image
    
    def _ocr_image(self, image: Image.Image) -> str:
        preprocessed = self._preprocess_image(image)
        config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(preprocessed, lang=self.language, config=config)
    
    def _process_pdf(self, file_path: Path) -> str:
        images = pdf2image.convert_from_path(
            str(file_path), 
            dpi=300,
            poppler_path=POPPLER_PATH
        )
        texts = [self._ocr_image(image) for image in images]
        return '\n\n--- Page Break ---\n\n'.join(texts)
    
    def _process_image(self, file_path: Path) -> str:
        image = Image.open(file_path)
        return self._ocr_image(image)
    
    def process_file(self, file_path: Union[str, Path]) -> str:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if self._is_pdf(path):
            return self._process_pdf(path)
        elif self._is_image(path):
            return self._process_image(path)
        else:
            raise ValueError(
                f"Unsupported file format: {path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_IMAGE_FORMATS | {self.SUPPORTED_PDF_FORMAT})}"
            )
    
    def process_batch(self, file_paths: List[Union[str, Path]]) -> dict:
        results = {}
        for file_path in file_paths:
            try:
                results[str(file_path)] = self.process_file(file_path)
            except Exception as e:
                results[str(file_path)] = f"Error: {str(e)}"
        return results

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("OCR Processor - Khmer Language Support")
        print("=" * 60)
        print("Supported formats: PNG, JPG, JPEG, TIFF, BMP, GIF, PDF")
        print("Output location: outputs/<filename>.txt")
        print("=" * 60)
        
        input_file = input("\nEnter file path: ").strip().strip('"')
        
        if not input_file:
            print("Error: No file path provided")
            sys.exit(1)
    else:
        input_file = sys.argv[1]
    
    try:
        output_dir = Path(__file__).parent / 'outputs'
        output_dir.mkdir(exist_ok=True)
        
        input_path = Path(input_file)
        output_filename = f"{input_path.stem}.txt"
        output_file = output_dir / output_filename
        
        processor = OCRProcessor(language='khm', use_preprocessing=True)
        text = processor.process_file(input_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\n✓ Text extracted successfully")
        print(f"✓ Saved to: {output_file}")
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()