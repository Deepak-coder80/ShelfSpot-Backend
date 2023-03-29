from fastapi import FastAPI
from server import models
from server.database import engine
from authenticationRoutes import adminRoutes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(adminRoutes.adminRouter)

@app.get("/")
def read_root():
    return {"status": "up", 'database-connection': 'established'}
