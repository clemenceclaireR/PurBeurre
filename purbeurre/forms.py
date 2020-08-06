#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django import forms


class SearchForm(forms.Form):
    """
    Product search form
    """
    research = forms.CharField(
        label="Recherche",
        widget=forms.TextInput(attrs={'placeholder': 'Trouvez un aliment',
                                      'class': 'form-control ',
                                      'autocomplete': 'off'})
    )
