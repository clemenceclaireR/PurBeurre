from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from purbeurre.views import user_login
from purbeurre.forms import UserRegistrationForm

class LoginTest(TestCase):

    def setUp(self):
         self.new_user = User.objects.create(username="test", password="test")

    def test_login(self):
        self.login = authenticate(username="test", password="test")
        if self.login:
            response = self.client.get(self.login)
            self.assertEqual(response['username'], "test")

    def test_login_return_expected_html(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_valid_credentials(self) :
        response = self.client.post(reverse("login"), {
            'username': self.new_user.username, 'password': self.new_user.password
        })
        self.assertTrue(response.status_code, 200)

    # def test_login_invalid_credentials(self):
    #     response = self.client.post(reverse("login"), {
    #         'username': self.new_user.username, 'password': 'wrong_password'
    #     })
    #     self.assertRedirects(response, 'registration/login.html')
    #


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

    def test_page_return_expected_html(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')



    def test_register(self):
        response = self.client.post(reverse("register"), data=self.data, follow=True,
                                    HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertTrue(response.status_code, 200)
        fake_user = User.objects.create_user(username="test", email="test@test.test", password="test")

        self.assertTrue(fake_user.username, "test")

