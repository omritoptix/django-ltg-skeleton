'''
For my TDD
Created on April 8, 2014

@authors: Yariv Katz & Omri Dagan
@version: 1.0
@copyright: LTG
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
    Ltg backend tests will be written here
    '''
    fixtures = ['ltg_backend_app']
    
    def test_register(self):
        '''
        test registration api
        1. regular user registration is successfull
        2. registration with duplicate email of the first this should fail
        3. registration without uuid should fail
        4. fourth with validation errors
        5. anonymous user registration only with uuid successfull
        5. registration only with uuid and mail fail (since not recognized as anonymous if email exists)
        6. test login of already registered anonymous user. will be indentified by uuid. 
        '''
        #regular user registration successfull
        user_count = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678','uuid':'12345'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #duplicate email
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678','uuid':'123456'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #registration without uuid
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk20@gmail.com', 'password': '12345678'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #various validation errors
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'yariv1gmail.com', 'password': '12','uuid':'1234567'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        #anonymous registration successfull
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'uuid':'12345678'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), user_count + 2)
        
        #registration only with uuid and mail fail (since not recognized as anonymous if email exists)
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'uuid':'123456789','email':'omri@ltg.com'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 2)
        
        #test login of already registered anonymous user. will be indentified by uuid.
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'uuid':'12345678'})
        self.assertHttpAccepted(resp)
    
    
#===============================================================================
# end testing
#===============================================================================
