import json
import random
from typing import List

import google.generativeai as genai

from llm_config import settings


class DataGenerator:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)

    def load_random_seeds(self, limit: int) -> List[str]:
        import pandas as pd

        try:
            df = pd.read_csv(settings.INPUT_CORPUS_PATH)
            df = df.dropna(subset=["NghiaTiengViet"])
            df = df[df["NghiaTiengViet"].str.strip() != ""]

            if len(df) < limit:
                sampled = df
            else:
                sampled = df.sample(n=limit, random_state=random.randint(0, 10000))

            keywords = []
            for value in sampled["NghiaTiengViet"]:
                value_str = str(value).strip()
                if "," in value_str:
                    first_word = value_str.split(",")[0].strip()
                else:
                    first_word = value_str
                if first_word:
                    keywords.append(first_word)

            return keywords
        except Exception:
            return []

    def generate_variants(self, keyword: str, num_variants: int) -> List[str]:
        prompt = (
            f"Từ khóa: '{keyword}'. "
            f"Hãy đặt 1 câu tiếng Việt ngắn gọn, tự nhiên chứa từ này. "
            f"Sau đó viết lại câu vừa đặt thành {num_variants} câu khác nhau về cấu trúc "
            f"nhưng giữ nguyên nghĩa và giữ nguyên từ khóa '{keyword}'. "
            f"Trả về kết quả dạng JSON List string."
        )

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            if isinstance(result, list):
                return [str(item) for item in result if item]
            return []
        except Exception:
            return []


if __name__ == "__main__":
    generator = DataGenerator()
    
    keywords = generator.load_random_seeds(settings.NUM_SEED_SAMPLES)
    
    for keyword in keywords:
        variants = generator.generate_variants(keyword, settings.VARIANTS_PER_SEED)
