import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app import schemas, crud
from app.database import Base
import pytest_asyncio

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a new engine and session for testing
engine_test = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionTest = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def async_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionTest() as session:
        yield session


@pytest.mark.asyncio
async def test_create_book(async_db):
    book_data = schemas.BookCreate(
        title="Test Book",
        author="Test Author",
        published_year=2000,
        summary="A unit test book",
    )
    book = await crud.create_book(async_db, book_data)
    assert book.id is not None
    assert book.title == "Test Book"


@pytest.mark.asyncio
async def test_get_book(async_db):
    book = await crud.get_book(async_db, 1)
    assert book is not None
    assert book.id == 1


@pytest.mark.asyncio
async def test_get_all_books(async_db):
    books = await crud.get_all_books(async_db)
    assert isinstance(books, list)
    assert len(books) >= 1


@pytest.mark.asyncio
async def test_update_book(async_db):
    updated_data = schemas.BookUpdate(
        title="Updated Title",
        author="Updated Author",
        published_year=2022,
        summary="Updated summary",
    )
    book = await crud.update_book(async_db, 1, updated_data)
    assert book.title == "Updated Title"
    assert book.published_year == 2022


@pytest.mark.asyncio
async def test_delete_book(async_db):
    deleted = await crud.delete_book(async_db, 1)
    assert deleted is not None
    assert deleted.id == 1

    not_found = await crud.get_book(async_db, 1)
    assert not_found is None
