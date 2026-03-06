import os
os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "5432")
os.environ.setdefault("MYSQL_USER", "test")
os.environ.setdefault("MYSQL_PASSWORD", "test")
os.environ.setdefault("MYSQL_DATABASE", "test_db")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
import auth
import database

# Prevent startup event from connecting to production PostgreSQL
# Must patch BEFORE importing main (which registers the startup handler)
database.init_db = lambda: None

from main import app
from models import TipoUserModel

import main as _main_module
_main_module.init_db = lambda: None

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
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

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[auth.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _seed_tipo(db, descricao="admin"):
    """Insert a TipoUser directly in the DB and return it."""
    tipo = TipoUserModel(descricao=descricao)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@pytest.fixture()
def tipo(db):
    """Fixture that seeds a single TipoUser 'admin'."""
    return _seed_tipo(db)


@pytest.fixture()
def auth_headers(client, db):
    """Register a test user and return headers with a valid JWT."""
    tipo = _seed_tipo(db)
    client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
    })
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": str(tipo.id),
    })
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
