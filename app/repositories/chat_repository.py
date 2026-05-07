from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage, ChatSession


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_session(self, session_id: UUID) -> ChatSession | None:
        return self.db.get(ChatSession, session_id)

    def create_session(self, user_id: UUID | None, title: str | None = None) -> ChatSession:
        session = ChatSession(user_id=user_id, title=title)
        self.db.add(session)
        self.db.flush()
        return session

    def add_message(
        self,
        session_id: UUID,
        role: str,
        content: str,
        latency_ms: int | None = None,
        model_name: str | None = None,
    ) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            latency_ms=latency_ms,
            model_name=model_name,
        )
        self.db.add(message)
        self.db.flush()
        return message

    def list_recent_messages(
        self,
        session_id: UUID,
        limit: int = 12,
    ) -> list[ChatMessage]:
        statement = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        return list(reversed(self.db.scalars(statement).all()))

    def list_sessions(self, user_id: UUID | None = None, limit: int = 20) -> list[ChatSession]:
        statement = select(ChatSession)
        if user_id:
            statement = statement.where(ChatSession.user_id == user_id)
        statement = statement.order_by(ChatSession.updated_at.desc()).limit(limit)
        return list(self.db.scalars(statement).all())
