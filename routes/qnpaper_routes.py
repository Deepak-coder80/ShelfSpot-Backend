from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from server import models
from server.database import engine, SessionLocal
from jose import jwt
import sys
import os

qnPaperRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)

load_dotenv(find_dotenv())
secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')


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


@qnPaperRouter.get('/qPaperSub/{subjectName}')
async def read_qn_paper_by_name(subjectName: str, db: Session = Depends(get_db)):
    qnPapers = db.query(models.QuestionPaperModel).filter(models.QuestionPaperModel.qnSubName == subjectName).first()
    if qnPapers is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question Papers not found')
    return qnPapers