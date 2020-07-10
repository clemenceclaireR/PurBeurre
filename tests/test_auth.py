from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginTest(TestCase):

    def setUp(self):
        self.new_user = User.objects.create(username="test", password="test")

    def test_login(self):
        self.login = authenticate(username="test", password="test")
        if self.login:
            response = self.client.get(self.login)
            self.assertEqual(response['username'], "test")


class UserRegistrationTest(TestCase):

    def test_register(self):
        data = {"username": "test", "mail": "test@test.fr", "password": "test",
                "first_name": "test", "last_name": "test"
                }

        response = self.client.post(reverse("register"), data=data, follow=True,
                                    HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertTrue(response.status_code, 200)
        fake_user = User.objects.create_user(username="test", email="test@test.test", password="test")

        self.assertTrue(fake_user.username, "test")
