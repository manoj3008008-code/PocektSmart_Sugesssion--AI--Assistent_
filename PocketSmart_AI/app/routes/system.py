from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return {"status":"ok","service":settings.app_name,"ai_mode":"mock" if settings.use_mock_ai else "gemini",
            "model":settings.gemini_model}
