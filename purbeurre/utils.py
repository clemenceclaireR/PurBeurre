#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.shortcuts import render, redirect
from .forms import SearchForm


def handle_search_form(search_request):
    """
    Display search forms
    """
    form = SearchForm(search_request)
    if form.is_valid():
        product = form.cleaned_data['research']
        return redirect('search_results/' + product + '/')
    else:
        form = SearchForm()


