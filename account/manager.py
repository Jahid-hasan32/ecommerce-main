from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, mobile,  password=None):

        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile = mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile, password=None):

        user = self.create_user(
            email,
            password=password,
            username=username,
            mobile = mobile,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


