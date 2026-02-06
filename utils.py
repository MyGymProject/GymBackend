from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")


def hash_password(password:str):
    hash_pwd=pwd_context.hash(password)
    return hash_pwd

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# from fastapi import HTTPException,status,Request,Depends
# from fastapi.responses import JSONResponse
# from models import User
 
# from database import get_db
# from config import setting
# from jose import jwt,JWTError
 
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session


# oauth2scheme=OAuth2PasswordBearer(tokenUrl='http://127.0.0.1:8009/auth/login')

# def verify_token(auth_header: str) -> str:
     
#     print(auth_header)
#     if not auth_header:
#         raise HTTPException(status_code=404, detail="Invalid authorization header")
#     return check_token(auth_header)  

# def check_token(token):
#     try:
#         payload=jwt.decode(token,setting.JWT_SECRET,algorithms=[setting.JWT_ALGORITHM])
#     except JWTError:
#         return None
#     return payload


 


# def get_curr_user(token:str= Depends(oauth2scheme),db: Session=Depends(get_db)):
   
#     token_data=verify_token(token)

     

#     if not token_data:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    
#     return token_data["user_id"]