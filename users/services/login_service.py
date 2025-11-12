from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class LoginService:
    @staticmethod
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }