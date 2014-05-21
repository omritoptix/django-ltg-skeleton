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
from ltg_backend_app.models import UserScore
from ltg_backend_app.third_party_extensions.tastypie_extensions import ModelFormValidation
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication
from ltg_backend_app.api.user import UserResource

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
    user = fields.ToOneField(UserResource,attribute='user')
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post','get']
        include_resource_uri = True
        always_return_data = True
        validation = ModelFormValidation(form_class=UserScoreForm)
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        queryset = UserScore.objects.all()      
        filtering = {
               'user' : ALL_WITH_RELATIONS,
               'date' : ALL,
           }
        ordering = ['date',]
#===============================================================================
# end user score resource
#===============================================================================