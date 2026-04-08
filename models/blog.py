from pydantic import BaseModel, Field
from typing import Optional

class BlogPostBase(BaseModel):
    title: str = Field(..., title="Tiêu đề bài viết", min_length=3, max_length=100)
    content: str = Field(..., title="Nội dung bài viết", min_length=10)

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=10)

class BlogPostResponse(BlogPostBase):
    id: int