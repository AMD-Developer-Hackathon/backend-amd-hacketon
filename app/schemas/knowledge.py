from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

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
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
