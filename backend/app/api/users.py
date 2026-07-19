from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import UploadFile, File
import os
import shutil

from app.ai.matcher import match_skills
from app.models.job import Job
from app.models.resume import Resume
from app.schemas.user import UserCreate
from app.models.user import User
from app.database.database import get_db
from app.auth.security import hash_password, verify_password
from app.schemas.user import UserLogin
from app.auth.jwt_handler import create_access_token
from app.auth.oauth2 import get_current_user
from app.parser.resume_parser import extract_text_from_pdf
from app.parser.info_parser import (
    extract_name,
    extract_email,
    extract_phone, 
    extract_skills,
    extract_education,
    extract_projects
)
from app.parser.job_parser import extract_job_title
from app.ai.ats_scorer import (
    calculate_ats_score,
    calculate_education_score,
    calculate_project_score,
    calculate_keyword_score
)

from app.ai.recommendation import (
    get_match_level,
    get_recommendations,
    get_strengths
)

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
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    upload_folder = "uploads/resumes"

    os.makedirs(upload_folder, exist_ok=True)
    import uuid
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(
        upload_folder,unique_filename
    )
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )
    text=extract_text_from_pdf(file_path)
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    print("Extracted Education:", education)
    projects = extract_projects(text)

    new_resume = Resume(
    filename=file.filename,
    name=name,
    email=email,
    phone=phone,
    skills=", ".join(skills),
    education=", ".join(education),
    projects=", ".join(projects),
    raw_text=text,
    user_id=user.id
)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    print(skills)
    return{
        "message": "Resume uploaded successfull",
        "resume_id": new_resume.id,
        "filename": file.filename,
        "candidate": {
            "name": name,
            "email": email,
            "phone": phone, 
            "skills": skills,
            "education": education,
            "projects": projects
        }
    }


@router.post("/upload-job")


def upload_job(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    upload_folder="uploads/jobs"
    os.makedirs(upload_folder, exist_ok=True)

    import uuid
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(
        upload_folder,
        unique_filename
    )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file,  buffer)
    text = extract_text_from_pdf(file_path)
    skills=extract_skills(text)
    title = extract_job_title(text)
    new_job = Job(
        title=title,
        filename=unique_filename,
        description=text,
        skills=", ".join(skills)
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return{
        'message': "Job uploaded suceesfully",
        'job_id': new_job.id,
        'title': title,
        'filename': file.filename,
        'skills': skills        
        }


@router.get("/match-resume/{resume_id}/{job_id}")


def match_resume(
    resume_id: int,
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail = "Resume not found"
        )
    job= db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    resume_skills = (
        resume.skills.split(", ")
        if resume.skills 
        else []
    )
    job_skills = (
        job.skills.split(", ")
        if job.skills
        else []
    )

    skill_result = match_skills(
        resume_skills,
        job_skills
    )

    skill_score = skill_result["score"]
    education_score = calculate_education_score(
        resume.education,
        job.description
    )
    project_score = calculate_project_score(
        resume.projects,
        job_skills
    )
    keyword_score = calculate_keyword_score(
        resume.raw_text,
        job_skills
    )
    ats_score = calculate_ats_score(
        skill_score,
        education_score,
        project_score,
        keyword_score
    )

    match_level = get_match_level(ats_score)
    
    strenghts = get_strengths(
        skill_result["matched"]
    )

    recommendations = get_recommendations(
        skill_result['missing']
    )

    return {
        "resume_id": resume.id,
        "job_id": job.id,

        "candidate": resume.name,
        "job_title": job.title,

        "ats_score": ats_score,

        "score_breakdown": {
            "skill_score": skill_score,
            "education_score": education_score,
            "project_score": project_score,
            "keyword_score": keyword_score 
        },

        "matched_skills": skill_result["matched"],
        "missing_skills": skill_result["missing"],

        "strengths": strenghts,

        "recommendation": recommendations
    }