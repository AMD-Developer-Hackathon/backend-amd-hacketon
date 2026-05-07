from time import perf_counter
from fastapi import Request

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatResponse
import logging
from app.services.ai_service import (
    AIProviderConfigError,
    AIProviderRequestError,
    AIProviderTimeoutError,
    AIService,
    AIResult,
)
from app.services.rag_service import RAGService


from uuid import UUID

router = APIRouter(prefix="/chat", tags=["chat"])
@router.get("/sessions")
async def get_sessions(
    user_id: UUID | None = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    chat_repository = ChatRepository(db)
    sessions = chat_repository.list_sessions(user_id=user_id, limit=limit)
    return {
        "sessions": [
            {
                "id": s.id,
                "title": s.title,
                "created_at": s.created_at,
                "updated_at": s.updated_at
            } for s in sessions
        ]
    }

@router.get("/sessions/{session_id}/messages")
async def get_chat_history(
    session_id: UUID,
    db: Session = Depends(get_db)
):
    chat_repository = ChatRepository(db)
    session = chat_repository.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )
    messages = chat_repository.list_recent_messages(session_id, limit=50)
    return {"session_id": session_id, "messages": messages}



from app.dependencies.limiter import limiter

@router.post("", response_model=ChatResponse)
@limiter.limit("20/minute")
async def create_chat_completion(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    started_at = perf_counter()
    settings = get_settings()
    chat_repository = ChatRepository(db)
    rag_service = RAGService(db)
    ai_service = AIService(settings)

    try:
        session = _get_or_create_session(chat_repository, chat_request)
        chat_repository.add_message(
            session_id=session.id,
            role="user",
            content=chat_request.message,
        )

        rag_result = rag_service.retrieve(chat_request.message)
        system_prompt = _build_system_prompt(rag_result.context)
        history = chat_repository.list_recent_messages(session.id)

        try:
            ai_result = await ai_service.complete(
                system_prompt=system_prompt,
                user_message=chat_request.message,
                history=history[:-1],
            )
        except (AIProviderTimeoutError, AIProviderRequestError) as exc:
            logging.warning(f"AI Provider failed: {exc}. Falling back gracefully to mock provider.")
            fallback_settings = get_settings().model_copy(update={"ai_provider": "mock"})
            fallback_service = AIService(fallback_settings)
            fallback_result = await fallback_service.complete(
                system_prompt=system_prompt,
                user_message=chat_request.message,
                history=history[:-1],
            )
            ai_result = AIResult(
                content=f"[Fallback] {fallback_result.content}",
                model=f"fallback:{fallback_result.model}",
                raw_response={"fallback_error": str(exc)}
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

Rules:
1. Answer clearly and simply.
2. Use Indonesian if the user asks in Indonesian. Use English if the user asks in English.
3. If the user asks for product recommendation, ask or infer: budget, use case, performance need, and portability need.
4. Do not invent product availability.
5. Explain technical terms in simple language.

Retrieved knowledge context:
{retrieved_context}
"""
