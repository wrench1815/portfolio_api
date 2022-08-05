from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import UserForm

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    '''Admin View for User'''

    add_form = UserForm

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    ordering = ['username']
    list_filter = [
        'is_active',
        'is_superuser',
    ]
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]

    #? fieldsets for viewing
    fieldsets = [
        [
            'Basic Info', {
                'fields': [
                    'avatar',
                    'username',
                    'first_name',
                    'last_name',
                    'gender',
                    'email',
                    'password',
                ],
            }
        ],
        ['Dates', {
            'fields': [
                'date_created',
                'last_login',
            ]
        }],
        [
            'Permissions', {
                'fields': [
                    'is_staff',
                    'is_superuser',
                    'is_active',
                ]
            }
        ],
        ['Groups', {
            'fields': [
                'groups',
            ]
        }],
    ]

    #? fieldsets for Creation
    add_fieldsets = [
        [
            'Basic Info', {
                'fields': [
                    'avatar',
                    'username',
                    'first_name',
                    'last_name',
                    'gender',
                    'email',
                    'password',
                ]
            }
        ],
        ['Dates', {
            'fields': [
                'date_created',
                'last_login',
            ]
        }],
        [
            'Permissions', {
                'fields': [
                    'is_staff',
                    'is_superuser',
                    'is_active',
                ]
            }
        ],
        ['Groups', {
            'fields': [
                'groups',
            ]
        }],
    ]
