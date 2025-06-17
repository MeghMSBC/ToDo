from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String,index=True)
    description = Column(String)
    completed = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("user.id"))
