#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from purbeurre.forms import SearchForm
from user.forms import UserRegistrationForm


class SearchFormTest(TestCase):
    """
    Form tests for search form
    """

    def test_field_label_name(self):
        """
        Checks field label name
        """
        form = SearchForm()
        self.assertTrue(form.fields['research'].label == 'Recherche')

    def test_search_form(self):
        """
        Checks if search form is valid
        """
        form_data = {'research': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class RegisterFormTest(TestCase):
    """
    Form tests for register form
    """
    def setUp(self):
        self.new_user = User()
        self.data = {
            'username': 'test2',
            'email': 'test@test.fr',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'test'
        }

    def test_register_form(self):
        """
        Check if register form is valid
        """
        form = UserRegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())
