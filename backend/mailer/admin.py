from django.contrib import admin, messages

from mailer.models import EmailLog
from mailer.tasks import send_email_task


@admin.action(description="Resend selected emails")
def resend_emails(modeladmin, request, queryset):
    count = 0
    for log in queryset:
        log.status = EmailLog.Status.PENDING
        log.error_message = ""
        log.retry_count = 0
        log.save(update_fields=["status", "error_message", "retry_count"])
        send_email_task.delay(str(log.id))
        count += 1
    modeladmin.message_user(
        request,
        f"{count} email(s) queued for resend.",
        messages.SUCCESS,
    )


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email_type",
        "recipient",
        "subject",
        "status",
        "retry_count",
        "created_at",
        "sent_at",
    ]
    list_filter = ["status", "email_type"]
    search_fields = ["recipient", "subject"]
    readonly_fields = [
        "id",
        "recipient",
        "subject",
        "email_type",
        "status",
        "context_data",
        "error_message",
        "retry_count",
        "created_at",
        "sent_at",
        "last_attempt_at",
    ]
    actions = [resend_emails]
    ordering = ["-created_at"]
