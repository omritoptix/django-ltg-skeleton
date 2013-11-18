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
        print resp.status_code
        print resp.content
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
        
    def test_deals(self):
        '''
        test the api for the deals
        - get with no cradentials get unauthorize
        - get with cradentials of other user get unauthorize
        - get with cradentials of other users get 0 objects
        - put with no cradentials fail
        - put with wrong cradentials fail
        - post for inactive user fail
        - post for active user success
        '''
        
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={})
        self.assertHttpOK(resp)
        
        
        resp = self.api_client.post(uri='/api/v1/deal/?username=yariv&api_key=12345678', format='json', 
                                    data={
                                            "original_price": 100, 
                                            "valid_from": "2013-11-13T02:00:00Z", 
                                            "description": "new beer promotion in a software company? kind of makes you wonder what the hell are they doing there", 
                                            "title": "1+1 beers", 
                                            "discounted_price": 50, 
                                            "num_total_places": 10, 
                                        }
        )
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.post(uri='/api/v1/deal/?username=ywarezk&api_key=12345678', format='json', 
                                    data={
                                            "original_price": 100, 
                                            "valid_from": "2013-11-13T02:00:00Z", 
                                            "description": "new beer promotion in a software company? kind of makes you wonder what the hell are they doing there", 
                                            "title": "1+1 beers", 
                                            "discounted_price": 50, 
                                            "num_total_places": 10, 
                                        }
        )
        self.assertHttpCreated(resp)
        self.assertEqual(Deal.objects.get(id=2).status, 1)
        
        resp = self.api_client.put(uri='/api/v1/deal/1/?username=yariv&api_key=12345678', format='json', 
                                    data={
                                            "original_price": 80, 
                                        }
        )
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.put(uri='/api/v1/deal/1/?username=ywarezk&api_key=12345678', format='json', 
                                    data={
                                            "original_price": 80, 
                                        }
        )
        self.assertHttpAccepted(resp)
        self.assertEqual(Deal.objects.get(id=1).status, 1)
        
    def test_deal_filter(self):
        '''
        test that the filtering works
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'status': 1})
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
        
        
        
        
        
    
        

#===============================================================================
# end testing
#===============================================================================