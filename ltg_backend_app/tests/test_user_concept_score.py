'''
will hold our user concept score tests
Created on April 28, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Concept, Section, UserProfile,\
    UserConceptScore, UserSectionScore
from django.contrib.auth.models import User

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user concept score test
#===============================================================================

class UserConceptScoreTest(ResourceTestCase):
    
    fixtures = ['initial_data','users_auth']
    
    def test_post_user_concept_score(self):
        '''
        1. test a POST of a single user concept score
        2. test a POST of a list of user concept scores - TODO - NOT IMPLEMENTED 
        '''
        # test a POST of a single user concept score
        user = User.objects.first()
        concept1_id = Concept.objects.first().id
        concept1_uri = '/api/v1/concept/%d/' % concept1_id
        # make the post request
        resp = self.api_client.post(uri='/api/v1/userconceptscore/', format='json',data = {'concept':concept1_uri,'score':666, 'username':user.username,'api_key':user.api_key.key,'date':'2014-11-12T15:02:10'})
        print resp
        self.assertHttpCreated(resp)
        # get the user profile we created the score for
        user_profile = user.profile
        # assert score for the concept was created
        self.assertTrue(UserConceptScore.objects.filter(concept_id = concept1_id, score = 666,user_profile = user_profile,date='2014-11-12T15:02:10').exists())
        
#===============================================================================
# end user concept score test
#===============================================================================