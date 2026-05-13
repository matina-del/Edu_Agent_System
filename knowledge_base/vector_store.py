from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class KnowledgeBase:
    """教育知识库"""
    def __init__(self, persist_directory: str = "./knowledge_db"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
    
    def load_knowledge(self, documents: list[dict]):
        texts = []
        metadatas = []
        for doc in documents:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50,
                separators=["\n\n", "\n", "。", "！", "？"]
            )
            chunks = text_splitter.split_text(doc["content"])
            for chunk in chunks:
                texts.append(chunk)
                metadatas.append({
                    "subject": doc.get("subject", ""),
                    "topic": doc.get("topic", ""),
                    "difficulty": doc.get("difficulty", ""),
                    "knowledge_points": doc.get("knowledge_points", [])
                })
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
    
    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        docs = self.vectorstore.similarity_search_with_score(query, k=top_k)
        return [{"content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in docs]