from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = User.objects.create(
            email="test1@sky.pro",
            is_active=True,
        )
        user1.set_password("12345678")
        user1.save()
        print("Пользователь_1 успешно создан")

        user2 = User.objects.create(
            email="test2@sky.pro",
            is_active=True,
        )
        user2.set_password("12345678")
        user2.save()
        print("Пользователь_2 успешно создан")

        user3 = User.objects.create(
            email="test3@sky.pro",
            is_active=True,
        )
        user3.set_password("12345678")
        user3.save()
        print("Пользователь_3 успешно создан")
