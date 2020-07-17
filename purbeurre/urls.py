from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext as _

urlpatterns = [
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.user_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('saved_products/', views.saved_products, name='saved_products'),
    url('searching/(?P<product>.*)/$', views.product_view, name='searching'),
    url('substitutes/(?P<product>.*)/$', views.search_result, name='substitutes'),
    url('save_done/(?P<product>.*)/$', views.save_product, name='save_product'),
    url('product_description/(?P<product>.*)/$', views.product_description, name='product_description'),
    path('legal_information/', views.legal_information, name='legal_information'),
    path('', views.index, name='index'),
    path(_('ajax'), views.AjaxView.as_view(), name=_('ajax')),
]

