from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.feedback import Feedback
from app.models.chat import ChatMessage
from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    message = db.get(ChatMessage, request.message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    feedback = Feedback(
        message_id=request.message_id,
        rating=request.rating,
        comment=request.comment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return FeedbackResponse(
        id=feedback.id,
        message_id=feedback.message_id,
        rating=feedback.rating,
        status="success"
    )
