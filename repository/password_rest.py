from datetime import timedelta
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import models, JWTtoken, email_utils, schemas, hashing


# Send mail to the user requesting password reset
async def password_reset_request(
    request: schemas.PasswordResetRequest, bg_task: BackgroundTasks, db: Session
):
    # Retrieve user by email
    user = db.query(models.User).filter(models.User.email == request.email).first()

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

    # Generate a JWT token for password reset
    reset_token = JWTtoken.create_access_token(
        data={"sub": request.email}, expires_delta=expires_delta
    )

    # Schedule the email sending task in the background
    bg_task.add_task(email_utils.send_reset_email, request.email, reset_token)

    return {"message": "Please check your email"}


# Resets password of the user
# Verifies the password reset request
async def password_reset_confirm(
    token: str, password: schemas.PasswordResetConfirm, db: Session
):
    # Verify the reset token and retrieve user
    user = JWTtoken.verify_access_token(token, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    # Hash and update the new password
    user.password = hashing.Hash.bcrypt(password.new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful."}
