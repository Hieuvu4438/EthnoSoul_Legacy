import argparse
import csv
from pathlib import Path

from tqdm import tqdm

from llm_config import settings
from step1_data_generator import DataGenerator
from step2_lexical_mapper import LexicalMapper
from step3_grammar_injector import GrammarInjector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="End-to-End Data Generation Pipeline"
    )
    parser.add_argument(
        "--num-seeds",
        type=int,
        default=settings.NUM_SEED_SAMPLES,
        help=f"Số lượng seed keywords (default: {settings.NUM_SEED_SAMPLES})"
    )
    parser.add_argument(
        "--variants-per-seed",
        type=int,
        default=settings.VARIANTS_PER_SEED,
        help=f"Số variants cho mỗi seed (default: {settings.VARIANTS_PER_SEED})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=settings.OUTPUT_DATASET_PATH,
        help=f"Đường dẫn file output (default: {settings.OUTPUT_DATASET_PATH})"
    )
    return parser.parse_args()


def run_pipeline(
    num_seeds: int,
    variants_per_seed: int,
    output_path: str
) -> None:
    generator = DataGenerator()
    mapper = LexicalMapper()
    injector = GrammarInjector()
    keywords = generator.load_random_seeds(num_seeds)

    if not keywords:
        return
    output_file = Path(output_path)
    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Original_Keyword',
            'Vietnamese_Variant',
            'Pidgin_Draft',
            'Target_Output'
        ])

    for keyword in tqdm(keywords, desc="Processing keywords"):
        try:
            variants = generator.generate_variants(keyword, variants_per_seed)

            if not variants:
                continue
            for variant in variants:
                try:
                    pidgin_draft = mapper.map_to_pidgin(variant)
                    target_output = injector.inject_grammar(pidgin_draft)
                    with open(output_file, mode='a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            keyword,
                            variant,
                            pidgin_draft,
                            target_output
                        ])

                except Exception:
                    continue

        except Exception:
            continue


def main() -> None:
    args = parse_args()

    run_pipeline(
        num_seeds=args.num_seeds,
        variants_per_seed=args.variants_per_seed,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
