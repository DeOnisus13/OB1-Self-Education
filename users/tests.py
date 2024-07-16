from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тест для модели пользователя"""

    def setUp(self):
        pass

    def test_user_create_login(self):
        """Тест создания и регистрации пользователя"""

        url = reverse("users:register")
        data = {
            "email": "test@test.ru",
            "password": "12345678",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(response.json().get("email"), "test@test.ru")


class CreateSuperuserCommandTest(TestCase):
    """Тест команды для создания суперпользователя"""

    def test_create_superuser(self):
        self.assertFalse(User.objects.filter(email="admin@sky.pro").exists())

        call_command('csu')

        user = User.objects.get(email="admin@sky.pro")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("admin"))

        self.assertEqual(User.objects.filter(email="admin@sky.pro").count(), 1)


class CreateManagerCommandTest(TestCase):
    """Тест команды для создания менеджера"""

    def test_create_manager(self):
        self.assertFalse(User.objects.filter(email="manager@sky.pro").exists())

        call_command('manager')

        user = User.objects.get(email="manager@sky.pro")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("admin"))

        self.assertEqual(User.objects.filter(email="manager@sky.pro").count(), 1)


class CreateUserCommandTest(TestCase):
    """Тест команды для создания пользователя"""

    def test_create_user(self):
        self.assertFalse(User.objects.filter(email="test1@sky.pro").exists())

        call_command('test_users')

        user = User.objects.get(email="test1@sky.pro")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("12345678"))

        self.assertEqual(User.objects.filter(email="test1@sky.pro").count(), 1)
