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
from tastypie.models import ApiKey
# from ticketz_backend_app.clock import close_deals

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
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv2@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertEqual(User.objects.count(), num_users + 1)
        self.assertEqual(Business.objects.count(), num_business + 1)
        
        #test duplicate
        num_users = User.objects.count()
        num_business = Business.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv1@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
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
        self.assertHttpUnauthorized(resp)
        
        
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
                                            "valid_from": "2013-11-23T20:00:00Z", 
                                            "valid_to": "2013-11-23T21:00:00Z", 
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
        #self.assertEqual(Deal.objects.get(id=1).status, 1)
        
        resp = self.api_client.put(uri='/api/v1/deal/1/', format='json', 
                                    data={
                                            "original_price": 70,
                                            "title":"a",
                                            "description":"a",
                                            "valid_from":"Tue, 19 Nov 2013 08:47:00 GMT",
                                            "valid_to":"Tue, 19 Nov 2013 09:47:00 GMT",
                                            "num_total_places":5,
                                            "image":"ClQgPkY6Rz6HXrBISsbn_TESTEST.png?Signature=2L1gApCKqIpdD7F4iZUTrA4vtRU%3D&Expires=1385033306&AWSAccessKeyId=AKIAIJRI4JLYPRLYWKKA",
                                            "original_price":50,
                                            "discounted_price":30,
                                            "status":0,
                                            "num_available_places":5,
                                            "creation_date":"Tue, 19 Nov 2013 08:48:15 GMT",
                                            "business":"/api/v1/business/3/",
                                            "username":"ywarezk",
                                            "api_key":"12345678"
                                        }
        )
        print resp.status_code
        self.assertHttpAccepted(resp)
        
    def test_deal_filter(self):
        '''
        test that the filtering works
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'status': 1, 'username': 'ywarezk', 'api_key': '12345678'})
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 2)
        
    def test_register_user(self):
        '''
        test the user registration through uuid
        '''
        
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'uuid': 'helloworld'})
        self.assertHttpCreated(resp)
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'uuid': 'helloworld'})
        self.assertHttpAccepted(resp)
        
    def test_register_and_deals(self):
        '''
        test the registration through the smartphone
        also test the registerd user can't add a deal
        '''
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'uuid': 'helloworld'})
        self.assertHttpCreated(resp)
        username = self.deserialize(resp)['username']
        api_key = self.deserialize(resp)['api_key']
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': username, 'api_key': api_key})
        self.assertHttpOK(resp)
        resp = self.api_client.post(uri='/api/v1/deal/', format='json', 
                                    data={
                                            "original_price": 100, 
                                            "valid_from": "2013-11-23T20:00:00Z", 
                                            "valid_to": "2013-11-23T21:00:00Z", 
                                            "description": "new beer promotion in a software company? kind of makes you wonder what the hell are they doing there", 
                                            "title": "1+1 beers", 
                                            "discounted_price": 50, 
                                            "num_total_places": 10, 
                                            'username': username,
                                            'api_key': api_key
                                        }
        )
        self.assertHttpUnauthorized(resp)
        
        
        
    def test_category_in_deal(self):
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'ywarezk', 'api_key': '12345678'})
        self.assertTrue('category' in self.deserialize(resp)['objects'][0])
        
    def test_order_validto(self):
        '''
        test the order by -valid_to
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'ywarezk', 'api_key': '12345678', 'order_by': '-valid_to'})
        objects = self.deserialize(resp)['objects']
        self.assertEqual(len(objects), 3)
        self.assertEqual(objects[0]['id'], 2)
        self.assertEqual(objects[1]['id'], 3)
        self.assertEqual(objects[2]['id'], 1)
        
    def test_num_available_places(self):
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'ywarezk', 'api_key': '12345678', 'order': '-valid_to'})
        self.assertTrue('num_available_places' in self.deserialize(resp)['objects'][0])
        
    def test_deal_category(self):
        '''
        reported bug: saving the category in deal creation is not saved
        '''
        resp = self.api_client.post(uri='/api/v1/deal/', format='json', data={
                                                                              'username': 'ywarezk', 
                                                                              'api_key': '12345678', 
                                                                              "title":"aaa",
                                                                              "description":"a",
                                                                              "valid_from":"Wed, 20 Nov 2013 12:53:00 GMT",
                                                                              "valid_to":"Wed, 20 Nov 2013 14:53:00 GMT",
                                                                              "num_total_places":5,
                                                                              "image":None,
                                                                              "original_price":5,
                                                                              "discounted_price":2,
                                                                              "status":0,
                                                                              "num_available_places":5,
                                                                              "creation_date":None,
                                                                              "business":"/api/v1/business/1/",
                                                                              "category":"/api/v1/category/1/"})
        self.assertHttpCreated(resp)
        num_deals = Deal.objects.all().count()
        deals = Deal.objects.all()
        new_deal = deals[num_deals - 1]
        self.assertEqual(new_deal.category.id, 1)
        
    def test_logger(self):
        '''
        test that our logger is documenting failed communication
        '''
        resp = self.api_client.put(uri='/api/v1/deal/1/?username=yariv&api_key=12345678', format='json', 
                                    data={
                                            "original_price": 80, 
                                        }
        )
        self.assertHttpUnauthorized(resp)
        self.assertEqual(Logger.objects.count(), 1)
        
    def test_transaction(self):
        '''
        will check the payment transactions
        for this test i put a user profile with a client id and payment id
        we need to pass deal and amount
        '''
        resp = self.api_client.post(uri='/api/v1/transaction/?username=ywarezk&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/', 'amount': 3})
        print resp.content
        self.assertHttpCreated(resp)
        self.assertEquals(UserProfile.objects.get(id=1).phone, '+972522441431')
        
        
    def test_unpaid_transaction(self):
        '''
        will check the api for the unpaid transaction
        '''
        resp = self.api_client.post(uri='/api/v1/unpaidtransaction/?username=yariv1&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/','phone': '+972522441432'})
        self.assertHttpCreated(resp)
        self.assertEquals(UserProfile.objects.get(id=3).phone, '+972522441432')
        
    def test_logger_api(self):
        '''
        test i can post to the logger
        '''
        resp = self.api_client.post(uri='/api/v1/logger/', format='json', data={'path': 'sdfsd', 'post': 'dfsdf', 'get': 'sdsdf', 'content': 'sdsd', 'free_text': 'sfdsdf'})
        self.assertHttpCreated(resp)
        
    def test_deal_business_filter(self):
        '''
        test the filter deal by business
        '''
        resp = self.api_client.get(uri='/api/v1/deal/?business__id=2&username=ywarezk&api_key=12345678', format='json', data={})
        print resp.content
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
        
    def test_deal_category_filter(self):
        '''
        test the filter deal by business
        '''
        resp = self.api_client.get(uri='/api/v1/deal/?category__id=1&username=ywarezk&api_key=12345678', format='json', data={})
        print resp.content
        self.assertHttpOK(resp)
        
    def test_search(self):
        '''
        test the api for the search deals
        '''
        resp = self.api_client.get(uri='/api/v1/deal/?search=promotion&username=ywarezk&api_key=12345678', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        
    def test_delete_deal(self):
        '''
        should allow settings the status to zero in the deal
        '''
        resp = self.api_client.put(uri='/api/v1/deal/1/', format='json', data={'username': 'ywarezk', 'api_key': '12345678', 'status': 0})
        self.assertHttpAccepted(resp)
        deal = Deal.objects.get(id=1)
        self.assertEqual(deal.status, 0)
        
    def test_confirm_deals(self):
        '''
        test the confirm deals api
        - first test will try to activate a transaction from a cradentials of another business
        - second test will try to successfully change
        '''
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12345'})
        self.assertHttpUnauthorized(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'ywarezk', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12345'})
        print resp.content
        self.assertHttpOK(resp)
        self.assertEqual(Transaction.objects.get(id=1).status, 3)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12344'})
        self.assertHttpUnauthorized(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'ywarezk', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12344'})
        self.assertHttpOK(resp)
        self.assertEqual(UnpaidTransaction.objects.get(id=1).status, 2)
        
    def test_new_business_cant_modify_deals(self):
        '''
        test that a new registered business cant modify old deals
        reported auth bug
        '''
         
        #register a new business and set it as active
        old_num_users = User.objects.all().count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv2@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.all().count(), old_num_users + 1)
        users = User.objects.all()
        for single_user in users:
            if single_user.id == 4:
                user = single_user
        user.is_active = True
        user.save()
        
        #find the api key of the user
        api_key = ApiKey()
        api_key.user = user
        api_key.save()
        
        #modify deal number one which doesnt belong to this business
        resp = self.api_client.put(uri='/api/v1/deal/1/', format='json', 
                                    data={
                                            "original_price": 80,
                                            'username': user.username,
                                            'api_key': api_key.key  
                                        }
        )
        self.assertHttpUnauthorized(resp)
        self.assertNotEquals(Deal.objects.get(id=1).original_price, 80)
        
    def test_user_profile_only_owner_can_read(self):
        '''
        test that a user profile cant read other user profiles
        '''
        resp = self.api_client.get(uri='/api/v1/userprofile/3/?username=ywaerzk&api_key=12345678', format='json')
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.put(uri='/api/v1/userprofile/3/?username=ywaerzk&api_key=12345678', format='json', data={'phone': '12345678'})
        self.assertHttpUnauthorized(resp)
        self.assertNotEqual(UserProfile.objects.get(id=3).phone, '12345678')
        
    def test_deal_contain_business(self):
        '''
        test that the deal api returns a business object
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'ywarezk', 'api_key': '12345678'})
        business = self.deserialize(resp)['objects'][0]['business']
        self.assertTrue('id' in business)
        
        
        
        
        
        
        
        
    
        
#     def test_refund(self):
#         '''
#         will check the the api for the refund is working
#         '''
#         #test refund is working
#         resp = self.api_client.post(uri='/api/v1/refund/?username=ywarezk&api_key=12345678', format='json', data={'transaction': '/api/v1/transaction/1/', 'description': 'Trying to work my way on a refund'})
#         self.assertHttpCreated(resp)
#         self.assertEqual(Refund.objects.all().count(), 1)
#         self.assertNotEqual(Refund.objects.all()[0].paymill_refund_id, None)
        
        
        
        
    
#===============================================================================
# end testing
#===============================================================================