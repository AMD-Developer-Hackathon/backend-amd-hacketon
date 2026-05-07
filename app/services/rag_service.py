from dataclasses import dataclass
import logging
import re

from sqlalchemy.orm import Session

try:
    from sentence_transformers import SentenceTransformer  # type: ignore[import-untyped]
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None  # type: ignore[assignment,misc]
    _SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.getLogger(__name__).warning(
        "sentence_transformers not installed. RAG will use keyword search fallback. "
        "Run: pip install sentence-transformers"
    )

from app.models.knowledge import KnowledgeDocument
from app.repositories.knowledge_repository import KnowledgeRepository
from app.schemas.chat import Source


@dataclass(frozen=True)
class RAGResult:
    documents: list[KnowledgeDocument]
    context: str
    sources: list[Source]


class RAGService:
    def __init__(self, db: Session) -> None:
        self.knowledge_repository = KnowledgeRepository(db)

    def retrieve(self, question: str, limit: int = 3) -> RAGResult:
        documents = self.search(question, limit=limit)
        return RAGResult(
            documents=documents,
            context=self.build_context(documents),
            sources=self.to_sources(documents),
        )

    def search(self, question: str, limit: int = 3) -> list[KnowledgeDocument]:
        # Try vector search first (requires sentence_transformers + pgvector)
        if _SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                model = SentenceTransformer("all-MiniLM-L6-v2")
                query_embedding = model.encode(question).tolist()
                documents = self.knowledge_repository.search_by_embedding(query_embedding, limit=limit)
                if documents:
                    return documents
                logging.info("Vector search returned 0 results, falling back to keyword search.")
            except Exception as exc:
                logging.error(f"Vector search failed, falling back to keyword search: {exc}")

        # Fallback: keyword frequency scoring
        keywords = self._keywords(question)
        if not keywords:
            return []

        candidates = self.knowledge_repository.search_by_keywords(keywords[:8])
        ranked_documents = sorted(
            candidates,
            key=lambda document: self._score_document(document, keywords),
            reverse=True,
        )
        return ranked_documents[:limit]

    def build_context(self, documents: list[KnowledgeDocument]) -> str:
        if not documents:
            return "No internal knowledge documents were retrieved for this question."

        blocks = []
        for index, document in enumerate(documents, start=1):
            content = document.content.strip()
            if len(content) > 1200:
                content = f"{content[:1200].rstrip()}..."
            source = document.source or "internal knowledge base"
            blocks.append(f"[{index}] Title: {document.title}\nSource: {source}\nContent: {content}")
        return "\n\n".join(blocks)

    def to_sources(self, documents: list[KnowledgeDocument]) -> list[Source]:
        return [
            Source(
                id=document.id,
                title=document.title,
                source=document.source,
            )
            for document in documents
        ]

    def _keywords(self, question: str) -> list[str]:
        words = re.findall(r"[a-zA-Z0-9+#.]+", question.lower())
        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "for",
            "how",
            "is",
            "of",
            "on",
            "or",
            "the",
            "to",
            "what",
            "with",
            "yang",
            "dan",
            "atau",
            "untuk",
            "dengan",
            "apa",
            "bagaimana",
            "produk",
        }
        seen = set()
        keywords = []
        for word in words:
            if len(word) <= 2 or word in stop_words or word in seen:
                continue
            keywords.append(word)
            seen.add(word)
        return keywords

    def _score_document(self, document: KnowledgeDocument, keywords: list[str]) -> int:
        title = document.title.lower()
        source = (document.source or "").lower()
        content = document.content.lower()

        score = 0
        for keyword in keywords:
            score += title.count(keyword) * 5
            score += source.count(keyword) * 2
            score += content.count(keyword)
        return score
