from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import RegistrationSerializer


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
