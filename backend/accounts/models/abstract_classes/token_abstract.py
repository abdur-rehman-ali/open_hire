import uuid
from django.utils import timezone
from django.db import models
from django.db.models import Q


class TokenAbstract(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    expiry_timedelta = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.expiry_timedelta is None:
            raise NotImplementedError("Subclasses must define expiry_timedelta")
        if not self.expires_at:
            self.expires_at = timezone.now() + self.expiry_timedelta
        super().save(*args, **kwargs)

    def invalidate(self):
        self.is_used = True
        self.expires_at = timezone.now()
        self.save(update_fields=["is_used", "expires_at"])

    @classmethod
    def delete_expired(cls):
        """Delete expired or used tokens"""
        return cls.objects.filter(
            Q(is_used=True) | Q(expires_at__lte=timezone.now())
        ).delete()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.__class__.__name__} for {self.user.username}"
