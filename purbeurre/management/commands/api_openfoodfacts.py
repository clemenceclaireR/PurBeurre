#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
import requests
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories


class APIInformation:
    """
    Parameters needed in order to use the OpenFoodFacts's API
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
    NUTRISCORE = ['A', 'B', 'C', 'D', 'E']
    CATEGORIES = [
        "Snacks salés",
        "Produits à tartiner salés",
        "Pâtes à tartiner aux noisettes",
        "Biscuits au chocolat",
        "Biscuits apéritifs",
        "Biscuits sablés",
        "Biscuits fourrés",
        "Biscuits secs",
        "Biscuits au chocolat au lait",
        "Fromages",
        "Confitures",
        "Chocolats",
        "Viennoiserie",
        "Dessert glacés",
        "Sirop",
        "Jus de fruits",
        "Sodas"
    ]


class Command(BaseCommand):
    """
    Get Openfoodfacts products in project database
    """

    def get_categories(self, categories):
        """
        Get categories by name inserted in parameter
        """
        category, created = Categories.objects.get_or_create(name=categories)
        category.save()

    def get_products(self, data, category):
        """
        Get products filtering needed product information and
        tie it to a category
        """
        for product_information in data['products']:
            name = product_information.get('product_name', None)
            # in order to remove linebreak from product name
            # print("WITH LINEBREAK : ", repr(name))
            if name:
                name = name.replace('\n', '')
                # print("WITHOUT LINEBREAK : ", repr(name))
            category = Categories.objects.get(name=category)
            nutriscore = product_information.get('nutrition_grades', None)
            link = product_information.get('url', None)
            image = product_information.get('image_url', None)
            nutrition_image = product_information.get\
                ('image_nutrition_url', None)
            if category is None \
                    or name is None \
                    or len(name) > 75 \
                    or nutriscore is None \
                    or link is None \
                    or image is None \
                    or nutrition_image is None:
                continue
            else:
                try:
                    product, created = Products.objects.get_or_create(
                        name=str(name),
                        category=category,
                        nutriscore=nutriscore,
                        link=link,
                        image=image,
                        nutrition_image=nutrition_image,
                    )
                    if created:
                        product.save()
                        print(product.name)

                except Products.DoesNotExist:
                    raise CommandError("Products %s could not been reached"
                                       % name)
                except IntegrityError:
                    continue

    def handle(self, *args, **options):
        """
        Loop open list of categories and create it,
        then get products through request and return json response
        which will be parsed
        """
        for category in APIInformation.CATEGORIES:
            self.get_categories(category)
            APIInformation.PARAMETERS['tag_0'] = category
            for tag in APIInformation.NUTRISCORE:
                APIInformation.PARAMETERS['tag_1'] = tag
                response = requests.get(APIInformation.PRODUCTS_LINK,
                                        params=APIInformation.PARAMETERS)
                products = response.json()

                self.get_products(products, category)
