"""Tests for Stripe webhook endpoint, checkout session, and Celery task processing."""

import json
from unittest.mock import patch, MagicMock

from tests.conftest import _seed_tipo, _seed_organization, _seed_plano


# ── Stripe Webhook endpoint ──────────────────────────────────────

def test_stripe_webhook_no_secret(client, db):
    """Webhook fails when STRIPE_WEBHOOK_SECRET is empty."""
    import main as m
    original = m.STRIPE_WEBHOOK_SECRET
    m.STRIPE_WEBHOOK_SECRET = ""
    try:
        resp = client.post("/stripe/webhook", content=b'{"id":"x"}', headers={"stripe-signature": "sig"})
        assert resp.status_code == 500
        assert "configurado" in resp.json()["detail"].lower()
    finally:
        m.STRIPE_WEBHOOK_SECRET = original


def test_stripe_webhook_invalid_payload(client, db):
    """Webhook returns 400 for invalid payload."""
    import main as m
    original = m.STRIPE_WEBHOOK_SECRET
    m.STRIPE_WEBHOOK_SECRET = "whsec_test"
    try:
        with patch("stripe.Webhook.construct_event", side_effect=ValueError("bad")):
            resp = client.post(
                "/stripe/webhook",
                content=b"bad-payload",
                headers={"stripe-signature": "sig"},
            )
            assert resp.status_code == 400
            assert "inválido" in resp.json()["detail"].lower() or "Payload" in resp.json()["detail"]
    finally:
        m.STRIPE_WEBHOOK_SECRET = original


def test_stripe_webhook_invalid_signature(client, db):
    """Webhook returns 400 for invalid Stripe signature."""
    import stripe as stripe_mod
    import main as m
    original = m.STRIPE_WEBHOOK_SECRET
    m.STRIPE_WEBHOOK_SECRET = "whsec_test"
    try:
        with patch(
            "stripe.Webhook.construct_event",
            side_effect=stripe_mod.SignatureVerificationError("bad sig", "sig"),
        ):
            resp = client.post(
                "/stripe/webhook",
                content=b"payload",
                headers={"stripe-signature": "bad"},
            )
            assert resp.status_code == 400
            assert "Assinatura" in resp.json()["detail"]
    finally:
        m.STRIPE_WEBHOOK_SECRET = original


def test_stripe_webhook_duplicate_event(client, db):
    """Webhook returns 'duplicate' for an already-processed event."""
    import main as m
    from app.models import StripeEventModel

    original = m.STRIPE_WEBHOOK_SECRET
    m.STRIPE_WEBHOOK_SECRET = "whsec_test"

    # Pre-insert the event
    evt = StripeEventModel(event_id="evt_duplicate_123", event_type="checkout.session.completed")
    db.add(evt)
    db.commit()

    payload = json.dumps({
        "id": "evt_duplicate_123",
        "type": "checkout.session.completed",
        "data": {"object": {}},
    })

    try:
        with patch("stripe.Webhook.construct_event", return_value=True):
            resp = client.post(
                "/stripe/webhook",
                content=payload.encode(),
                headers={"stripe-signature": "valid"},
            )
            assert resp.status_code == 200
            assert resp.json()["status"] == "duplicate"
    finally:
        m.STRIPE_WEBHOOK_SECRET = original


def test_stripe_webhook_queues_event(client, db):
    """Webhook queues a new event via Celery and returns 'queued'."""
    import main as m

    original = m.STRIPE_WEBHOOK_SECRET
    m.STRIPE_WEBHOOK_SECRET = "whsec_test"

    payload = json.dumps({
        "id": "evt_new_456",
        "type": "invoice.payment_failed",
        "data": {"object": {"metadata": {"user_id": "1"}, "customer_email": "a@b.com"}},
    })

    try:
        with patch("stripe.Webhook.construct_event", return_value=True), \
             patch("main.process_stripe_event.delay") as mock_delay:
            resp = client.post(
                "/stripe/webhook",
                content=payload.encode(),
                headers={"stripe-signature": "valid"},
            )
            assert resp.status_code == 200
            assert resp.json()["status"] == "queued"
            mock_delay.assert_called_once()
    finally:
        m.STRIPE_WEBHOOK_SECRET = original


# ── Checkout session ──────────────────────────────────────────────

def test_create_checkout_session_free_plan_rejected(client, db, auth_headers):
    """Cannot checkout on a free plan (price = 0)."""
    from app.models import PlanoModel
    free = db.query(PlanoModel).filter(PlanoModel.preco == 0).first()
    resp = client.post(
        "/create-checkout-session",
        json={"plano_id": free.id},
        headers=auth_headers,
    )
    assert resp.status_code == 400
    assert "gratuito" in resp.json()["detail"].lower()


