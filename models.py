from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'    
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    state = Column(Boolean())
