from django.shortcuts import render, redirect
from .forms import SearchForm

def handle_search_form():
    """
    Display search forms
    """
    if form.is_valid():
        prod = form.cleaned_data['research']
        return redirect('search_results/' + prod + '/')
