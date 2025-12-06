
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple

from llm_config import settings


class LexicalMapper:

    def __init__(self, corpus_path: str | None = None) -> None:
        self.corpus_path = Path(corpus_path or settings.INPUT_CORPUS_PATH)
        self.vi_to_thai: Dict[str, str] = {}
        self._sorted_keys: List[str] = []
        self._regex_pattern: re.Pattern | None = None
        
        self._load_corpus()
        self._build_regex_pattern()

    def _load_corpus(self) -> None:
        with open(self.corpus_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                tu_ngu = row.get('TuNgu', '').strip()
                nghia_tieng_viet = row.get('NghiaTiengViet', '').strip()
                
                if not tu_ngu or not nghia_tieng_viet:
                    continue
                meanings = self._parse_meanings(nghia_tieng_viet)
                
                for meaning in meanings:
                    meaning_lower = meaning.lower().strip()
                    if meaning_lower and meaning_lower not in self.vi_to_thai:
                        self.vi_to_thai[meaning_lower] = tu_ngu
        self._sorted_keys = sorted(
            self.vi_to_thai.keys(), 
            key=len, 
            reverse=True
        )

    def _parse_meanings(self, nghia_raw: str) -> List[str]:
        parts = nghia_raw.split(',')
        meanings: List[str] = []
        
        for part in parts:
            cleaned = part.strip()
            cleaned = re.sub(r'\([^)]*\)', '', cleaned).strip()
            if cleaned:
                meanings.append(cleaned)
        
        return meanings

    def _build_regex_pattern(self) -> None:
        if not self._sorted_keys:
            self._regex_pattern = None
            return
        escaped_keys = [re.escape(key) for key in self._sorted_keys]
        
        pattern_str = r'\b(' + '|'.join(escaped_keys) + r')\b'
        
        self._regex_pattern = re.compile(pattern_str, re.IGNORECASE)

    def _replace_match(self, match: re.Match) -> str:
        matched_text = match.group(0).lower()
        return self.vi_to_thai.get(matched_text, match.group(0))

    def map_to_pidgin(self, vietnamese_text: str) -> str:
        if not vietnamese_text or not self._regex_pattern:
            return vietnamese_text
        result = self._regex_pattern.sub(self._replace_match, vietnamese_text)
        
        return result

    def get_mapping_stats(self) -> Dict[str, int]:
        return {
            'total_mappings': len(self.vi_to_thai),
            'unique_thai_words': len(set(self.vi_to_thai.values())),
            'longest_key_length': len(self._sorted_keys[0]) if self._sorted_keys else 0,
        }

    def lookup(self, vietnamese_word: str) -> str | None:
        return self.vi_to_thai.get(vietnamese_word.lower().strip())


def main() -> None:
    mapper = LexicalMapper()
    
    # In thống kê
    stats = mapper.get_mapping_stats()
    print("=" * 50)
    print("LEXICAL MAPPER - THỐNG KÊ")
    print("=" * 50)
    print(f"Tổng số mappings: {stats['total_mappings']}")
    print(f"Số từ Thái Đen unique: {stats['unique_thai_words']}")
    print(f"Độ dài key dài nhất: {stats['longest_key_length']}")
    print()
    
    # Test với một số câu mẫu
    test_sentences = [
        "Con quạ đen như con quạ",
        "Tôi ngồi ở giữa trưa",
        "Anh ấy rất dũng cảm và gan góc",
        "Bắc cầu qua sông",
        "Đây là câu không có từ trong từ điển",
    ]
    
    print("=" * 50)
    print("KẾT QUẢ CHUYỂN ĐỔI")
    print("=" * 50)
    
    for sentence in test_sentences:
        pidgin = mapper.map_to_pidgin(sentence)
        print(f"VI: {sentence}")
        print(f"PD: {pidgin}")
        print("-" * 50)


if __name__ == "__main__":
    main()
