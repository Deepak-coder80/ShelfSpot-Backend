import os
import sys
sys.path.append('../')

from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from app.server.database import SessionLocal
from app.server import models
from dotenv import load_dotenv,find_dotenv

# find the environment file
load_dotenv(find_dotenv())

# get the environment variables needed
secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')
scheme1 = os.environ.get('BCRYPT_SCHEM1')
scheme2 = os.environ.get('BCRYPT_SCHEM2')

# create crypt context instance
bcrypt_context = CryptContext(schemes=[scheme1, scheme2], deprecated='auto')


### Admin Util Models ###

# new admin model
class CreateAdmin(BaseModel):
    email: str
    password: str
    collage: str


### Student Util Models ###

# student model
class CreateStudent(BaseModel):
    email: str
    password: str
    collage: str

### General Util Models ###

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
