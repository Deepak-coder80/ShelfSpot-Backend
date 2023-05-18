# student authentication routes
import sys
sys.path.append("../")

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.server import models
from app.server.database import engine
import app.authenticationRoutes.authentication_utils as utils

studentRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)



# route for creating a new student
@studentRouter.post("/create/student")
async def create_student(student: utils.CreateStudent, db: Session = Depends(utils.get_db)):
    create_student_model = models.Student()
    create_student_model.email = student.email
    create_student_model.password = utils.get_hash_password(student.password)
    create_student_model.collage = student.collage

    # add new student to the database
    db.add(create_student_model)

    # commit the transaction
    db.commit()

    return {"status": "new student created successfully"}


# get jwt token
@studentRouter.post("/tokenforstudent")
async def login_for_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    # get the student user according to entered credential
    student_user = await utils.authenticate_student(form_data.username, form_data.password, db)

    if not student_user:
        # not a student user raise an exception
        raise HTTPException(status_code=404, detail='student not found')
    else:
        # get user details and create the jwt and return
        student_det = db.query(models.Student).filter(form_data.username == models.Student.email).first()
        token = utils.create_jwt_access_token(email=student_det.email, collage=student_det.collage, student_id=student_det.id)
        return token
