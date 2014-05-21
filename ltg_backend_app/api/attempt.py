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

from ltg_backend_app.api.base import LtgResource
from tastypie import fields, http
from ltg_backend_app.models import Attempt, Question
from ltg_backend_app.api.question import QuestionResource
from tastypie.exceptions import ImmediateHttpResponse
from django.db.models.aggregates import Max
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from ltg_backend_app.forms import AttemptForm
from ltg_backend_app.third_party_extensions.tastypie_extensions import ModelFormValidation
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication
from ltg_backend_app.api.user import UserResource

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
    user = fields.ToOneField(UserResource,attribute='user')
    
    class Meta(LtgResource.Meta):
        queryset = Attempt.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        allowed_methods = ['post','get','patch']
        detail_allowed_methods = ['put','patch']
        validation = ModelFormValidation(form_class=AttemptForm)
        filtering = {
            'user_profile' : ALL_WITH_RELATIONS,
            'question' : ALL_WITH_RELATIONS,
            'attempt' : ALL,
        }
        ordering = ['question','attempt',]
        
    def hydrate_attempt(self, bundle):
        # get the attempt's user
        user = bundle.request.user
        # get the attempt's question
        try:
            question = QuestionResource().get_via_uri(bundle.data['question'])
        except Question.DoesNotExist:
            raise ImmediateHttpResponse(response=http.HttpNotFound("question does not exist"))
        
        # find the max attempt made for this question by this user
        max_attempt = Attempt.objects.filter(question_id = question.id,user_id = user.id).aggregate(Max('attempt'))
        if (max_attempt['attempt__max'] is None):
            bundle.data['attempt'] = 1
        else:
            bundle.data['attempt'] = max_attempt['attempt__max'] + 1
            
        return bundle
    
    
    def dehydrate(self,bundle):
        # add the question index
        question_id = AttemptResource().get_pk_from_uri(bundle.data['question'])
        bundle.data['question_index'] = Question.objects.get(id=question_id).index
        
        return bundle
        
        
    
#===============================================================================
# end attempt resource
#===============================================================================