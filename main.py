from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def getroot():
    return {"status": "connection established"}