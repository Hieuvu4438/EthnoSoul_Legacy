import csv
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SwitchOutConfig:
    tau_src: float = 0.1  
    tau_tgt: float = 0.1 
    num_augment: int = 1  
    seed: Optional[int] = 42


class SwitchOut:
    def __init__(self, config: SwitchOutConfig):
        self.config = config
        self.vocab_src: List[str] = []  
        self.vocab_tgt: List[str] = []  
        
        if config.seed is not None:
            random.seed(config.seed)
    
    def _tokenize(self, text: str) -> List[str]:
        return text.strip().split() if text.strip() else []
    
    def _detokenize(self, tokens: List[str]) -> str:
        return ' '.join(tokens)
    
    def build_vocab(self, pairs: List[Tuple[str, str]]) -> None:
        vocab_src_set = set()
        vocab_tgt_set = set()
        
        for src, tgt in pairs:
            vocab_src_set.update(self._tokenize(src))
            vocab_tgt_set.update(self._tokenize(tgt))
        
        self.vocab_src = list(vocab_src_set)
        self.vocab_tgt = list(vocab_tgt_set)
    
    def _switchout_sentence(self, tokens: List[str], vocab: List[str], tau: float) -> List[str]:
        if not tokens or not vocab or tau <= 0:
            return tokens.copy()
        
        result = []
        for token in tokens:
            if random.random() < tau:
                new_token = random.choice(vocab)
                result.append(new_token)
            else:
                result.append(token)
        
        return result
    
    def augment_pair(self, src: str, tgt: str) -> List[Tuple[str, str]]:

        src_tokens = self._tokenize(src)
        tgt_tokens = self._tokenize(tgt)
        
        augmented = []
        for _ in range(self.config.num_augment):
            new_src_tokens = self._switchout_sentence(
                src_tokens, self.vocab_src, self.config.tau_src
            )
            new_tgt_tokens = self._switchout_sentence(
                tgt_tokens, self.vocab_tgt, self.config.tau_tgt
            )
            
            new_src = self._detokenize(new_src_tokens)
            new_tgt = self._detokenize(new_tgt_tokens)
            
            if new_src != src or new_tgt != tgt:
                augmented.append((new_src, new_tgt))
        
        return augmented
    
    def augment_corpus(self, pairs: List[Tuple[str, str]]) -> List[Tuple[str, str, bool]]:
        if not self.vocab_src or not self.vocab_tgt:
            self.build_vocab(pairs)
        
        result = []
        for src, tgt in pairs:
            result.append((src, tgt, False))
  
            augmented = self.augment_pair(src, tgt)
            for aug_src, aug_tgt in augmented:
                result.append((aug_src, aug_tgt, True))
        
        return result


def load_corpus(csv_path: str) -> List[Tuple[str, str]]:

    pairs = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vietnamese = row.get('NghiaTiengViet', '').strip()
            tai_dam = row.get('TuNgu', '').strip()
            
            if vietnamese and tai_dam:
                pairs.append((vietnamese, tai_dam))
    
    return pairs


def save_augmented_corpus(
    data: List[Tuple[str, str, bool]], 
    output_path: str,
    include_flag: bool = True
) -> None:
    """Lưu corpus đã augment ra file CSV."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if include_flag:
            fieldnames = ['vietnamese', 'tai_dam', 'is_augmented']
        else:
            fieldnames = ['vietnamese', 'tai_dam']
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            row = {'vietnamese': item[0], 'tai_dam': item[1]}
            if include_flag:
                row['is_augmented'] = item[2]
            writer.writerow(row)


def main():
    input_file = 'corpus.csv'
    output_file = 'corpus_switchout.csv'

    pairs = load_corpus(input_file)
    config = SwitchOutConfig(
        tau_src=0.15,  
        tau_tgt=0.10,  
        num_augment=2,  
        seed=42
    )
    
    switchout = SwitchOut(config)
    switchout.build_vocab(pairs)
    
    augmented_data = switchout.augment_corpus(pairs)
    
    save_augmented_corpus(augmented_data, output_file)
    
    original_count = len(pairs)
    augmented_count = sum(1 for item in augmented_data if item[2])
    total_count = len(augmented_data)
    
    print(f"Original pairs: {original_count}")
    print(f"Augmented pairs: {augmented_count}")
    print(f"Total pairs: {total_count}")
    print(f"Vocab size (Vietnamese): {len(switchout.vocab_src)}")
    print(f"Vocab size (Tai Dam): {len(switchout.vocab_tgt)}")


if __name__ == '__main__':
    main()
