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
    list_display = ('id', 'phone', 'uuid')

class RegionAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    pass

class UserPrefrenceAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'title', 'description', 'valid_from', 'valid_to', 'num_total_places', 'original_price', 'discounted_price', 'status', 'category')

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('title', 'business_number', 'get_email', 'phone', 'send_activation')
    search_fields = ['user_profile__user__email','title', 'business_id']
    list_filter = ('modified_data','creation_date')
    def get_email(self, business):
        return business.user_profile.user.email
    def send_activation(self, business):
        '''
        will redirect to a business approval page
        @param business: the business model
        '''
        return "<a href='/confirm-business/%s'>Activate</a>" % (business.id)
    send_activation.allow_tags = True
    
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('path', 'post', 'get', 'content')
    search_fields = ['path', 'post', 'get', 'content']
    
class TransactionAdmin(admin.ModelAdmin):
    pass

class UnpaidTransactionAdmin(admin.ModelAdmin):
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
admin.site.register(Deal, DealAdmin)
admin.site.register(Logger, LoggerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UnpaidTransaction, UnpaidTransactionAdmin)

#===============================================================================
# end admin site registration
#===============================================================================