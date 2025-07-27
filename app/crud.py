from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_all_books(db: AsyncSession):
    result = await db.execute(select(models.Book))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate):
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
