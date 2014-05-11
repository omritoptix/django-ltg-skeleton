'''
will hold our user section score tests
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

class UserSectionScoreTest(ResourceTestCase):
    
    fixtures = ['initial_data','users_auth']
    
    def test_post_user_section_score(self):
        '''
        1. test a POST of a single user section score
        2. test a POST of a list of user section scores - TODO - NOT IMPLEMENTED 
        '''
        # set authentication header
        user = User.objects.get(username='yariv')
        authentication_header = 'ApiKey '+user.username+':'+user.api_key.key
        
        # test a POST of a single user section score
        user = User.objects.first()
        section1_id = Section.objects.first().id
        section1_uri = '/api/v1/section/%d/' % section1_id
        # make the post request
        resp = self.api_client.post(uri='/api/v1/usersectionscore/', format='json',data = {'section':section1_uri,'score':666,'date':'2014-11-12T15:02:10'}, authentication=authentication_header)
        self.assertHttpCreated(resp)
        # get the user profile we created the score for
        user_profile = user.profile
        # assert score for the concept was created
        self.assertTrue(UserSectionScore.objects.filter(section_id = section1_id, score = 666,user_profile = user_profile,date='2014-11-12T15:02:10').exists())
        
        # test bulk create of user section scores
        num_user_section_scores =  UserSectionScore.objects.all().count()
        resp = self.api_client.patch(uri='/api/v1/usersectionscore/', format='json', data={'objects':[{'section':section1_uri,'date':'2014-11-12T15:02:10','score':565},{'section':section1_uri,'date':'2014-11-12T15:02:10','score':566}]},authentication = authentication_header)
        self.assertHttpAccepted(resp)
        # make sure the objects were really created since patch return accepted (not created) on bulk operations
        self.assertEqual(num_user_section_scores + 2, UserSectionScore.objects.all().count())
        
#===============================================================================
# end user concept score test
#===============================================================================