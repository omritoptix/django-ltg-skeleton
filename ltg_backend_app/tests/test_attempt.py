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
from django.contrib.auth.models import User
from tastypie.models import ApiKey

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin attempt test
#===============================================================================

class AttemptTest(ResourceTestCase):
    
    fixtures = ['users_auth','initial_data','questions']
    
    def test_post_attempt(self):
        '''
        will test that an attempt is created upon POST request
        1. create a new attempt and make sure it was created
        2. post without credentails failes
        3. post with invalid question id fails  
        '''
        # get question uri for the attempt 
        question_id = Question.objects.first().id
        question_uri = '/api/v1/question/%d/' % question_id
        # get the user credentials for the attempt
        user = User.objects.get(username='yariv')
        api_key = ApiKey.objects.get(user = user.id)
        # post a new attempt
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':question_uri,'username':user.username,'api_key':api_key.key,'answer':2,'duration':'1min,10sec'})
        self.assertHttpCreated(resp)
        # check new attempt was created with correct values
        attempt = Attempt.objects.latest('creation_date')
        self.assertEqual(attempt.question_id,question_id)
        self.assertEqual(attempt.user_profile_id,user.profile.id)
        self.assertEqual(attempt.answer, 2)
        
        # post without credentials failes
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':question_uri,'answer':2,'duration':'1min,10sec'})
        self.assertHttpUnauthorized(resp)
        
        # post with invalid question id fails
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':'/api/v1/question/99999999/','answer':2,'duration':'1min,10sec','username':user.username,'api_key':api_key.key})
        self.assertHttpNotFound(resp)

        
#===============================================================================
# end attempt test
#===============================================================================