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
#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','uuid','full_name','get_email')
    search_fields=['user__email','user__first_name','user__last_name']
    
    def full_name(self,user_profile):
        return ("%s %s" % (user_profile.user.last_name, user_profile.user.first_name))
    full_name.short_description = "Full Name"
    
    def get_email(self, user_profile):
        return user_profile.user.email
    get_email.short_description = "Email"    


#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(UserProfile, UserProfileAdmin)

#===============================================================================
# end admin site registration
#===============================================================================