from fastapi import FastAPI
import models
from database import engine
from routers import (
    user,
    authenticate,
    hospital,
    patient,
    test_image,
    result_image,
    password_reset,
)
from middleware.hospital_access import HospitalAccessMiddleware

app = FastAPI()

# Create all database tables (if not already created) using SQLAlchemy models
models.Base.metadata.create_all(engine)

# Add middleware to the app. The HospitalAccessMiddleware restricts access based on the user
app.add_middleware(HospitalAccessMiddleware)

app.include_router(user.router)

app.include_router(authenticate.router)

app.include_router(hospital.router)

app.include_router(patient.router)

app.include_router(test_image.router)

app.include_router(result_image.router)

app.include_router(password_reset.router)
