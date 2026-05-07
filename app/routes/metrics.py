from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import datetime

from app.database import get_db
from app.models.chat import ChatMessage
from app.dependencies.auth import verify_admin_key
from app.config import get_settings

router = APIRouter(prefix="/admin/stats", tags=["admin", "metrics"], dependencies=[Depends(verify_admin_key)])

@router.get("")
def get_metrics(db: Session = Depends(get_db)):
    settings = get_settings()
    
    # Total requests
    total_requests = db.query(func.count(ChatMessage.id)).filter(ChatMessage.role == "assistant").scalar() or 0
    
    # Average latency
    avg_latency = db.query(func.avg(ChatMessage.latency_ms)).filter(ChatMessage.role == "assistant").scalar() or 0
    
    # Model distribution
    model_dist = {}
    model_counts = db.query(ChatMessage.model_name, func.count(ChatMessage.id)).filter(ChatMessage.role == "assistant").group_by(ChatMessage.model_name).all()
    for model_name, count in model_counts:
        key = model_name or "unknown"
        model_dist[key] = count
        
    # Requests today
    today = datetime.datetime.now(datetime.timezone.utc).date()
    # Simple query for today's requests
    today_requests = db.query(func.count(ChatMessage.id)).filter(
        ChatMessage.role == "assistant",
        func.date(ChatMessage.created_at) == today
    ).scalar() or 0

    return {
        "total_requests": total_requests,
        "avg_latency_ms": int(avg_latency),
        "model_distribution": model_dist,
        "requests_today": today_requests,
        "ai_provider": settings.ai_provider
    }
