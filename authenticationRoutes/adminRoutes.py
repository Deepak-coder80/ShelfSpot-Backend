# admin authentication routes

from fastapi import APIRouter, Depends
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


load_dotenv(find_dotenv())
secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# database instance
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# hash password
def get_hash_password(password):
    return bcrypt_context.hash(password)


# verify hash password
def verify_hash_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


# authenticate admin
async def authenticate_admin(email: str, password: str, db):
    admin = db.query(models.Admin).filter(models.Admin.email == email).first()
    if not admin:
        return False
    if not verify_hash_password(password, admin.password):
        return False
    return True


# create jwt access token
def create_jwt_access_token(email: str, collage: str, id: int):
    encode = {"id": id, "email": email, "collage": collage}
    return jwt.encode(encode, secret_key, algorithm=algorithm)


@adminRouter.post("/create/admin")
async def create_admin(admin: CreateAdmin, db: Session = Depends(get_db)):
    create_admin_model = models.Admin()
    create_admin_model.email = admin.email
    create_admin_model.password = get_hash_password(admin.password)
    create_admin_model.college = admin.collage

    db.add(create_admin_model)
    db.commit()

    return {"status": "new admin created successfully"}
