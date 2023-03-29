# admin authentication routes

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from server import models
from server.database import engine, SessionLocal

adminRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)


# admin model
class CreateAdmin(BaseModel):
    email: str
    password: str
    collage: str


# database instance
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@adminRouter.post("/create/admin")
async def create_admin(admin: CreateAdmin, db: Session = Depends(get_db)):
    create_admin_model = models.Admin()
    create_admin_model.email = admin.email
    create_admin_model.password = admin.password
    create_admin_model.college = admin.collage

    db.add(create_admin_model)
    db.commit()

    return {"status": "new admin created successfully"}
