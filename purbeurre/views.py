from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SearchForm
from .utils import handle_search_form
from user.forms import UserRegistrationForm, LoginForm
from .models.products import Products
from .models.favorites import Favorites
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View


def index(request):
    """
    Display homepage with search forms
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data['research']
            return redirect('search_results/' + prod + '/')
        else:
            form = SearchForm()
    else:
        form = SearchForm()
    return render(request, 'index.html', locals())


@login_required
def account(request):
    """
    Display user account page
    """
    form = SearchForm(request.POST)
    if form.is_valid():
        prod = form.cleaned_data['research']
        return redirect('search_results/' + prod + '/')
    else:
        form = SearchForm()
    return render(request, 'registration/account.html', locals())


def legal_information(request):
    """
    Display legal information about the website
    """
    form = SearchForm(request.POST)
    return render(request, 'legal_information.html', locals())


def search_results(request, product):
    """
    Search for a product written in the search form by a user
    """
    form = SearchForm(request.POST)
    current_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            product= form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            SearchForm()
    else:
        SearchForm()
    product_list = Products.objects.filter\
        (nutriscore__range=('d', 'e'), name__icontains=product)

    try:
        for item in product_list:
            favorites = Favorites.objects.filter(user=User.objects.get(id=current_user.id), substitute=item.id)
            if favorites :
                item.is_favorite = True
            else:
                item.is_favorite = False
    except User.DoesNotExist:
        pass

    return render(request, 'purbeurre/search_results.html',locals())


@login_required
def save_product(request, product):
    """
    Get user's product to register and check if
    it's not already in his favorites
    """
    product_to_save = Products.objects.get(name=product)
    current_user = request.user

    if request.method == 'POST':

    # verify if this product is already saved by the user and tag it as favorite in Products table
        product = Favorites.objects.filter(substitute=product_to_save, user=User.objects.get(id=current_user.id))
        if not product:
            validated_product = Favorites(substitute=product_to_save, user=User.objects.get(id=current_user.id))
            validated_product.save()
            message = messages.add_message(request, messages.SUCCESS, 'Produit sauvegardé', fail_silently=True)
    return redirect(request.META['HTTP_REFERER'], locals())


@login_required
def saved_products(request):
    """
    Display user's saved products
    """
    form = SearchForm(request.POST)
    current_user = request.user
    favorites = Favorites.objects.filter(user=current_user.id)
    list_favorites = []
    for i in favorites:
        favorite = Products.objects.get(name=i.substitute)
        list_favorites.append(favorite)

    return render(request, 'purbeurre/saved_products.html', locals())

@login_required
def delete_saved_product(request):
    """
    Remove a given product from favorites
    """
    if request.method == 'POST':
        prod_name = request.POST.get('delete_product')
        prod_to_delete = Products.objects.get(name=prod_name)
        current_user = request.user
        Favorites.objects.get(substitute=prod_to_delete, user=current_user.id).delete()
        message = messages.add_message(request, messages.SUCCESS, 'Produit supprimé', fail_silently=True)
        return redirect('/saved_products', locals())
    return render(request, 'purbeurre/saved_products.html', locals())


def search_substitutes(request, product):
    """
    Search substitutes for a given product
    """
    form = SearchForm(request.POST)
    current_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            SearchForm()
    else:
        SearchForm()
    research = Products.objects.get(name=product)
    product_list = Products.objects.filter(nutriscore__range=('a', 'c'), category=research.category)

    try:
        for item in product_list:
            favorites = Favorites.objects.filter(user=User.objects.get(id=current_user.id), substitute=item.id)
            if favorites :
                item.is_favorite = True
            else:
                item.is_favorite = False
    except User.DoesNotExist:
        pass

    return render(request, 'purbeurre/substitutes.html', locals())


def product_description(request, product):
    """
    Display nutritional information for a
    given product
    """
    form = SearchForm(request.POST)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            SearchForm()
    else:
        SearchForm()
    product_description = Products.objects.get(name=product)
    return render(request, 'purbeurre/product_page.html', locals())

