from fastapi import FastAPI
import models
from database import engine
from routers import user, authenticate, hospital, patient

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)

app.include_router(authenticate.router)

app.include_router(hospital.router)

app.include_router(patient.router)
