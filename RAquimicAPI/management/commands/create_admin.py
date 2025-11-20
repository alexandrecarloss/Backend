from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="admincarlos").exists():
            User.objects.create_superuser(
                username="admincarlos",
                password="admin123",
                email="admin@example.com"
            )
            print("Superuser criado!")
        else:
            print("Superuser já existe.")
