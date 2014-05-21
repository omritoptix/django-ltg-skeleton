'''
will hold our score tests 
Created on April 28, 2014
 
@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''
 
#===============================================================================
# begin imports
#===============================================================================
 
from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Section, UserSectionScore, UserScore
from django.contrib.auth.models import User
from tastypie.models import ApiKey
from django.contrib.auth import get_user_model
 
#===============================================================================
# end imports
#===============================================================================
 
#===============================================================================
# begin score test
#===============================================================================
 
class ScoreTest(ResourceTestCase):
     
    fixtures = ['users_auth']
     
    def test_post_score(self):
        '''
        will test the score api resource.
        1. create a score for a user for a specific date 
        '''
        # create a score for a user for a specific date
        User = get_user_model()
        user = User.objects.first()
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        resp = self.api_client.post(uri='/api/v1/userscore/', format='json', data = {'score':546,'date':'2014-11-12T15:02:10'},authentication=authentication_header)
        self.assertHttpCreated(resp)
        self.assertTrue(UserScore.objects.filter(user = user, score = 546, date = '2014-11-12T15:02:10').exists(), True)
         
#===============================================================================
# end score test
#===============================================================================