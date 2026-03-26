from tests.conftest import _seed_tipo, _seed_organization, _seed_plano


def test_register_success(client, db):
    org = _seed_organization(db)
    plano = _seed_plano(db)
    tipo = _seed_tipo(db)
    resp = client.post("/auth/", json={
        "username": "newuser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
        "plano_id": plano.id,
        "organization_id": org.id,
    })
    assert resp.status_code == 201
    assert resp.json()["message"] == "Utilizador Criado com Sucesso"


def test_register_duplicate_username(client, db):
    org = _seed_organization(db)
    plano = _seed_plano(db)
    tipo = _seed_tipo(db)
    payload = {"username": "dup", "password": "Pass1!abc", "tipo_id": tipo.id, "plano_id": plano.id, "organization_id": org.id}
    client.post("/auth/", json=payload)
    resp = client.post("/auth/", json={**payload, "password": "Pass2!abc"})
    assert resp.status_code == 400


def test_login_returns_jwt(client, db):
    org = _seed_organization(db)
    plano = _seed_plano(db)
    tipo = _seed_tipo(db)
    client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
        "plano_id": plano.id,
        "organization_id": org.id,
    })
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "Str0ng!Pass",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, db):
    org = _seed_organization(db)
    plano = _seed_plano(db)
    tipo = _seed_tipo(db)
    client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
        "plano_id": plano.id,
        "organization_id": org.id,
    })
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "wrong",
    })
    assert resp.status_code == 401


def test_protected_route_without_token(client):
    resp = client.get("/clubes")
    assert resp.status_code == 401
