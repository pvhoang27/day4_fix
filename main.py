import time

from fastapi import FastAPI
from fastapi import Request

from api.routes import router as blog_router

app = FastAPI(
    title="Day 5-7 - Blog API Service",
    description="Blog API với MySQL, Alembic, JWT Auth, RBAC, Middleware, Background Tasks và Docker.",
)


@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


app.include_router(blog_router)


@app.get("/")
def root():
    return {"message": "Welcome to Blog API Day 5-7. Truy cap /docs de test API."}