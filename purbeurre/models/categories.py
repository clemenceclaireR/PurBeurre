from django.db import models



class Categories(models.Model):
    """
    This class represents the table Categories and its columns
    """

    class Meta:
        db_table = 'categories'
    name = models.CharField(max_length=75, unique= True)

    def __str__(self):
        return str(self.name)
