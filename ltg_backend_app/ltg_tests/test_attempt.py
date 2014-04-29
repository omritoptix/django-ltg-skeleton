'''
will hold our attempt tests
Created on April 28, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from ltg_backend_app.models import UserProfile, Question, Attempt
from ltg_backend_app.ltg_api.user_profile import UserProfileResource
from ltg_backend_app.ltg_api.question import QuestionResource
import pdb
from ltg_backend_app.ltg_api.anonymous_user_profile import AnonymousUserProfileResource
from django.contrib.auth.models import User
from tastypie.models import ApiKey

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin attempt test
#===============================================================================

class AttemptTest(ResourceTestCase):
    
    fixtures = ['ltg_backend_app']
    
    def test_post_attempt(self):
        '''
        will test that an attempt is created upon POST request
        1. create a new attempt and make sure it was created
        2. post without credentails failes
        3. post with invalid question id fails  
        '''
        # get question uri for the attempt (for some reason 'question_uri' returns empty, so had to hardcode the question uri)
        question = Question.objects.first()
        question_uri = QuestionResource().get_resource_uri(question)
        # get the user credentials for the attempt
        user = User.objects.first()
        api_key = ApiKey.objects.get(user = user.id)
        # post a new attempt
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':'/api/v1/question/1/','username':user.username,'api_key':api_key.key,'answer':2,'duration':'1min,10sec'})
        self.assertHttpCreated(resp)
        # check new attempt was created with correct values
        attempt = Attempt.objects.latest('creation_date')
        self.assertEqual(attempt.question_id,question.id)
        self.assertEqual(attempt.user_profile_id,user.profile.id)
        self.assertEqual(attempt.answer, 2)
        
        # post without credentails failes
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':'/api/v1/question/1/','answer':2,'duration':'1min,10sec'})
        self.assertHttpUnauthorized(resp)
        
        # post with invalid question id fails
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':'/api/v1/question/99999999/','answer':2,'duration':'1min,10sec','username':user.username,'api_key':api_key.key})
        self.assertHttpNotFound(resp)

        
#===============================================================================
# end attempt test
#===============================================================================