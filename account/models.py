from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . manager import UserManager
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    mobile = models.PositiveIntegerField()
    creation_date   = models.DateField(auto_now_add=True)
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return self.is_superuser

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return self.is_superuser

