from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import PaymentTransaction


class PaymentRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        if request.path == '/api/upload/':
            # Manually authenticate JWT token
            try:
                user_auth_tuple = self.jwt_auth.authenticate(request)
                if user_auth_tuple is None:
                    return JsonResponse({"error": "Authentication required"}, status=401)

                user, token = user_auth_tuple
                request.user = user

                has_paid = PaymentTransaction.objects.filter(
                    user=user,
                    status='success'
                ).exists()

                if not has_paid:
                    return JsonResponse({"error": "You must complete payment before uploading"}, status=403)

            except Exception as e:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)
