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
        "Какие технологии детектирования поддерживает kedr?",
    ]

    answers = []

    for question in tqdm(questions):
        response = rag_pipeline.get_response(question)
        answers.append(response)
        time.sleep(1.5)

    for question, answer in zip(questions, answers):
        print(f"Query: '{question}'.\nResponse: '{answer}'\n\n")

if __name__ == "__main__":
    _main()