'''
will hold our concept statistics tests
Created on May 12, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.models import Concept, ConceptStatistics
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin concept statistics test
#===============================================================================

class ConceptStatisticsTest(ResourceTestCase):

    fixtures=['initial_data','users_auth']
    
    def setUp(self):
        ''' 
        - create concept statistics data
        '''
        # create concept statistics for the objects
        concept = Concept.objects.first()
        ConceptStatistics.objects.create(concept_id=concept.id, mean_score=30.0, std_score=11.0)
        return super(ConceptStatisticsTest,self).setUp()
    
    def test_get_concept_statistics(self):
        '''
        will test the concept statistics api resource.
        1. get a single concept statistics
        2. get a list of concept statistics
        '''
        # init authentication header
        user = User.objects.first()
        authentication_header = 'ApiKey '+user.username+':'+user.api_key.key
        # get a single question 
        cs_uri = '/api/v1/conceptstatistics/%d/' % (ConceptStatistics.objects.first().id)
        resp = self.api_client.get(uri=cs_uri, format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['mean_score'], 30.0)
        
        #get questions statistics
        resp = self.api_client.get(uri='/api/v1/conceptstatistics/', format='json', authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'][0]['std_score'], 11.0)
        
    def test_post_concept_statistics(self):
        '''
        test that a POST request to a conecpt statistics is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/conceptstatistics/')
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end concept statistics test
#===============================================================================