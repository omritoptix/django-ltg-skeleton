'''
will hold our question statistics tests
Created on May 12, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.models import Question , QuestionStatistics,\
    WrongAnswersPercentage
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.contrib.auth import get_user_model

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question statistics test
#===============================================================================

class QuestionStatisticsTest(ResourceTestCase):

    fixtures=['initial_data','users_auth','questions']
    
    def setUp(self):
        ''' 
        - create question statistics data
        - create WrongAnswersPercentage object to relate the question statistics
        '''
        # create question statistics for the objects
        question = Question.objects.first()
        qs1 = QuestionStatistics.objects.create(question_id=question.id, attempt=1,mean_time=30, std_time=12, percentage_right=50.0, score=650)
        WrongAnswersPercentage.objects.create(question_statistics_id = qs1.id, answer=2,percentage_wrong=20.0)
        return super(QuestionStatisticsTest,self).setUp()
    
    def test_get_question_statistics(self):
        '''
        will test the question statistics api resource.
        1. get a single question statistics
        2. get a list of questions statistics
        '''
        # init authentication header
        User = get_user_model()
        user = User.objects.first()
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        # get a single question 
        qs_uri = '/api/v1/questionstatistics/%d/' % (QuestionStatistics.objects.first().id)
        resp = self.api_client.get(uri=qs_uri, format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['mean_time'], "0:00:30")
        self.assertEqual(self.deserialize(resp)['percentage_wrong'][0]['C'], "20.00")
        
        #get questions statistics
        resp = self.api_client.get(uri='/api/v1/questionstatistics/', format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'][0]['mean_time'], "0:00:30")
        
    def test_post_question_statistics(self):
        '''
        test that a POST request to a question statistics is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/questionstatistics/')
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end question statistics test
#===============================================================================