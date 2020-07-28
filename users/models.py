from django.contrib.auth import models as auth_models
from django.db import models


class UserManager(auth_models.UserManager):
    def exists_with_email(self, email):
        return self.filter(email=email).exists()


class User(auth_models.AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField("email address", unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
