"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


# ==========================================
# USER SCHEMAS
# ==========================================

class UserCreate(BaseModel):
    """User registration schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class UserResponse(BaseModel):
    """User response schema (no password)"""
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded token data"""
    username: Optional[str] = None


# ==========================================
# BOARD SCHEMAS
# ==========================================

class BoardCreate(BaseModel):
    """Create board schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class BoardUpdate(BaseModel):
    """Update board schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None


class BoardImageResponse(BaseModel):
    """Board image response"""
    id: int
    image_url: str
    filename: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class BoardResponse(BaseModel):
    """Board response with images"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    images: List[BoardImageResponse] = []
    
    class Config:
        from_attributes = True


class BoardListItem(BaseModel):
    """Board list item (without images)"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    image_count: int
    
    class Config:
        from_attributes = True