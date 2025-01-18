from langchain import hub
from langchain_mistralai import ChatMistralAI


class Generator:
    def __init__(self):
        self.model = ChatMistralAI(model="mistral-large-latest", max_tokens=200)
        self.prompt = hub.pull("rlm/rag-prompt")

    def generate(self, query: str, documents: list):
        docs_content = "\n\n".join(doc.page_content for doc in documents)
        messages = self.prompt.invoke({"question": query, "context": docs_content})
        response = self.model.invoke(messages)
        return {"answer": response.content}
