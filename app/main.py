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
    """
    Create a new book in the database.

    Args:
        book (schemas.BookCreate): The book to create.

    Returns:
        schemas.BookRead: The created book.
    """
    return await crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.BookRead])
async def list_books(db: AsyncSession = Depends(get_db)):
    """Get a list of all books in the database."""
    return await crud.get_all_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a book from the database by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.

    Returns:
        schemas.BookRead: The book with the given ID, or raises a 404 error if not found.
    """

    book = await crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookRead)
async def update_book(
    book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update a book in the database by its ID.

    Args:
        book_id (int): The ID of the book to update.
        book (schemas.BookUpdate): The updated book data.

    Returns:
        schemas.BookRead: The updated book, or raises a 404 error if not found.
    """
    updated = await crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a book from the database by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Raises:
        HTTPException: If the book does not exist, with a status code of 404 and a detail of "Book not found".
    """
    deleted = await crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
