from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from repository import passwordrest
import database, schemas

router = APIRouter(prefix="/password-reset", tags=["Password Rest"])
get_db = database.get_db


@router.post("/request")
async def password_reset_request(
    email: str, bg_task: BackgroundTasks, db: Session = Depends(get_db)
):
    return await passwordrest.password_reset_request(email, bg_task, db)


@router.post("/confirm")
async def password_reset_confirm(
    passwords: schemas.PasswordResetConfirm,
    db: Session = Depends(get_db),
    token: str = Query(...),
):
    return await passwordrest.password_reset_confirm(token, passwords, db)
