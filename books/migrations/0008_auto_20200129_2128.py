# Generated by Django 2.2 on 2020-01-29 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_remove_book_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]