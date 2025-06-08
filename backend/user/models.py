from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator  # Import for phone number validation
from django.db import models
from user.managers import UserManager

phone_number_regex = r"^\+?1?\d{9,15}$"  # E.g., +1234567890, 07700900000
phone_number_validator = RegexValidator(
    regex=phone_number_regex,
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # A unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions_set",  # A unique related_name
        related_query_name="user",
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_number_validator],
        unique=True,
    )
    email = models.EmailField(
        unique=True,
        null=True,  # Allow null for email if phone is the primary identifier
        blank=True,
        help_text='Optional: Primary email address for the user.',
    )
    password = models.CharField(max_length=128, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(
                fields=('phone_number',),
                name='user_phone_number_idx',
            ),
        ]

    def __str__(self):
        return self.phone_number
