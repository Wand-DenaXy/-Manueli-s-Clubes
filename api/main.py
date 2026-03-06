import os
import auth
from fastapi import FastAPI, Depends, HTTPException,Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from openai import OpenAI
from dotenv import load_dotenv
from typing import Annotated
from datetime import datetime
from sqlalchemy import extract,func

from auth import get_current_user
from sqlalchemy.orm import joinedload
from database import get_db, init_db
from models import (
    ClubeModel, ClubeCreate, ClubeResponse,
    UtilizadorModel, UtilizadorCreate, UtilizadorResponse,
    TipoUserModel, TipoUserCreate, TipoUserResponse,
    MapaModel, MapaCreate, MapaResponse,
    ChatRequest
)

app = FastAPI(title="API Manueli's Clubes", description="API para gestão de clubes e utilizadores")
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UtilizadorModel, Depends(get_current_user)]
load_dotenv()
OPENAI_API_KEY = "https://router.huggingface.co/v1"
client = OpenAI(api_key=OPENAI_API_KEY)

@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API Manueli's Clubes", "docs": "/docs"}


MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    totalClubes = db.query(ClubeModel).count()
    totalUtilizadores = db.query(UtilizadorModel).count()
    totalTiposUser = db.query(TipoUserModel).count()
    totalMapas = db.query(MapaModel).count()

    
    return {
        "clubes": totalClubes,
        "utilizadores": totalUtilizadores,
        "tipousers": totalTiposUser,
        "mapas": totalMapas
    }
@app.get("/statstpuser")
def get_stats_tpuser(
    db: Session = Depends(get_db),
    current_user: UtilizadorModel = Depends(get_current_user)
):
    tipos = db.query(TipoUserModel).all()

    resultado = {}

    for tipo in tipos:
        total = db.query(UtilizadorModel).filter(
            UtilizadorModel.tipo_id == tipo.id
        ).count()

        resultado[tipo.descricao] = total

    return resultado


@app.get("/registrations")
def registrations_by_month(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):


    year = datetime.utcnow().year

    result = (
        db.query(
            extract("month", UtilizadorModel.created_at).label("month"),
            func.count(UtilizadorModel.id).label("count")
        )
        .filter(extract("year", UtilizadorModel.created_at) == year)
        .group_by("month")
        .order_by("month")
        .all()
    )

    counts = {i + 1: 0 for i in range(12)}
    for row in result:
        counts[int(row.month)] = row.count

    data = [{"month": MESES[m - 1], "count": counts[m]} for m in range(1, 13)]
    return data

@app.post("/chat")
def chat_ai(data: ChatRequest, db: Session = Depends(get_db), user: UtilizadorModel = Depends(get_current_user)):
    message = data.message.lower()

    # CASO 1: consulta sobre clubes do mês
    if ("clubes" in message and "mês") or ("mes" in message):
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year

        total = (
            db.query(func.count(ClubeModel.id))
            .filter(
                extract("month", ClubeModel.created_at) == current_month,
                extract("year", ClubeModel.created_at) == current_year
            )
            .scalar()
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "És assistente da empresa Puro Encanto."},
                {"role": "user",
                 "content": f"O utilizador perguntou: '{data.message}'. Tivemos {total} eventos este mês. Responde de forma profissional."}
            ]
        )
        return {"response": response.choices[0].message.content}

    # CASO 2: qualquer outra pergunta
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "És assistente da empresa Puro Encanto."},
            {"role": "user", "content": data.message}
        ]
    )
    return {"response": response.choices[0].message.content}

