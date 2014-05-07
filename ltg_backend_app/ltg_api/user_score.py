'''
will be used to create a user total score for a specified date 
Created on May 7th, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.base import LtgResource
from tastypie import fields
from tastypie.validation import FormValidation
from tastypie.authorization import Authorization
from ltg_backend_app.models import UserConceptScore, UserScore
from ltg_backend_app.ltg_api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.ltg_api.user_profile import UserProfileResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user score resource
#===============================================================================

class UserScoreResource(LtgResource):
    '''
    resource for our user concept score model
    '''
    user_profile = fields.ToOneField(UserProfileResource,attribute='user_profile')
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post']
        include_resource_uri = True
        always_return_data = True
#         validation = FormValidation(form_class=UserProfileForm)
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        queryset = UserScore.objects.all()
        
    def hydrate_user_profile(self, bundle):
        # set the user profile to the requesting user profile
        user_profile_uri = UserProfileResource().get_resource_uri(bundle.request.user.profile)
        bundle.data['user_profile'] = user_profile_uri
        
        return bundle
    
#===============================================================================
# end user score resource
#===============================================================================