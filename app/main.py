from fastapi import FastAPI, Depends, HTTPException
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


app = FastAPI(title="Project: Book Catalog ", lifespan=lifespan)


@app.post("/books/", response_model=schemas.BookRead, status_code=201)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.BookRead])
async def list_books(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookRead)
async def update_book(
    book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
