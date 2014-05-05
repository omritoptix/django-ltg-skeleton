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
from tastypie import fields, http
from ltg_backend_app.models import Attempt, Question
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from ltg_backend_app.ltg_api.question import QuestionResource
from ltg_backend_app.ltg_api.user_profile import UserProfileResource
from tastypie.exceptions import ImmediateHttpResponse
from django.db.models.aggregates import Max
from ltg_backend_app.ltg_api.authentication import LtgApiKeyAuthentication
from tastypie.constants import ALL_WITH_RELATIONS, ALL

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin attempt resource
#===============================================================================

class AttemptResource(LtgResource):
    '''
    resource for the attempt model
    '''
    question = fields.ToOneField(QuestionResource,attribute='question')
    user_profile = fields.ToOneField(UserProfileResource,attribute='user_profile')
    
    class Meta(LtgResource.Meta):
        queryset = Attempt.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['post','get']
        filtering = {
            'user_profile' : ALL_WITH_RELATIONS,
            'question' : ALL_WITH_RELATIONS,
            'attempt' : ALL,
        }
        ordering = ['question','attempt',]
        
    def hydrate_attempt(self, bundle):
        # get the attempt's user profile
        user_profile = bundle.request.user.profile
        # get the attempt's question
        try:
            question = QuestionResource().get_via_uri(bundle.data['question'])
        except Question.DoesNotExist:
            raise ImmediateHttpResponse(response=http.HttpNotFound("question does not exist"))
        
        # find the max attempt made for this question by this user
        max_attempt = Attempt.objects.filter(question_id = question.id,user_profile_id = user_profile.id).aggregate(Max('attempt'))
        if (max_attempt['attempt__max'] is None):
            bundle.data['attempt'] = 1
        else:
            bundle.data['attempt'] = max_attempt['attempt__max'] + 1
            
        return bundle
    
    def hydrate_user_profile(self, bundle):
        # set the user profile to the requesting user profile
        user_profile_uri = UserProfileResource().get_resource_uri(bundle.request.user.profile)
        bundle.data['user_profile'] = user_profile_uri
        
        return bundle
    
#===============================================================================
# end attempt resource
#===============================================================================