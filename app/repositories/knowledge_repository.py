from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeDocument


class KnowledgeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_document(self, title: str, content: str, source: str | None = None, embedding: list[float] | None = None) -> KnowledgeDocument:
        doc = KnowledgeDocument(
            title=title,
            content=content,
            source=source,
            embedding=embedding,
            embedding_status="completed" if embedding else "pending"
        )
        self.db.add(doc)
        self.db.flush()
        return doc

    def search_by_embedding(
        self,
        query_embedding: list[float],
        limit: int = 3,
    ) -> list[KnowledgeDocument]:
        statement = (
            select(KnowledgeDocument)
            .where(KnowledgeDocument.embedding != None)
            .order_by(KnowledgeDocument.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def search_by_keywords(
        self,
        keywords: list[str],
        candidate_limit: int = 20,
    ) -> list[KnowledgeDocument]:
        if not keywords:
            return []

        conditions = []
        for keyword in keywords:
            pattern = f"%{keyword}%"
            conditions.extend(
                [
                    KnowledgeDocument.title.ilike(pattern),
                    KnowledgeDocument.source.ilike(pattern),
                    KnowledgeDocument.content.ilike(pattern),
                ]
            )

        statement = (
            select(KnowledgeDocument)
            .where(or_(*conditions))
            .order_by(KnowledgeDocument.updated_at.desc())
            .limit(candidate_limit)
        )
        return list(self.db.scalars(statement).all())

    def list_documents(self, limit: int = 100) -> list[KnowledgeDocument]:
        statement = (
            select(KnowledgeDocument)
            .order_by(KnowledgeDocument.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def delete_document(self, doc_id) -> bool:
        doc = self.db.get(KnowledgeDocument, doc_id)
        if not doc:
            return False
        self.db.delete(doc)
        return True
