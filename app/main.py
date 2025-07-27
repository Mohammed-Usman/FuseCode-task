from fastapi import FastAPI, Depends
from fastapi.concurrency import asynccontextmanager
from app import crud, schemas
from app.database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Startup complete
    # Optional: add async shutdown logic here


app = FastAPI(title="Book Catalog API (Async + aiosqlite)", lifespan=lifespan)


@app.post("/books/", response_model=schemas.BookRead, status_code=201)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db, book)
