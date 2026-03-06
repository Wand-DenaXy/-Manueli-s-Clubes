from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import UtilizadorModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class OAuth2PasswordRequestFormWithTipo:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        tipo_id: int = Form(1),
        grant_type: str = Form(None),
        scope: str = Form(""),
    ):
        self.username = username
        self.password = password
        self.tipo_id = tipo_id
        self.grant_type = grant_type
        self.scope = scope


class CreateUserRequest(BaseModel):
    username: str
    password: str
    tipo_id: int = 1


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
    user = authenticate_user(db, form_data.username, form_data.password,form_data.tipo_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(db: Session, username: str, password: str, tipo_id: int):
    user = db.query(UtilizadorModel).filter(
        UtilizadorModel.username == username
    ).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    if user.tipo_id != tipo_id:
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        tipo_id: int = payload.get("tipo_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "id": user_id, "tipo_id": tipo_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")