from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.blog import BlogPost
from models.schemas import BlogPostCreate, BlogPostUpdate


async def get_all_posts(db: AsyncSession, limit: int = 10) -> list[BlogPost]:
    stmt = select(BlogPost).order_by(BlogPost.id.desc()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_post_by_id(db: AsyncSession, post_id: int) -> BlogPost | None:
    stmt = select(BlogPost).where(BlogPost.id == post_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_post(db: AsyncSession, post: BlogPostCreate, author_id: int) -> BlogPost:
    new_post = BlogPost(title=post.title, content=post.content, author_id=author_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


async def update_post(db: AsyncSession, post: BlogPost, post_update: BlogPostUpdate) -> BlogPost:
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post: BlogPost) -> None:
    await db.delete(post)
    await db.commit()