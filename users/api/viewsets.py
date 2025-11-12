from rest_framework.response import Response
from rest_framework import viewsets, status, throttling
from rest_framework.decorators import action
from .serializers import UserSignUpSerializer, UserLoginSerializer
from users.services.signup_service import UserService
from users.services.login_service import LoginService
from users.models import User
from .throttle import LoginThrottle


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    @action(detail=False, methods=["post"], url_path="signup")
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.signup_user(serializer.validated_data)
        output = UserSignUpSerializer(user)
        return Response({"detail": "User created successfully, please log in.", "user": output.data },status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="login", throttle_classes=[LoginThrottle])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = LoginService.get_token(user)

        return Response({
            "detail": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)

