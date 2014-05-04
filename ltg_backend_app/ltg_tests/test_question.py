'''
will hold our question tests
Created on April 22, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Question , ScoreTable

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question
#===============================================================================

class QuestionTest(ResourceTestCase):

    fixtures=['initial_data','questions']
    
    def test_get_questions(self):
        '''
        will test the question api resource.
        1. get a single question
        2. get a list of questions 
        '''
        question_uri = '/api/v1/question/%d/' % (Question.objects.first().id)
        resp = self.api_client.get(uri=question_uri, format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)) > 0)
        
        #get questions
        resp = self.api_client.get(uri='/api/v1/question/', format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)['objects']) > 0)
        
#===============================================================================
# end question
#===============================================================================