'''
will hold our question statistics resource
Created on May 13, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import QuestionStatistics, WrongAnswersPercentage
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from ltg_backend_app.api.question import QuestionResource
from ltg_backend_app.api.wrong_answers_percentage import WrongAnswersPercentageResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question statistics resource
#===============================================================================

class QuestionStatisticsResource(LtgResource):
    '''
    resource for the question statistics model
    '''
    question = fields.ToOneField(QuestionResource,attribute='question', full=True)
    
    class Meta(LtgResource.Meta):
        queryset = QuestionStatistics.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'question' : ALL_WITH_RELATIONS,
               'attempt' : ALL,
               'mean_time' : ALL,
               'std_time' : ALL,
               'percentage' : ALL,
               'score' : ALL,
           }
        ordering = ['question','attempt',]
        
    def dehydrate(self, bundle):
        # init percentage wrong list
        percentage_wrong_list = []
        # get all percenatage wrong objects which relate to this question statistics object
        wrong_answer_percentage_set = WrongAnswersPercentage.objects.filter(question_statistics_id = bundle.data['id'])
        # populate the percentage wrong list
        for wrong_answer_percentage in wrong_answer_percentage_set:
            # init percentage wrong dict
            percentage_wrong_dict = {}
            percentage_wrong_dict[wrong_answer_percentage.get_answer_display()] = wrong_answer_percentage.percentage_wrong
            percentage_wrong_list.append(percentage_wrong_dict)
        bundle.data['percentage_wrong'] = percentage_wrong_list
        
        return bundle
    
#===============================================================================
# end question statistics resource
#===============================================================================