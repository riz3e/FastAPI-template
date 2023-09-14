from sqlalchemy import Boolean, Column, Integer, String
from database  import Base  


class User(Base): # Table in db
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True,)
    email = Column(String, unique=True, index=True)
    name =  Column(String, unique=False)
    surname = Column(String, unique=False)
    hashed_password = Column(String, unique=False, )
    is_teacher = Column(Boolean, unique=False)
    grade = Column(Integer, unique=False, index=True)
    letter = Column(String, unique=False, index=True)