import csv
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

import google.generativeai as genai
import config


@dataclass
class TranslationExample:
    vietnamese: str
    tai_dam: str
    word_type: str
    description: str


class FewShotInContextLearning:
    
    def __init__(self, grammar_file: str, corpus_file: str):
        self.grammar_rules = self._load_grammar(grammar_file)
        self.corpus = self._load_corpus(corpus_file)
        self._setup_api()
    
    def _setup_api(self) -> None:
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config={
                "temperature": config.TEMPERATURE,
                "max_output_tokens": config.MAX_OUTPUT_TOKENS,
            }
        )
    
    def _load_grammar(self, grammar_file: str) -> str:
        with open(grammar_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_corpus(self, corpus_file: str) -> List[TranslationExample]:
        examples = []
        with open(corpus_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vietnamese = row.get('NghiaTiengViet', '').strip()
                tai_dam = row.get('TuNgu', '').strip()
                word_type = row.get('LoaiTu', '').strip()
                desc1 = row.get('MoTa1', '').strip()
                
                if vietnamese and tai_dam:
                    examples.append(TranslationExample(
                        vietnamese=vietnamese,
                        tai_dam=tai_dam,
                        word_type=word_type,
                        description=desc1
                    ))
        return examples
    
    def _select_high_quality_examples(self, k: int = 10) -> List[TranslationExample]:
        quality_examples = [
            ex for ex in self.corpus 
            if ex.description and ':' in ex.description and len(ex.vietnamese) > 1
        ]
        
        if len(quality_examples) < k:
            quality_examples = [ex for ex in self.corpus if len(ex.vietnamese) > 1]
        
        word_types = {}
        for ex in quality_examples:
            wt = ex.word_type or 'other'
            if wt not in word_types:
                word_types[wt] = []
            word_types[wt].append(ex)
        
        selected = []
        per_type = max(1, k // len(word_types)) if word_types else k
        
        for wt, exs in word_types.items():
            sampled = random.sample(exs, min(per_type, len(exs)))
            selected.extend(sampled)
            if len(selected) >= k:
                break
        
        if len(selected) < k:
            remaining = [ex for ex in quality_examples if ex not in selected]
            selected.extend(random.sample(remaining, min(k - len(selected), len(remaining))))
        
        return selected[:k]
    
    def _extract_grammar_summary(self) -> str:
        key_sections = []
        
        key_sections.append("""
NGỮ PHÁP TIẾNG THÁI CỔ (TAI DAM):

1. TRẬT TỰ TỪ: SVO (Chủ ngữ - Vị ngữ - Tân ngữ)
   - Ví dụ: ꪢꪴ ꪵꪚꪙ ꪎꪺꪙ = lợn phá vườn

2. TÍNH TỪ đứng SAU danh từ:
   - Ví dụ: ꪚ꫁ꪱꪙ ꪻꪐ꪿ = bản to

3. PHỦ ĐỊNH dùng ꪹꪚ꪿ꪱ (không):
   - Ví dụ: ꪹꪚ꪿ꪱ ꪣꪲ ꪹꪥꪸꪒ = không làm

4. SO SÁNH dùng ꪹꪁꪷ꪿ (như):
   - Ví dụ: ꪒꪾ ꪹꪁꪷ꪿ ꪶꪔ ꪀꪱ = đen như con quạ

5. TỪ GHÉP: ghép 2 từ đơn
   - ꪮ꫁ꪱꪥ ꪹꪯꪸꪣ = bố mẹ (cha + mẹ)

6. HỆ THỐNG THANH ĐIỆU:
   - Không dấu: thanh ngang
   - Dấu ꪿: thanh sắc  
   - Dấu ꫁: thanh huyền
""")
        return ''.join(key_sections)
    
    def _build_prompt(self, examples: List[TranslationExample], source_text: str) -> str:
        grammar_summary = self._extract_grammar_summary()
        
        prompt_parts = [
            "Bạn là chuyên gia ngôn ngữ học về Tiếng Thái Cổ (Tai Dam/Thái Đen) - một ngôn ngữ low-resource tại Việt Nam.",
            "",
            "=== QUY TẮC NGỮ PHÁP ===",
            grammar_summary,
            "",
            "=== CÁC VÍ DỤ DỊCH TỪ TIẾNG VIỆT SANG TIẾNG THÁI CỔ ===",
            "Hãy học cấu trúc ngữ pháp và từ vựng từ các ví dụ sau:",
            ""
        ]
        
        for i, ex in enumerate(examples, 1):
            example_text = f"Ví dụ {i}:"
            example_text += f"\n  Tiếng Việt: {ex.vietnamese}"
            example_text += f"\n  Tiếng Thái Cổ: {ex.tai_dam}"
            if ex.word_type:
                example_text += f"\n  Loại từ: {ex.word_type}"
            if ex.description and ':' in ex.description:
                parts = ex.description.split(':', 1)
                if len(parts) == 2:
                    example_text += f"\n  Ví dụ trong câu: {parts[0].strip()} → {parts[1].strip()}"
            prompt_parts.append(example_text)
            prompt_parts.append("")
        
        prompt_parts.extend([
            "=== NHIỆM VỤ ===",
            f"Dựa trên các quy tắc ngữ pháp và ví dụ trên, hãy dịch câu sau sang Tiếng Thái Cổ:",
            "",
            f"Câu cần dịch: {source_text}",
            "",
            "Chỉ trả lời bản dịch Tiếng Thái Cổ, không giải thích."
        ])
        
        return '\n'.join(prompt_parts)
    
    def translate(self, source_text: str, k: int = None) -> str:
        if k is None:
            k = config.NUM_EXAMPLES
        
        examples = self._select_high_quality_examples(k)
        prompt = self._build_prompt(examples, source_text)
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def translate_batch(
        self, 
        source_texts: List[str], 
        output_file: str,
        k: int = None
    ) -> List[Dict[str, str]]:
        results = []
        
        for source in source_texts:
            try:
                translation = self.translate(source, k)
                results.append({
                    'vietnamese': source,
                    'tai_dam_pseudo': translation,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'vietnamese': source,
                    'tai_dam_pseudo': '',
                    'status': f'error: {str(e)}'
                })
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['vietnamese', 'tai_dam_pseudo', 'status'])
            writer.writeheader()
            writer.writerows(results)
        
        return results


def load_sentences_to_translate(file_path: str) -> List[str]:
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(line)
    return sentences


def main():
    translator = FewShotInContextLearning(
        grammar_file='thai_grammar.txt',
        corpus_file='corpus.csv'
    )
    
    test_sentences = [
        "con chim bay",
        "nước chảy",
        "bố mẹ",
        "nhà to",
        "anh em",
    ]
    
    results = translator.translate_batch(
        source_texts=test_sentences,
        output_file='pseudo_labels.csv',
        k=config.NUM_EXAMPLES
    )
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"Translated: {success_count}/{len(results)}")


if __name__ == '__main__':
    main()
