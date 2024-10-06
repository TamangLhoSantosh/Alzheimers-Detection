from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import JWTtoken, database, models
from sqlalchemy.orm import Session
from hashing import Hash
from emailutils import send_verification_email

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    # generate a JWT token and return
    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    await send_verification_email(user.email, access_token)
    return {"access_token": access_token, "token_type": "bearer"}
