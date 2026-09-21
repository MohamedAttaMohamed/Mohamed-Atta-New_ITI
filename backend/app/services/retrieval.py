"""
Loads the persisted vector store (built by notebooks/rag_pipeline.ipynb)
and exposes a retrieval function used by the /query endpoint.
"""
import os
import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings

_client = None
_collection = None


def get_vector_store_path() -> str:
    path = settings.vector_store_dir
    if not os.path.isabs(path):
        # Resolve relative path from backend root if needed
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        resolved = os.path.abspath(os.path.join(base_dir, path))
        if os.path.exists(resolved):
            return resolved
    return path


def load_vector_store() -> None:
    """Load the persisted Chroma collection once, at app startup."""
    global _client, _collection

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model_name
    )

    store_path = get_vector_store_path()
    _client = chromadb.PersistentClient(path=store_path)
    _collection = _client.get_or_create_collection(
        name=settings.collection_name,
        embedding_function=embedding_fn,
    )


def retrieve(question: str, top_k: int | None = None) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks for a question.

    Returns a list of {"text": ..., "source": ..., "distance": ...} dicts.
    """
    if _collection is None:
        load_vector_store()

    k = top_k or settings.top_k
    results = _collection.query(query_texts=[question], n_results=k)

    chunks = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": doc,
                "source": (meta or {}).get("source", "unknown"),
                "distance": dist,
            }
        )
    return chunks
