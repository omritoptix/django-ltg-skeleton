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
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question
#===============================================================================

class QuestionTest(ResourceTestCase):

    fixtures=['initial_data','users_auth','questions']
    
    def test_get_questions(self):
        '''
        will test the question api resource.
        1. get a single question
        2. get a list of questions 
        '''
        User = get_user_model()
        user = User.objects.first()
        auth_data = {'username':user.email,'api_key':user.api_key.key}
        question_uri = '/api/v1/question/%d/' % (Question.objects.first().index)
        resp = self.api_client.get(uri=question_uri, format='json', data = auth_data)
        self.assertHttpOK(resp)
        
        #get questions
        resp = self.api_client.get(uri='/api/v1/question/', format='json', data = auth_data)
        self.assertHttpOK(resp)
        
    def test_post_question(self):
        '''
        test that a POST request to a question is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/question/',data={'index':9999})
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end question
#===============================================================================