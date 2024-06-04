import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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
templates = Jinja2Templates(directory="templates")

def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    user = ORM.auth(credentials.username, credentials.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submitform")
async def index(login: str = Form(...), password: str = Form(...), credentials = Depends(check_credentials)):
    
    return RedirectResponse("/home", status_code=303)

@app.get("/add_book")
async def add_book(request : Request):
    return templates.TemplateResponse("add_book.html",{"request":request})
@app.post("/submit_add_book")
async def add_book(author:str = Form(),name:str = Form(),pages:str = Form(),submit: str = Form(), credentials = Depends(check_credentials)):
    book_db = Book(author = author,name = name, pages = pages)
    ORM.add_book(book_db)
    return RedirectResponse("/home", status_code=303)


@app.get("/home", response_class=HTMLResponse) 
def home(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})
@app.post("/submithome")
def submithome(b_add:str = Form(),b_refill:str=Form(),b_delete:str=Form(),b_info:str=Form()):
    
    if b_add:
        print("redirect")
        return RedirectResponse("/add_book",status_code=303)
    if b_refill:
        return RedirectResponse("/refill_book",status_code=303)
    if b_delete:
        return RedirectResponse("/delete_book",status_code=303)
    if b_info:
        return RedirectResponse("/info",status_code=303)
    

@app.get("/{author}_books")
def get_books_by_author(author : str, username = Depends(check_credentials)):
    return ORM.get_book_by_author(author)
@app.patch("/refill_book")
def refill(name : str, book : BookBase,username = Depends(check_credentials)):
    return ORM.refil_book(name=name, new_book=book)
@app.delete("/delete_book")
def delete_book(name:str, username = Depends(check_credentials)):
    
    return ORM.delete_author(name)
@app.get("/info")
def info(request : Request):
    return templates.TemplateResponse("info.html",{"request": request,"books" : ORM.get_all_books()})
