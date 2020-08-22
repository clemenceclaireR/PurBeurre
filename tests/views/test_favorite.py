#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from purbeurre.models.favorites import Favorites
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories


class FavoriteProductTest(TestCase):
    """
    Views tests for saving/deleting and consulting saved products
    """
    def setUp(self):
        self.user = User.objects.create_user(id=1, username="test",
                                             password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella',
                                               nutriscore='d',
                                               link="http://test.test.fr",
                                               image="path/to/image",
                                               category=Categories.objects.get
                                               (name=self.category))

        self.product2 = Products.objects.create(id=2, name='nocciolata',
                                       nutriscore='d',
                                       link="http://test.test.fr",
                                       image="path/to/image",
                                       category=Categories.objects.get
                                       (name=self.category))
        self.product3 = Products.objects.create(id=3, name='tuc',
                                          nutriscore='d',
                                          link="http://test.test.fr",
                                          image="path/to/image",
                                          category=Categories.objects.get
                                          (name=self.category))
        self.favorite = Favorites.objects.create(user=User.objects.get(id=1),
                                 substitute=Products.objects.get
                                 (name="nocciolata"))

    def test_insert_new_favorite(self):
        """
        User add a substitute product to his favorites
        """
        self.client.login(username='test', password='test')
        response = self.client.post('/save_done/nutella/', {
            'product': self.product.name
        }, HTTP_REFERER='/substitutes/nutella')
        self.assertEqual(Favorites.objects.all().count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_delete_favorite(self):
        """
        User delete a product from his favorites
        """
        self.client.login(username='test', password='test')
        response = self.client.post('/deleted_saved_product/', {
            'delete_product': self.product2
        }, )
        self.assertEqual(Favorites.objects.all().count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_view_delete_favorite_page(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('delete_saved_product'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        """
        Not authenticated user is redirect when he wants saved products page
        """
        response = self.client.get(reverse('saved_products'))
        self.assertRedirects(response, '/login/?next=/saved_products/')

    def test_view_if_logged_in(self):
        """
        User wants to access his saved products page
        """
        self.client.login(username='test', password='test')
        Favorites.objects.create(substitute=self.product3, user=self.user)
        response = self.client.get(reverse('saved_products'))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_last_page_if_id_page_out_of_range(self):
        """
        View return last page if page number given is out o range
        """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('saved_products'),
                                   {'query': '', 'page': 5})
        self.assertEquals(response.context['products'].number, 1)
