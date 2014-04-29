'''
will hold our tutor resource tests
Created on April 22, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''
#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin test case
#===============================================================================

class Tutor(ResourceTestCase):
    
    def test_get_tutor(self):
        '''
        will test the tutor api resource.
        1. get a single tutor and check it returns a 'first_name' field
        2. get a list of tutors and check that the first object returns a 'first_name' field 
        '''
        #get tutor
        resp = self.api_client.get(uri='/api/v1/tutor/8092/', format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)) > 0)
        self.assertTrue(self.deserialize(resp)['first_name'])
        
        #get tutors
        resp = self.api_client.get(uri='/api/v1/tutor/', format='json')
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)) > 0)
        self.assertTrue(len(self.deserialize(resp)['objects'][0]['first_name']))
        
#===============================================================================
# end test case
#===============================================================================