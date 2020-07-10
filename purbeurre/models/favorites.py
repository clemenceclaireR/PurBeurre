from django.db import models
from django.conf import settings
from .products import Products


class Favorites(models.Model):
    """
    This class represents the table Favorites and its columns
    """

    class Meta:
        db_table = 'favorites'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    substitute = models.ForeignKey(Products,
                                   on_delete=models.CASCADE,
                                   related_name='saved_substitute')



