# admin authentication routes

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

adminRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# admin model
class CreateAdmin(BaseModel):
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


# authenticate admin
async def authenticate_admin(email: str, password: str, db):
    # get the admin form the database
    admin = db.query(models.Admin).filter(models.Admin.email == email).first()

    # if not present
    if not admin:
        return False
    # if present then verify the password
    if not verify_hash_password(password, admin.password):
        return False
    return True


# create jwt access token
def create_jwt_access_token(email: str, collage: str, admin_id: int):
    # create jwt message
    encode = {"id": admin_id, "email": email, "collage": collage}
    # return jwt encoded with secret key and algorithm
    return jwt.encode(encode, secret_key, algorithm=algorithm)


# route for creating a new admin
@adminRouter.post("/create/admin")
async def create_admin(admin: CreateAdmin, db: Session = Depends(get_db)):
    create_admin_model = models.Admin()
    create_admin_model.email = admin.email
    create_admin_model.password = get_hash_password(admin.password)
    create_admin_model.college = admin.collage

    # add new admin to the database
    db.add(create_admin_model)

    # commit the transaction
    db.commit()

    db.refresh(create_admin_model.id)

    if not create_admin_model.id:
        raise HTTPException(status_code=404, detail='Admin not created')

    return {"status": "new admin created successfully"}


# get jwt token
@adminRouter.post("/token")
async def login_for_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get the admin user according to entered credential
    admin_user = await authenticate_admin(form_data.username, form_data.password, db)

    if not admin_user:
        # not a admin user raise an exception
        raise HTTPException(status_code=404, detail='Admin not found')
    else:
        # get user details and create the jwt and return
        admin_det = db.query(models.Admin).filter(models.Admin.email == form_data.username).first()
        token = create_jwt_access_token(email=admin_det.email, collage=admin_det.college, admin_id=admin_det.id)
        return token
