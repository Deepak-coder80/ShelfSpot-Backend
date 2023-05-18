import sys
sys.path.append("../")

import uvicorn
from fastapi import FastAPI
from app.server import models
from app.server.database import engine
from app.authenticationRoutes import adminRoutes, studentRoutes
from app.routes import qnpaper_routes,bookroutes

# create all model schemas
models.Base.metadata.create_all(bind=engine)

# root router
app = FastAPI(
    title='Shelf Spot Backend API',
    version= "1.0"
)

# root route
@app.get("/")
def read_root():
    return {"status": "up"}

# Admin associated Routes
app.include_router(adminRoutes.adminRouter, tags = ["Admin Authentication Routes"])

# Student associated Routes
app.include_router(studentRoutes.studentRouter, tags = ["Student Authentication Routes"])

# book management route
app.include_router(bookroutes.bookRouter, tags = ["Book Mangement Routes"])

# 
app.include_router(qnpaper_routes.qnPaperRouter, tags = ["Question Paper Mangement Routes"])


# run the app
if __name__ == '__main__':
    uvicorn.run(app = app)