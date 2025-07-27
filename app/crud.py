from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    """Create a new book in the database.

    Args:
        db (AsyncSession): The async SQLAlchemy session to use.
        book (schemas.BookCreate): The book to create.

    Returns:
        models.Book: The created book."""
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_all_books(db: AsyncSession):
    """Get all books in the database.

    Args:
        db (AsyncSession): The async SQLAlchemy session to use.

    Returns:
        list[models.Book]: A list of all books in the database."""

    result = await db.execute(select(models.Book))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    """Get a book from the database by its ID.

    Args:
        db (AsyncSession): The async SQLAlchemy session to use.
        book_id (int): The ID of the book to retrieve.

    Returns:
        models.Book: The book with the given ID, or None if it does not exist."""

    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate):
    """Update a book in the database by its ID.

    Args:
        db (AsyncSession): The async SQLAlchemy session to use.
        book_id (int): The ID of the book to update.
        book (schemas.BookUpdate): The book data to update.

    Returns:
        models.Book: The updated book, or None if it does not exist."""

    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book
