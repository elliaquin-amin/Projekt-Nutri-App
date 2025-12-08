from sqlalchemy import Column, Integer, String, Float
from database import Base

class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    grupo = Column(String(255), nullable=False)
    cal = Column(Float, nullable=False)
    carb = Column(Float, nullable=False)
    prot = Column(Float, nullable=False)
    gord = Column(Float, nullable=False)
    fibra = Column(Float, nullable=False)
