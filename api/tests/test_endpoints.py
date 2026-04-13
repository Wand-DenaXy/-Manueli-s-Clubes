"""Tests for /me, /me/plano, /clubesAdmin, /organizations, /notificacoes, /planos CRUD."""



# ── GET /me ───────────────────────────────────────────────────────

def test_get_me(client, db, auth_headers):
    resp = client.get("/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["tipo"]["descricao"] == "Administrador"
    assert data["plano"] is not None


# ── PUT /me/plano/{id} ───────────────────────────────────────────

def test_confirmar_plano_success(client, db, auth_headers):
    from app.models import PlanoModel
    pro = PlanoModel(nome="Pro", preco=9.99, limite_clubes=15, limite_mapas=20)
    db.add(pro)
    db.commit()
    db.refresh(pro)

    resp = client.put(f"/me/plano/{pro.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["plano"]["nome"] == "Pro"


def test_confirmar_plano_not_found(client, db, auth_headers):
    resp = client.put("/me/plano/9999", headers=auth_headers)
    assert resp.status_code == 404


# ── GET /clubesAdmin ──────────────────────────────────────────────

def test_list_clubes_admin(client, db, auth_headers):
    # Create a club first
    client.post("/clubes", json={"nome": "AdminClub"}, headers=auth_headers)
    resp = client.get("/clubesAdmin", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


# ── /organizations ────────────────────────────────────────────────

def test_create_organization(client, db, auth_headers):
    resp = client.post("/organizations?nome=NewOrg", headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["nome"] == "NewOrg"


def test_list_organizations(client, db, auth_headers):
    resp = client.get("/organizations", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── GET /notificacoes ─────────────────────────────────────────────

def test_list_notificacoes_empty(client, db, auth_headers):
    resp = client.get("/notificacoes", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_notificacoes_with_data(client, db, auth_headers):
    from app.models import NotificacaoModel, UtilizadorModel
    user = db.query(UtilizadorModel).filter(UtilizadorModel.username == "testuser").first()
    notif = NotificacaoModel(
        utilizador_id=user.id,
        tipo="payment_succeeded",
        titulo="Pagamento OK",
        mensagem="Teste",
    )
    db.add(notif)
    db.commit()

    resp = client.get("/notificacoes", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["tipo"] == "payment_succeeded"


# ── /planos CRUD ──────────────────────────────────────────────────

def test_list_planos(client, db, auth_headers):
    resp = client.get("/planos")
    assert resp.status_code == 200


def test_create_plano(client, db, auth_headers):
    resp = client.post(
        "/planos",
        json={"nome": "Ultra", "preco": 49.99, "limite_clubes": -1, "limite_mapas": -1},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["nome"] == "Ultra"


def test_update_plano(client, db, auth_headers):
    from app.models import PlanoModel
    p = PlanoModel(nome="Old", preco=1.0, limite_clubes=1, limite_mapas=1)
    db.add(p)
    db.commit()
    db.refresh(p)

    resp = client.put(
        f"/planos/{p.id}",
        json={"nome": "New", "preco": 2.0, "limite_clubes": 5, "limite_mapas": 5},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["nome"] == "New"


def test_update_plano_404(client, db, auth_headers):
    resp = client.put(
        "/planos/9999",
        json={"nome": "X", "preco": 0, "limite_clubes": 0, "limite_mapas": 0},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_delete_plano(client, db, auth_headers):
    from app.models import PlanoModel
    p = PlanoModel(nome="ToDelete", preco=1.0, limite_clubes=1, limite_mapas=1)
    db.add(p)
    db.commit()
    db.refresh(p)

    resp = client.delete(f"/planos/{p.id}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_plano_404(client, db, auth_headers):
    resp = client.delete("/planos/9999", headers=auth_headers)
    assert resp.status_code == 404
