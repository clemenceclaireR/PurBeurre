# Generated by Django 3.0.7 on 2020-07-18 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0003_products_is_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='is_favorite',
        ),
    ]