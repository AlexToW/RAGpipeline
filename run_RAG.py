from rag.pipeline import RAGPipeline
from langchain_mistralai import ChatMistralAI
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

    llm_answers = []
    model = ChatMistralAI(model="mistral-large-latest", max_tokens=200)

    # Формируем сообщение для модели
    # messages = [{"role": "user", "content": query}]

    # Отправляем запрос и получаем ответ
    # response = model.invoke(messages)

    for question in tqdm(questions):
        response = rag_pipeline.get_response(question)
        answers.append(response)
        time.sleep(1.5)
        messages = [{"role": "user", "content": question}]
        llm_answer = model.invoke(messages)
        llm_answers.append(llm_answer.content)
        time.sleep(1.5)

    for question, answer, llm_answer in zip(questions, answers, llm_answers):
        print(f"Query: '{question}'.\nRAG response: {answer}\nLLM response: '{llm_answer}'\n\n")

if __name__ == "__main__":
    _main()