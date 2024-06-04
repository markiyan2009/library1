import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from fastapi.staticfiles import StaticFiles
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
app.mount("/static",StaticFiles(directory="templates/css"),"static")

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
async def add_book(author:str = Form(),name:str = Form(),pages:str = Form(), credentials = Depends(check_credentials)):
    book_db = Book(author = author,name = name, pages = pages)
    ORM.add_book(book_db)
    return RedirectResponse("/home", status_code=303)


@app.get("/home", response_class=HTMLResponse) 
def home(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})


# @app.get("/author_books")
# def get_books_by_author(request:Request):
#     return templates.TemplateResponse("")
@app.get("/refill_book")
def refill(request : Request):
    return templates.TemplateResponse("refill.html",{"request":request})
@app.post("/submit_refill_book")
def submit_refill(request:Request,old_book:str = Form(),author:str = Form(),name:str = Form(),pages:str = Form(),credentials = Depends(check_credentials)):
    
    ORM.refil_book(old_book,name,author,pages)
    
    return RedirectResponse("/home",status_code=303)
    

@app.get("/info")
def info(request : Request):
    return templates.TemplateResponse("info.html",{"request": request,"books" : ORM.get_all_books()})
@app.get("/delete")
def delete(request:Request):
    return templates.TemplateResponse("delete.html",{"request":request})
@app.post("/submit_delete")
def submit_delete(name:str = Form(),credentials = Depends(check_credentials)):
    ORM.delete_author(name)
    return RedirectResponse("/home",status_code=303)
