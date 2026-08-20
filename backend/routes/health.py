from datetime import UTC, datetime

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "quickdrop-backend",
        "timestamp": datetime.now(UTC).isoformat(),
    }

