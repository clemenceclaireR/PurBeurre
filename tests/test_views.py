from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPageTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LegalInformationTestCase(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/legal_information/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('legal_information'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('legal_information'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal_information.html')



class UserHasToBeLoggedTest(TestCase, LoginRequiredMixin):

    def test_access_page_if_logged_in(self):
        pass

class AccountTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/login/?next=/account/')



