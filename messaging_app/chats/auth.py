from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class.
    You can override methods if needed.
    """
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        # Optional: Add custom checks or logging here
        return user
