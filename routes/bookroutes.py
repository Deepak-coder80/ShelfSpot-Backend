from fastapi import APIRouter
from server import models
from server.database import engine

bookRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)