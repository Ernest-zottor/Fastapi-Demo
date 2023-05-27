from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(login_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == login_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    password_verified = utils.verify(login_credentials.password, user.password)

    if not password_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token({"email": user.email})

    return {'access_token':access_token, 'token_type': 'bearer'}
