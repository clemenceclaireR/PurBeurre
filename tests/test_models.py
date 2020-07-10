from django.test import TestCase
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories
from purbeurre.models.favorites import Favorites
from django.contrib.auth.models import User



class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Categories.objects.create(id=1, name="pâte à tariner")

    def test_category_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        categories = Categories.objects.create(id=1, name="pâte à tariner")
        Products.objects.create(name='nutella', nutriscore='d', link="http://test.test.fr",
                               image="path/to/image", category=Categories.objects.get(name=categories))

    def test_product_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')



class FavoriteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(password="test", is_superuser=False, username="test", first_name="test",
                                   last_name="test", email="test")
        categories = Categories.objects.create(id=1, name="pâte à tariner")
        products = Products.objects.create(name='nutella', nutriscore='d', link="http://test.test.fr",
                               image="path/to/image", category=Categories.objects.get(name=categories))
        Favorites.objects.create(substitute=Products.objects.get(name=products), user=User.objects.get(username=user))
"""
    def test_favorite_fk(self):
        favorites = Favorites.objects.get(id=1)
        field_fk = favorites._meta.get_field('substitute').verbose_name
        self.assertEquals(field_fk, 'substitute')
"""

