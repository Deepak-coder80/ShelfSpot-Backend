from fastapi import APIRouter
from server import models
from server.database import engine

qnPaperRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# route for getting qnpaper by subject

# route for getting qnpaper by semester