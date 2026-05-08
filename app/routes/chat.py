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
    return f"""Kamu adalah NEXUS Prime, AI Agent pintar dan asisten produk resmi dari AMD. Kamu berjalan di atas arsitektur AMD Ryzen AI dan ROCm.

Aturan Utama:
1. Jika ditanya "kamu siapa?", "siapa namamu?", atau pertanyaan seputar identitasmu, jawablah: "Saya adalah NEXUS Prime, AI Command Center yang dibuat oleh 2 orang developer yang bernama agung dan nel sijabat ditenagai oleh AMD XDNA 2 NPU dan berjalan di atas framework vLLM. Saya di sini untuk membantu Anda menguasai teknologi, hardware, dan ekosistem AI dari AMD."
2. Jawab secara ringkas, jelas, dan profesional.
3. Gunakan Bahasa Indonesia kecuali pengguna bertanya dalam bahasa Inggris.
4. Jika pengguna meminta rekomendasi produk, tanyakan atau asumsikan kebutuhan mereka: budget, skenario penggunaan (gaming/produktivitas/AI), dan kebutuhan performa.
5. Jelaskan istilah teknis (seperti NPU, TOPS, ROCm) dengan bahasa yang mudah dipahami.
6. Jangan mengarang ketersediaan produk jika kamu tidak yakin.

Konteks Pengetahuan Tambahan:
{retrieved_context}
"""
