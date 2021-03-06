# Generated by Django 3.0.7 on 2020-08-06 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purbeurre', '0004_remove_products_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='substitute',
            field=models.ForeignKey(help_text='Foreign key to the Product table', on_delete=django.db.models.deletion.CASCADE, related_name='saved_substitute', to='purbeurre.Products', verbose_name='Substitute'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(help_text='Website user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
