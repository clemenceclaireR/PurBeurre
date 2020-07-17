from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from purbeurre.forms import SearchForm
from purbeurre.models import Favorites, Products, Categories


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

    def test_search_form(self):
        form_data = {'research': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_search_form_is_valid(self) :
        response = self.client.post(reverse('index'), {
            'research': 'product'
        })
        self.assertRedirects(response, '/searching/product/')

    def test_post_search_form_empty(self) :
        response = self.client.post(reverse('index'), {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)



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

class AccountTest(TestCase):
    # def setUp(self) :
    #     User.objects.create(password="test", is_superuser=False, username="test", first_name="test",
    #                                last_name="test", email="test")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, '/login/?next=/account/')

    def test_redirect_if_logged_in(self):
        pass



class ProductViewTest(TestCase):


    def test_search_form(self):
        form_data = {'research': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_post_search_form_is_valid(self) :
        response = self.client.post('/searching/product/', {
            'research': 'test'
        })
        # 302 found, searching/produit
        self.assertEqual(response.status_code, 302)
        #self.assertRedirects(response, '/searching/test', target_status_code=301, status_code=302)

    def test_post_search_form_empty(self) :
        response = self.client.post('/searching/product/', {
            'research': ''
        })
        self.assertEqual(response.status_code, 200)




class SubstituteProductTest(TestCase):

    def test_post_search_form_is_valid(self) :
        response = self.client.post('/substitutes/product/', {
            'research': 'nutella'
        })
        # 302 found, searching/produit
        self.assertEqual(response.status_code, 302)
        #self.assertRedirects(response, '/searching/test', target_status_code=301, status_code=302)

    # def test_post_search_form_empty(self) :
    #     response = self.client.post('/substitutes/product/', {
    #         'research': ''
    #     })
    #     self.assertEqual(response.status_code, 200)



class FavoriteProductTest(TestCase):
    # def setUp(self):
    #     self.user = User.objects.create_user(id=1, username='test', password='test')
    #     self.category = Categories.objects.create(id=1, name="pâte à tariner")
    #     self.product = Products.objects.create(id=1, name='nutella', nutriscore='d', link="http://test.test.fr",
    #                                    image="path/to/image", category=Categories.objects.get(name=self.category))


    def test_insert_new_favorite(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/searching/nutella', {
            'substitute': 1, 'user':1
        })
        #self.assertEqual(Favorites.objects.filter(user=1).count(), 1)
        self.assertEqual(response.status_code, 301)

    # def test_save_product(self):
    #     validated_product = Favorites.objects.create(substitute=Products.objects.get(name='nutella'),
    #                                                                                  user=User.objects.get
    #                                                                                  (username='test'))
    #     validated_product.save()
    #     self.assertTrue(validated_product.substitute, 'nutella')