#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.db import models


class Categories(models.Model):
    """
    This class represents the table Categories and its columns
    """

    class Meta:
        db_table = 'categories'
        ordering = ['-id']

    name = models.CharField(max_length=75,
                            unique=True,
                            verbose_name='Name',
                            help_text='Name of the category')

    def __str__(self):
        return str(self.name)
