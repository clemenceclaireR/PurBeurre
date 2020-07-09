from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.user_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('user_food_items/', views.user_food_items, name='user_food_items'),
    path('search_result/', views.search_result, name='search_result'),
    path('searching/<str:product>/', views.product_view, name='searching'),
    path('search_result/<str:product>/', views.search_result, name='search_result'),
    path('food_item_description/', views.food_item_description, name='food_item_description'),
    path('', views.index, name='index')
]