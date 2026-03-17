from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import os
from dotenv import load_dotenv
from database import SessionLocal
from models import UtilizadorModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")



bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class OAuth2PasswordRequestFormWithTipo:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        grant_type: str = Form(None),
        scope: str = Form(""),
    ):
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.scope = scope


class CreateUserRequest(BaseModel):
    username: str
    password: str
    tipo_id: int = 1
    plano_id: int = 1


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]




@router.post("/", status_code=status.HTTP_201_CREATED)
async def register(db: db_dependency, create_user_request: CreateUserRequest):
    user = db.query(UtilizadorModel).filter(
        UtilizadorModel.username == create_user_request.username
    ).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt_context.hash(create_user_request.password)
    new_user = UtilizadorModel(
        username=create_user_request.username,
        password=hashed_password,
        tipo_id=create_user_request.tipo_id,
        plano_id=create_user_request.plano_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilizador Criado com Sucesso"}


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestFormWithTipo, Depends()],
    db: db_dependency,
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(user, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UtilizadorModel).filter(
        UtilizadorModel.username == username
    ).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return False
    return user



def create_access_token(user: UtilizadorModel, expires_delta: timedelta):
    to_encode = {
        "sub": user.username,
        "id": user.id,
        "tipo_id": user.tipo_id,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    from sqlalchemy.orm import joinedload
    user = db.query(UtilizadorModel).options(
        joinedload(UtilizadorModel.tipo),
        joinedload(UtilizadorModel.plano),
    ).filter(UtilizadorModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilizador não encontrado")
    return user