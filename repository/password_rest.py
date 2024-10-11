from datetime import timedelta

from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import models, JWTtoken, email_utils, schemas, hashing


async def password_reset_request(email: str, bg_task: BackgroundTasks, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email is not registered."
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your email is not verified yet.",
        )

    expires_delta = timedelta(hours=24)

    # generate a JWT token and return
    reset_token = JWTtoken.create_access_token(
        data={"sub": email}, expires_delta=expires_delta
    )

    bg_task.add_task(email_utils.send_reset_email, email, reset_token)

    return {"message": "Please check your email"}


async def password_reset_confirm(
    token: str, passwords: schemas.PasswordResetConfirm, db: Session
):
    user = JWTtoken.verify_token(token, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match."
        )

    user.password = hashing.Hash.bcrypt(passwords.new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful."}
