from chromadb import Client
from chromadb.utils import embedding_functions


class SemanticMemory:
    def __init__(self):

        self.client = Client()

        self.embedding = embedding_functions.OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small"
        )

        self.collection = self.client.get_or_create_collection(
            name="memory",
            embedding_function=self.embedding
        )

    # =========================
    # STORE MEMORY
    # =========================
    def store(self, query, answer):

        text = f"User: {query}\nAI: {answer}"

        self.collection.add(
            documents=[text],
            ids=[query]  # simple id (can improve later)
        )

    # =========================
    # RETRIEVE MEMORY
    # =========================
    def retrieve(self, query, k=3):

        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        docs = results.get("documents", [[]])[0]

        return "\n".join(docs)