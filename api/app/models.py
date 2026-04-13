from datetime import datetime,date
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text,ForeignKey,UniqueConstraint,Date
from sqlalchemy import Float
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from app.database import Base 



class StripeEventModel(Base):
    __tablename__ = "stripe_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(255), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  

    utilizadores = relationship("UtilizadorModel", back_populates="organization")
    clubes = relationship("ClubeModel", back_populates="organization")

class ClubeModel(Base):
    __tablename__ = "clubes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    telefone = Column(String(20))
    localidade = Column(String(100))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    evento_at = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    organization = relationship("OrganizationModel", back_populates="clubes")
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

class PlanoModel(Base):
    __tablename__ = "planos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=True)
    preco = Column(Float, default=0.0)
    limite_clubes = Column(Integer, default=-1)
    limite_mapas = Column(Integer, default=-1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    utilizadores = relationship("UtilizadorModel", back_populates="plano")

   
class TipoUserModel(Base):
    __tablename__ = "tipouser"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)

    utilizadores = relationship("UtilizadorModel", back_populates="tipo")

class UtilizadorModel(Base):
    __tablename__ = "utilizador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tipo_id = Column(Integer, ForeignKey("tipouser.id"), nullable=False)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)


    organization = relationship("OrganizationModel", back_populates="utilizadores")
    tipo = relationship("TipoUserModel", back_populates="utilizadores")
    plano = relationship("PlanoModel", back_populates="utilizadores")
    notificacoes = relationship("NotificacaoModel", back_populates="utilizador", cascade="all, delete-orphan")
    clubes_inscritos = relationship("MembroClubeModel",back_populates="utilizador",cascade="all, delete-orphan")


class NotificacaoModel(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    utilizador_id = Column(Integer, ForeignKey("utilizador.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    titulo = Column(String(255), nullable=False)
    mensagem = Column(Text, nullable=False)
    lida = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    utilizador = relationship("UtilizadorModel", back_populates="notificacoes")


class MapaModel(Base):
    __tablename__ = "mapas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    clube_id = Column(Integer, ForeignKey("clubes.id"), nullable=False)

    clube = relationship("ClubeModel", back_populates="mapas")



class OrganizationCreate(BaseModel):
    nome: str

class OrganizationResponse(BaseModel):
    id: int
    nome: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ClubeCreate(BaseModel):
    nome: str
    email: str | None = None
    telefone: str | None = None
    localidade: str | None = None
    evento_at: Optional[date] = None



class ClubeResponse(ClubeCreate):
    id: int
    organization_id: int

    class Config:
        from_attributes = True

class PlanoCreate(BaseModel):
    nome: str
    preco: float = 0.0
    limite_clubes: int = -1
    limite_mapas: int = -1

class PlanoResponse(BaseModel):
    id: int
    nome: str | None = None
    preco: float
    limite_clubes: int
    limite_mapas: int

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
    email: str | None = None
    tipo_id: int


class UtilizadorResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
    tipo: TipoUserResponse
    plano: PlanoResponse | None = None
    organization: OrganizationResponse | None = None 
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

class CheckoutRequest(BaseModel):
    plano_id: int

    class Config:
        from_attributes = True


class NotificacaoResponse(BaseModel):
    id: int
    tipo: str
    titulo: str
    mensagem: str
    lida: bool
    created_at: datetime

    class Config:
        from_attributes = True

