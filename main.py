from fastapi import FastAPI
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
def index():
    return {"message": "Hello World"}
