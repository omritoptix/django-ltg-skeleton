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

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import UserSectionScore
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.api.user_profile import UserProfileResource
from ltg_backend_app.api.section import SectionResource
from ltg_backend_app.api.user_score import UserScoreResource
from ltg_backend_app.third_party_extensions.tastypie_extensions import ModelFormValidation
from ltg_backend_app.forms import UserSectionScoreForm
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL

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
        allowed_methods = ['post','get','patch']
        detail_allowed_methods = ['put','patch']
        include_resource_uri = True
        always_return_data = True
        validation = ModelFormValidation(form_class=UserSectionScoreForm)
        authentication = LtgApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        queryset = UserSectionScore.objects.all()
        filtering = {
               'user_profile' : ALL_WITH_RELATIONS,
               'section' : ALL_WITH_RELATIONS,
               'date' : ALL,
           }
    
#===============================================================================
# end user section score resource
#===============================================================================