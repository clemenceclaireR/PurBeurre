#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories
from purbeurre.models.favorites import Favorites


class SubstituteProductTest(TestCase):
    """
    Views tests for substitute products view
    """
    def setUp(self):
        self.user = User.objects.create_user(id=1, username="test", password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product1 = Products.objects.create(id=1, name='nutella',
                                                nutriscore='d',
                                                link="http://test.test.fr",
                                                image="path/to/image",
                                                category=Categories.objects.get(name=self.category))
        self.product2 = Products.objects.create(id=2, name='nocciolata',
                                                nutriscore='c',
                                                link="http://test.test.fr",
                                                image="path/to/image",
                                                category=Categories.objects.get
                                                (name=self.category))
        self.product3 = Products.objects.create(id=3, name='nutella bio',
                                                nutriscore='c',
                                                link="http://test.test.fr",
                                                image="path/to/image",
                                                category=Categories.objects.get
                                                (name=self.category))

        self.favorite = Favorites.objects.create(user=User.objects.get(id=1),
                                                 substitute=Products.objects.get
                                                 (name="nocciolata"))

    def test_post_search_form_is_valid(self):
        """
        Search form works from substitutes page
        """
        response = self.client.post('/substitutes/product/', {
            'research': 'nutella'
        })
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        """
        Results page is accessible with url name
        """
        response = self.client.get('/substitutes/nutella/')
        self.assertEqual(response.status_code, 200)

    def test_view_returns_last_page_if_id_page_out_of_range(self):
        """
        View return last page if page number given is out o range
        """
        response = self.client.get('/substitutes/nutella/',
                                   {'query': '', 'page': 5})
        self.assertEquals(response.context['products'].number, 1)

    def test_view_url_propose_product_already_in_favorites(self):
        """
        One of the products displayed is in user's favorites
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/substitutes/nutella/')
        self.assertEqual(response.status_code, 200)
