from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


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



