#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from purbeurre.models.categories import Categories
from purbeurre.models.products import Products


class LoginTest(TestCase):
    """
    Login function test
    """

    def setUp(self):
        User.objects.create_user(username="test",
                                 first_name="test",
                                 password="test",
                                 email="test@test.fr")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella',
                                               nutriscore='d',
                                               link="http://test.test.fr",
                                               image="path/to/image",
                                               category=Categories.objects.get
                                               (name=self.category))

    def test_login_return_expected_html(self):
        """
        Login page is accessible with 'login'
        """
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_valid_credentials(self):
        """
        Login page redirects when right credentials is posted
        """
        response = self.client.post(reverse("login"), {
            'email': "test@test.fr", 'password': "test"
        })
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/')

    def test_login_invalid_credentials(self):
        """
        Login page does not redirects when right credentials is posted
        """
        response = self.client.post(reverse("login"), {
            'email': "false@test.fr", 'password': 'wrong_password'
        })
        self.assertTrue(response.status_code, 200)


class UserRegistrationTest(TestCase):
    """
    Registration function test
    """

    def setUp(self):
        self.new_user = User.objects.create_user(id=1,
                                                 first_name="user1",
                                                 username="user1",
                                                 password="test",
                                                 email="user1@test.fr")
        self.data = {
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
        }

    def test_page_return_expected_html(self):
        """
        Register view uses register.html file
        """
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register(self):
        """
        Add user when posted data is correct
        """
        response = self.client.post(reverse("register"), data=self.data, follow=True,
                                    HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertEqual(User.objects.all().count(), 2)


    def test_register_psw_dont_match(self):
        """
        Doesn't add user when password don't match in posted data
        """
        response = self.client.post(reverse("register"), data={
            'username': 'test',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'wrong',
            'first_name': 'test'
        }, follow=True, HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertEqual(User.objects.all().count(), 1)


    def test_register_email_alrd_registered(self):
        """
        Doesn't add user when entered email in posted data
        is already registered
        """
        response = self.client.post(reverse("register"), data={
            'username': 'test',
            'email': 'user1@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test'
        }, follow=True, HTTP_X_REQUESTED='XMLHttpRequest')
        self.assertEqual(User.objects.all().count(), 1)

