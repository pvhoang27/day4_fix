from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    content: str = Field(..., min_length=10)


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    content: str | None = Field(default=None, min_length=10)


class BlogPostResponse(BlogPostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: Literal["user", "admin"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
