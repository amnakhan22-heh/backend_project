from users.models import User

class UserService:
    @staticmethod
    def signup_user(validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
