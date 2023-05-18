import sys
sys.path.append("../")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
import app.routes.routes_utils as utils
from app.authenticationRoutes.authentication_utils import get_db
from app.server import models
from app.server.database import engine


# router
bookRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# route for adding new book
@bookRouter.post('/add_new_book')
async def add_new_book(book: utils.CreateBook, db: Session = Depends(get_db)):
    # create a model
    new_book = models.BookModel()
    # assign properties
    new_book.bookName = book.bookName
    new_book.bookAuthor = book.bookAuthor
    new_book.count = book.count
    new_book.shelfNumber = book.shelfNumber
    new_book.racNumber = book.racNumber
    new_book.position = book.position
    new_book.collage = book.collage
    new_book.book_description = book.description
    new_book.book_id = book.book_id
    # add model to database
    db.add(new_book)
    # commit the change
    db.commit()

    db.refresh(new_book)

    if not new_book.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not added')

    return {'status': 'successful'}


# route for getting book by name
@bookRouter.post('/bookName/')
async def get_book_by_name(book_name: utils.GetBookByName, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(models.BookModel.bookName == book_name.name).filter(
        models.BookModel.collage == book_name.collage).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return books


# route for getting book by author name
@bookRouter.post('/bookAuthor/')
async def get_book_by_author_name(book_author: utils.GetBookByAuthor, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(models.BookModel.bookAuthor == book_author.author).filter(
        models.BookModel.collage == book_author.collage).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return books
