import os
import stripe
from app import auth
from fastapi import FastAPI, Depends, HTTPException,Response,Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Annotated
from datetime import datetime
from sqlalchemy import extract, func, text, inspect as sa_inspect
from app.auth import get_current_user
from sqlalchemy.orm import joinedload
from app.database import get_db, init_db, engine as _engine
from app.cache import cache_get, cache_set, cache_invalidate
from app.models import (
    ClubeModel, ClubeCreate, ClubeResponse,
    UtilizadorModel, UtilizadorCreate, UtilizadorResponse,
    TipoUserModel, TipoUserCreate, TipoUserResponse,
    MapaModel, MapaCreate, MapaResponse,
    MembroClubeModel, IngressarResponse,
    PlanoModel, PlanoCreate, PlanoResponse,
    CheckoutRequest
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
bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


@app.on_event("startup")
def startup():
    init_db()
    db = next(get_db())
    try:
        if db.query(TipoUserModel).count() == 0:
            db.add_all([TipoUserModel(descricao=d) for d in ["Administrador", "Gestor", "Cliente"]])
            db.commit()
        if db.query(PlanoModel).count() == 0:
            db.add_all([
                PlanoModel(nome="Free",preco=0.0,   limite_clubes=3,  limite_mapas=1),
                PlanoModel(nome="Pro",preco=9.99,  limite_clubes=15, limite_mapas=20),
                PlanoModel(nome="Enterprise",preco=29.99, limite_clubes=-1, limite_mapas=-1),
            ])
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API Manueli's Clubes", "docs": "/docs"}


MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def require_roles(*roles: str):
    def role_checker(user: UtilizadorModel = Depends(get_current_user)):
        if user.tipo.descricao not in roles:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return role_checker

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    cached = cache_get("stats")
    if cached is not None:
        return cached

    result = {
        "clubes": db.query(ClubeModel).count(),
        "utilizadores": db.query(UtilizadorModel).count(),
        "tipousers": db.query(TipoUserModel).count(),
        "mapas": db.query(MapaModel).count(),
    }
    cache_set("stats", result, ttl=60)
    return result

@app.get("/statstpuser")
def get_stats_tpuser(
    db: Session = Depends(get_db),
    current_user: UtilizadorModel = Depends(get_current_user)
):
    cached = cache_get("statstpuser")
    if cached is not None:
        return cached

    tipos = db.query(TipoUserModel).all()
    resultado = {}
    for tipo in tipos:
        resultado[tipo.descricao] = db.query(UtilizadorModel).filter(
            UtilizadorModel.tipo_id == tipo.id
        ).count()

    cache_set("statstpuser", resultado, ttl=60)
    return resultado


@app.get("/registrations")
def registrations_by_month(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    year = datetime.utcnow().year
    cache_key = f"registrations:{year}"

    cached = cache_get(cache_key)
    if cached is not None:
        return cached

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
    cache_set(cache_key, data, ttl=300)
    return data

@app.get("/me", response_model=UtilizadorResponse)
def get_me(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    db_user = db.query(UtilizadorModel).options(
        joinedload(UtilizadorModel.tipo),
        joinedload(UtilizadorModel.plano)
    ).filter(UtilizadorModel.id == user.id).first()

    return {
        "id": db_user.id,
        "username": db_user.username,
        "tipo": {"id": db_user.tipo.id, "descricao": db_user.tipo.descricao},
        "plano": {
            "id": db_user.plano.id,
            "nome": db_user.plano.nome,
            "preco": db_user.plano.preco,
            "limite_clubes": db_user.plano.limite_clubes,
            "limite_mapas": db_user.plano.limite_mapas,
        } if db_user.plano else None,
        "created_at": db_user.created_at,
    }

@app.put("/me/plano/{plano_id}", response_model=UtilizadorResponse)
def confirmar_plano(
    plano_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    plano = db.query(PlanoModel).filter(PlanoModel.id == plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    db_user = db.query(UtilizadorModel).filter(UtilizadorModel.id == user.id).first()
    db_user.plano_id = plano_id
    db.commit()
    db.refresh(db_user)
    cache_invalidate("utilizadores:")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "tipo": {"id": db_user.tipo.id, "descricao": db_user.tipo.descricao},
        "plano": {
            "id": db_user.plano.id,
            "nome": db_user.plano.nome,
            "preco": db_user.plano.preco,
            "limite_clubes": db_user.plano.limite_clubes,
            "limite_mapas": db_user.plano.limite_mapas,
        },
        "created_at": db_user.created_at,
    }

@app.post("/clubes", response_model=ClubeResponse)
def create_clube(   
    clube: ClubeCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador","Gestor"))
):
    db_clube = ClubeModel(**clube.dict())
    db.add(db_clube)
    db.commit()
    db.refresh(db_clube)
    cache_invalidate("stats", "clubes:")
    return {
        "id": db_clube.id,
        "nome": db_clube.nome,
        "email": db_clube.email,
        "telefone": db_clube.telefone,
        "localidade": db_clube.localidade,
        "evento_at": db_clube.evento_at,
    }

@app.get("/clubes", response_model=list[ClubeResponse])
def list_clubes(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    cached = cache_get("clubes:list")
    if cached is not None:
        return cached
    result = db.query(ClubeModel).all()
    clubes_dict = [
        {
            "id": clube.id,
            "nome": clube.nome,
            "email": clube.email,
            "telefone": clube.telefone,
            "localidade": clube.localidade,
            "evento_at": clube.evento_at
        }
        for clube in result
    ]
    cache_set("clubes:list", clubes_dict, ttl=30)
    return clubes_dict

@app.put("/clubes/{clube_id}", response_model=ClubeResponse)
def update_clube(
    clube_id: int,
    clube: ClubeCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador"))
):
    db_clube = db.query(ClubeModel).filter(ClubeModel.id == clube_id).first()
    if not db_clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    for key, value in clube.dict().items():
        setattr(db_clube, key, value)
    db.commit()
    db.refresh(db_clube)
    cache_invalidate("stats", "clubes:")
    return {
        "id": db_clube.id,
        "nome": db_clube.nome,
        "email": db_clube.email,
        "telefone": db_clube.telefone,
        "localidade": db_clube.localidade,
        "evento_at": db_clube.evento_at,
    }

@app.delete("/clubes/{clube_id}", status_code=204)
def delete_clube(
    clube_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador"))
):
    db_clube = db.query(ClubeModel).filter(ClubeModel.id == clube_id).first()
    if not db_clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    db.delete(db_clube)
    db.commit()
    cache_invalidate("stats", "clubes:")
    return None

@app.get("/utilizadores", response_model=list[UtilizadorResponse])
def list_utilizadores(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador"))
):
    cached = cache_get("utilizadores:list")
    if cached is not None:
        return cached
    result = db.query(UtilizadorModel).options(joinedload(UtilizadorModel.tipo), joinedload(UtilizadorModel.plano)).all()
    utilizadores_dict = [
        {
            "id": utilizador.id,
            "username": utilizador.username,
            "tipo": {"id": utilizador.tipo.id, "descricao": utilizador.tipo.descricao},
            "plano": {"id": utilizador.plano.id, "nome": utilizador.plano.nome, "preco": utilizador.plano.preco, "limite_clubes": utilizador.plano.limite_clubes, "limite_mapas": utilizador.plano.limite_mapas},
            "created_at": utilizador.created_at
        }
        for utilizador in result
    ]
    cache_set("utilizadores:list", utilizadores_dict, ttl=30)
    return utilizadores_dict

@app.delete("/utilizadores/{utilizador_id}", status_code=204)
def delete_utilizador(
    utilizador_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador"))
):
    db_utilizador = db.query(UtilizadorModel).filter(UtilizadorModel.id == utilizador_id).first()
    if not db_utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    db.delete(db_utilizador)
    db.commit()
    cache_invalidate("stats", "statstpuser", "registrations:")
    return Response(status_code=204)

@app.put("/utilizadores/{utilizador_id}", response_model=UtilizadorResponse)
def update_utilizador(
    utilizador_id: int,
    utilizador: UtilizadorCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador"))
):
    db_utilizador = db.query(UtilizadorModel).filter(UtilizadorModel.id == utilizador_id).first()
    if not db_utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    for key, value in utilizador.dict().items():
        if key == "password":
            setattr(db_utilizador, key, bcrypt_context.hash(value))
        else:
            setattr(db_utilizador, key, value)
    db.commit()
    db.refresh(db_utilizador)
    cache_invalidate("stats", "statstpuser")
    return {
        "id": db_utilizador.id,
        "username": db_utilizador.username,
        "tipo": {"id": db_utilizador.tipo.id, "descricao": db_utilizador.tipo.descricao},
        "created_at": db_utilizador.created_at,
    }


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
    cache_invalidate("stats", "statstpuser", "tipouser:")
    return {"id": novo_tipo.id, "descricao": novo_tipo.descricao}

@app.get("/tipouser", response_model=list[TipoUserResponse])
def list_tipo_user(
    db: Session = Depends(get_db),
):
    cached = cache_get("tipouser:list")
    if cached is not None:
        return cached
    result = db.query(TipoUserModel).all()
    tipouser_dict = [
        {"id": tipo.id, "descricao": tipo.descricao}
        for tipo in result
    ]
    cache_set("tipouser:list", tipouser_dict, ttl=120)
    return tipouser_dict

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
    cache_invalidate("stats", "statstpuser", "tipouser:")
    return {"id": db_tipo.id, "descricao": db_tipo.descricao}

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
    cache_invalidate("stats", "statstpuser", "tipouser:")
    return None

@app.post("/mapas", response_model=MapaResponse)
def create_mapa(
    mapa: MapaCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador","Gestor"))
):
    clube = db.query(ClubeModel).filter(ClubeModel.id == mapa.clube_id).first()
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    
    db_mapa = MapaModel(**mapa.dict())
    db.add(db_mapa)
    db.commit()
    db.refresh(db_mapa)
    cache_invalidate("stats", "mapas:")
    return {
        "id": db_mapa.id,
        "descricao": db_mapa.descricao,
        "latitude": db_mapa.latitude,
        "longitude": db_mapa.longitude,
        "clube_id": db_mapa.clube_id,
    }

@app.get("/mapas", response_model=list[MapaResponse])
def list_mapas(
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user)
):
    cached = cache_get("mapas:list")
    if cached is not None:
        return cached
    result = db.query(MapaModel).all()
    mapas_dict = [
        {
            "id": mapa.id,
            "descricao": mapa.descricao,
            "latitude": mapa.latitude,
            "longitude": mapa.longitude,
            "clube_id": mapa.clube_id,
        }
        for mapa in result
    ]
    cache_set("mapas:list", mapas_dict, ttl=60)
    return mapas_dict

@app.put("/mapas/{mapa_id}", response_model=MapaResponse)
def update_mapa(
    mapa_id: int,
    mapa: MapaCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador","Gestor"))
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
    cache_invalidate("stats", "mapas:")
    return {
        "id": db_mapa.id,
        "descricao": db_mapa.descricao,
        "latitude": db_mapa.latitude,
        "longitude": db_mapa.longitude,
        "clube_id": db_mapa.clube_id,
    }

@app.delete("/mapas/{mapa_id}", status_code=200)
def delete_mapa(
    mapa_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(require_roles("Administrador","Gestor"))
):
    mapa = db.query(MapaModel).filter(MapaModel.id == mapa_id).first()

    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa não encontrado")

    db.delete(mapa)
    db.commit()
    cache_invalidate("stats", "mapas:")
    return {"message": "Mapa apagado com sucesso"}

@app.get("/planos", response_model=list[PlanoResponse])
def list_planos(db: Session = Depends(get_db)):
    cached = cache_get("planos:list")
    if cached is not None:
        return cached
    result = db.query(PlanoModel).all()
    planos_dict = [
        {"id": p.id, "nome": p.nome, "preco": p.preco,
         "limite_clubes": p.limite_clubes, "limite_mapas": p.limite_mapas}
        for p in result
    ]
    cache_set("planos:list", planos_dict, ttl=120)
    return planos_dict

@app.post("/planos", response_model=PlanoResponse, status_code=201)
def create_plano(
    plano: PlanoCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    db_plano = PlanoModel(**plano.dict())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    cache_invalidate("planos:")
    return db_plano

@app.put("/planos/{plano_id}", response_model=PlanoResponse)
def update_plano(
    plano_id: int,
    plano: PlanoCreate,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    db_plano = db.query(PlanoModel).filter(PlanoModel.id == plano_id).first()
    if not db_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    for key, value in plano.dict().items():
        setattr(db_plano, key, value)
    db.commit()
    db.refresh(db_plano)
    cache_invalidate("planos:")
    return db_plano

@app.delete("/planos/{plano_id}", status_code=204)
def delete_plano(
    plano_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    db_plano = db.query(PlanoModel).filter(PlanoModel.id == plano_id).first()
    if not db_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    db.delete(db_plano)
    db.commit()
    cache_invalidate("planos:")
    return None



@app.post("/create-checkout-session")
def create_checkout_session(
    req: CheckoutRequest,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    plano = db.query(PlanoModel).filter(PlanoModel.id == req.plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if plano.preco <= 0:
        raise HTTPException(status_code=400, detail="Este plano é gratuito")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": f"Plano {plano.nome}"},
                    "unit_amount": int(round(plano.preco * 100)),
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{FRONTEND_URL}/planos?success=true&plano_id={plano.id}",
            cancel_url=f"{FRONTEND_URL}/planos?canceled=true",
            metadata={"user_id": str(user.id), "plano_id": str(plano.id)},
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {"url": session.url}


@app.post("/clubes/{clube_id}/ingressar", response_model=IngressarResponse, status_code=201)
def ingressar_clube(
    clube_id: int,
    db: Session = Depends(get_db),
    user: UtilizadorModel = Depends(get_current_user),
):
    clube = db.query(ClubeModel).filter(ClubeModel.id == clube_id).first()
    if not clube:
        raise HTTPException(status_code=404, detail="Clube não encontrado")

    nova_inscricao = MembroClubeModel(
        utilizador_id=user.id,
        clube_id=clube_id,
    )
    db.add(nova_inscricao)

    try:
        db.commit()
        db.refresh(nova_inscricao)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Já está inscrito no clube '{clube.nome}'",
        )

    return IngressarResponse(
        mensagem=f"Inscrito com sucesso no clube '{clube.nome}'!",
        clube_id=clube.id,
        clube_nome=clube.nome,
        inscrito_em=nova_inscricao.inscrito_em,
    )