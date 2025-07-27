from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book
