from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import RegistrationSerializer, VerifyEmailSerializer


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Register a new user account and send an email verification link.

        POST /api/v1/accounts/register

        Args:
            request: DRF Request containing username, email, password, role,
                     and optional bio / phone_number fields.

        Returns:
            Response: 201 with user id, username, email, profile, and
                      email_verification expiry; 400 on validation errors.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            serializer.to_representation(user), status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Consume a verification token and mark the user's email as verified.

        POST /api/v1/accounts/verify-email/

        Args:
            request: DRF Request containing a `token` UUID field.

        Returns:
            Response: 200 with a success message on valid token; 400 if the
                      token is missing, invalid, expired, or already used.
        """
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Email verified successfully."}, status=status.HTTP_200_OK
        )
