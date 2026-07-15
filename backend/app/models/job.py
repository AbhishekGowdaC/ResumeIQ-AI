from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    filename = Column(String)
    description = Column(String)
    skills = Column(String)