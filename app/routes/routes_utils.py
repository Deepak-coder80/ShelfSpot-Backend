import sys
sys.path.append("../")

from pydantic import BaseModel
from sqlalchemy import null

from app.server.database import SessionLocal


### Question Paper Utils Models ###

# add new question paper model
class CreateQuestionPaper(BaseModel):
    qnSubName: str
    qnMonth: str
    qnScheme: int
    qnSemester: int
    qnYear: int
    qnLink: str
    collage: str

# get question paper by it's name request model
class GetQnPaperByName(BaseModel):
    name: str
    collage: str

# get question paper by semester request model
class GetQnPaperBySemester(BaseModel):
    semester: int
    collage: str

### Book Utils Models ###

# create new book model
class CreateBook(BaseModel):

    bookName: str
    bookAuthor: str
    count: int
    shelfNumber: int
    racNumber: int
    position: int
    collage: str
    description: str
    book_id: int

# get book  by it's name request model
class GetBookByName(BaseModel):
    name: str
    collage: str

# get book by author name  request model
class GetBookByAuthor(BaseModel):
    author: str
    collage: str