def test_create_checkout_session_plan_not_found(client, db, auth_headers):
    """Checkout fails on a non-existent plan."""
    resp = client.post(
        "/create-checkout-session",
        json={"plano_id": 9999},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_create_checkout_session_success(client, db, auth_headers):
    """Checkout creates a Stripe session and returns a URL."""
    from app.models import PlanoModel
    pro = PlanoModel(nome="Pro", preco=9.99, limite_clubes=15, limite_mapas=20)
    db.add(pro)
    db.commit()
    db.refresh(pro)

    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"
    with patch("stripe.checkout.Session.create", return_value=mock_session):
        resp = client.post(
            "/create-checkout-session",
            json={"plano_id": pro.id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://checkout.stripe.com/test"


def test_create_checkout_session_stripe_error(client, db, auth_headers):
    """Checkout returns 502 when Stripe API fails."""
    import stripe as stripe_mod
    from app.models import PlanoModel
    pro = PlanoModel(nome="ProErr", preco=19.99, limite_clubes=15, limite_mapas=20)
    db.add(pro)
    db.commit()
    db.refresh(pro)

    with patch(
        "stripe.checkout.Session.create",
        side_effect=stripe_mod.StripeError("Connection error"),
    ):
        resp = client.post(
            "/create-checkout-session",
            json={"plano_id": pro.id},
            headers=auth_headers,
        )
        assert resp.status_code == 502


# ── Celery task: process_stripe_event ─────────────────────────────

def _make_db_session(db_fixture):
    """Create a mock SessionLocal that returns the test DB session."""
    def fake_session_local():
        return db_fixture
    return fake_session_local


def test_task_checkout_session_completed(db):
    """Task processes checkout.session.completed and updates user plan."""
    from app.models import UtilizadorModel
    from app.task import process_stripe_event

    org = _seed_organization(db)
    plano_free = _seed_plano(db, "Free", 0.0, 3, 1)
    plano_pro = _seed_plano(db, "Pro", 9.99, 15, 20)
    tipo = _seed_tipo(db)

    user = UtilizadorModel(
        username="taskuser", password="hashed",
        tipo_id=tipo.id, plano_id=plano_free.id, organization_id=org.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch("app.task.cache_invalidate"), \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_checkout_001",
            event_type="checkout.session.completed",
            event_data={"metadata": {"user_id": str(user.id), "plano_id": str(plano_pro.id)}},
        )

    assert result["status"] == "processed"
    db.refresh(user)
    assert user.plano_id == plano_pro.id


def test_task_invoice_payment_failed(db):
    """Task processes invoice.payment_failed — reverts user to Free + creates notification."""
    from app.models import UtilizadorModel, NotificacaoModel
    from app.task import process_stripe_event

    org = _seed_organization(db)
    plano_free = _seed_plano(db, "Free", 0.0, 3, 1)
    plano_pro = _seed_plano(db, "Pro", 9.99, 15, 20)
    tipo = _seed_tipo(db)

    user = UtilizadorModel(
        username="failuser", password="hashed", email="fail@test.com",
        tipo_id=tipo.id, plano_id=plano_pro.id, organization_id=org.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch("app.task.cache_invalidate"), \
         patch("app.task.payment_failed_email") as mock_email, \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_fail_001",
            event_type="invoice.payment_failed",
            event_data={"metadata": {"user_id": str(user.id)}, "customer_email": "fail@test.com"},
        )

    assert result["status"] == "processed"
    db.refresh(user)
    assert user.plano_id == plano_free.id
    # Notification was created
    notif = db.query(NotificacaoModel).filter(NotificacaoModel.utilizador_id == user.id).first()
    assert notif is not None
    assert notif.tipo == "payment_failed"
    mock_email.assert_called_once_with("fail@test.com", "failuser")


def test_task_invoice_payment_succeeded(db):
    """Task processes invoice.payment_succeeded — creates notification + sends email."""
    from app.models import UtilizadorModel, NotificacaoModel
    from app.task import process_stripe_event

    org = _seed_organization(db)
    plano_free = _seed_plano(db, "Free", 0.0, 3, 1)
    tipo = _seed_tipo(db)

    user = UtilizadorModel(
        username="successuser", password="hashed", email="ok@test.com",
        tipo_id=tipo.id, plano_id=plano_free.id, organization_id=org.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch("app.task.cache_invalidate"), \
         patch("app.task.payment_succeeded_email") as mock_email, \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_success_001",
            event_type="invoice.payment_succeeded",
            event_data={"metadata": {"user_id": str(user.id)}, "customer_email": "ok@test.com"},
        )

    assert result["status"] == "processed"
    notif = db.query(NotificacaoModel).filter(NotificacaoModel.utilizador_id == user.id).first()
    assert notif is not None
    assert notif.tipo == "payment_succeeded"
    mock_email.assert_called_once_with("ok@test.com", "successuser")


def test_task_duplicate_event_skipped(db):
    """Task skips an already-processed event (idempotency)."""
    from app.models import StripeEventModel
    from app.task import process_stripe_event

    # Pre-insert
    evt = StripeEventModel(event_id="evt_dup_task", event_type="checkout.session.completed")
    db.add(evt)
    db.commit()

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_dup_task",
            event_type="checkout.session.completed",
            event_data={"metadata": {"user_id": "1", "plano_id": "1"}},
        )
    assert result["status"] == "duplicate"


def test_task_checkout_missing_metadata(db):
    """Task skips checkout event with incomplete metadata."""
    from app.task import process_stripe_event

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_no_meta",
            event_type="checkout.session.completed",
            event_data={"metadata": {}},
        )
    assert result["status"] == "skipped"
    assert result["reason"] == "missing metadata"


def test_task_payment_failed_user_not_found(db):
    """Task skips payment_failed when no user can be resolved."""
    from app.task import process_stripe_event

    with patch("app.task.SessionLocal", _make_db_session(db)), \
         patch.object(db, "close"):
        result = process_stripe_event(
            event_id="evt_no_user",
            event_type="invoice.payment_failed",
            event_data={"metadata": {}, "customer_email": "ghost@nowhere.com"},
        )
    assert result["status"] == "skipped"
    assert result["reason"] == "user not found"
