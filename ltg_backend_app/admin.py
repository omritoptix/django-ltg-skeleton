'''
will hold the admin interface models
Created on November 7, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================
from django.contrib import admin
from ltg_backend_app.models import *
from django.contrib.auth.admin import UserAdmin
from ltg_backend_app.forms import UserChangeForm, UserCreationForm

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================
    
class LtgUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','username','first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email','username','password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()


#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(LtgUser, LtgUserAdmin)

#===============================================================================
# end admin site registration
#===============================================================================