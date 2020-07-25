from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from user.forms import UserRegistrationForm
from django import forms


class LoginTest(TestCase):

    def setUp(self):
         User.objects.create_user(username="test", password="test", email="test@test.fr")

    def test_login(self):
        self.client.login(email="test@test.fr", password="test")
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_return_expected_html(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_valid_credentials(self) :
        response = self.client.post(reverse("login"), {
            'username': "test", 'password': "test"
        })
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/')

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("login"), {
            'username': "false", 'password': 'wrong_password'
        })
        self.assertTrue(response.status_code, 200)


class UserRegistrationTest(TestCase):

    def setUp(self) :
        self.new_user = User.objects.create_user(id=1 ,username="user1", password="test", email="user1@test.fr")
        self.data ={
            'username': 'test',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'test'
        }

    def test_page_return_expected_html(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')


    def test_register(self):
        response = self.client.post(reverse("register"), data=self.data, follow=True,
                                    HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertEqual(User.objects.all().count(), 2)
        self.assertTrue(response.status_code, 200)

    def test_register_psw_dont_match(self):
        response = self.client.post(reverse("register"), data={
            'username': 'test',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'wrong',
            'first_name': 'test',
            'last_name': 'test'
        }, follow=True, HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertTrue(response.status_code, 200)

    def test_register_email_alrd_registered(self):
        response = self.client.post(reverse("register"), data={
            'username': 'test',
            'email': 'user1@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'test'
        }, follow=True, HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertTrue(response.status_code, 200)


