import logging

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import F
from django.utils import timezone
from mailer.models import EmailLog
from mailer.registry import TEMPLATE_MAP

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, email_log_id: str):

    try:
        log = EmailLog.objects.get(id=email_log_id)
    except EmailLog.DoesNotExist:
        logger.error(f"EmailLog {email_log_id} not found")
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

    except Exception as exception:
        log = EmailLog.objects.get(id=log.id).update(
            retry_count=F("retry_count") + 1,
            error_message=str(exception)
        )
        log.refresh_from_db()

        try:
            raise self.retry(exc=exception, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesExceededError:
            log.status = EmailLog.Status.FAILED
            log.save(update_fields=["status"])
            logger.error(
                f"Email {log.email_type} to {log.recipient} permanently failed after {log.retry_count} retries: {exception}"
            )
