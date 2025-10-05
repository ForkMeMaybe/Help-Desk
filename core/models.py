from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("agent", "Agent"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "email"
    email = models.EmailField(_("email address"), unique=True)
    REQUIRED_FIELDS = []
