from django.urls import path
from .views import (
    RegistrationView,
    VerifyEmailView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

app_name = "accounts"

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("verify-email", VerifyEmailView.as_view(), name="verify-email"),
    path("password-reset", PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "password-reset/confirm",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
