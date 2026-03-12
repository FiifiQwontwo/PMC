import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .manager import CustomUserManager
import uuid
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Enter a valid email address.")]
                              )
    phone = models.CharField(max_length=16, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()

        domain = self.email.split('@')[-1]

        if '.' not in domain:
            raise ValidationError({'email': "Enter a valid email domain."})

        if not re.match(r'^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', domain):
            raise ValidationError({'email': "Enter a valid email domain."})


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    full_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated_ip = models.GenericIPAddressField(blank=True, null=True)
    last_user_agent = models.CharField(max_length=255, blank=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.email}"


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_staff')
    full_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated_ip = models.GenericIPAddressField(blank=True, null=True)
    last_user_agent = models.CharField(max_length=255, blank=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.email}"


class AdminInvite(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invited_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='admin_invites'
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} invited by {self.invited_by.email}"