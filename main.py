from fastapi import FastAPI, Query, Depends,status,HTTPException
from fastapi.responses import JSONResponse,Response
from fastapi.params import Body
from sqlalchemy.orm import Session
from pydantic import BaseModel,EmailStr
from typing import Optional
from typing import List
from datetime import datetime 
from utils import hash_password,verify
from oauth2 import create_token,get_curr_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


 
from database import get_db,engine
 
from psycopg2.extras import RealDictCursor

 
from fastapi.middleware.cors import CORSMiddleware
from models import Base,User,Amount,Expense,Member
from datetime import date

app=FastAPI()
Base.metadata.create_all(bind=engine)

 

class Trainerdata(BaseModel):
    firstname:str
    lastname:str
    email:EmailStr
    password: str
    role:str



class Memberdata(BaseModel):
    firstname:str
    lastname:str
    email:EmailStr
    role:str

class AmountRequest(BaseModel):
    amount: int
    start_date: date
    end_date: date
    user_id:int

class EditAmountRequest(BaseModel):
    amount: int
    start_date: date
    end_date: date
    amount_id: int
     
class ResponseAmount(BaseModel):
    amount: int
    start_date: date
    end_date: date
    user_id:int
     
class ResponseMemberdata(BaseModel):
    id:int
    firstname:str
    lastname:str
    email:str
    role:str
    amounts: List[ResponseAmount] = []

    class Config: 
        orm_mode = True

