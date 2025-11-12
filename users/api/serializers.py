from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) # for confirmation
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs


class UserLoginSerializer(serializers.Serializer):
   username = serializers.CharField(required=True)
   password = serializers.CharField(required=True)

   def validate(self, attrs):
       username = attrs.get('username')
       password = attrs.get('password')

       user = authenticate(username=username, password=password) #retunrs the user object if credentials are valid
       if not user:
           raise serializers.ValidationError('Invalid username or password')

       attrs['user'] = user
       return attrs

