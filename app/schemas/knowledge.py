from uuid import UUID
from pydantic import BaseModel

class KnowledgeUploadRequest(BaseModel):
    title: str
    content: str
    source: str | None = None

class KnowledgeUploadResponse(BaseModel):
    id: UUID
    title: str
    status: str

class KnowledgeDocumentResponse(BaseModel):
    id: UUID
    title: str
    source: str | None
    embedding_status: str
    created_at: str | None = None  # Using string for easier serialization or datetime if configured

    class Config:
        from_attributes = True
