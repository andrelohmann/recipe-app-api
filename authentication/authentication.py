from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


# .requirements/rest_framework_simplejwt/authentication.py
# -> override authenticate method
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)

            if header is None:
                # read the rqaw_token from the AUTH_COOKIE
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except Exception:
            return None