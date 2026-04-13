def test_create_clube(client, auth_headers):
    resp = client.post("/clubes", json={
        "nome": "Clube Teste",
        "email": "teste@clube.pt",
        "telefone": "912345678",
        "localidade": "Lisboa",
        "evento_at": "2026-06-15",
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["nome"] == "Clube Teste"
    assert data["id"] is not None


def test_list_clubes(client, auth_headers):
    client.post("/clubes", json={"nome": "C1"}, headers=auth_headers)
    client.post("/clubes", json={"nome": "C2"}, headers=auth_headers)
    resp = client.get("/clubes", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Old"}, headers=auth_headers)
    cid = create.json()["id"]
    resp = client.put(f"/clubes/{cid}", json={"nome": "New"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["nome"] == "New"


def test_delete_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "ToDelete"}, headers=auth_headers)
    cid = create.json()["id"]
    resp = client.delete(f"/clubes/{cid}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_clube_404(client, auth_headers):
    resp = client.delete("/clubes/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_ingressar_clube(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Ingresso"}, headers=auth_headers)
    cid = create.json()["id"]
    resp = client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["clube_id"] == cid
    assert "inscrito_em" in data


def test_ingressar_duplicate_409(client, auth_headers):
    create = client.post("/clubes", json={"nome": "Dup"}, headers=auth_headers)
    cid = create.json()["id"]
    client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    resp = client.post(f"/clubes/{cid}/ingressar", headers=auth_headers)
    assert resp.status_code == 409


def test_ingressar_clube_inexistente_404(client, auth_headers):
    resp = client.post("/clubes/9999/ingressar", headers=auth_headers)
    assert resp.status_code == 404


def test_create_clube_plan_limit_enforced(client, db):
    """Users on Free plan (limite_clubes=1) get 403 after hitting the limit."""
    from tests.conftest import _seed_organization, _seed_plano, _seed_tipo

    org = _seed_organization(db)
    plano = _seed_plano(db, nome="Starter", preco=0.0, limite_clubes=1, limite_mapas=1)
    tipo = _seed_tipo(db, descricao="Administrador")

    client.post("/auth/", json={
        "username": "limituser",
        "password": "Str0ng!Pass",
        "tipo_id": tipo.id,
        "plano_id": plano.id,
        "organization_id": org.id,
    })
    resp = client.post("/auth/token", data={
        "username": "limituser",
        "password": "Str0ng!Pass",
    })
    headers = {"Authorization": f"Bearer {resp.json()['access_token']}"}

    # First clube — within limit
    r1 = client.post("/clubes", json={"nome": "Club1"}, headers=headers)
    assert r1.status_code == 201

    # Second clube — exceeds limit → 403
    r2 = client.post("/clubes", json={"nome": "Club2"}, headers=headers)
    assert r2.status_code == 403
