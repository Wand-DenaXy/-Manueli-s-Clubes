import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)


def send_email(to: str, subject: str, body_html: str) -> bool:
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, to]):
        logger.warning("SMTP não configurado ou destinatário vazio — email não enviado.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, [to], msg.as_string())
        logger.info("Email enviado para %s — assunto: %s", to, subject)
        return True
    except Exception:
        logger.exception("Falha ao enviar email para %s", to)
        return False

def payment_failed_email(to: str, username: str) -> bool:
    subject = "Pagamento falhou — Manueli's Clubes"
    body = f"""
    <html><body>
    <h2>Olá {username},</h2>
    <p>O teu pagamento <strong>não foi processado com sucesso</strong>.</p>
    <p>O teu plano foi revertido para <strong>Free</strong>. 
       Para continuar a usufruir das funcionalidades premium, 
       por favor atualiza o teu método de pagamento.</p>
    <p><a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/planos">
       Atualizar plano</a></p>
    <br>
    <p>— Equipa Manueli's Clubes</p>
    </body></html>
    """
    return send_email(to, subject, body)

def payment_succeeded_email(to: str, username: str) -> bool:
    subject = "Pagamento bem-sucedido — Manueli's Clubes"
    body = f"""
    <html><body>
    <h2>Olá {username},</h2>
    <p>O teu pagamento <strong>foi processado com sucesso</strong>.</p>
    <p>O teu plano foi atualizado para o próximo escalão.</p>
    <br>
    <p>— Equipa Manueli's Clubes</p>
    </body></html>
    """
    return send_email(to, subject, body)
