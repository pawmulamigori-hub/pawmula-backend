import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawmula_backend.settings')
django.setup()

from accounts.models import AdminUser

email = "pawmula@gmail.com"
password = "Pawmula@2026"

if not AdminUser.objects.filter(email=email).exists():
    AdminUser.objects.create_superuser(email=email, password=password)
    print(f"Superuser {email} created successfully!")
else:
    print(f"Superuser {email} already exists.")
