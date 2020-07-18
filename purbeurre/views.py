from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, SearchForm
from .models.products import Products
from .models.favorites import Favorites
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import View


def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data['research']
            return redirect('search_results/' + prod + '/')
        else:
            form = SearchForm()
    else:
        form = SearchForm()
    return render(request, 'index.html', {'form': form,
                                          })


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
    return render(request, 'registration/register.html', {'user_form': user_form })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('../')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form })


@login_required
def account(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        prod = form.cleaned_data['research']
        return redirect('search_results/' + prod + '/')
    else:
        form = SearchForm()
    return render(request, 'registration/account.html', {'form': form })


def legal_information(request):
    form = SearchForm(request.POST)
    return render(request, 'legal_information.html', {'form': form })





def search_results(request, product):
    form = SearchForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            product= form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            SearchForm()
    else:
        SearchForm()
    product_list = Products.objects.filter(
        nutriscore__range=('d', 'e'), name__icontains=product)
    return render(request, 'purbeurre/search_results.html', {'product_list':product_list,
                                                             'form': form })


@login_required
def save_product(request, product):
    product_to_save = Products.objects.get(name=product)
    current_user = request.user

    if request.method == 'POST':

    # verify if this product is already saved by the user and tag it as favorite in Products table
        product = Favorites.objects.filter(substitute=product_to_save, user=User.objects.get(id=current_user.id))
        product_to_save.is_favorite = True
        product_to_save.save()
        if not product:
            validated_product = Favorites(substitute=product_to_save, user=User.objects.get(id=current_user.id))
            validated_product.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def saved_products(request):
    form = SearchForm(request.POST)
    current_user = request.user
    favorites = Favorites.objects.filter(user=current_user.id)
    list_favorites = []
    for i in favorites:
        favorite = Products.objects.get(name=i.substitute)
        list_favorites.append(favorite)

    return render(request, 'purbeurre/saved_products.html', {'list_favorites':list_favorites,
                                                             'form': form
                                                             })



def search_substitutes(request, product):
    form = SearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('/' + product + '/')
        else:
            SearchForm()
    else:
        SearchForm()
    research = Products.objects.get(name=product)
    # ICI
    product_list = Products.objects.filter(nutriscore__range=('a', 'c'), category=research.category)

    return render(request, 'purbeurre/substitutes.html', {'product_list': product_list,
                                                          'research':research,
                                                          'form': form}
                                                          )



def product_description(request, product):
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

