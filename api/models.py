from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Table, Text,ForeignKey
from sqlalchemy import Float
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from database import Base 


class ClubeModel(Base):
    __tablename__ = "clubes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    telefone = Column(String(20))
    localidade = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  

    mapas = relationship("MapaModel", back_populates="clube", cascade="all, delete")
    
class TipoUserModel(Base):
    __tablename__ = "tipouser"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)

    utilizadores = relationship("UtilizadorModel", back_populates="tipo")

class UtilizadorModel(Base):
    __tablename__ = "utilizador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tipo_id = Column(Integer, ForeignKey("tipouser.id"), nullable=False)

    tipo = relationship("TipoUserModel", back_populates="utilizadores")


class MapaModel(Base):
    __tablename__ = "mapas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    clube_id = Column(Integer, ForeignKey("clubes.id"), nullable=False)

    clube = relationship("ClubeModel", back_populates="mapas")


class ClubeCreate(BaseModel):
    nome: str
    email: str | None = None
    telefone: str | None = None
    localidade: str | None = None


class ClubeResponse(ClubeCreate):
    id: int
    class Config:
        from_attributes = True

class TipoUserResponse(BaseModel):
    id: int
    descricao: str

    class Config:
        from_attributes = True

class TipoUserCreate(BaseModel):
    descricao: str

class UserLogin(BaseModel):
    username: str
    password: str

class UtilizadorCreate(BaseModel):
    username: str
    password: str
    tipo_id: int


class UtilizadorResponse(BaseModel):
    id: int
    username: str
    tipo: TipoUserResponse
    created_at: datetime

    class Config:
        from_attributes = True

class MapaCreate(BaseModel):
    descricao: str | None = None
    latitude: float
    longitude: float
    clube_id: int

class MapaResponse(BaseModel):
    id: int
    descricao: str | None = None
    latitude: float
    longitude: float
    clube_id: int

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

