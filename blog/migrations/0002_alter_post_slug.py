# Generated by Django 4.1 on 2022-08-05 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_AddBlogModel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(editable=False, max_length=150),
        ),
    ]