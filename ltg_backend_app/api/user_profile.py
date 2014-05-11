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

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.api.user import UserResource
from tastypie.validation import FormValidation
from ltg_backend_app.forms import UserProfileForm
from ltg_backend_app.models import UserProfile
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.authorization import Authorization

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
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['get']
        include_resource_uri = True
        always_return_data = True
        validation = FormValidation(form_class=UserProfileForm)
        authentication = LtgApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        

#===============================================================================
# end user profile resource
#===============================================================================