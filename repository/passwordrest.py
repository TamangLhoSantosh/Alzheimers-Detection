from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, JWTtoken, emailutils


async def password_reset_request(email: str, db: Session):
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

    await emailutils.send_reset_email(email, reset_token)

    return {"message": "Please check your email"}
