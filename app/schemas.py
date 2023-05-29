from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name:str 

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse  # The UserResponse class must always be above the Post. This will return the UserResponse schema


    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int


    class Config:
        orm_mode = True


# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # We want to know whether the user is liking or unliking a post. 0 means like and 1 means otherwise. CONINT will make sure the values will be between 0 and 1