from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    author:str
    name: str
    pages: int

class BookFull(BookBase):
    id: int

    class Config:
        from_attributes=True