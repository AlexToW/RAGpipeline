import os
import time
from tqdm import tqdm
from logger import logger
from config import RAGConfig
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



class Retriever:
    def __init__(self, config: RAGConfig):
        self.config = config

        self.embeddings = MistralAIEmbeddings(model="mistral-embed")
        self.vector_store = InMemoryVectorStore(self.embeddings)

        if not os.path.exists(self.config.vector_store_path):
            logger.info("Vector store not found. Building vector store...")
            if not os.path.exists(self.config.source_data_path):
                raise ValueError("Source data not found.")
            self._build_vector_store()

        self.vector_store = self.vector_store.load(self.config.vector_store_path, embedding=self.embeddings)
        logger.info("Vector store loaded.")
    
    def _build_vector_store(self):
        loader = PyPDFLoader(self.config.source_data_path)
        pages = []
        for page in loader.lazy_load():
            pages.append(page)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_splits = text_splitter.split_documents(pages)

        for i in tqdm(range(len(all_splits)), desc="Building vector store"):
            _ = self.vector_store.add_documents(documents=[all_splits[i]])
            time.sleep(2)


    def retrieve(self, query: str, top_k: int = 4):
        query_embedding = self.embeddings.embed_query(query)
        similar_documents_with_scores = self.vector_store.similarity_search_with_score_by_vector(
            embedding=query_embedding,
            k=top_k
        )

        similar_documents = []
        similarity_scores = []

        for doc, score in similar_documents_with_scores:
            similar_documents.append(doc)
            similarity_scores.append(score)

        return similar_documents, similarity_scores