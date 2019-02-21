"""Admin Panel for Common Module's Models"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User

"""Since we have removed Username field from User Model and added email
field, we need to make changes to UserAdmin to be able to use it in
admin panel.
Refer: https://www.fomfus.com/articles/how-to-use-email-as-username (cont)
-for-django-authentication-removing-the-username"""

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'user_type')
    search_fields = ('email', 'first_name', 'last_name', 'user_type')
    ordering = ('email',)
