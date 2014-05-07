'''
will hold our concept tests
Created on April 28, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Concept,UserProfile, UserConceptScore
import datetime

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin concept test
#===============================================================================

class ConceptTest(ResourceTestCase):
    
    fixtures=['users_auth']
    
    def setUp(self):
        '''
        create concept and concept score
        '''
        concept = Concept.objects.create(title="Concept1")
        UserConceptScore.objects.create(user_profile = UserProfile.objects.first(),concept = concept, score = 300,date = datetime.datetime.now())     
        return super(ConceptTest,self).setUp()
    
    def test_get_concepts(self):
        '''
        will test the concept api resource.
        1. get a single concept and make sure statistics for this concept are returned
        2. get a list of concepts and make sure statistics for a concept is returned 
        '''
        
        # get a single concept
        concept_id = Concept.objects.first().id
        resp = self.api_client.get(uri='/api/v1/concept/%d/' % concept_id, format='json')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['statistics']['mean'],300)
        self.assertEqual(self.deserialize(resp)['statistics']['std'],0)
        
        # get concepts list
        resp = self.api_client.get(uri='/api/v1/concept/', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'][0]['statistics']['mean'],300)
        
    def test_post_concept(self):
        '''
        test that a POST request to a concept is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/concept/',data={'title':'hey'})
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end concept test
#===============================================================================