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

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.forms import UserScoreForm
from tastypie.authorization import Authorization
from ltg_backend_app.models import UserScore
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.api.user_profile import UserProfileResource
from ltg_backend_app.third_party_subclasses.tastypie_subclasses import ModelFormValidation


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
        validation = ModelFormValidation(form_class=UserScoreForm)
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