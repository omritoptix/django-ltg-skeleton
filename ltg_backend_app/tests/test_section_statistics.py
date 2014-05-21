'''
will hold our section statistics tests
Created on May 12, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.models import Section, SectionStatistics
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.contrib.auth import get_user_model

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin concept statistics test
#===============================================================================

class SectionStatisticsTest(ResourceTestCase):

    fixtures=['initial_data','users_auth']
    
    def setUp(self):
        ''' 
        - create section statistics data
        '''
        # create concept statistics for the objects
        section = Section.objects.first()
        SectionStatistics.objects.create(section_id=section.id, mean_score=30.0, std_score=11.0)
        return super(SectionStatisticsTest,self).setUp()
    
    def test_get_section_statistics(self):
        '''
        will test the section statistics api resource.
        1. get a single section statistics
        2. get a list of section statistics
        '''
        # init authentication header
        User = get_user_model()
        user = User.objects.first()
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        # get a single question 
        ss_uri = '/api/v1/sectionstatistics/%d/' % (SectionStatistics.objects.first().id)
        resp = self.api_client.get(uri=ss_uri, format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['mean_score'], 30.0)
        
        #get questions statistics
        resp = self.api_client.get(uri='/api/v1/sectionstatistics/', format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'][0]['std_score'], 11.0)
        
    def test_post_section_statistics(self):
        '''
        test that a POST request to a section statistics is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/sectionstatistics/')
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end section statistics test
#===============================================================================