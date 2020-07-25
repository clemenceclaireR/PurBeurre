from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from purbeurre.forms import SearchForm
from purbeurre.models.products import Products
from purbeurre.models.favorites import Favorites
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View


def register(request):
    """
    Register a user account
    """
    form = SearchForm(request.POST)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        form = SearchForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          locals())

        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')

    else:
        user_form = UserRegistrationForm()
        form = SearchForm()
    return render(request, 'registration/register.html', locals())


def user_login(request):
    """
    User login management
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        form = SearchForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('../')
            else:
                return HttpResponse('Invalid login')
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')
    else:
        login_form = LoginForm()
        form = SearchForm(request.POST)
    return render(request, 'registration/login.html', locals())