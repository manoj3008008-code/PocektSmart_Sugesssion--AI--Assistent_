from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import RegisterRequest, LoginRequest, UserResponse
from app.services.auth import create_user, authenticate
from app.core.security import create_access_token, get_current_user_id
from app.models.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, data.name, data.email, data.password)
    if not user:
        raise HTTPException(409, "Email is already registered")
    return user

@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate(db, data.email, data.password)
    if not user:
        raise HTTPException(401, "Invalid email or password")
    token = create_access_token(user.id)
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return {"message":"Login successful", "access_token":token, "user":{"id":user.id,"name":user.name,"email":user.email}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message":"Logged out"}

@router.get("/session-info")
def session_info(request: Request, db: Session = Depends(get_db)):
    try:
        user_id = get_current_user_id(request)
        user = db.get(User, user_id)
        return {"logged_in": bool(user), "user": {"id":user.id,"name":user.name,"email":user.email} if user else None}
    except HTTPException:
        return {"logged_in": False, "user": None}

@router.get("/session-data")
def session_data(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    user = db.get(User, user_id)
    return {"user_id": user_id, "name": user.name, "email": user.email}
