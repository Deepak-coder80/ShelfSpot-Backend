import sys
sys.path.append("../")

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.server import models
from app.server.database import engine
import app.routes.routes_utils as utils
from app.authenticationRoutes.authentication_utils import get_db

unverifed_qp_router = APIRouter(prefix='qp/unverified')
models.Base.metadata.create_all(bind=engine)

@unverifed_qp_router.post('/add')
async def add_unverified_qp(qp: utils.CreateQuestionPaper, db: Session = Depends(get_db)):
   new_unverifed_qp = models.UnVerifiedQuestionPaperModel()

   new_unverifed_qp.qnSubName = qp.qnSubName
   new_unverifed_qp.qnSemester = qp.qnSemester
   new_unverifed_qp.qnLink = qp.qnLink
   new_unverifed_qp.qnMonth = qp.qnMonth
   new_unverifed_qp.qnYear = qp.qnYear
   new_unverifed_qp.qnScheme = qp.qnScheme
   new_unverifed_qp.collage = qp.collage

   db.add(new_unverifed_qp)
   db.commit()
   db.refresh(new_unverifed_qp)

   if not new_unverifed_qp.id:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book not added')

   return {'status': 'successful'}

@unverifed_qp_router.post('/read/all/{collage_name}')
async def read_all_unverified_qp(collage_name: str, db: Session = Depends(get_db)):
   question_paper = db.query(models.UnVerifiedQuestionPaperModel)\
    .filter(models.UnVerifiedQuestionPaperModel.collage == collage_name).all()
   
   if not question_paper:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No QP find')
   return question_paper

@unverifed_qp_router.post('/verify/{book_id}')
async def read_all_unverified_qp(book_id: int, db: Session = Depends(get_db)):
   qn_paper = db.query(models.UnVerifiedQuestionPaperModel)\
    .filter(models.UnVerifiedQuestionPaperModel.id == book_id).first()
   
   if not qn_paper:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No QP find')
   new_qn_paper = models.QuestionPaperModel()
    # assign properties
   new_qn_paper.qnSubName = qn_paper.qnSubName
   new_qn_paper.qnSemester = qn_paper.qnSemester
   new_qn_paper.qnLink = qn_paper.qnLink
   new_qn_paper.qnMonth = qn_paper.qnMonth
   new_qn_paper.qnYear = qn_paper.qnYear
   new_qn_paper.qnScheme = qn_paper.qnScheme
   new_qn_paper.collage = qn_paper.collage

   db.add(new_qn_paper)
   db.commit()
   db.refresh(new_qn_paper)
   if not new_qn_paper.id:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='some error occured')
   db.delete(qn_paper)
   return {'message':'verified'}



