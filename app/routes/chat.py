from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import (
    AIProviderConfigError,
    AIProviderRequestError,
    AIProviderTimeoutError,
    AIService,
)
from app.services.rag_service import RAGService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def create_chat_completion(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    started_at = perf_counter()
    settings = get_settings()
    chat_repository = ChatRepository(db)
    rag_service = RAGService(db)
    ai_service = AIService(settings)

    try:
        session = _get_or_create_session(chat_repository, request)
        chat_repository.add_message(
            session_id=session.id,
            role="user",
            content=request.message,
        )

        rag_result = rag_service.retrieve(request.message)
        system_prompt = _build_system_prompt(rag_result.context)
        history = chat_repository.list_recent_messages(session.id)

        ai_result = await ai_service.complete(
            system_prompt=system_prompt,
            user_message=request.message,
            history=history[:-1],
        )

        chat_repository.add_message(
            session_id=session.id,
            role="assistant",
            content=ai_result.content,
            latency_ms=int((perf_counter() - started_at) * 1000),
            model_name=ai_result.model,
        )
        db.commit()

        latency_ms = int((perf_counter() - started_at) * 1000)
        return ChatResponse(
            answer=ai_result.content,
            session_id=session.id,
            sources=rag_result.sources,
            latency_ms=latency_ms,
            model=ai_result.model,
        )
    except HTTPException:
        db.rollback()
        raise
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except AIProviderConfigError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except AIProviderTimeoutError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except AIProviderRequestError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while processing chat request",
        ) from exc


def _get_or_create_session(
    chat_repository: ChatRepository,
    request: ChatRequest,
):
    if request.session_id:
        session = chat_repository.get_session(request.session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found",
            )
        return session

    title = request.message.strip()[:80]
    return chat_repository.create_session(user_id=request.user_id, title=title)


def _build_system_prompt(retrieved_context: str) -> str:
    return f"""You are AMD Smart Product Assistant, a concise and practical AI assistant for AMD products and technologies.

You help users understand AMD Ryzen, Radeon, AMD Instinct, ROCm, vLLM, GPU acceleration, and AI workload planning.
Prefer accurate, implementation-ready guidance. If the user asks for product recommendations, ask for workload, budget, and deployment constraints when needed.
Do not claim to run ROCm or AMD GPU inference locally on a Mac. For local development, explain that the backend can use a mock provider and later switch to vLLM on AMD Developer Cloud.

Retrieved knowledge context:
{retrieved_context}
"""
