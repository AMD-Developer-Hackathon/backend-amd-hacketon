from fastapi import Header, HTTPException, status
from app.config import get_settings

async def verify_admin_key(x_admin_key: str = Header(...)):
    if x_admin_key != get_settings().admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin key",
        )
