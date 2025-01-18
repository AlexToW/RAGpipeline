from rag.pipeline import RAGPipeline
from config import RAGConfig
import yaml
import os
from tqdm import tqdm
import time


def _main():
    with open('credentials.yaml', 'r') as file:
        creds = yaml.load(file, Loader=yaml.FullLoader)

    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = creds["mistral_api_key"]
    rag_config = RAGConfig()
    rag_pipeline = RAGPipeline(rag_config)


    questions = [
        "Что такое KATA?",
        "Можно ли добавить в исключение IDS и TAA правила?",
        "Сколько серверов минимально необходимо при кластерной установке?",
        "В каком формате нужно добавлять пользовательские ioc?",
        "Какие технологии детектирования поддерживает kedr?"
    ]

    for question in tqdm(questions):
        response = rag_pipeline.get_response(question)
        print(f"query: '{question}'.\nResponse: '{response}'")
        time.sleep(5)


if __name__ == "__main__":
    _main()