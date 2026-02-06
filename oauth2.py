from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
 
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User
oauth2scheme=OAuth2PasswordBearer(tokenUrl="login")
from  pydantic import BaseModel

JWT_SECRET= 'gfbefi3web3kej3efluwfedfelwufdfedned'
JWT_ALGORITHM ='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = int(expire.timestamp())
    encoded_jwt=jwt.encode(to_encode,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return encoded_jwt

class TokenData(BaseModel):
    user_id: int

# def check_token(token,err):
#     try:
#         payload=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
         
        
#         id=payload.get("user_id")
         
#         if id is None:
#             raise err
        
#         token_data = TokenData(user_id=int(id))
         
             
        
#     except JWTError:
         
#         raise err
#     return token_data


import logging
logger = logging.getLogger("uvicorn")

def check_token(token, err):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
         
        user_id = payload.get("user_id")
         

        if user_id is None:
            raise err

        token_data = TokenData(user_id=int(user_id))
         
    except JWTError as e:
         
        raise err
    return token_data


def get_curr_user(token:str= Depends(oauth2scheme),db: Session=Depends(get_db)):

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
   
    token_data=check_token(token,credentials_exception)
    print(token_data)

    user=db.query(User).filter(User.id==token_data.user_id).first()
    return user