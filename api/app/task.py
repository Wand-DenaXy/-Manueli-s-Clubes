import logging
from app.celery_app import celery
from app.database import SessionLocal
from app.models import StripeEventModel, UtilizadorModel, PlanoModel, NotificacaoModel
from app.cache import cache_invalidate
from app.email_service import payment_failed_email

logger = logging.getLogger(__name__)


@celery.task(
    bind=True,
    max_retries=5,
    default_retry_delay=30,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def process_stripe_event(self, event_id: str, event_type: str, event_data: dict):
    db = SessionLocal()
    try:
        existing = db.query(StripeEventModel).filter(
            StripeEventModel.event_id == event_id
        ).first()
        if existing:
            logger.info("Evento Stripe %s já processado, a ignorar.", event_id)
            return {"status": "duplicate", "event_id": event_id}

        if event_type == "checkout.session.completed":
            metadata = event_data.get("metadata", {})
            user_id = metadata.get("user_id")
            plano_id = metadata.get("plano_id")

            if not user_id or not plano_id:
                logger.warning("Metadata incompleta no evento %s", event_id)
                return {"status": "skipped", "reason": "missing metadata"}

            user = db.query(UtilizadorModel).filter(
                UtilizadorModel.id == int(user_id)
            ).first()
            if not user:
                logger.warning("Utilizador %s não encontrado para evento %s", user_id, event_id)
                return {"status": "skipped", "reason": "user not found"}

            plano = db.query(PlanoModel).filter(
                PlanoModel.id == int(plano_id)
            ).first()
            if not plano:
                logger.warning("Plano %s não encontrado para evento %s", plano_id, event_id)
                return {"status": "skipped", "reason": "plano not found"}

            user.plano_id = plano.id
            db.add(user)

        elif event_type in (
            "payment_intent.payment_failed",
            "checkout.session.async_payment_failed",
        ):
            metadata = event_data.get("metadata", {})
            user_id = metadata.get("user_id")

            if not user_id:
                logger.warning("Metadata sem user_id no evento %s", event_id)
                return {"status": "skipped", "reason": "missing user_id"}

            user = db.query(UtilizadorModel).filter(
                UtilizadorModel.id == int(user_id)
            ).first()
            if not user:
                logger.warning("Utilizador %s não encontrado para evento %s", user_id, event_id)
                return {"status": "skipped", "reason": "user not found"}

            plano_free = db.query(PlanoModel).filter(PlanoModel.preco == 0).first()
            if plano_free:
                user.plano_id = plano_free.id
                db.add(user)
                logger.info(
                    "Pagamento falhou — utilizador %s revertido para plano Free (evento %s)",
                    user_id, event_id,
                )

            notif = NotificacaoModel(
                utilizador_id=user.id,
                tipo="payment_failed",
                titulo="Pagamento falhou",
                mensagem="O teu pagamento não foi processado. O teu plano foi revertido para Free. "
                         "Atualiza o teu método de pagamento para continuar com funcionalidades premium.",
            )
            db.add(notif)

            if user.email:
                payment_failed_email(user.email, user.username)

        db_event = StripeEventModel(event_id=event_id, event_type=event_type)
        db.add(db_event)
        db.commit()

        cache_invalidate("utilizadores:", "planos:")
        logger.info("Evento Stripe %s processado com sucesso.", event_id)
        return {"status": "processed", "event_id": event_id}

    except Exception as exc:
        db.rollback()
        logger.exception("Erro ao processar evento Stripe %s", event_id)
        raise self.retry(exc=exc)
    finally:
        db.close()
