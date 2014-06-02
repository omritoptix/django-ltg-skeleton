'''
will hold our user tests
Created on May 20, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from django.contrib.auth import get_user_model
import datetime
from django.utils.timezone import utc

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user test
#===============================================================================

class UserTest(ResourceTestCase):
    
    fixtures=['users_auth']
    
    def test_post_user(self):
        """
        will test that an user is created upon POST request
        1. create a new user and make sure it was created
        2. post with duplicate mail fails
        3. post with invalid password fails  
        
        # note : on creation, a hubspot contact is also created.
        when you run this test you might get an exception 409 conflict, since the user wer'e creating here may already exists
        in hubspot.
        """
        User = get_user_model()
        # create a new user and make sure it was created
        resp = self.api_client.post(uri='/api/v1/user/', format='json', data={'email':'omri2@ltgexam.com','password':'1234567899','uuid':'123123','first_name':'omri','last_name':'dagan'})
        self.assertHttpCreated(resp)
        # check new attempt was created with correct values
        recent_user = User.objects.latest('date_joined')
        self.assertEqual(recent_user.uuid,'123123')
        self.assertTrue(recent_user.check_password('1234567899'), True)
        
        # post with duplicate mail fails
        resp = self.api_client.post(uri='/api/v1/user/', format='json', data={'email':'omri2@ltgexam.com','password':'1234567899','uuid':'123123','first_name':'omri','last_name':'dagan'})
        self.assertHttpBadRequest(resp)
        
        # post with invalid password fails
        resp = self.api_client.post(uri='/api/v1/user/', format='json', data={'email':'omri3@ltgexam.com','password':'12345','uuid':'123123','first_name':'omri','last_name':'dagan'})
        self.assertHttpBadRequest(resp)
       
    def test_get_user(self):
        """
        will test that only the user which is the owner
        of the user resource can GET it.
        1. GET the user with user credentails - success
        2. GET the user with anonymous user - unauthorized
        3. GET the user with other user credentials - unauthorized
        """
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email="yariv@nerdeez.com")
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        
        # GET the user with user credentails - success
        user_uri = '/api/v1/user/%d/' % user.id
        resp = self.api_client.get(uri=user_uri, format='json', authentication=authentication_header)
        self.assertHttpOK(resp)
        
        # GET the user with anonymous user - fail
        resp = self.api_client.get(uri=user_uri, format='json')
        self.assertHttpUnauthorized(resp)
        
        # set authentication header
        user = User.objects.get(email="omri@ltgexam.com")
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        
        # GET the user with other user credentials - fail
        resp = self.api_client.get(uri=user_uri, format='json',data={}, authentication=authentication_header)
        self.assertHttpUnauthorized(resp)
        
    def test_update_user(self):
        """
        test update of user details
        1. update first name, last name, language, platform - success
        2. update password, username - fails
        3. update email - fail
        4. update other user's details (not my user details) - unauthorized
        5. test 'start-session' endpoint - need to update session num, last login, and other user details found in the payload
        """
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email="yariv@nerdeez.com")
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        
        # update first name, last name, language, platform
        user_uri = '/api/v1/user/%d/' % user.id
        resp = self.api_client.patch(uri=user_uri, format='json',data={'first_name':'doron','last_name':'nachshon','language':0,'platform_last_logged_in':0}, authentication=authentication_header)
        self.assertHttpAccepted(resp)
        # make sure first name and last name were updated
        user = User.objects.get(email="yariv@nerdeez.com")
        self.assertEqual(user.first_name,'doron')
        self.assertEqual(user.last_name,'nachshon')
        self.assertEqual(user.language,0)
        self.assertEqual(user.platform_last_logged_in,0)
        
        # update password, username - fails
        resp = self.api_client.patch(uri=user_uri, format='json',data={'password':'987654321','username':'AAA'}, authentication=authentication_header)
        self.assertHttpAccepted(resp)
        # make sure username and password are not updated
        user = User.objects.get(email="yariv@nerdeez.com")
        self.assertFalse(user.check_password('987654321'))
        self.assertNotEqual(user.username,'AAA')
        
        # update email - fail
        resp = self.api_client.patch(uri=user_uri, format='json',data={'email':'a@a.com'}, authentication=authentication_header)
        self.assertHttpAccepted(resp)
        # make sure username and password are not updated
        user = User.objects.get(username="yariv")
        self.assertNotEqual(user.email,'a@a.com')
        
        # update other user details - unauthorized
        user = User.objects.get(email="omri@ltgexam.com")
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        resp = self.api_client.patch(uri=user_uri, format='json',data={'last_name':'omri'}, authentication=authentication_header)
        self.assertHttpUnauthorized(resp)
        
        # test 'start session' for user
        num_of_sessions = user.num_of_sessions
        increment_session_uri = '/api/v1/user/start-session/'
        resp = self.api_client.post(uri=increment_session_uri, format='json',data={}, authentication=authentication_header)
        self.assertHttpOK(resp)
        user = User.objects.get(email="omri@ltgexam.com")
        self.assertEqual(user.num_of_sessions, num_of_sessions + 1)
        self.assertEqual(user.last_login,datetime.datetime.now().replace(microsecond=0,tzinfo=utc))
        
#===============================================================================
# end user test
#===============================================================================