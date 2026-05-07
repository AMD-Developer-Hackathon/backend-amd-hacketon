from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

try:
    from sentence_transformers import SentenceTransformer # type: ignore[import-untyped, import-not-found]
    _ST_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    _ST_AVAILABLE = False

from app.database import get_db
from app.dependencies.auth import verify_admin_key
from app.repositories.knowledge_repository import KnowledgeRepository
from app.schemas.knowledge import KnowledgeUploadRequest, KnowledgeUploadResponse, KnowledgeDocumentResponse

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(verify_admin_key)])

@router.post("/knowledge/upload", response_model=KnowledgeUploadResponse)
async def upload_knowledge(
    request: KnowledgeUploadRequest,
    db: Session = Depends(get_db)
):
    repo = KnowledgeRepository(db)
    embedding = None
    try:
        if _ST_AVAILABLE:
            model = SentenceTransformer("all-MiniLM-L6-v2")
            embedding = model.encode(request.content).tolist()
        else:
            logging.warning("SentenceTransformer not available, skipping embedding generation")
    except Exception as e:
        logging.error(f"Failed to generate embedding: {e}")
        
    doc = repo.add_document(
        title=request.title,
        content=request.content,
        source=request.source,
        embedding=embedding
    )
    db.commit()

    return KnowledgeUploadResponse(
        id=doc.id,
        title=doc.title,
        status="uploaded" if embedding else "uploaded_without_embedding"
    )

@router.get("/knowledge", response_model=list[KnowledgeDocumentResponse])
async def list_knowledge(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repo = KnowledgeRepository(db)
    docs = repo.list_documents(limit=limit)
    return [
        KnowledgeDocumentResponse(
            id=doc.id,
            title=doc.title,
            source=doc.source,
            embedding_status=doc.embedding_status,
            created_at=doc.created_at
        )
        for doc in docs
    ]

@router.delete("/knowledge/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge(
    doc_id: UUID,
    db: Session = Depends(get_db)
):
    repo = KnowledgeRepository(db)
    success = repo.delete_document(doc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    db.commit()
