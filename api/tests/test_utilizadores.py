from tests.conftest import _seed_tipo


def test_list_utilizadores(client, auth_headers):
    resp = client.get("/utilizadores", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert "username" in data[0]
    assert "tipo" in data[0]


def test_update_utilizador(client, auth_headers, db):
    users = client.get("/utilizadores", headers=auth_headers).json()
    uid = users[0]["id"]

    _seed_tipo(db, descricao="aluno")

    resp = client.put(f"/utilizadores/{uid}", json={
        "username": "updated_user",
        "password": "NewStr0ng!Pass",
        "tipo_id": 2,
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "updated_user"


def test_delete_utilizador(client, auth_headers):
    users = client.get("/utilizadores", headers=auth_headers).json()
    uid = users[0]["id"]
    resp = client.delete(f"/utilizadores/{uid}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_utilizador_404(client, auth_headers):
    resp = client.delete("/utilizadores/9999", headers=auth_headers)
    assert resp.status_code == 404
