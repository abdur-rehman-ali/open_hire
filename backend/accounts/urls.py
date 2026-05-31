from django.urls import path
from .views import RegistrationView, VerifyEmailView

app_name = "accounts"

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("verify-email", VerifyEmailView.as_view(), name="verify-email"),
]