@app.post("/clubes", response_model=ClubeResponse)
def create_clube(   
    clube: ClubeCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_clube = ClubeModel(**clube.dict())
    db.add(db_clube)
    db.commit()
    db.refresh(db_clube)
    return db_clube

@app.get("/clubes", response_model=list[ClubeResponse])
def list_clubes(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    return db.query(ClubeModel).all()

@app.put("/clubes/{clube_id}", response_model=ClubeResponse)
def update_clube(
    clube_id: int,
    clube: ClubeCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_clube = db.query(ClubeModel).filter(ClubeModel.id == clube_id).first()
    if not db_clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    for key, value in clube.dict().items():
        setattr(db_clube, key, value)
    db.commit()
    db.refresh(db_clube)
    return db_clube

@app.delete("/clubes/{clube_id}", status_code=204)
def delete_clube(
    clube_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_clube = db.query(ClubeModel).filter(ClubeModel.id == clube_id).first()
    if not db_clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    db.delete(db_clube)
    db.commit()
    return None

@app.get("/utilizadores", response_model=list[UtilizadorResponse])
def list_utilizadores(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    utilizadores = db.query(UtilizadorModel).options(joinedload(UtilizadorModel.tipo)).all()
    return [UtilizadorResponse.from_orm(u) for u in utilizadores]

@app.delete("/utilizadores/{utilizador_id}", status_code=204)
def delete_utilizador(
    utilizador_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_utilizador = db.query(UtilizadorModel).filter(UtilizadorModel.id == utilizador_id).first()
    if not db_utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    db.delete(db_utilizador)
    db.commit()
    return Response(status_code=204)

@app.put("/utilizadores/{utilizador_id}", response_model=UtilizadorResponse)
def update_utilizador(
    utilizador_id: int,
    utilizador: UtilizadorCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_utilizador = db.query(UtilizadorModel).filter(UtilizadorModel.id == utilizador_id).first()
    if not db_utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    for key, value in utilizador.dict().items():
        setattr(db_utilizador, key, value)
    db.commit()
    db.refresh(db_utilizador)
    
    return UtilizadorResponse.from_orm(db_utilizador)


@app.post("/tipouser", response_model=TipoUserResponse)
def create_tipo_user(
    tipo: TipoUserCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    novo_tipo = TipoUserModel(**tipo.dict())
    db.add(novo_tipo)
    db.commit()
    db.refresh(novo_tipo)
    return novo_tipo

@app.get("/tipouser", response_model=list[TipoUserResponse])
def list_tipo_user(
    db: Session = Depends(get_db),
):
    return db.query(TipoUserModel).all()

@app.put("/tipouser/{tipo_id}", response_model=TipoUserResponse)
def update_tipo_user(
    tipo_id: int,
    tipo: TipoUserCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_tipo = db.query(TipoUserModel).filter(TipoUserModel.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")

    db_tipo.descricao = tipo.descricao
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@app.delete("/tipouser/{tipo_id}", status_code=204)
def delete_tipo_user(
    tipo_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_tipo = db.query(TipoUserModel).filter(TipoUserModel.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")

    db.delete(db_tipo)
    db.commit()
    return None

@app.post("/mapas", response_model=MapaResponse)
def create_mapa(
    mapa: MapaCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    clube = db.query(ClubeModel).filter(ClubeModel.id == mapa.clube_id).first()
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    
    db_mapa = MapaModel(**mapa.dict())
    db.add(db_mapa)
    db.commit()
    db.refresh(db_mapa)
    return db_mapa

@app.get("/mapas", response_model=list[MapaResponse])
def list_mapas(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    return db.query(MapaModel).all()

@app.put("/mapas/{mapa_id}", response_model=MapaResponse)
def update_mapa(
    mapa_id: int,
    mapa: MapaCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    db_mapa = db.query(MapaModel).filter(MapaModel.id == mapa_id).first()
    if not db_mapa:
        raise HTTPException(status_code=404, detail="Mapa não encontrado")
    
    clube = db.query(ClubeModel).filter(ClubeModel.id == mapa.clube_id).first()
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    
    for key, value in mapa.dict().items():
        setattr(db_mapa, key, value)
    
    db.commit()
    db.refresh(db_mapa)
    return db_mapa

@app.delete("/mapas/{mapa_id}", status_code=200)
def delete_mapa(mapa_id: int, db: Session = Depends(get_db)):
    mapa = db.query(MapaModel).filter(MapaModel.id == mapa_id).first()

    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa não encontrado")

    db.delete(mapa) 
    db.commit()

    return {"message": "Mapa apagado com sucesso"}