from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import UserSignUpSerializer, UserLoginSerializer
from users.services.signup_service import UserService
from users.services.login_service import LoginService
from users.models import User
from .throttle import LoginThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from users.permissions import IsModeratororSelf

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [IsAuthenticated, IsModeratororSelf]

    def get_permissions(self):
        if self.action in ["signup", "login"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == "moderator":
            return User.objects.all()
        if user.role == "user":
            return User.objects.filter(id=user.id)
    @action(detail=False,
            methods=["post"],
            url_path="signup",
            serializer_class=UserSignUpSerializer)
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.signup_user(serializer.validated_data)
        output = UserSignUpSerializer(user) #passing user object to serializer

        return Response({"detail": "User created successfully, please log in.", "user": output.data },status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=["post"],
            url_path="login",
            serializer_class=UserLoginSerializer,
            throttle_classes=[LoginThrottle])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = LoginService.get_token(user)

        return Response({
            "detail": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)

