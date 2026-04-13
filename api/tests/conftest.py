import os

# ── env vars must be set BEFORE any app imports ──────────────────
os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "5432")
os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test_db")
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_dummy")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Patch init_db BEFORE importing main so the startup event is a no-op
import app.database as database
database.init_db = lambda: None

import app.auth as auth
from main import app
from app.models import TipoUserModel, PlanoModel, OrganizationModel

import main as _main_module
_main_module.init_db = lambda: None

# ── in-memory SQLite engine for tests ────────────────────────────
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test and drop them after."""
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[database.get_db] = override_get_db
    app.dependency_overrides[auth.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── seed helpers ──────────────────────────────────────────────────

def _seed_organization(db, nome="TestOrg"):
    org = OrganizationModel(nome=nome)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def _seed_plano(db, nome="Free", preco=0.0, limite_clubes=3, limite_mapas=1):
    plano = PlanoModel(nome=nome, preco=preco, limite_clubes=limite_clubes, limite_mapas=limite_mapas)
    db.add(plano)
    db.commit()
    db.refresh(plano)
    return plano


def _seed_tipo(db, descricao="Administrador"):
    """Insert a TipoUser directly in the DB and return it."""
    tipo = TipoUserModel(descricao=descricao)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@pytest.fixture()
def tipo(db):
    """Fixture that seeds a single TipoUser 'Administrador'."""
    return _seed_tipo(db)


@pytest.fixture()
def auth_headers(client, db):
    """
    Seeds Organisation + Plano + TipoUser, registers a test user with role
    'Administrador' (required by RBAC for clube/mapa/utilizador endpoints),
    logs in, and returns the Authorization headers.
    """
    org = _seed_organization(db)
    plano = _seed_plano(db)
    tipo = _seed_tipo(db, descricao="Administrador")

    resp = client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
        "plano_id": plano.id,
        "organization_id": org.id,
    })
    assert resp.status_code == 201, f"Register failed: {resp.text}"

    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "Str0ng!Pass",
    })
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
