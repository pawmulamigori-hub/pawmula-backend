from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ["email", "name", "role", "active", "is_staff"]
    list_filter = ["role", "active"]
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("name", "role", "avatar_url", "active")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "name", "role", "password1", "password2")}),
    )
    search_fields = ["email", "name"]
