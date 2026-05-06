import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


load_dotenv()



class RAGTool:
    def __init__(self, data_path="data"):

        self.data_path = data_path
        self.embedding = OpenAIEmbeddings()

        self.collection = self._load_or_create_db()

    # =========================
    # LOAD OR CREATE DB
    # =========================
    def _load_or_create_db(self):

        if os.path.exists("chroma_db"):
            return Chroma(
                persist_directory="chroma_db",
                embedding_function=self.embedding
            )

        documents = self._load_documents()
        chunks = self._chunk_documents(documents)

        db = Chroma.from_texts(
            texts=chunks,
            embedding=self.embedding,
            persist_directory="chroma_db"
        )

        return db

    # =========================
    # LOAD FILES
    # =========================
    def _load_documents(self):

        docs = []

        for file in os.listdir(self.data_path):
            with open(os.path.join(self.data_path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())

        return docs

    # =========================
    # CHUNKING
    # =========================
    def _chunk_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )

        chunks = []

        for doc in documents:
            chunks.extend(splitter.split_text(doc))

        return chunks

    # =========================
    # RETRIEVAL
    # =========================
    def run(self, query, k=3):

        results = self.collection.similarity_search(query, k=k)

        return [doc.page_content for doc in results]