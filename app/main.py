from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from app.database import engine, Base
from app.routers import books


app = FastAPI(
    title="Book Storage API",
    description="Collect your your books in one space",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(books.router)

app.add_middleware(DBSessionMiddleware, db_url="sqlite:///./test.db")
