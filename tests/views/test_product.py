from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from purbeurre.forms import SearchForm
from purbeurre.models import Favorites, Products, Categories

class ProductViewTest(TestCase):
    """
    Views test for the search results page and the product description page
    """
    def setUp(self):
        # init user for login
        self.new_user = User.objects.create_user(id=1, username="test", password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella', nutriscore='d', link="http://test.test.fr",
                                            image="path/to/image", category=Categories.objects.get(name=self.category))


    def test_search_form(self):
        form_data = {'research': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_post_search_form_is_valid(self) :
        response = self.client.post('/search_results/product/', {
            'research': 'nutella'
        })
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/search_results/nutella/')
        self.assertEqual(response.status_code, 200)


    def test_post_search_form_empty(self) :
        response = self.client.post('/search_results/product/', {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)

    def test_post_form_from_product_details_page(self):
        response = self.client.post('/product_description/product/', {
            'research': 'product'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_form_empty_from_product_details_page(self):
        response = self.client.post('/product_description/nutella/', {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)

    def test_view_product_description_page(self):
        response = self.client.get('/product_description/nutella/')
        self.assertEqual(response.status_code, 200)