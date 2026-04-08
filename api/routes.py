from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from models.schemas import (
    BlogPostCreate,
    BlogPostResponse,
    BlogPostUpdate,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from models.user import User
from services import auth as auth_service
from services import blog as blog_service
from services.background import write_blog_created_event

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = await auth_service.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/auth/register", response_model=UserResponse, tags=["Auth"], status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_username = await auth_service.get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = await auth_service.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=auth_service.hash_password(user_data.password),
        role="user",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = auth_service.create_access_token(subject=user.username, role=user.role)
    return TokenResponse(access_token=access_token)


@router.get("/blogs", response_model=list[BlogPostResponse], tags=["Blogs"])
async def get_blogs(
    limit: int = Query(10, ge=1, le=50, description="Số lượng bài viết tối đa cần lấy"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    _ = current_user
    return await blog_service.get_all_posts(db, limit=limit)


@router.get("/blogs/{post_id}", response_model=BlogPostResponse, tags=["Blogs"])
async def get_blog_by_id(
    post_id: int = Path(..., title="ID của bài viết cần tìm", ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    _ = current_user
    post = await blog_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return post


@router.post("/blogs", response_model=BlogPostResponse, tags=["Blogs"], status_code=201)
async def create_blog_post(
    post: BlogPostCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    created_post = await blog_service.create_post(db, post, author_id=current_user.id)
    background_tasks.add_task(write_blog_created_event, created_post.id, current_user.id)
    return created_post


@router.put("/blogs/{post_id}", response_model=BlogPostResponse, tags=["Blogs"])
async def update_blog_post(
    post_update: BlogPostUpdate,
    post_id: int = Path(..., ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = await blog_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để cập nhật")

    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền sửa bài viết này")

    return await blog_service.update_post(db, post, post_update)


@router.delete("/blogs/{post_id}", tags=["Blogs"])
async def delete_blog_post(
    post_id: int = Path(..., ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    post = await blog_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để xóa")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Chỉ admin mới được xóa bài viết")

    await blog_service.delete_post(db, post)
    return {"message": "Đã xóa bài viết thành công"}