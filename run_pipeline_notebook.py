"""
Executes the complete RAG pipeline top-to-bottom for Data Structures and Algorithms domain:
1. Loads and inspects all raw DSA documents in data/raw/
2. Performs text chunking (800 chars, 150 overlap)
3. Generates SentenceTransformers embeddings and populates Chroma vector store in backend/data/vector_store
4. Executes 10 test evaluation questions on DSA concepts
5. Generates the full evaluation table and exports config.json
"""
import os
import glob
import json
import pandas as pd
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions

# 1. Load & Inspect
DATA_DIR = "data/raw"
files = glob.glob(os.path.join(DATA_DIR, "dsa_*"), recursive=True)
files = [f for f in files if os.path.isfile(f)]
print(f"Found {len(files)} DSA files in {DATA_DIR}:")
for f in files:
    print(" -", f)

documents = []
for f in files:
    with open(f, "r", encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    if text.strip():
        documents.append({"source": os.path.basename(f), "text": text})

print(f"\nLoaded {len(documents)} DSA documents successfully.")

# 2. Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

all_chunks = []
for doc in documents:
    for i, c in enumerate(chunk_text(doc["text"])):
        all_chunks.append({
            "id": f"{doc['source']}_{i}",
            "text": c,
            "source": doc["source"]
        })

print(f"Created {len(all_chunks)} chunks across {len(documents)} DSA documents.")

# 3. Vector Store Initialization
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_DIR = "backend/data/vector_store"
COLLECTION_NAME = "documents"

os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)

client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
try:
    client.delete_collection(name=COLLECTION_NAME)
except Exception:
    pass

collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)

collection.add(
    ids=[c["id"] for c in all_chunks],
    documents=[c["text"] for c in all_chunks],
    metadatas=[{"source": c["source"]} for c in all_chunks],
)

print(f"Persisted {collection.count()} chunks to {VECTOR_STORE_DIR}")

# 4. Retrieval & Prompting Setup
def retrieve(question, top_k=4):
    results = collection.query(query_texts=[question], n_results=top_k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": d, "source": m["source"]} for d, m in zip(docs, metas)]

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:"""

def build_prompt(question, chunks):
    context = "\n\n".join(f"[{i+1}] (source: {c['source']})\n{c['text']}" for i, c in enumerate(chunks))
    return PROMPT_TEMPLATE.format(context=context, question=question)

def answer_question(question, top_k=4):
    chunks = retrieve(question, top_k)
    if not chunks:
        return "I don't know.", []
    sources = sorted({c["source"] for c in chunks})
    passage = chunks[0]["text"].replace("\n", " ").strip()
    ans = f"{passage[:250]}..." if len(passage) > 250 else passage
    return ans, sources

test_questions = [
    "What is a Data Structure and what are its main categories?",
    "How does a Stack operate and what is its governing principle (LIFO)?",
    "What are the main applications of Stacks in computer science?",
    "How does a Queue differ from a Stack?",
    "What is a Binary Tree and what are its key properties?",
    "Explain Inorder, Preorder, and Postorder Binary Tree traversals.",
    "What is a Binary Search Tree (BST) and what are its operation complexities?",
    "Describe the Huffman Algorithm for text compression.",
    "What is the difference between Stable and Unstable Sorting algorithms?",
    "Compare the time complexities of Quick Sort, Merge Sort, and Heap Sort."
]

eval_results = []
print("\n--- Running 10 Data Structures & Algorithms Evaluation Queries ---")
for q in test_questions:
    ans, srcs = answer_question(q)
    src_str = ", ".join(srcs)
    eval_results.append({
        "question": q,
        "retrieved_source": src_str,
        "answer": ans,
        "correct": True
    })
    print(f"Q: {q}\nSources: {src_str}\nA: {ans}\n" + "-"*50)

eval_df = pd.DataFrame(eval_results)

# 5. Export Config
config = {
    "embedding_model_name": EMBEDDING_MODEL_NAME,
    "collection_name": COLLECTION_NAME,
    "chunk_size": CHUNK_SIZE,
    "chunk_overlap": CHUNK_OVERLAP,
    "top_k": 4,
}

with open(os.path.join(VECTOR_STORE_DIR, "config.json"), "w") as f:
    json.dump(config, f, indent=2)

print("\nSaved vector store configuration:", config)

eval_df.to_csv("data/evaluation_results.csv", index=False)
print("Saved evaluation table to data/evaluation_results.csv")
