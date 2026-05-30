import logging

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from mailer.registry import TEMPLATE_MAP

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, email_log_id: str):
    from mailer.models import EmailLog

    try:
        log = EmailLog.objects.get(id=email_log_id)
    except EmailLog.DoesNotExist:
        logger.error("EmailLog %s not found", email_log_id)
        return

    log.last_attempt_at = timezone.now()
    log.save(update_fields=["last_attempt_at"])

    try:
        templates = TEMPLATE_MAP[log.email_type]
        html_body = render_to_string(templates["html"], log.context_data)
        text_body = render_to_string(templates["txt"], log.context_data)

        msg = EmailMultiAlternatives(
            subject=log.subject,
            body=text_body,
            to=[log.recipient],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        log.status = EmailLog.Status.SENT
        log.sent_at = timezone.now()
        log.save(update_fields=["status", "sent_at"])

    except Exception as exc:
        log.retry_count += 1
        log.error_message = str(exc)
        log.save(update_fields=["retry_count", "error_message"])

        try:
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesExceededError:
            log.status = EmailLog.Status.FAILED
            log.save(update_fields=["status"])
            logger.error(
                "Email %s to %s permanently failed after %d retries: %s",
                log.email_type,
                log.recipient,
                log.retry_count,
                exc,
            )
