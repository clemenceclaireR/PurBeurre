from django.test import TestCase
from purbeurre.forms import SearchForm
from user.forms import UserRegistrationForm
from django.contrib.auth.models import User



class SearchFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = SearchForm()
        self.assertTrue(form.fields['research'].label == 'Recherche')


class RegisterFormTest(TestCase):
    def setUp(self) :
        self.new_user = User()
        self.data ={
            'username': 'test2',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'test'
        }

    def test_register_form(self):
        form = UserRegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())