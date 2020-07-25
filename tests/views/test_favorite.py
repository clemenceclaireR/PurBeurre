from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from purbeurre.forms import SearchForm
from purbeurre.models import Favorites, Products, Categories



class FavoriteProductTest(TestCase):
    """
    Views tests for saving/deleting and consulting saved products
    """
    def setUp(self):
        self.new_user = User.objects.create_user(id=1 ,username="test", password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella', nutriscore='d', link="http://test.test.fr",
                                       image="path/to/image", category=Categories.objects.get(name=self.category))


    def test_insert_new_favorite(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/save_done/nutella/', {
            'product': self.product.name
        }, HTTP_REFERER='/substitutes/nutella')
        self.assertEqual(Favorites.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_delete_favorite(self):
        prod = Products.objects.create(id=2, name='nocciolata', nutriscore='d', link="http://test.test.fr",
                                image="path/to/image", category=Categories.objects.get(name=self.category))
        Favorites.objects.create(user=User.objects.get(id=1),
                                            substitute=Products.objects.get(name="nocciolata"))
        self.client.login(username='test', password='test')
        response = self.client.post('/deleted_saved_product/', {
            'delete_product': prod
        }, )
        self.assertEqual(Favorites.objects.all().count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_view_delete_favorite_page(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('delete_saved_product'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('saved_products'))
        self.assertRedirects(response, '/login/?next=/saved_products/')

    def test_view_if_logged_in(self):
        self.client.login(username='test', password='test')
        product = Products.objects.create(id=2, name='tuc', nutriscore='d', link="http://test.test.fr",
                                               image="path/to/image",
                                               category=Categories.objects.get(name=self.category))
        Favorites.objects.create(substitute=product, user=self.new_user)
        response = self.client.get(reverse('saved_products'))
        self.assertEqual(response.status_code, 200)
