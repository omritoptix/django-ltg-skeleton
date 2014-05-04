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
from ltg_backend_app.models import UserProfile
import pdb

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
    
    def test_register(self):
        '''
        test registration api
        1. valid details registration is successfull
        2. registration with duplicate email should fail
        3. registration without uuid should fail
        4. registration with validation error
        5. registration without password should fail
        '''
        # valid details registration is successfull
        user_count = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678','uuid':'12345'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        # make sure user created with is_anonymous = False
        latest_user = User.objects.latest('date_joined')
        self.assertFalse(latest_user.profile.is_anonymous)
    
        # registration with duplicate email will fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678','uuid':'123456'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
          
        # registration without uuid will fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk20@gmail.com', 'password': '12345678'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
          
        # various validation errors
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'yariv1gmail.com', 'password': '12','uuid':'1234567'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        # registration without password should fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk3@gmail.com','uuid':'12345abcd'})
        self.assertHttpBadRequest(resp)

    def test_skip_register(self):
        '''
        test skip register
        1. skip register for the first time will create the user
        2. skip register for the next times will get the user and not create it
        3. skip register without uuid will fail
        4. skip register with uuid and mail is not allowed
        '''
        # skip register for the first time will create the user
        user_count = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/skip-register/', format='json', data={'uuid':'12345678'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        # make sure user created with is_anonymous = True
        latest_user = User.objects.latest('date_joined')
        self.assertTrue(latest_user.profile.is_anonymous)
        
        # skip register for the next times will get the user and not create it
        resp = self.api_client.post(uri='/api/v1/utilities/skip-register/', format='json', data={'uuid':'12345678'})
        self.assertHttpOK(resp)
        self.assertEqual(User.objects.count(), user_count + 1)
        
        # skip register without uuid will fail
        resp = self.api_client.post(uri='/api/v1/utilities/skip-register/', format='json')
        self.assertHttpBadRequest(resp)
        
        # skip register with uuid and mail is not allowed
        resp = self.api_client.post(uri='/api/v1/utilities/skip-register/', format='json', data={'uuid':'123456789','email':'omri@ltg.com'})
        self.assertHttpBadRequest(resp)
        
    def test_register_existing_anonymous_user(self):
        '''
        will test anonymous user which used to do 'skip register' now wants to register.
        the user is identified by it's uuid.
        1. test register without email will fail
        2. test register without password will fail
        3. test register with existing email will fail
        4. test anonymous register will update the anonymous user details and not create new user.
        '''
        # create the anonymous user (skip-register)
        resp = self.api_client.post(uri='/api/v1/utilities/skip-register/', format='json', data={'uuid':'12345678'})
        self.assertHttpCreated(resp)
        anonymous_user = User.objects.latest('date_joined')
        # assert email is empty
        self.assertEqual(anonymous_user.email,'')
        # get current number of users
        user_count = User.objects.count()
        
        # test register without email will fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'omri', 'last_name': 'dagan', 'password': '12345678','uuid':'12345678'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count)
        
        # test register without password will fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'omri', 'last_name': 'dagan', 'email': 'omri@gmail.com','uuid':'12345678'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count)
        
        # test register with existing email will fail
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'omri', 'last_name': 'dagan', 'email': 'yariv@nerdeez.com','uuid':'12345678','password': '12345678'})
        self.assertHttpBadRequest(resp)
        self.assertEqual(User.objects.count(), user_count)
        
        # test anonymous register will update the anonymous user details and not create new user
        user_count = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'ywarezk@gmail.com', 'password': '12345678','uuid':'12345678'})
        self.assertHttpCreated(resp)
        # assert new user not created
        self.assertEqual(User.objects.count(), user_count)
        registered_user = User.objects.latest('date_joined')
        # assert the former and later user are the same user only with updated details
        self.assertEqual(anonymous_user.id, registered_user.id)
        # assert email was updated
        self.assertEqual(registered_user.email,'ywarezk@gmail.com')
        
class UtilitiesLoginTest(ResourceTestCase):
    
    def setUp(self):
        '''
        create a user and user profile for the login test
        '''
        user = User.objects.create_user(username='omridagan', email='omridagan@ltg.com', password='top_secret')
        user.save()
        user_profile = UserProfile.objects.create(uuid='12345678',user=user)
        user_profile.save()
        return super(UtilitiesLoginTest,self).setUp()
        
    def test_login(self):
        '''
        will test email password login.
        1. test successfull login with correct credentails.
        2. test login without email
        3. test login without password
        4. test login with bad credentails
        '''
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
        
#===============================================================================
# end utilities test
#===============================================================================