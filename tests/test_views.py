from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#from purbeurre.authentication import EmailAuthBackend
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from purbeurre.forms import SearchForm
from purbeurre.models import Favorites, Products, Categories


class IndexPageTestCase(TestCase):
    """
    Views test for the index page
    """

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

    def test_search_form(self):
        form_data = {'research': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_search_form_is_valid(self) :
        response = self.client.post(reverse('index'), {
            'research': 'product'
        })
        self.assertRedirects(response, '/search_results/product/')

    def test_post_search_form_empty(self) :
        response = self.client.post(reverse('index'), {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)


class LegalInformationTestCase(TestCase):
    """
    Views test for the legal mentions page
    """
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


class AccountTest(TestCase):
    """
    Views test for the account page
    """

    def setUp(self):
         User.objects.create_user(username="test", password="test")

         self.category = Categories.objects.create(id=1, name="pâte à tariner")
         self.product = Products.objects.create(id=1, name='nutella', nutriscore='d', link="http://test.test.fr",
                                           image="path/to/image", category=Categories.objects.get(name=self.category))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/login/?next=/account/')

    def test_access_if_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_post_form_from_account_page(self):
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('account'), {
                'research': 'product'
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/search_results/product/')

    def test_post_form_empty_from_account_page(self):
        response = self.client.post(reverse('account'), {
            'research': ''
        })
        self.assertEqual(response.status_code, 302)



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

