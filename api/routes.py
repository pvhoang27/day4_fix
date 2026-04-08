from fastapi import APIRouter, HTTPException, Path, Query, Header, Cookie
from typing import List, Optional
from models.blog import BlogPostCreate, BlogPostResponse, BlogPostUpdate
from services import blog as blog_service

router = APIRouter(prefix="/blogs", tags=["Blogs"])

# CREATE: Tạo bài viết mới (có demo đọc Header)
@router.post("/", response_model=BlogPostResponse)
def create_blog_post(
    post: BlogPostCreate, 
    user_agent: Optional[str] = Header(None, description="Lấy thông tin User-Agent từ Header")
):
    print(f"Request từ trình duyệt/client: {user_agent}")
    return blog_service.create_post(post)

# READ: Lấy danh sách bài viết (có demo Query Param và Cookie)
@router.get("/", response_model=List[BlogPostResponse])
def get_blogs(
    limit: int = Query(10, ge=1, le=50, description="Số lượng bài viết tối đa cần lấy"),
    session_token: Optional[str] = Cookie(None, description="Đọc token từ Cookie (nếu có)")
):
    print(f"Session Token từ Cookie: {session_token}")
    return blog_service.get_all_posts(limit=limit)

# READ: Lấy chi tiết 1 bài viết (sử dụng Path Param)
@router.get("/{post_id}", response_model=BlogPostResponse)
def get_blog_by_id(
    post_id: int = Path(..., title="ID của bài viết cần tìm", ge=1)
):
    post = blog_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return post

# UPDATE: Cập nhật bài viết
@router.put("/{post_id}", response_model=BlogPostResponse)
def update_blog_post(
    post_update: BlogPostUpdate,
    post_id: int = Path(..., ge=1)
):
    updated_post = blog_service.update_post(post_id, post_update)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để cập nhật")
    return updated_post

# DELETE: Xóa bài viết
@router.delete("/{post_id}")
def delete_blog_post(post_id: int = Path(..., ge=1)):
    success = blog_service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để xóa")
    return {"message": "Đã xóa bài viết thành công"}