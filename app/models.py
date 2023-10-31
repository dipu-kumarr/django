from sqlalchemy import Column, Integer,String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base):
    __tablename__= 'text12345'
     
    id= Column(Integer, primary_key=True,nullable=False)
    title= Column(String, nullable=False)
    content=Column(String, nullable=False )
    Published=Column(Boolean, Server_default='TRUE',nullable=False)
    