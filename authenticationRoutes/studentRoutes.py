# student authentication routes

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from server import models
from server.database import engine, SessionLocal
from dotenv import load_dotenv, find_dotenv
from passlib.context import CryptContext
from jose import jwt
import sys
import os
sys.path.append("/")

studentRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# student model
class CreateStudent(BaseModel):
    email: str
    password: str
    collage: str


# find the environment file
load_dotenv(find_dotenv())

# get the environment variables needed
secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')
scheme1 = os.environ.get('BCRYPT_SCHEM1')
scheme2 = os.environ.get('BCRYPT_SCHEM2')

# create crypt context instance
bcrypt_context = CryptContext(schemes=[scheme1, scheme2], deprecated='auto')


# database instance
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# hash password
def get_hash_password(password):
    # hash the password according to crypt context
    return bcrypt_context.hash(password)


# verify hash password
def verify_hash_password(plain_password, hashed_password):
    # verify the hashed password and entered password
    return bcrypt_context.verify(plain_password, hashed_password)


# authenticate student
async def authenticate_student(email: str, password: str, db):
    # get the student form the database
    student = db.query(models.Student).filter(models.Student.email == email).first()

    # if not present
    if not student:
        return False
    # if present then verify the password
    if not verify_hash_password(password, student.password):
        return False
    return True


# create jwt access token
def create_jwt_access_token(email: str, collage: str, student_id: int):
    # create jwt message
    encode = {"id": student_id, "email": email, "collage": collage}
    # return jwt encoded with secret key and algorithm
    return jwt.encode(encode, secret_key, algorithm=algorithm)


# route for creating a new student
@studentRouter.post("/create/student")
async def create_student(student: CreateStudent, db: Session = Depends(get_db)):
    create_student_model = models.Student()
    create_student_model.email = student.email
    create_student_model.password = get_hash_password(student.password)
    create_student_model.collage = student.collage

    # add new student to the database
    db.add(create_student_model)

    # commit the transaction
    db.commit()

    return {"status": "new student created successfully"}


# get jwt token
@studentRouter.post("/tokenforstudent")
async def login_for_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get the student user according to entered credential
    student_user = await authenticate_student(form_data.username, form_data.password, db)

    if not student_user:
        # not a student user raise an exception
        raise HTTPException(status_code=404, detail='student not found')
    else:
        # get user details and create the jwt and return
        student_det = db.query(models.Student).filter(form_data.username == models.Student.email).first()
        token = create_jwt_access_token(email=student_det.email, collage=student_det.collage, student_id=student_det.id)
        return token
