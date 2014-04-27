'''
will hold our attempt resource
Created on April 27, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import Attempt
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from ltg_backend_app.ltg_api.question import QuestionResource
from ltg_backend_app.ltg_api.user_profile import UserProfileResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin attempt resource
#===============================================================================

class AttemptResource(LtgResource):
    '''
    resource for the question model
    '''
    question = fields.ToOneField(QuestionResource,attribute='question')
    user_profile = fields.ToOneField(UserProfileResource,attribute='user_profile')
    
    class Meta(LtgResource.Meta):
        queryset = Attempt.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ['post']
    
#===============================================================================
# end attempt resource
#===============================================================================