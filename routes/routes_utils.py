from pydantic import BaseModel
from sqlalchemy import null

from server.database import SessionLocal


class CreateQuestionPaper(BaseModel):
    qnSubName: str
    qnMonth: str
    qnScheme: int
    qnSemester: int
    qnYear: int
    qnLink: str
    collage: str


class GetQnPaperByName(BaseModel):
    name: str
    collage: str


class GetQnPaperBySemester(BaseModel):
    semester: int
    collage: str


class CreateBook(BaseModel):

    bookName: str
    bookAuthor: str
    count: int
    shelfNumber: int
    racNumber: int
    position: int
    collage: str


class GetBookByName(BaseModel):
    name: str
    collage: str


class GetBookByAuthor(BaseModel):
    author: str
    collage: str


def get_db():
    db = null
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

