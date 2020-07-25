from django.db import models
from django.conf import settings
from .categories import Categories


class Products(models.Model):
    """
    This class represents the table Products and its columns
    """

    class Meta:
        db_table = 'products'
    name = models.CharField(max_length=75, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    nutriscore = models.CharField(max_length=1, null=True)
    link = models.URLField()
    image = models.URLField()
    nutrition_image = models.URLField()


    def __str__(self):
        return str(self.name)