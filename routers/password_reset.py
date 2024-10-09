from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository import passwordrest
import database

router = APIRouter(prefix="/password-reset", tags=["Password Rest"])
get_db = database.get_db


@router.post("/request")
async def password_reset_request(email: str, db: Session = Depends(get_db)):
    return await passwordrest.password_reset_request(email, db)
