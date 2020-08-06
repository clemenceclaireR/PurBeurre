#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.db import models
from django.conf import settings
from .products import Products


class Favorites(models.Model):
    """
    This class represents the table Favorites and its columns
    """

    class Meta:
        db_table = 'favorites'
        ordering = ['-id']

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             db_index=True,
                             verbose_name='User',
                             help_text='Website user')
    substitute = models.ForeignKey(Products,
                                   on_delete=models.CASCADE,
                                   related_name='saved_substitute',
                                   db_index=True,
                                   verbose_name='Substitute',
                                   help_text='Foreign key to the Product table')
