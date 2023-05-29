# admin authentication routes

import os
import sys
sys.path.append("../")

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.authenticationRoutes.authentication_utils as utils
from app.server import models
from app.server.database import engine



adminRouter = APIRouter()
models.Base.metadata.create_all(bind=engine)

# route for creating a new admin
@adminRouter.post("/create/admin")
async def create_admin(admin: utils.CreateAdmin, db: Session = Depends(utils.get_db)):
    create_admin_model = models.Admin()
    create_admin_model.email = admin.email
    create_admin_model.password = utils.get_hash_password(admin.password)
    create_admin_model.collage = admin.collage

    # add new admin to the database
    db.add(create_admin_model)

    # commit the transaction
    db.commit()

    db.refresh(create_admin_model)

    if not create_admin_model.id:
        raise HTTPException(status_code=404, detail='Admin not created')

    return {"status": "new admin created successfully"}


# get jwt token
@adminRouter.post("/token/admin")
async def login_for_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    # get the admin user according to entered credential
    admin_user = await utils.authenticate_admin(form_data.username, form_data.password, db)

    if not admin_user:
        # not a admin user raise an exception
        raise HTTPException(status_code=404, detail='Admin not found')
    else:
        # get user details and create the jwt and return
        admin_det = db.query(models.Admin).filter(models.Admin.email == form_data.username).first()
        token = utils.create_jwt_access_token(email=admin_det.email, collage=admin_det.collage, id=admin_det.id)
        return token


@adminRouter.get("/collages/")
def get_all_collages_of_admin(db: Session = Depends(utils.get_db)):
    query = db.query(getattr(models.Admin, "collage")).distinct()
    result = [row[0] for row in query.all()]
    return result
