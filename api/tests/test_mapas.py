def _create_clube(client, auth_headers, nome="MapaClube"):
    """Helper: create a clube and return its id."""
    resp = client.post("/clubes", json={"nome": nome}, headers=auth_headers)
    return resp.json()["id"]


def test_create_mapa(client, auth_headers):
    cid = _create_clube(client, auth_headers)
    resp = client.post("/mapas", json={
        "descricao": "Sede do clube",
        "latitude": 38.7223,
        "longitude": -9.1393,
        "clube_id": cid,
    }, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["latitude"] == 38.7223
    assert data["clube_id"] == cid


def test_create_mapa_clube_inexistente(client, auth_headers):
    resp = client.post("/mapas", json={
        "descricao": "X",
        "latitude": 0.0,
        "longitude": 0.0,
        "clube_id": 9999,
    }, headers=auth_headers)
    assert resp.status_code == 404


def test_list_mapas(client, auth_headers):
    cid = _create_clube(client, auth_headers)
    client.post("/mapas", json={
        "latitude": 1.0, "longitude": 2.0, "clube_id": cid,
    }, headers=auth_headers)
    client.post("/mapas", json={
        "latitude": 3.0, "longitude": 4.0, "clube_id": cid,
    }, headers=auth_headers)
    resp = client.get("/mapas", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_mapa(client, auth_headers):
    cid = _create_clube(client, auth_headers)
    create = client.post("/mapas", json={
        "latitude": 1.0, "longitude": 2.0, "clube_id": cid,
    }, headers=auth_headers)
    mid = create.json()["id"]
    resp = client.put(f"/mapas/{mid}", json={
        "descricao": "Atualizado",
        "latitude": 10.0,
        "longitude": 20.0,
        "clube_id": cid,
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["latitude"] == 10.0
    assert resp.json()["descricao"] == "Atualizado"


def test_update_mapa_404(client, auth_headers):
    cid = _create_clube(client, auth_headers)
    resp = client.put("/mapas/9999", json={
        "latitude": 1.0, "longitude": 2.0, "clube_id": cid,
    }, headers=auth_headers)
    assert resp.status_code == 404


def test_delete_mapa(client, auth_headers):
    cid = _create_clube(client, auth_headers)
    create = client.post("/mapas", json={
        "latitude": 1.0, "longitude": 2.0, "clube_id": cid,
    }, headers=auth_headers)
    mid = create.json()["id"]
    resp = client.delete(f"/mapas/{mid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Mapa apagado com sucesso"


def test_delete_mapa_404(client, auth_headers):
    resp = client.delete("/mapas/9999", headers=auth_headers)
    assert resp.status_code == 404
