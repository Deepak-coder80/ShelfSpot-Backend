from fastapi import FastAPI
from server import models
from server.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "up", 'database-connection': 'established'}
