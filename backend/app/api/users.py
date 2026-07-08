from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate
from app.models.user import User
from app.database.database import get_db
from app.auth.security import hash_password, verify_password
from app.schemas.user import UserLogin
from app.auth.jwt_handler import create_access_token

router=APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return {
    "message": "User registered successfully",
    "user_id": new_user.id
}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail = "Invalid email or password"
        )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
        data={"sub": db_user.email}
    )
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }