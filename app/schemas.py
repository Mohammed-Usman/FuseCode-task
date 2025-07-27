from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    published_year: int = Field(..., ge=1450, le=2100)
    summary: Optional[str] = None
