'''
For my TDD, bitch
Created on November 7, 2013

@author: ywarezk
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin testing
#===============================================================================

class ApiTest(ResourceTestCase):
    '''
    nerdeez backend tests will be written here
    '''
    fixtures = ['ltg_backend_app']
    
    def test_register(self):
        '''
        test registration api
        - first registration is successfull
        - second registration with duplicate email of the first this should fail
        - third with validation errors
        '''
        #success
        user_count = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678'})
        print resp.content
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #duplicate email
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678'})
        self.assertHttpConflict(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #validation errors
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'yariv1@gmail.com', 'password': '12'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
    
    
#===============================================================================
# end testing
#===============================================================================
