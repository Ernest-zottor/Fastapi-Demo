from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import  List
from sqlalchemy import func
from .. database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2 



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int=5, skip: int=0):


    # posts = db.query(models.Post).limit(limit).offset(skip).all()
    # print([post.owner.id for post in current_user.posts])

    results = db.query(models.Post, func.count(models.Votes.post_id).label('votes')
                       ).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True
                              ).group_by(models.Post.id).limit(limit).offset(skip).all()
    
    return results



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    

    new_post = models.Post(user_id= current_user.id ,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}' , response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # post_query = db.query(models.Post).filter(models.Post.id ==id)
    # post_query = db.query(models.Post).get(id)
  
    post = db.query(models.Post, func.count(models.Votes.post_id).label('votes')
                       ).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).filter(models.Post.id ==id).group_by(models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    # Reason for post.Post.user_id is in learning.py 
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform requested action')
    
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform requested action')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id ==id)
    db_post = post_query.first()
    
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform requested action')
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()