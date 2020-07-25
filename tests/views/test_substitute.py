from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from purbeurre.forms import SearchForm
from purbeurre.models import Favorites, Products, Categories




class SubstituteProductTest(TestCase):
    """
    Views tests for substitute products view
    """
    def setUp(self):
        # init user
        self.new_user = User.objects.create_user(id=1, username="test", password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product1 = Products.objects.create(id=1, name='nutella', nutriscore='d', link="http://test.test.fr",
                                                image="path/to/image",
                                                category=Categories.objects.get(name=self.category))


    def test_post_search_form_is_valid(self) :
        response = self.client.post('/substitutes/product/', {
            'research': 'nutella'
        })
        self.assertEqual(response.status_code, 302)


    def test_post_search_form_empty(self) :
        self.client.login(username='test', password='test')
        response = self.client.post('/substitutes/nutella/', {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/substitutes/nutella/')
        self.assertEqual(response.status_code, 200)