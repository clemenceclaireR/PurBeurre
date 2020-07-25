from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class LoginForm(forms.Form):
    """
    Login form
    """
    username = UsernameField(label="", widget=forms.TextInput(attrs={'autofocus': True,
                                                           'class': "form-control form-control-user",
                                                           'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(label="", strip=False,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                                                 'class': "form-control form-control-user",
                                                                 'placeholder': "Mot de passe"}), )


class UserRegistrationForm(forms.ModelForm):
    """
    Subscription form
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    username = UsernameField(label="", widget=forms.TextInput(attrs={'autofocus': True,
                                                                     'placeholder': "Nom d'utilisateur",
                                                                     'class': "form-control form-control-user",
                                                                     'id': "exampleInputEmail"
                                                                     }))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={
                                                                     'placeholder': "Prénom",
                                                                     'class': "form-control form-control-user",
                                                                     'id': "exampleInputEmail"
                                                                     }))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={
                                                                     'placeholder': "Nom",
                                                                     'class': "form-control form-control-user",
                                                                     'id': "exampleInputEmail"
                                                                     }))

    password = forms.CharField(label='',
                               strip=False,
                               widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe",
                                                                 'class': "form-control form-control-user",
                                                                 'id':"exampleInputEmail"}),)
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': "Répétez votre mot de passe",
                                                                  'class': "form-control form-control-user",
                                                                  'id': "exampleInputEmail"}), )
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={
                                                                     'placeholder': "Adresse e-mail",
                                                                     'class': "form-control form-control-user",
                                                                     'id': "exampleInputEmail"
                                                                     }),)

    def clean_email(self):
        """
        Check if e-mail is already used
        """
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email address is already registered")
        return self.cleaned_data['email']

    def clean_password2(self):
        """
        check if password are identical ; if its not, clean
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']