from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeDocument


class KnowledgeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

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
