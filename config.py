from pathlib import Path

class Config:
    def __init__(self, telegram_token: str, mistral_api_key: str):
        self.telegram_token = telegram_token
        self.mistral_api_key = mistral_api_key


class RAGConfig:
    def __init__(self):
        self.vector_store_path = Path("data/vector_store.vs")
        self.source_data_path = Path("data/kl_025.6_ru_en_v1.0 (2)")
