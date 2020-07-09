from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, SearchForm, HomeSearchForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        form_body = HomeSearchForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data['research']
            return redirect('searching/' + prod + '/')
        else:
            form = SearchForm()
            form_body = HomeSearchForm()
        if form_body.is_valid():
            prod = form.cleaned_data['research']
            return redirect('searching/' + prod + '/')
    else:
        form = SearchForm()
        form_body = HomeSearchForm()
    return render(request, 'index.html', {'form': form, 'form_body': form_body})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def account(request):
    return render(request, 'registration/account.html')


def user_food_items(request):
    return render(request, 'purbeurre/user_food_items.html')


def product_view(request, product):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data['research']
            return redirect('/' + prod + '/')
        else:
            form = SearchForm()
    else:
        form = SearchForm()
    # rajouter query bdd pour le produit et le nutriscore
    return render(request, 'purbeurre/searching.html')


def search_result(request, product):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            form = SearchForm()
    else:
        form = SearchForm()
        # rajouter query bdd pour le produit et le nutriscore
    return render(request, 'product/search_result.html')



def food_item_description(request):
    return render(request, 'purbeurre/food_item_description.html')