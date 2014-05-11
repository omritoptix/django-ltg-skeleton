'''
will be used to create a user concept score 
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
from ltg_backend_app.models import UserConceptScore
from ltg_backend_app.api.concept import ConceptResource
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.api.user_profile import UserProfileResource
from ltg_backend_app.api.user_score import UserScoreResource
from ltg_backend_app.third_party_extensions.tastypie_extensions import ModelFormValidation
from ltg_backend_app.forms import UserConceptScoreForm
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user concept score resource
#===============================================================================

class UserConceptScoreResource(UserScoreResource):
    '''
    resource for our user concept score model
    '''
    user_profile = fields.ToOneField(UserProfileResource,attribute='user_profile')
    concept = fields.ToOneField(ConceptResource,attribute='concept')
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post','get','patch']
        detail_allowed_methods = ['put','patch']
        include_resource_uri = True
        always_return_data = True
        validation = ModelFormValidation(form_class=UserConceptScoreForm)
        authentication = LtgApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        queryset = UserConceptScore.objects.all()
        filtering = {
               'user_profile' : ALL_WITH_RELATIONS,
               'concept' : ALL_WITH_RELATIONS,
               'date' : ALL,
           }
    
#===============================================================================
# end user concept score resource
#===============================================================================