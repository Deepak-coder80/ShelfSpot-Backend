# routes for question paper management
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from server import models
from server.database import engine, SessionLocal
from jose import jwt
import os

# router
qnPaperRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)

# get environment files
load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('JWT_ALGORITHM')


# route for getting qnpaper by subject

def create_jwt_for_qn_subject(subject: str, qn_id: int, link: str):
    # create jwt message
    encode = {"id": qn_id, "subjectName": subject, "link": link}
    # return jwt encoded with secret key and algorithm
    return jwt.encode(encode, secret_key, algorithm=algorithm)


# route for getting qnpaper by semester

def create_jwt_for_qn_semester(semester: str, qn_id: int, link: str):
    # create jwt message
    encode = {"id": qn_id, "semester": semester, "link": link}
    # return jwt encoded with secret key and algorithm
    return jwt.encode(encode, secret_key, algorithm=algorithm)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# route for get question paper by subject name
@qnPaperRouter.get('/qPaperSub/{subjectName}')
async def read_qn_paper_by_name(subjectName: str, db: Session = Depends(get_db)):
    qnPapers = db.query(models.QuestionPaperModel).filter(models.QuestionPaperModel.qnSubName == subjectName).all()
    if not qnPapers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question Papers not found')
    return qnPapers


# route for getting question paper by semeter
@qnPaperRouter.get('/qPaperSem/{semester}')
async def read_qn_paper_by_semester(semester: int, db: Session = Depends(get_db)):
    qnPapers = db.query(models.QuestionPaperModel).filter(models.QuestionPaperModel.qnSemester == semester).all()
    if not qnPapers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question Papers not found')
    return qnPapers


# model for new question paper also reading form
class CreateQuestionPaper(BaseModel):
    qnSubName: str
    qnMonth: str
    qnScheme: int
    qnSemester: int
    qnYear: int
    qnLink: str


# route for adding new question paper
@qnPaperRouter.post('/addqnpaper')
async def add_question_paper(qnPaper: CreateQuestionPaper, db: Session = Depends(get_db)):
    # create a model
    new_qn_paper = models.QuestionPaperModel()
    # assign properties
    new_qn_paper.qnSubName = qnPaper.qnSubName
    new_qn_paper.qnSemester = qnPaper.qnSemester
    new_qn_paper.qnLink = qnPaper.qnLink
    new_qn_paper.qnMonth = qnPaper.qnMonth
    new_qn_paper.qnYear = qnPaper.qnYear
    new_qn_paper.qnScheme = qnPaper.qnScheme
    # add model to database
    db.add(new_qn_paper)
    # commit the change
    db.commit()
    return {'status': 'successful'}
