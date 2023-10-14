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
    creation_date   = models.DateField(auto_now=True)
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    
