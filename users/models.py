from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("moderator", "Moderator"), #can see write edit comments
        ("user", "User"),  # cannot access comments
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
