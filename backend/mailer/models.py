import uuid
from django.db import models


class EmailLog(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    class EmailType(models.TextChoices):
        EMAIL_VERIFICATION = "email_verification", "Email Verification"
        PASSWORD_RESET = "password_reset", "Password Reset"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    email_type = models.CharField(max_length=50, choices=EmailType.choices)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    context_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True, default="")
    retry_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Email Log"
        verbose_name_plural = "Email Logs"
        indexes = [models.Index(fields=["status", "created_at"])]

    def __str__(self):
        return f"[{self.email_type}] {self.recipient} — {self.status}"
