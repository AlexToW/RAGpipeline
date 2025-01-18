from rag.retriever import Retriever
from rag.generator import Generator


class RAGPipeline:
    def __init__(self, rag_config):
        self.retriever = Retriever(rag_config)
        self.generator = Generator()

    def get_response(self, query: str) -> str:
        documents, scores = self.retriever.retrieve(query)

        response = self.generator.generate(query, documents)

        return response["answer"]
