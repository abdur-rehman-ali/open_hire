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
        """
        Set expires_at from expiry_timedelta on first save.

        Args:
            *args: Passed through to Model.save.
            **kwargs: Passed through to Model.save.

        Returns:
            None
        """
        if self.expiry_timedelta is None:
            raise NotImplementedError("Subclasses must define expiry_timedelta")
        if not self.expires_at:
            self.expires_at = timezone.now() + self.expiry_timedelta
        super().save(*args, **kwargs)

    def invalidate(self):
        """
        Mark the token as used and immediately expire it.

        Args:
            None

        Returns:
            None
        """
        self.is_used = True
        self.expires_at = timezone.now()
        self.save(update_fields=["is_used", "expires_at"])

    @classmethod
    def delete_expired(cls):
        """
        Delete all tokens that are used or past their expiry time.

        Args:
            None

        Returns:
            tuple: (number_deleted, {model_label: count}) from QuerySet.delete().
        """
        return cls.objects.filter(
            Q(is_used=True) | Q(expires_at__lte=timezone.now())
        ).delete()

    def is_expired(self):
        """
        Check whether the token is expired or already used.

        Args:
            None

        Returns:
            bool: True if the token is used or past its expiry time.
        """
        return self.is_used or timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.__class__.__name__} for {self.user.username}"
