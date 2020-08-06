#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from purbeurre.forms import SearchForm
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories


class IndexPageTestCase(TestCase):
    """
    Views test for the index page
    """

    def test_view_url_exists_at_desired_location(self):
        """
        Index page is accessible at base location
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        Index page is accessible with 'index'
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Index view uses index.html file
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_post_search_form_is_valid(self):
        """
        Search form works from index page
        """
        response = self.client.post(reverse('index'), {
            'research': 'product'
        })
        self.assertRedirects(response, '/search_results/product/')


class LegalInformationTestCase(TestCase):
    """
    Views test for the legal mentions page
    """

    def test_view_url_accessible_by_name(self):
        """
        Legal information page is accessible with 'legal_information'
        """
        response = self.client.get(reverse('legal_information'))
        self.assertEqual(response.status_code, 200)


class AccountTest(TestCase):
    """
    Views test for the account page
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella',
                                               nutriscore='d',
                                               link="http://test.test.fr",
                                               image="path/to/image",
                                               category=Categories.objects.get
                                               (name=self.category))

    def test_redirect_if_not_logged_in(self):
        """
        If not authenticated user wants to access account page,
        redirected to login page
        """
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/login/?next=/account/')

    def test_access_if_logged_in(self):
        """
        Authenticated user can access account page
        """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_post_form_from_account_page(self):
        """
        Search form works from account page
        """
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('account'), {
            'research': 'product'
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/search_results/product/')
