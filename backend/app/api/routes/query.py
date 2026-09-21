import logging

from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import retrieve
from app.services.generation import generate_answer

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    try:
        chunks = retrieve(request.question)
        if not chunks:
            return QueryResponse(
                answer="I couldn't find anything relevant in the documents to answer that.",
                sources=[],
            )

        answer = generate_answer(request.question, chunks)
        sources = sorted({c["source"] for c in chunks})
        return QueryResponse(answer=answer, sources=sources)

    except RuntimeError as e:
        # e.g. vector store not loaded
        logger.exception("Retrieval service not ready")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        logger.exception("Unexpected error handling /query")
        raise HTTPException(status_code=500, detail="Internal server error")
