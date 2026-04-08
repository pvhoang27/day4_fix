## Blog API Training - Day 5 to Day 7

Project da duoc nang cap tu Day 4 (CRUD in-memory) len Day 5-7 voi:

- MySQL + SQLAlchemy Async
- Alembic migration
- JWT Authentication (OAuth2 Password Flow)
- Role-based access control (user/admin)
- Middleware gan header `X-Process-Time`
- Background task ghi log khi tao bai viet
- Docker + docker-compose

Day 4 checklist da co trong API hien tai:

- Pydantic validation (schema request/response)
- Path params (vi du: /blogs/{post_id})
- Query params (limit)
- Header demo (User-Agent)
- Cookie demo (session_token)

## 1) Cau truc theo huong micro service (don gian)

- `api/`: endpoint layer
- `models/`: ORM entities + Pydantic schemas
- `services/`: business logic
- `core/`: config, database
- `alembic/`: migration scripts

## 2) Chuan bi `.env` (co password DB)

Da su dung `.env` de khai bao ket noi MySQL, phu hop voi viec dung MySQL Workbench.

Vi du:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=blog
JWT_SECRET_KEY=your_super_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 3) Chay local bang `uv`

```bash
uv sync
uv run alembic upgrade head
uv run python scripts/seed_demo.py
uv run uvicorn main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

Tai khoan demo sau khi seed:

- `admin_demo / Admin123!`
- `user_demo / User123!`

## 4) Endpoints chinh

### Auth

- `POST /auth/register`: dang ky user
- `POST /auth/login`: dang nhap, tra ve bearer token

### Blogs (yeu cau Bearer token)

- `GET /blogs`
- `GET /blogs/{post_id}`
- `POST /blogs`
- `PUT /blogs/{post_id}`
- `DELETE /blogs/{post_id}` (chi admin duoc xoa)

## 5) RBAC hien tai

- `user`: tao/sua bai viet cua chinh minh
- `admin`: co them quyen xoa bai viet

## 6) Background task

Khi tao bai viet moi, he thong tao log tai:

- `logs/blog_events.log`

## 7) Chay bang Docker

```bash
docker compose up --build
```

API: `http://127.0.0.1:8000`
MySQL: `localhost:3306`

## 8) Demo nhanh bang Postman

Import collection:

- `postman/day7_blog_api.postman_collection.json`

Chay theo thu tu request trong collection:

1. Auth - Login Admin
2. Blogs - List
3. Blogs - Create
4. Blogs - Update
5. Blogs - Delete (admin)

## 9) Goi y workflow Git (theo yeu cau training)

- Commit theo Conventional Commits, vi du:
	- `feat(auth): add jwt login and register`
	- `feat(blog): migrate blog CRUD to mysql async`
	- `chore(docker): add compose for api and mysql`
- Tao PR moi ngay de review.
