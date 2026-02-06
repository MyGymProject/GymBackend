from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Date
from sqlalchemy.orm import relationship
 


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname=Column(String(255),nullable=False)
    lastname=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False,unique=True)
    password=Column(String(2555),nullable=False)
    role=Column(String(2555),nullable=False,server_default="Trainer")
     
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(String(255), nullable=False, server_default="Member")
    amounts = relationship("Amount", back_populates="user", cascade="all, delete-orphan")


class Amount(Base): 
    __tablename__ = "amounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    user = relationship("Member", back_populates="amounts")


class Expense(Base): 
    __tablename__ = "expenses" 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    expense_amount = Column(Integer, nullable=False) 
    expense_date = Column(Date, nullable=False) 
    description=Column(String(500),nullable=False)
     
   


 
