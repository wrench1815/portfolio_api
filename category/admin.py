from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name', 'slug')
