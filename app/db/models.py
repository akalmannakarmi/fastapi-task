from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,unique=True,index=True)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False,index=True)
    hashed_password = Column(String,nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    customers = relationship("Customer", back_populates="user")
    tasks = relationship("Task", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String,primary_key=True,unique=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship("User", back_populates="refresh_tokens")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer,primary_key=True,unique=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,index=True)
    amount = Column(Integer,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", back_populates="customers")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer,primary_key=True,unique=True,index=True)
    status = Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    queued_task_id = Column(String,index=True)
    
    total_records = Column(Integer,default=0)
    failed = Column(Integer,default=0)
    succesful = Column(Integer,default=0)
    user_id = Column(Integer,ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", back_populates="tasks")
