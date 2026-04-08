from fastapi import FastAPI
from api.routes import router as blog_router

app = FastAPI(
    title="Day 4 - Blog Cá Nhân API",
    description="CRUD API cho ứng dụng Blog, minh họa Pydantic, Path/Query Params, Header/Cookie."
)

# Đăng ký các routes
app.include_router(blog_router)

@app.get("/")
def root():
    return {"message": "Welcome to Blog API Day 4. Truy cập /docs để xem Swagger UI."}