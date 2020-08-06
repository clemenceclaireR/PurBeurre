#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.db import models
from .categories import Categories


class Products(models.Model):
    """
    This class represents the table Products and its columns
    """

    class Meta:
        db_table = 'products'
        ordering = ['-id']

    name = models.CharField(max_length=75,
                            unique=True,
                            verbose_name='Name',
                            help_text='Product name')

    category = models.ForeignKey(Categories,
                                 on_delete=models.CASCADE,
                                verbose_name = 'Category',
                                help_text = 'Foreign key to the category of the product')
    nutriscore = models.CharField(max_length=1,
                                  null=True,
                                  verbose_name='Nutriscore',
                                  help_text='Nutritional score of the product')
    link = models.URLField(verbose_name='Link',
                                  help_text='Hyperlink to Openfoodfacts product page')
    image = models.URLField(verbose_name='Image',
                                  help_text='Hyperlink to Openfoodfacts product image')
    nutrition_image = models.URLField(verbose_name='Nutrition image',
                                  help_text='Hyperlink to Openfoodfacts ranking nutriscore image')

    def __str__(self):
        return str(self.name)
