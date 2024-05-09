from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password : str

class UserFull(UserBase):
    id: int

    class Config:
        from_attributes=True
