"""Tests for email_service.py — SMTP mocked."""

from unittest.mock import patch, MagicMock


def test_send_email_not_configured():
    """Returns False when SMTP is not configured."""
    from app.email_service import send_email
    with patch("app.email_service.SMTP_HOST", ""), \
         patch("app.email_service.SMTP_USER", ""), \
         patch("app.email_service.SMTP_PASSWORD", ""):
        assert send_email("test@x.com", "Subject", "<p>body</p>") is False


def test_send_email_success():
    """Returns True when SMTP sends successfully."""
    from app.email_service import send_email
    mock_smtp = MagicMock()
    with patch("app.email_service.SMTP_HOST", "smtp.test.com"), \
         patch("app.email_service.SMTP_USER", "user"), \
         patch("app.email_service.SMTP_PASSWORD", "pass"), \
         patch("app.email_service.SMTP_FROM", "from@test.com"), \
         patch("smtplib.SMTP", return_value=mock_smtp):
        mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
        mock_smtp.__exit__ = MagicMock(return_value=False)
        result = send_email("dest@x.com", "Subject", "<p>OK</p>")
        assert result is True


def test_send_email_failure():
    """Returns False when SMTP raises an exception."""
    from app.email_service import send_email
    with patch("app.email_service.SMTP_HOST", "smtp.test.com"), \
         patch("app.email_service.SMTP_USER", "user"), \
         patch("app.email_service.SMTP_PASSWORD", "pass"), \
         patch("smtplib.SMTP", side_effect=ConnectionRefusedError("SMTP down")):
        result = send_email("dest@x.com", "Subject", "<p>fail</p>")
        assert result is False


def test_payment_failed_email():
    """payment_failed_email calls send_email with correct subject."""
    from app.email_service import payment_failed_email
    with patch("app.email_service.send_email", return_value=True) as mock_send:
        result = payment_failed_email("user@x.com", "TestUser")
        assert result is True
        args = mock_send.call_args
        assert "falhou" in args[0][1].lower()


def test_payment_succeeded_email():
    """payment_succeeded_email calls send_email with correct subject."""
    from app.email_service import payment_succeeded_email
    with patch("app.email_service.send_email", return_value=True) as mock_send:
        result = payment_succeeded_email("user@x.com", "TestUser")
        assert result is True
        args = mock_send.call_args
        assert "sucedido" in args[0][1].lower() or "bem-sucedido" in args[0][1].lower()
