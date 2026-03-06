def test_create_clube(client, auth_headers):
    resp = client.post("/clubes", json={
        "nome": "Clube Teste",
        "email": "teste@clube.pt",
        "telefone": "912345678",
        "localidade": "Lisboa",
        "evento_at": "2026-06-15",
    }, headers=auth_headers)
    assert resp.status_code == 200
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
