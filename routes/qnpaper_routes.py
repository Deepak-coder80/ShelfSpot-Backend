from fastapi import APIRouter
from server import models
from server.database import engine

qnPaperRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)
