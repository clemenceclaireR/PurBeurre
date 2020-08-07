#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories
from purbeurre.models.favorites import Favorites


class ModelsTest(TestCase):
    """
    Models tests
    """
    def setUp(self):
        user = User.objects.create_user(password="test", is_superuser=False,
                                   username="test", first_name="test",
                                   last_name="test", email="test")
        categories = Categories.objects.create(id=1, name="pâte à tariner")
        products = Products.objects.create(id=1, name='nutella', nutriscore='d',
                                           link="http://test.test.fr",
                                           image="path/to/image",
                                           category=Categories.objects.get
                                           (name=categories))
        Favorites.objects.create(id=1, substitute=Products.objects.get(name=products),
                                 user=User.objects.get(username=user))

    def test_category_label(self):
        """
        Checks field label name in Categories table
        """
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_product_label(self):
        """
        Checks field label name in Products table
        """
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_favorite_fk(self):
        """
        Checks field label name in Favorites table
        """
        favorites = Favorites.objects.get(id=1)
        field_fk = favorites._meta.get_field('substitute').verbose_name
        self.assertEqual(field_fk, 'Substitute')
