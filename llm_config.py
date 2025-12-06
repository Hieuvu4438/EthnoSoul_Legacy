from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    INPUT_CORPUS_PATH: str = "D:\\Back Translation\\corpus.csv"
    INPUT_GRAMMAR_PATH: str = "D:\\Back Translation\\thai_grammar.txt"
    OUTPUT_DATASET_PATH: str = "augmented_dataset.csv"
    NUM_SEED_SAMPLES: int = 50
    VARIANTS_PER_SEED: int = 3
    MODEL_NAME: str = "gemini-2.5-pro"

    class Config:
        env_file = ".env"


settings = Settings()
