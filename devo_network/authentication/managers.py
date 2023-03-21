from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """ Manager for create user & superuser """

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Every user should have an email.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.full_clean()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser equals True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active equals True")

        return self._create_user(email, password, **extra_fields)
