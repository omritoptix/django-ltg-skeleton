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
        # test a POST of a single user section score
        user = User.objects.first()
        section1_id = Section.objects.first().id
        section1_uri = '/api/v1/section/%d/' % section1_id
        # make the post request
        resp = self.api_client.post(uri='/api/v1/usersectionscore/', format='json',data = {'section':section1_uri,'score':666, 'username':user.username,'api_key':user.api_key.key,'date':'2014-11-12T15:02:10'})
        self.assertHttpCreated(resp)
        # get the user profile we created the score for
        user_profile = user.profile
        # assert score for the concept was created
        self.assertTrue(UserSectionScore.objects.filter(section_id = section1_id, score = 666,user_profile = user_profile,date='2014-11-12T15:02:10').exists())
        
#===============================================================================
# end user concept score test
#===============================================================================