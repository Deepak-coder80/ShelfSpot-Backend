import sys
sys.path.append('./')
import uvicorn
from fastapi import FastAPI
from app.server import models
from app.server.database import engine
from app.authenticationRoutes import adminRoutes, studentRoutes
from app.routes import qnpaper_routes,bookroutes

# create all model schemas
models.Base.metadata.create_all(bind=engine)

# root router
mainRouter = FastAPI(
    title='Shelf Spot Backend API',
    version= "1.0"
)

# root route
@mainRouter.get("/")
def read_root():
    return {"status": "up"}

# Admin associated Routes
mainRouter.include_router(adminRoutes.adminRouter, tags = ["Admin Authentication Routes"])

# Student associated Routes
mainRouter.include_router(studentRoutes.studentRouter, tags = ["Student Authentication Routes"])

# book management route
mainRouter.include_router(bookroutes.bookRouter, tags = ["Book Mangement Routes"])

# 
mainRouter.include_router(qnpaper_routes.qnPaperRouter, tags = ["Question Paper Mangement Routes"])

