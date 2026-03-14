from datetime import datetime,date
from sqlalchemy import Column, Integer, String, DateTime, Table, Text,ForeignKey,UniqueConstraint,Date
from sqlalchemy import Float
from typing import Optional
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
    evento_at = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  

    mapas = relationship("MapaModel", back_populates="clube", cascade="all, delete")
    membros = relationship("MembroClubeModel",back_populates="clube",cascade="all, delete-orphan")

class MembroClubeModel(Base):
    __tablename__ = "membro_clube"

    id = Column(Integer, primary_key=True, autoincrement=True)
    utilizador_id = Column(Integer, ForeignKey("utilizador.id"), nullable=False)
    clube_id = Column(Integer, ForeignKey("clubes.id"), nullable=False)
    inscrito_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("utilizador_id", "clube_id", name="uq_membro_clube"),
    )

    utilizador = relationship("UtilizadorModel", back_populates="clubes_inscritos")
    clube = relationship("ClubeModel", back_populates="membros")

    
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
    clubes_inscritos = relationship("MembroClubeModel",back_populates="utilizador",cascade="all, delete-orphan")


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
    evento_at: Optional[date] = None


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

class IngressarResponse(BaseModel):
    mensagem:    str
    clube_id:    int
    clube_nome:  str
    inscrito_em: datetime

    class Config:
        from_attributes = True

