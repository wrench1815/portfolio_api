# Generated by Django 4.1 on 2022-08-05 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_AddCategoryModel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(editable=False, max_length=100),
        ),
    ]