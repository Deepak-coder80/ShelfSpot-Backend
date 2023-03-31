from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from server import models
from server.database import engine, SessionLocal

import os

#router

bookRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)

# get environment files
load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('JWT_ALGORITHM')

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# route for getting book by name
@bookRouter.get('/bookName/{bookName}')
async def get_book_by_name(bookName: str, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(models.BookModel.bookName == bookName).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return books


# route for getting book by author name
@bookRouter.get('/bookAuthor/{bookAuthor}')
async def get_book_by_author_name(bookAuthor: str, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(models.BookModel.bookAuthor == bookAuthor ).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return books

# model for new book
class CreateBook(BaseModel):

    bookName: str
    bookAuthor: str
    count: int
    shelfNumber: int
    racNumber: int
    position: int

# route for adding new book
@bookRouter.post('/addnewbook')
async def add_new_book(book: CreateBook, db: Session = Depends(get_db)):
    # create a model
    new_book = models.BookModel()
    # assign properties
    new_book.bookName = book.bookName
    new_book.bookAuthor = book.bookAuthor
    new_book.count = book.count
    new_book.shelfNumber = book.shelfNumber
    new_book.racNumber = book.racNumber
    new_book.position = book.position
    # add model to database
    db.add(new_book)
    # commit the change
    db.commit()
    return {'status': 'successful'}
