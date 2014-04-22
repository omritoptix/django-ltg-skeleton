'''
will hold our user profile resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.base import LtgResource
from tastypie import fields
from ltg_backend_app.ltg_api.user import UserResource
from tastypie.validation import FormValidation
from ltg_backend_app.forms import UserProfileForm
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from ltg_backend_app.models import UserProfile

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user profile resource
#===============================================================================

class UserProfileResource(LtgResource):
    '''
    resource for our user profile model
    '''
    user = fields.ToOneField(UserResource,'user')
    class Meta:
        allowed_methods = ['post']
        include_resource_uri = True
        always_return_data = True
        validation = FormValidation(form_class=UserProfileForm)
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        
#===============================================================================
# end user profile resource
#===============================================================================