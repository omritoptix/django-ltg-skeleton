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
from ticketz_backend_app.models import *

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================

class FlatPageAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

class RegionAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    pass

class UserPrefrenceAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('title', 'business_id', 'get_email', 'phone', 'send_activation')
    def get_email(self, business):
        return business.user_profile.user.email
    def send_activation(self, business):
        pass

#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(UserPrefrence, UserPrefrenceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Business, BusinessAdmin)

#===============================================================================
# end admin site registration
#===============================================================================