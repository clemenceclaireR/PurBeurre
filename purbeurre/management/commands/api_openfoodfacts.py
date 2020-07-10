#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories
from purbeurre.models.favorites import Favorites
import requests
import json
from django.db.utils import IntegrityError



class APIInformation:
    """
    Constants necessary in order to use the OpenFoodFacts's API
    """
    PRODUCTS_LINK = "https://fr.openfoodfacts.org/cgi/search.pl?"
    PARAMETERS = {
        "search_simple": '1',
        "action": 'process',
        "tagtype_0": 'categories',
        "tagtype_1": "nutrition_grades",
        "tag_contains_0": 'contains',
        "page": 1,
        "page_size": 100,
        "json": '1',
    }
    PAGE_MIN = 1
    PAGE_MAX = 20
    NUTRISCORE = ['A', 'B', 'C', 'D', 'E']
    CATEGORIES = [
        "Snacks salés",
        "Plats préparés",
        "Produits à tartiner salés",
        "Produits à tartiner sucrés",
        "Biscuits et Gâteaux",
        "Fromages",
        "Confitures",
        "Petit-déjeuner",
        "Chocolats",
        "Viennoiserie",
        "Dessert glacés",
        "Sirop",
        "Jus de fruits",
        "Sodas"
    ]


class Command(BaseCommand):

    def get_categories(self, categories):
        category, created = Categories.objects.get_or_create(name=categories)
        category.save()

    def get_products(self, data, category):
        for product_information in data['products']:
            name = product_information.get('product_name', None)
            category = Categories.objects.get(name=category)
            nutriscore = product_information.get('nutrition_grades', None)
            link = product_information.get('url', None)
            image = product_information.get('image_url', None)
            if category is None \
                    or name is None \
                    or len(name) > 75 \
                    or nutriscore is None \
                    or link is None \
                    or image is None:
                continue
            else:
                try:
                    product, created = Products.objects.get_or_create(
                        name=name,
                        category=category,
                        nutriscore=nutriscore,
                        link=link,
                        image=image,
                    )
                    if created:
                        product.save()
                        print(product.name)
                except Products.DoesNotExist:
                    raise CommandError("Products %s could not been reached" % name)
                except IntegrityError:
                    continue

    def handle(self, *args, **options):
        for category in APIInformation.CATEGORIES:
            self.get_categories(category)
            APIInformation.PARAMETERS['tag_0'] = category
            for tag in APIInformation.NUTRISCORE:
                APIInformation.PARAMETERS['tag_1'] = tag
                response = requests.get(APIInformation.PRODUCTS_LINK, params=APIInformation.PARAMETERS)
                products = response.json()

                self.get_products(products, category)
