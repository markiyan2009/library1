import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query, status

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from database.ORM import ORM
from database.models import Book, User
from schemas.book import BookBase, BookFull
from schemas.user import UserBase, UserFull

app = FastAPI(title="invent_products")
library = {}
security = HTTPBasic()


def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credits.username, ORM.auth_username(credits.username))
    correct_password = secrets.compare_digest(credits.password, ORM.auth_password(credits.password))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credits.username

@app.post("/auth")
def auth(username=Depends(check_credentials)):
    return {"msg":"Авторизація пройшла успішно"}

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

