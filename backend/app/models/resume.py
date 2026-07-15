from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    skills = Column(String)

    education = Column(String)

    projects = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")