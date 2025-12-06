

import google.generativeai as genai
from llm_config import settings


class GrammarInjector:

    def __init__(self) -> None:
        with open(settings.INPUT_GRAMMAR_PATH, "r", encoding="utf-8") as f:
            self.grammar_content: str = f.read()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)

    def inject_grammar(self, pidgin_text: str) -> str:
        system_instruction = f"""Bạn là một engine sắp xếp ngữ pháp cho ngôn ngữ Thái Đen. Dựa trên luật: 
{self.grammar_content}
. Nhiệm vụ: Sắp xếp lại trật tự các từ trong câu input để đúng ngữ pháp (SVO, Tính từ sau Danh từ, Phủ định trước Động từ). TUYỆT ĐỐI KHÔNG dịch các từ tiếng Việt còn sót lại. TUYỆT ĐỐI KHÔNG thay đổi từ tiếng Thái đã có. Chỉ thay đổi vị trí."""

        # Tạo model với system instruction
        model_with_instruction = genai.GenerativeModel(
            model_name=settings.MODEL_NAME,
            system_instruction=system_instruction
        )

        # Gọi API
        response = model_with_instruction.generate_content(pidgin_text)

        # Trả về kết quả sạch
        result: str = response.text.strip()
        return result


if __name__ == "__main__":
    # Test thử
    injector = GrammarInjector()

    # Ví dụ câu Pidgin test
    test_pidgin = "ꪀꪲꪙ ꪹꪜꪸ꫁ꪙ ꪀꪴ"
    result = injector.inject_grammar(test_pidgin)
    print(f"Input:  {test_pidgin}")
    print(f"Output: {result}")
