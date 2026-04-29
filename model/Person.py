from sqlalchemy import Column, Integer, String
from db.database import Base
class Person(Base):
    __abstract__ = True  
    
    id      = Column(Integer, primary_key=True, autoincrement=True)
    nome     = Column(String(120), nullable=False)
    telefone = Column(String(20),  nullable=False)
    endereco   = Column(String(200), nullable=False)


