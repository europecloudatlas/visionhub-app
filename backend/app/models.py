"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"


class Board(Base):
    """Vision Board model"""
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="boards")
    images = relationship("BoardImage", back_populates="board", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Board(name='{self.name}')>"


class BoardImage(Base):
    """Board Image model"""
    __tablename__ = "board_images"
    
    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    board = relationship("Board", back_populates="images")
    
    def __repr__(self):
        return f"<BoardImage(filename='{self.filename}')>"