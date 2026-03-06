from tests.conftest import _seed_tipo


def test_register_success(client, db):
    _seed_tipo(db)
    resp = client.post("/auth/", json={
        "username": "newuser",
        "password": "Str0ng!Pass",
        "tipo_id": 1,
    })
    assert resp.status_code == 201
    assert resp.json()["message"] == "Utilizador Criado com Sucesso"


def test_register_duplicate_username(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={"username": "dup", "password": "Pass1!abc", "tipo_id": 1})
    resp = client.post("/auth/", json={"username": "dup", "password": "Pass2!abc", "tipo_id": 1})
    assert resp.status_code == 400


def test_login_returns_jwt(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": 1,
    })
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": "1",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, db):
    _seed_tipo(db)
    client.post("/auth/", json={
        "username": "testuser",
        "password": "Str0ng!Pass",
        "tipo_id": 1,
    })
    resp = client.post("/auth/token", data={
        "username": "testuser",
        "password": "wrong",
        "tipo_id": "1",
    })
    assert resp.status_code == 401


def test_protected_route_without_token(client):
    resp = client.get("/clubes")
    assert resp.status_code == 401
