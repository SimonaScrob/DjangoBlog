from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property


class User(AbstractUser):
    ADMIN = "A"
    MANAGER = "M"
    SIMPLE_USER = "S"
    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (MANAGER, 'MANAGER'),
        (SIMPLE_USER, 'SIMPLE_USER')
    )

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=SIMPLE_USER)
    username = models.CharField(max_length=100, unique=True)

    @property
    def is_admin(self):
        if self.role == "A":
            return True
        return False

    @property
    def is_manager(self):
        if self.role == "M":
            return True
        return False

    @property
    def is_simple_user(self):
        if self.role == "S":
            return True
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
