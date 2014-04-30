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

from ltg_backend_app.ltg_api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import Question
from tastypie.authentication import Authentication

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
        authentication = Authentication()
        allowed_methods = ['get']
    
#===============================================================================
# end question resource
#===============================================================================