from django.shortcuts import render, redirect
from .forms import SearchForm

def handle_search_form(request):
    """
    Display search forms
    """
    form = SearchForm(request.POST)
    if form.is_valid():
        prod = form.cleaned_data['research']
        return redirect('search_results/' + prod + '/')
    else:
        form = SearchForm()