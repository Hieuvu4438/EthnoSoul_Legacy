import json
from typing import Optional

import google.generativeai as genai


def paraphrase_sentence(sentence: str, api_key: str) -> list[str]:
    if not sentence or not sentence.strip():
        return []
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = f"""Viết lại câu sau thành 3 biến thể tiếng Việt giữ nguyên nghĩa gốc và các thực thể (Entity).
Chỉ trả về định dạng JSON list, không giải thích thêm.

Câu gốc: "{sentence}"

Ví dụ output mong muốn:
["Biến thể 1", "Biến thể 2", "Biến thể 3"]"""
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return [sentence]
        result = _parse_json_response(response.text)
        
        if result and isinstance(result, list) and len(result) > 0:
            return result
        
        return [sentence]
        
    except json.JSONDecodeError:
        return [sentence]
    except Exception:
        return [sentence]


def _parse_json_response(response_text: str) -> Optional[list[str]]:
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed if item]
        return None
    except json.JSONDecodeError:
        return None


async def paraphrase_sentence_async(sentence: str, api_key: str) -> list[str]:
    if not sentence or not sentence.strip():
        return []
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""Viết lại câu sau thành 3 biến thể tiếng Việt giữ nguyên nghĩa gốc và các thực thể (Entity).
Chỉ trả về định dạng JSON list, không giải thích thêm.

Câu gốc: "{sentence}"

Ví dụ output mong muốn:
["Biến thể 1", "Biến thể 2", "Biến thể 3"]"""

        response = await model.generate_content_async(prompt)
        
        if not response or not response.text:
            return [sentence]
        
        result = _parse_json_response(response.text)
        
        if result and isinstance(result, list) and len(result) > 0:
            return result
        
        return [sentence]
        
    except Exception:
        return [sentence]


if __name__ == "__main__":
    import os
    API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

    test_sentence = "Hôm nay tôi đi học ở trường Đại học Bách khoa Hà Nội."
    
    print(f"Original: {test_sentence}")
    print("-" * 50)
    
    results = paraphrase_sentence(test_sentence, API_KEY)
    
    print("Paraphrased versions:")
    for i, variant in enumerate(results, 1):
        print(f"  {i}. {variant}")
