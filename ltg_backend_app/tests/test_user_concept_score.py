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
from ltg_backend_app.models import Concept, Section,\
    UserConceptScore, UserSectionScore
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
 
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
        2. test bulk create of user concepts score 
        '''
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email='yariv@nerdeez.com')
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
         
        # test a POST of a single user concept score
        concept1_id = Concept.objects.first().id
        concept1_uri = '/api/v1/concept/%d/' % concept1_id
        # make the post request
        resp = self.api_client.post(uri='/api/v1/userconceptscore/', format='json',data = {'concept':concept1_uri,'score':666,'date':'2014-11-12T15:02:10'},authentication = authentication_header)
        self.assertHttpCreated(resp)
        # assert score for the concept was created
        self.assertTrue(UserConceptScore.objects.filter(concept_id = concept1_id, score = 666,user = user,date='2014-11-12T15:02:10').exists())
         
        # test bulk create of user concept scores
        num_user_concept_scores =  UserConceptScore.objects.all().count()
        resp = self.api_client.patch(uri='/api/v1/userconceptscore/', format='json', data={'objects':[{'concept':concept1_uri,'date':'2014-11-12T15:02:10','score':565},{'concept':concept1_uri,'date':'2014-11-12T15:02:10','score':566}]},authentication = authentication_header)
        self.assertHttpAccepted(resp)
        # make sure the objects were really created since patch return accepted (not created) on bulk operations
        self.assertEqual(num_user_concept_scores + 2, UserConceptScore.objects.all().count())
         
#===============================================================================
# end user concept score test
#===============================================================================