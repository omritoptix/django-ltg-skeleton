'''
will hold our utilities tests
Created on April 22, 2014
 
@authors: Yariv Katz & Omri Dagan
@version: 1.0
@copyright: LTG
'''
 
#===============================================================================
# begin import
#===============================================================================
 
from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
import pdb
from django.contrib.auth import authenticate, get_user_model
 
#===============================================================================
# end import
#===============================================================================
 
#===============================================================================
# begin utilities test
#===============================================================================
 
class UtilitiesRegisterTest(ResourceTestCase):
    '''
    will test the 'register' and 'skip-register' methods of the utilities resouce.
    '''
    fixtures = ['users_auth']
         
class UtilitiesLoginTest(ResourceTestCase):
     
    def setUp(self):
        '''
        create a user  for the login test
        '''
        User = get_user_model()
        user = User.objects.create_user(username='omridagan', email='omridagan@ltg.com', password='top_secret')
        user.save()
        return super(UtilitiesLoginTest,self).setUp()
         
    def test_login(self):
        '''
        will test email password login.
        1. test successfull login with correct credentails.
        2. test login without email
        3. test login without password
        4. test login with bad credentails
        '''
        User = get_user_model()
        # test successfull login with correct credentails.
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'omridagan@ltg.com','password':'top_secret'})
        self.assertHttpOK(resp)
        # make sure username and api key are returned in the response and are correct
        self.assertEqual(self.deserialize(resp)['username'],'omridagan')
        self.assertEqual(self.deserialize(resp)['api_key'],User.objects.get(username='omridagan').api_key.key)
         
        # test login without email 
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'password':'top_secret'})
        self.assertHttpUnauthorized(resp)
         
        # test login without password 
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'omri@ltg.com'})
        self.assertHttpUnauthorized(resp)
         
        # test login with bad credentails
        resp = self.api_client.post(uri='/api/v1/utilities/login/', format='json', data={'email': 'omri2@ltg.com','password':'bottom_secret'})
        self.assertHttpUnauthorized(resp)
         
         
class UtilitiesForgotPasswordTest(ResourceTestCase):
      
    fixtures=['users_auth']
      
    def test_forgot_password(self):
        '''
        test forgot password api.
        1. test with valid email address
        2. test with invalid email address (not in the system)
        3. test with valid email address but user is not active
        '''
        User = get_user_model()
        # set up resource uri
        forgot_password_uri = '/api/v1/utilities/forgot-password/'
        # test with valid email address
        user1 = User.objects.get(email='omri@ltgexam.com')
        resp = self.api_client.post(uri=forgot_password_uri, format='json', data={'email':user1.email})
        self.assertHttpAccepted(resp)
         
        # test with invalid email address
        resp = self.api_client.post(uri=forgot_password_uri, format='json', data={'email':'non-existent-email'})
        self.assertHttpNotFound(resp)
         
        # test with valid email address but user is not active
        user2 = User.objects.get(email='tzachi@ltgexam.com')
        resp = self.api_client.post(uri=forgot_password_uri, format='json', data={'email':user2.email})
        self.assertHttpNotFound(resp)
         
class UtilitiesResetPasswordTest(ResourceTestCase):
      
    fixtures=['users_auth']
      
    def test_reset_password(self):
        '''
        test reset password api.
        1. test reset password of authenticated user
        2. test reset password of anonymous user (without authentication header)
        3. test reset password for not active user
        4. test reset password with not valid password
        '''
        # set up resource uri
        reset_password_uri = '/api/v1/utilities/reset-password/'
         
        # test reset password of authenticated user
        User = get_user_model()
        user1 = User.objects.get(email='omri@ltgexam.com')
        user1_authentication_header = 'ApiKey ' + user1.email + ':' + user1.api_key.key
        resp = self.api_client.post(uri = reset_password_uri, format='json', data = {'password':'1234567899'}, authentication = user1_authentication_header)
        self.assertHttpOK(resp)
        # make sure the password really updated by authenticating the user with the new password
        result = authenticate(email=user1.email, password='1234567899')
        self.assertNotEqual(result, None)
         
        # test reset password of anonymous user (without authentication header)
        resp = self.api_client.post(uri = reset_password_uri, format='json', data = {'password':'1234567899'})
        self.assertHttpUnauthorized(resp)
         
        # test reset password for not active user
        user2 = User.objects.get(email='tzachi@ltgexam.com')
        user2_authentication_header = 'ApiKey: '+user2.email+':'+user2.api_key.key 
        resp = self.api_client.post(uri = reset_password_uri, format='json', data = {'password':'1234567899'}, authentication = user2_authentication_header)
        self.assertHttpUnauthorized(resp)
         
        # test reset password with not valid password
        user1 = User.objects.get(email='omri@ltgexam.com')
        user1_authentication_header = 'ApiKey '+user1.email+':'+user1.api_key.key 
        resp = self.api_client.post(uri = reset_password_uri, format='json', data = {'password':'123'}, authentication = user1_authentication_header)
        self.assertHttpBadRequest(resp)
         
         
#===============================================================================
# end utilities test
#===============================================================================