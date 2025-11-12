from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], allow_blank=False)
    confirm_password = serializers.CharField(write_only=True, required=True, allow_blank=False) # for confirmation
    email = serializers.EmailField(required=True, allow_blank=False)
    first_name = serializers.CharField(required=True,allow_blank=False)
    last_name = serializers.CharField(required=True,allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs


class UserLoginSerializer(serializers.Serializer):
   username = serializers.CharField(required=True , write_only=True)
   password = serializers.CharField(required=True, write_only=True)

   def validate(self, attrs):
       username = attrs.get('username')
       password = attrs.get('password')

       user = authenticate(username=username, password=password) #retunrs the user object if credentials are valid
       if not user:
           raise serializers.ValidationError('Invalid username or password')

       attrs['user'] = user #saving user obj in attr dict
       return attrs

