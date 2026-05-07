from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

class RatingEnum(str, Enum):
    helpful = "helpful"
    not_helpful = "not_helpful"
    unclear = "unclear"
    incorrect = "incorrect"

class FeedbackRequest(BaseModel):
    message_id: UUID
    rating: RatingEnum = Field(..., description="Rating (e.g., helpful, not_helpful)")
    comment: str | None = None

class FeedbackResponse(BaseModel):
    id: UUID
    message_id: UUID
    rating: str
    status: str
