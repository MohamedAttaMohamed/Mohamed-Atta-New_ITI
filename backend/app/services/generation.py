"""
Builds the grounded prompt from retrieved chunks and calls the local Ollama LLM
with a resilient fallback synthesizer if Ollama is unreachable.
"""
import logging
import ollama

from app.core.config import settings

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions using ONLY the context below.
If the answer is not contained in the context, say you don't know — do not make anything up.
Cite the source document(s) you used at the end of your answer.

Context:
{context}

Question: {question}

Answer:"""


def build_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[{i + 1}] (source: {c['source']})\n{c['text']}" for i, c in enumerate(chunks)
    )
    return PROMPT_TEMPLATE.format(context=context, question=question)


def _synthesize_grounded_fallback(question: str, chunks: list[dict]) -> str:
    """
    Fallback context-grounded answer synthesis when local Ollama service is unreachable.
    Extracts relevant context sentences directly from retrieved chunks.
    """
    if not chunks:
        return "I couldn't find anything relevant in the documents to answer that."

    sources = sorted({c["source"] for c in chunks})
    sources_str = ", ".join(sources)

    # Combine top relevant passages
    passages = []
    for c in chunks[:2]:
        text = c["text"].strip()
        lines = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("#")]
        if lines:
            passages.append(" ".join(lines[:3]))

    answer_body = " ".join(passages)
    return f"{answer_body}\n\n[Sources: {sources_str}]"


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "I couldn't find anything relevant in the documents to answer that."

    prompt = build_prompt(question, chunks)

    try:
        client = ollama.Client(host=settings.ollama_host)
        response = client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as exc:
        logger.warning(
            f"Ollama server connection failed ({exc}). Falling back to grounded context synthesis."
        )
        return _synthesize_grounded_fallback(question, chunks)
