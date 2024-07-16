from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="manager@sky.pro",
            is_active=True,
            is_staff=True,
        )
        user.set_password("admin")
        user.save()
        print("Менеджер успешно создан")
