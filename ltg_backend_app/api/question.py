'''
will hold our question resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import Question
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.authorization import Authorization

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question resource
#===============================================================================

class QuestionResource(LtgResource):
    '''
    resource for the question model
    '''
    percentage_score_statistics = fields.ListField(attribute='percentage_score_statistics')
    time_statistics = fields.ListField(attribute='time_statistics')
    
    class Meta(LtgResource.Meta):
        queryset = Question.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        
    def dehydrate_answer(self, bundle):
        return bundle.obj.get_answer_display()
    
#===============================================================================
# end question resource
#===============================================================================