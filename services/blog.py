from models.blog import BlogPostCreate, BlogPostResponse, BlogPostUpdate
from typing import List, Optional

# Fake Database
fake_db: List[BlogPostResponse] = []
current_id = 1

def get_all_posts(limit: int = 10) -> List[BlogPostResponse]:
    return fake_db[:limit]

def get_post_by_id(post_id: int) -> Optional[BlogPostResponse]:
    for post in fake_db:
        if post.id == post_id:
            return post
    return None

def create_post(post: BlogPostCreate) -> BlogPostResponse:
    global current_id
    new_post = BlogPostResponse(id=current_id, **post.model_dump())
    fake_db.append(new_post)
    current_id += 1
    return new_post

def update_post(post_id: int, post_update: BlogPostUpdate) -> Optional[BlogPostResponse]:
    for index, post in enumerate(fake_db):
        if post.id == post_id:
            updated_data = post.model_copy(update=post_update.model_dump(exclude_unset=True))
            fake_db[index] = updated_data
            return updated_data
    return None

def delete_post(post_id: int) -> bool:
    for index, post in enumerate(fake_db):
        if post.id == post_id:
            fake_db.pop(index)
            return True
    return False