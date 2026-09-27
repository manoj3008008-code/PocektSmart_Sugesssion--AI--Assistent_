import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import HomeRequest, PartyRequest, RecommendationResponse, JewelryRequest
from app.core.security import get_current_user_id
from app.core.config import settings
from app.services.gemini import gemini_service
from app.models.models import RecommendationHistory

router = APIRouter()

def save_history(db, user_id, planner, request_data, response_data):
    row = RecommendationHistory(user_id=user_id, planner=planner,
                                request_json=json.dumps(request_data),
                                response_json=json.dumps(response_data))
    db.add(row); db.commit()

@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home(data: HomeRequest, request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    payload = data.model_dump()
    result = gemini_service.generate_home(payload)
    save_history(db, user_id, "home", payload, result)
    return result

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(data: PartyRequest, request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    payload = data.model_dump()
    result = gemini_service.generate_party(payload)
    save_history(db, user_id, "party", payload, result)
    return result

@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    outfit_color: str = Form(""),
    outfit_notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    if budget <= 0:
        raise HTTPException(422, "Budget must be greater than zero")
    image_bytes = None
    mime = None
    if outfit_image:
        if not outfit_image.content_type or not outfit_image.content_type.startswith("image/"):
            raise HTTPException(400, "Only image uploads are supported")
        image_bytes = await outfit_image.read()
        if len(image_bytes) > settings.max_image_mb * 1024 * 1024:
            raise HTTPException(413, f"Image must be <= {settings.max_image_mb} MB")
        mime = outfit_image.content_type
    payload = {"budget":budget,"occasion":occasion,"style":style,
               "outfit_color":outfit_color or None,"outfit_notes":outfit_notes or None}
    result = gemini_service.generate_jewelry(payload, image_bytes, mime)
    save_history(db, user_id, "jewelry", payload, result)
    return result

@router.get("/recommendations-details")
def recommendation_details(request: Request, planner: str = "home", db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    row = db.query(RecommendationHistory).filter_by(user_id=user_id, planner=planner).order_by(RecommendationHistory.id.desc()).first()
    if not row:
        raise HTTPException(404, "No recommendation found")
    return json.loads(row.response_json)
