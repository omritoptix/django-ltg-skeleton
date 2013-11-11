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
from ticketz_backend_app.models import *

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
    fixtures = ['ticketz_backend_app']
    
    def test_login(self):
        '''
        test the login api
        - check success login
        - check login failed on user not active
        - check login fails on gibrish
        '''
        
        #test success login
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'ywarezk@gmail.com', 'password': 'housekitten4'})
        self.assertHttpAccepted(resp)
        self.assertTrue(self.deserialize(resp)['success'])
        
        #test user is not active
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'yariv@nerdeez.com', 'password': '12345'})
        self.assertHttpUnauthorized(resp)
        
        #test gibrish login
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'dsgsdfg@nerdeez.com', 'password': '12345'})
        self.assertHttpUnauthorized(resp)
        
    def test_register(self):
        '''
        test the registration api
        - test success registration
        - test registration duplication
        '''
        #test success registration
        num_users = User.objects.count()
        num_business = Business.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv1@nerdeez.com', 'business_id': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertEqual(User.objects.count(), num_users + 1)
        self.assertEqual(Business.objects.count(), num_business + 1)
        
        #test duplicate
        num_users = User.objects.count()
        num_business = Business.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv1@nerdeez.com', 'business_id': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertHttpConflict(resp)
        self.assertEqual(User.objects.count(), num_users)
        self.assertEqual(Business.objects.count(), num_business)
        
    def test_forgot_password(self):
        '''
        test the api for the forgot password
        - test with random mail
        - test with mail not activated
        - test with mail activated
        '''
        
        resp = self.api_client.post(uri='/api/v1/utilities/forgot-password/', format='json', data={'email': '@gmail.com'})
        self.assertHttpNotFound(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/forgot-password/', format='json', data={'email': 'yariv@nerdeez.com'})
        self.assertHttpUnauthorized(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/forgot-password/', format='json', data={'email': 'ywarezk@gmail.com'})
        self.assertHttpAccepted(resp)
        
    
        

#===============================================================================
# end testing
#===============================================================================