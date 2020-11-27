# Generated by Django 2.2.5 on 2020-01-27 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_category_product'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='product',
            index_together=None,
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
