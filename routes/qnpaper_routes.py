# routes for question paper management
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from routes.routes_utils import CreateQuestionPaper, GetQnPaperBySemester, GetQnPaperByName, get_db
from server import models
from server.database import engine

# router
qnPaperRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# route for adding new question paper
@qnPaperRouter.post('/add_qn_paper')
async def add_question_paper(qn_paper: CreateQuestionPaper, db: Session = Depends(get_db)):
    # create a model
    new_qn_paper = models.QuestionPaperModel()
    # assign properties
    new_qn_paper.qnSubName = qn_paper.qnSubName
    new_qn_paper.qnSemester = qn_paper.qnSemester
    new_qn_paper.qnLink = qn_paper.qnLink
    new_qn_paper.qnMonth = qn_paper.qnMonth
    new_qn_paper.qnYear = qn_paper.qnYear
    new_qn_paper.qnScheme = qn_paper.qnScheme
    new_qn_paper.collage = qn_paper.collage
    # add model to database
    db.add(new_qn_paper)
    # commit the change
    db.commit()
    db.refresh(new_qn_paper)

    if not new_qn_paper.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not added')

    return {'status': 'successful'}


# route for get question paper by subject name
@qnPaperRouter.post('/qPaperSub/')
async def read_qn_paper_by_name(qn_paper: GetQnPaperByName, db: Session = Depends(get_db)):
    qn_papers = db.query(models.QuestionPaperModel) \
        .filter(models.QuestionPaperModel.qnSubName == qn_paper.name) \
        .filter(models.QuestionPaperModel.collage == qn_paper.collage) \
        .all()
    if not qn_papers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question Papers not found')
    return qn_papers


# route for getting question paper by semester
@qnPaperRouter.post('/qPaperSem/')
async def read_qn_paper_by_semester(qn_paper: GetQnPaperBySemester, db: Session = Depends(get_db)):
    qn_papers = db.query(models.QuestionPaperModel) \
        .filter(models.QuestionPaperModel.qnSemester == qn_paper.semester) \
        .filter(models.QuestionPaperModel.collage == qn_paper.collage) \
        .all()
    if not qn_papers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question Papers not found')
    return qn_papers
