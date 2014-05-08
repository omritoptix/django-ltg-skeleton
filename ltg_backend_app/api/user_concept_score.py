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
from tastypie.authorization import Authorization
from ltg_backend_app.models import UserConceptScore
from ltg_backend_app.api.concept import ConceptResource
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from ltg_backend_app.api.user_profile import UserProfileResource
from ltg_backend_app.api.user_score import UserScoreResource
from ltg_backend_app.third_party_subclasses.tastypie_subclasses import ModelFormValidation
from ltg_backend_app.forms import UserConceptScoreForm

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
        allowed_methods = ['post']
        include_resource_uri = True
        always_return_data = True
#         validation = FormValidation(form_class=UserProfileForm)
        validation = ModelFormValidation(form_class=UserConceptScoreForm)
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        queryset = UserConceptScore.objects.all()
    
#===============================================================================
# end user concept score resource
#===============================================================================