'''
will hold our question resource tests
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
# begin question resource
#===============================================================================

class Question(ResourceTestCase):
    
    fixtures = ['ltg_backend_app']
    
    def test_get_questions(self):
        '''
        will test the question api resource.
        1. get a single question
        2. get a list of questions 
        '''
        resp = self.api_client.get(uri='/api/v1/question/1/', format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)) > 0)
        
        #get questions
        resp = self.api_client.get(uri='/api/v1/question/', format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)['objects']) > 0)
        
#===============================================================================
# end question resource
#===============================================================================