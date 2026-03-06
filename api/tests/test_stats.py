def test_stats_public(client):
    """GET /stats is public — no auth required."""
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "clubes" in data
    assert "utilizadores" in data
    assert "tipousers" in data
    assert "mapas" in data


def test_statstpuser(client, auth_headers):
    resp = client.get("/statstpuser", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) >= 1


def test_registrations(client, auth_headers):
    resp = client.get("/registrations", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 12
    assert "month" in data[0]
    assert "count" in data[0]


def test_statstpuser_no_auth(client):
    resp = client.get("/statstpuser")
    assert resp.status_code == 401


def test_registrations_no_auth(client):
    resp = client.get("/registrations")
    assert resp.status_code == 401
