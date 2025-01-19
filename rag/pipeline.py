from rag.retriever import Retriever
from rag.generator import Generator
import time


class RAGPipeline:
    def __init__(self, rag_config):
        self.retriever = Retriever(rag_config)
        self.generator = Generator()

    def get_response(self, query: str) -> str:
        documents, scores = self.retriever.retrieve(query)
        time.sleep(1.5) # both retriever and generator require API call
        response = self.generator.generate(query, documents)

        return response["answer"]
