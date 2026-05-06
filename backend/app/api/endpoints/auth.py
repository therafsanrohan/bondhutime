from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, Token
import uuid

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(
        (User.username == user_in.username) | 
        (User.email == user_in.email) | 
        (User.phone_number == user_in.phone_number)
    ).first()
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username, email, or phone number already exists in the system.",
        )
        
    user = User(
        username=user_in.username,
        email=user_in.email,
        phone_number=user_in.phone_number,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        date_of_birth=user_in.date_of_birth,
        address=user_in.address,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Form data username could be username, email, or phone
    user = db.query(User).filter(
        (User.username == form_data.username) | 
        (User.email == form_data.username) | 
        (User.phone_number == form_data.username)
    ).first()
    
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email/phone/username or password")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
