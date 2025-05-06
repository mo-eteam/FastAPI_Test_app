from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'
    COMPANY_ADMIN = 'company_admin'

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    company_id = Column(String, ForeignKey('companies.id'), nullable=True)
    
    company = relationship("Company", backref="users")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    prompts = relationship("PromptManagement", back_populates="company")

class PromptManagement(Base):
    __tablename__ = "prompt_management"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, ForeignKey('companies.id'), nullable=False)
    prompt_title = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="prompts")
