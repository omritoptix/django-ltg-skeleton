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
from ltg_backend_app.models import Question, Attempt
from django.contrib.auth.models import User
from tastypie.models import ApiKey
from django.contrib.auth import get_user_model
 
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
        4. test bulk create of attempts
        '''
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email='yariv@nerdeez.com')
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
         
        # get question uri for the attempt 
        question = Question.objects.first()
        question_index = question.index
        question_uri = '/api/v1/question/%d/' % question_index
        # post a new attempt
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':question_uri,'answer':2,'duration':'1min,10sec'},authentication = authentication_header)
        self.assertHttpCreated(resp)
        # check new attempt was created with correct values
        attempt = Attempt.objects.latest('creation_date')
        self.assertEqual(attempt.question_id,question.id)
        self.assertEqual(attempt.user_id,user.id)
        self.assertEqual(attempt.answer, 2)
         
        # post without credentials failes
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':question_uri,'answer':2,'duration':'1min,10sec'})
        self.assertHttpUnauthorized(resp)
         
        # post with invalid question index fails
        resp = self.api_client.post(uri='/api/v1/attempt/', format='json', data={'question':'/api/v1/question/99999999/','answer':2,'duration':'1min,10sec'},authentication = authentication_header)
        self.assertHttpNotFound(resp)
         
        # test bulk create of attempts
        num_attempts =  Attempt.objects.all().count()
        resp = self.api_client.patch(uri='/api/v1/attempt/', format='json', data={'objects':[{'question':question_uri,'answer':2,'duration':'1min,10sec'},{'question':question_uri,'answer':4,'duration':'1min,10sec'}]},authentication = authentication_header)
        self.assertHttpAccepted(resp)
        # make sure the objects were really created since patch return accepted (not created) on bulk operations
        self.assertEqual(num_attempts + 2, Attempt.objects.all().count())
 
         
#===============================================================================
# end attempt test
#===============================================================================