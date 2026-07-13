from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import UploadFile, File
import os
import shutil

from app.schemas.user import UserCreate
from app.models.user import User
from app.database.database import get_db
from app.auth.security import hash_password, verify_password
from app.schemas.user import UserLogin
from app.auth.jwt_handler import create_access_token
from app.auth.oauth2 import get_current_user

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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.get("/me")
def get_me (
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    return{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...)
):
    upload_folder = "uploads/resumes"

    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(
        upload_folder,file.filename
    )
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )
    return{
        "message": "Resume uploaded successfull",
        "filename": file.filename
    }