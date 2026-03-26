def test_create_tipo_user(client, auth_headers):
    resp = client.post("/tipouser", json={"descricao": "professor"}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["descricao"] == "professor"
    assert data["id"] is not None


def test_list_tipo_user(client, auth_headers):
    # auth_headers already seeds 1 tipo ("Administrador"); add a second one
    client.post("/tipouser", json={"descricao": "aluno"}, headers=auth_headers)
    resp = client.get("/tipouser")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


def test_update_tipo_user(client, auth_headers):
    create = client.post("/tipouser", json={"descricao": "old_tipo"}, headers=auth_headers)
    tid = create.json()["id"]
    resp = client.put(f"/tipouser/{tid}", json={"descricao": "new_tipo"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["descricao"] == "new_tipo"


def test_update_tipo_user_404(client, auth_headers):
    resp = client.put("/tipouser/9999", json={"descricao": "x"}, headers=auth_headers)
    assert resp.status_code == 404


def test_delete_tipo_user(client, auth_headers):
    create = client.post("/tipouser", json={"descricao": "to_delete"}, headers=auth_headers)
    tid = create.json()["id"]
    resp = client.delete(f"/tipouser/{tid}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_tipo_user_404(client, auth_headers):
    resp = client.delete("/tipouser/9999", headers=auth_headers)
    assert resp.status_code == 404
