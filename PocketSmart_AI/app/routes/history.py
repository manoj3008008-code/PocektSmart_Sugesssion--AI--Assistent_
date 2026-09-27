import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user_id
from app.models.models import RecommendationHistory

router = APIRouter()

@router.get("/history")
def history(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    rows = db.query(RecommendationHistory).filter_by(user_id=user_id).order_by(RecommendationHistory.id.desc()).limit(50).all()
    return {"items":[{"id":r.id,"planner":r.planner,"request":json.loads(r.request_json),
                      "response":json.loads(r.response_json),"created_at":r.created_at.isoformat()} for r in rows]}
