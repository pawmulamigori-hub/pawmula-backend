from rest_framework import serializers
from accounts.models import AdminUser


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "name", "email", "role", "active"]


class InviteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "name", "email", "role"]

    def create(self, validated_data):
        import secrets
        temp_password = secrets.token_urlsafe(12)
        user = AdminUser.objects.create_user(password=temp_password, **validated_data)
        # In production: send an email with a password-set link instead of
        # returning the temp password. Left as a clearly isolated TODO —
        # no email/SMTP provider has been configured yet.
        return user