class EditMemberdata(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
     
class EditTrainerdata(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]




class RequestExpense(BaseModel):
    expense_amount: int
    expense_date: date
    description: str

class ResponseExpense(BaseModel):
    expense_amount: int
    expense_date: date
    description: str 

    class Config: 
        orm_mode = True


class RequestToken(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    user_id: int 


 
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 

 
@app.get("/root")
def root():
    return JSONResponse(content={"STATUS":"CONNECTED"},status_code=200)


@app.get("/get_members",status_code=status.HTTP_200_OK,response_model=list[ResponseMemberdata])
def get_all_members(db: Session=Depends(get_db),curr_user: User =Depends(get_curr_user)):
    post=db.query(Member).all()
    return post


@app.get("/get_trainer",status_code=status.HTTP_200_OK,response_model=list[ResponseMemberdata])
def get_all_members(db: Session=Depends(get_db),curr_user: User =Depends(get_curr_user)):
    post=db.query(User).all()
    return post

@app.get("/get_members/{id}", response_model=ResponseMemberdata)
def get_specific_member(id:int, db: Session=Depends(get_db),curr_user:str=Depends(get_curr_user)):

    

    result=db.query(Member).filter(Member.id==id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Member not found with id :{id}")

     
     
    return result


@app.get("/get_trainer/{id}", response_model=ResponseMemberdata)
def get_specific_member(id:int, db: Session=Depends(get_db),curr_user:str=Depends(get_curr_user)):

    

    result=db.query(User).filter(User.id==id).one()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Member not found with id :{id}")

     
     
    return result

@app.post("/Add_Trainer",response_model=ResponseMemberdata)
def addtrainer(data: Trainerdata, db: Session=Depends(get_db)):
    if len(data.password.encode("utf-8")) > 72: 
        raise HTTPException( status_code=400, detail="Password too long. Must be 72 characters or fewer." )
    hash_pwd=hash_password(data.password)
    data.password=hash_pwd
    
    user = User( firstname=data.firstname, lastname=data.lastname, email=data.email, password=hash_pwd, # store hash in DB 
                role=data.role )
    db.add(user)
    db.commit()
    db.refresh(user)
    
     
     


    return user

@app.post("/Add_Member",response_model=ResponseMemberdata)
def addmember(data: Memberdata, db: Session=Depends(get_db)):
     
    
    user = Member( firstname=data.firstname, lastname=data.lastname, email=data.email, # store hash in DB 
                role=data.role )
    db.add(user)
    db.commit()
    db.refresh(user)
    
     
     


    return user

@app.put("/update_Trainer/{email}", response_model=ResponseMemberdata) 
def update_trainer(email: str, user_update: EditTrainerdata, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    
    
    result = db.query(User).filter(User.email == email).first()
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Member not found with id: {email}" ) 
    # # Update only provided fields 
    if user_update.firstname is not None: 
        result.firstname = user_update.firstname 
    if user_update.lastname is not None: 
        result.lastname = user_update.lastname 
     
    
    db.commit() 
    db.refresh(result)
      

    
     
    return result



@app.put("/update_member/{email}", response_model=ResponseMemberdata) 
def update_member(email: str, user_update: EditMemberdata, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    
    
    result = db.query(Member).filter(Member.email == email).first()
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Member not found with id: {email}" ) 
    # # Update only provided fields 
    if user_update.firstname is not None: 
        result.firstname = user_update.firstname 
    if user_update.lastname is not None: 
        result.lastname = user_update.lastname 
     
    
    db.commit() 
    db.refresh(result)
      

    
     
    return result

@app.delete("/Delete_Member/{email}", status_code=status.HTTP_204_NO_CONTENT) 
def deletemember(email: str, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    result = db.query(Member).filter(Member.email == email).first() 
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Member not found with id: {id}" ) 
    db.delete(result) 
    db.commit()  


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/Delete_Trainer/{email}", status_code=status.HTTP_204_NO_CONTENT) 
def deletemember(email: str, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    result = db.query(User).filter(User.email == email).first() 
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Member not found with id: {id}" ) 
    db.delete(result) 
    db.commit()  


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/Add_Amount",response_model=ResponseAmount,status_code=status.HTTP_201_CREATED)
def add_amount(amount:AmountRequest, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)):

    transaction=Amount(**amount.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

@app.put("/Edit_Amount/{user_id}", response_model=ResponseAmount, status_code=status.HTTP_200_OK)
def edit_amount(user_id: int, amount_request: EditAmountRequest, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)):
    # Find the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    # Find the specific amount belonging to this user
    amount = db.query(Amount).filter(Amount.id == amount_request.amount_id, Amount.user_id == user_id).first()
    if not amount:
        raise HTTPException(status_code=404, detail=f"Amount with id {amount_request.amount_id} not found for user {user_id}")

    # Update fields
    if amount_request.amount is not None:
        amount.amount = amount_request.amount
    if amount_request.start_date is not None:
        amount.start_date = amount_request.start_date
    if amount_request.end_date is not None:
        amount.end_date = amount_request.end_date

    db.commit()
    db.refresh(amount)

    return amount

@app.delete("/Delete_Expense/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def deleteexpense(id: int, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    result = db.query(Expense).filter(Expense.id == id).first() 
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense not found with id: {id}" ) 
    db.delete(result) 
    db.commit()  


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/Add_Expense",response_model=ResponseExpense,status_code=status.HTTP_201_CREATED)
def add_expense(expense:RequestExpense, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)):

    transaction=Expense(**expense.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction
 

@app.get("/get_Expense",response_model=List[ResponseExpense],status_code=status.HTTP_200_OK)
def get_expense(db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)):

    result = db.query(Expense).all() 
    return result  


@app.put("/edit_Expense/{id}", response_model=ResponseExpense) 
def update_expense(id: int, expense:RequestExpense, db: Session = Depends(get_db),curr_user:int=Depends(get_curr_user)): 
    
    
    result = db.query(Expense).filter(Expense.id == id).first()
    if not result: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense not found with id: {id}" ) 
    # # Update only provided fields 
    if expense.expense_amount is not None: 
        result.expense_amount = expense.expense_amount 
    if expense.description is not None: 
        result.description = expense.description
    if expense.expense_date is not None: 
        result.expense_date = expense.expense_date
     
    
    db.commit() 
    db.refresh(result)
      

    
     
    return result
 
class MemberLogin(BaseModel):
    email:EmailStr
    password:str


@app.post("/login",response_model=RequestToken)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
     
    
    user=db.query(User).filter(User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    encodedtoken=create_token(data={"user_id":user.id,"role": user.role})
    return {"access_token":encodedtoken,"token_type":"Bearer"}