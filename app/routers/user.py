from fastapi import  status, HTTPException, Depends, APIRouter
from typing import  List
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..email import send_registration_email





router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email already exists')
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_registration_email(subject='Registration Successful', email_to=new_user.email, 
                            body={
                                'title': 'Registration Successful',
                                'name': new_user.first_name +' '+ new_user.last_name
                            })
    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'user with id: {id} was not found')
    return user

@router.get('/',response_model= List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users