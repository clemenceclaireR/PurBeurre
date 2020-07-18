from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from purbeurre.forms import UserRegistrationForm
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
        self.new_user = User()
        self.data ={
            'username': 'test2',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'test'
        }

    def test_register_form(self):
        form = UserRegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())


    def test_register_form_empty(self) :
        response = self.client.post(reverse('register'), data= {
            'username': '',
            'email': '',
            'password': '',
            'password2': '',
            'first_name': '',
            'last_name': ''
        })
        self.assertEqual(response.status_code, 200)

    def test_register_password_dont_match(self) :
        response = self.client.post(reverse('register'), data= {
            'username': 'test3',
            'email': 'test3@test.fr',
            'password': 'test',
            'password2': 'wrong',
            'first_name': 'test',
            'last_name': 'test'
        })
        self.assertEqual(response.status_code, 200)

    def test_page_return_expected_html(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')



    def test_register(self):
        response = self.client.post(reverse("register"), data=self.data, follow=True,
                                    HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertTrue(response.status_code, 200)
        fake_user = User.objects.create_user(username="test", email="test@test.test", password="test")

        self.assertTrue(fake_user.username, "test")

