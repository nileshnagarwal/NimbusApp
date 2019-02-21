"""Here we extend and alter the Base User Model of Django. We remove the Username
field and make email the primary unique field.
Refer: https://www.fomfus.com/articles/how-to-use-email-as-username-for (cont)
-django-authentication-removing-the-username
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Model Managers are added here.
# UserManager is overriden to change username to email
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Create your models here.
# User model is overriden to add user_type and change username to email.
class User(AbstractUser):
    """Base User Model + userType field"""

    USERTYPE_CHOICES = (
        (1, 'Developer'),
        (2, 'Admin'),
        (3, 'Sales'),
        (4, 'Traffic Incharge'),
        (5, 'Accounts'),
    )

    username = None

    user_type = models.IntegerField(choices=USERTYPE_CHOICES, default=4)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
