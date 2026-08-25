import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class AdminUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role="EDITOR", **extra):
        if not email:
            raise ValueError("Admin users must have an email address")
        user = self.model(email=self.normalize_email(email), name=name, role=role, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra):
        extra.setdefault("role", "SUPER_ADMIN")
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra)


class AdminUser(AbstractBaseUser, PermissionsMixin):
    """
    Spec section 30 roles. Backend is the source of truth for permissions —
    the React admin's sidebar filtering is UX only, this is what's actually
    enforced (see accounts/permissions.py).
    """
    ROLE_CHOICES = [
        ("SUPER_ADMIN", "Super Admin"),
        ("ADMIN", "Admin"),
        ("EDITOR", "Editor"),
        ("EVENT_MANAGER", "Event Manager"),
        ("BOOKING_MANAGER", "Booking Manager"),
        ("CONTENT_MANAGER", "Content Manager"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="EDITOR")
    avatar_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AdminUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_active(self):
        return self.active
