# 📚 FuseCode Book API

A modern, asynchronous REST API for managing books, built using **FastAPI**, **SQLAlchemy 2.0 async ORM**, and **aiosqlite**. Includes full integration and CRUD test suites using `pytest`, `pytest-asyncio`, and `httpx`.

---

## 🚀 Features

- Async FastAPI endpoints
- SQLAlchemy 2.0 async ORM with `aiosqlite`
- Full CRUD functionality for books
- Modular and testable codebase
- Two test suites:
  - `test_crud.py` for DB logic
  - `test_api.py` for HTTP API layer
- Fully typed with `pyproject.toml` and `uv` support

---

## 📦 Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (recommended Python package manager)
- SQLite3 (included with Python)

---

## 📁 Project Structure

```
fusecode-task/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_curd.py
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## ⚙️ Setup & Installation

### ✅ 1. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e .[test]
```

---

## ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

Visit the API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📖 API Endpoints

| Method | Endpoint       | Description           |
|--------|----------------|-----------------------|
| GET    | `/books/`      | List all books        |
| GET    | `/books/{id}`  | Get book by ID        |
| POST   | `/books/`      | Create a new book     |
| PUT    | `/books/{id}`  | Update a book         |
| DELETE | `/books/{id}`  | Delete a book         |

---

## 🧪 Run Tests

### ✅ Run all test files:

```bash
pytest
```

### 🧪 Run individual test files:

```bash
pytest tests/test_crud.py
pytest tests/test_api.py
```

---

## ✅ Example Book Payload (POST/PUT)

```json
{
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt",
  "published_year": 1999,
  "summary": "A classic book on software craftsmanship."
}
```

---

## 👨‍💻 Author

**Muhammad Usman**  
Built for the **FuseCode Task**

---