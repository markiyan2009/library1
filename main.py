
import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from database.ORM import ORM
from database.models import Book
from schemas.book import BookBase, BookFull
app = FastAPI(title="invent_products")
library = {}
users = [{"username":"ya","password":"1234"}]


def check_credentials(username: str, password: str):
    for user in users:
        if username != user["username"] and password != user["password"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Помилка!!!!!")
    return username


@app.post("/add_book")
def add_book(book : BookBase, username = Depends(check_credentials)):
    print(username)
    book_db = Book(author = book.author,name = book.name, pages = book.pages)
    ORM.add_book(book_db)
    return "Книжка додана"
@app.get("/{author}_books")
def get_books_by_author(author : str):
    return ORM.get_book_by_author(author)
@app.patch("/refill_{name}")
def refill(name : str, book : BookBase):
    return ORM.refil_book(name=name, new_book=book)
def delete_book(name:str):
    
    return ORM.delete_author(name)

@app.post("/add_user")
def add_user(username:str, password:str):
    
    users.append({"username":username,"password":password})
    return "Користувач доданий"