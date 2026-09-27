from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User

def create_user(db: Session, name: str, email: str, password: str):
    existing = db.scalar(select(User).where(User.email == email.lower()))
    if existing:
        return None
    user = User(name=name.strip(), email=email.lower(), password_hash=generate_password_hash(password))
    db.add(user); db.commit(); db.refresh(user)
    return user

def authenticate(db: Session, email: str, password: str):
    user = db.scalar(select(User).where(User.email == email.lower()))
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
