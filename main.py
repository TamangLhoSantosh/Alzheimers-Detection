from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import models
from database import engine
from routers import (
    user,
    authenticate,
    hospital,
    patient,
    test,
    test_image,
    password_reset,
)
from middleware.hospital_access import HospitalAccessMiddleware

app = FastAPI()

# Create all database tables (if not already created) using SQLAlchemy models
models.Base.metadata.create_all(engine)

# Mounts the 'media' directory to the '/media' URL path.
app.mount("/media", StaticFiles(directory="media"), name="media")

# URL of the second FastAPI program (Analysis Service)
ANALYSIS_URL = "http://localhost:8080/predict"

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to the app. The HospitalAccessMiddleware restricts access based on the user
app.add_middleware(HospitalAccessMiddleware)

app.include_router(user.router)

app.include_router(authenticate.router)

app.include_router(hospital.router)

app.include_router(patient.router)
app.include_router(patient.router_all_patients)

app.include_router(test.router)

app.include_router(test_image.router)

app.include_router(password_reset.router)
