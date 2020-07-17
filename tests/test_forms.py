from django.test import TestCase
from purbeurre.forms import SearchForm




class SearchFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = SearchForm()
        self.assertTrue(form.fields['research'].label == 'Recherche')

