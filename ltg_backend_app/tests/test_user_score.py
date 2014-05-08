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
from ltg_backend_app.models import Section,UserProfile, UserSectionScore, UserScore
from django.contrib.auth.models import User
from tastypie.models import ApiKey

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
        user = User.objects.first()
        resp = self.api_client.post(uri='/api/v1/userscore/', format='json', data = {'username':user.username,'api_key':user.api_key.key,'score':546,'date':'2014-11-12T15:02:10'})
        self.assertHttpCreated(resp)
        self.assertTrue(UserScore.objects.filter(user_profile = user.profile, score = 546, date = '2014-11-12T15:02:10').exists(), True)
        
#===============================================================================
# end score test
#===============================================================================