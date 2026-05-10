from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded  # type: ignore[import-untyped, import-not-found]
from app.dependencies.limiter import limiter

import app.models  # noqa: F401
from app.config import get_settings
from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.feedback import router as feedback_router
from app.routes.admin import router as admin_router
from app.routes.metrics import router as metrics_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

from slowapi import _rate_limit_exceeded_handler  # type: ignore[import-untyped, import-not-found]

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # pyright: ignore[reportArgumentType]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://investmateai.cloud",
        "https://www.investmateai.cloud",
        "http://localhost:3000/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(chat_router, prefix=settings.api_prefix)
app.include_router(feedback_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)
app.include_router(metrics_router, prefix=settings.api_prefix)
