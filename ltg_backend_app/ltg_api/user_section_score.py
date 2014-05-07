'''
will be used to create a user section score 
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
from ltg_backend_app.models import UserConceptScore, UserSectionScore
from ltg_backend_app.ltg_api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.ltg_api.user_profile import UserProfileResource
from ltg_backend_app.ltg_api.section import SectionResource
from ltg_backend_app.ltg_api.user_score import UserScoreResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user section score resource
#===============================================================================

class UserSectionScoreResource(UserScoreResource):
    '''
    resource for our user section score model
    '''
    user_profile = fields.ToOneField(UserProfileResource,attribute='user_profile')
    section = fields.ToOneField(SectionResource,attribute='section')
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post']
        include_resource_uri = True
        always_return_data = True
#         validation = FormValidation(form_class=UserProfileForm)
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        queryset = UserSectionScore.objects.all()
    
#===============================================================================
# end user section score resource
#===============================================================================