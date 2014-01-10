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
from dateutil.relativedelta import relativedelta
import datetime
from ticketz_backend_app.tasks import close_unactive_reservation
from ticketz_backend_app.tasks import send_push_notification

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
        num_business = BusinessProfile.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv3@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertEqual(User.objects.count(), num_users + 1)
        self.assertEqual(BusinessProfile.objects.count(), num_business + 1)
        
        #test duplicate
        num_users = User.objects.count()
        num_business = BusinessProfile.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv1@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertHttpConflict(resp)
        self.assertEqual(User.objects.count(), num_users)
        self.assertEqual(BusinessProfile.objects.count(), num_business)
        
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
        - get with no cradentials get only active deals
        - post for unautorized user fails
        - put with no cradentials fail
        - put with wrong cradentials fail
        - post for inactive user fail
        - post for active user success
        '''
        
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={})
        self.assertHttpOK(resp)
        self.assertTrue(len(self.deserialize(resp)['objects']) > 0)
        for single_deal in self.deserialize(resp)['objects']:
            self.assertEqual(single_deal['status'], 4)
        
        
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
        resp = self.api_client.post(uri='/api/v1/deal/?username=yariv1&api_key=12345678', format='json', 
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
        resp = self.api_client.put(uri='/api/v1/deal/1/?username=yariv1&api_key=12345678', format='json', 
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
                                            "username":"yariv1",
                                            "api_key":"12345678"
                                        }
        )
        self.assertHttpAccepted(resp)
        
    def test_deal_filter(self):
        '''
        test that the filtering works
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'id__in' : '2,3' , 'valid_from__gte' : '2011-05-20T00:46:38', 'valid_to__lte' : '2014-05-20T00:46:38',  'status': 1, 'username': 'yariv1', 'api_key': '12345678'})
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        
        
    def test_register_and_deals(self):
        '''
        test the registration through the smartphone
        also test the registerd user can't add a deal
        '''
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@gmail.com', 'password': '12345678'})
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
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'yariv1', 'api_key': '12345678'})
        self.assertTrue('category' in self.deserialize(resp)['objects'][0])
        
    def test_order_validto(self):
        '''
        test the order by -valid_to
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'yariv1', 'api_key': '12345678', 'order_by': '-valid_to'})
        objects = self.deserialize(resp)['objects']
        self.assertEqual(len(objects), 6)
        self.assertEqual(objects[0]['id'], 2)
        self.assertEqual(objects[1]['id'], 3)
        self.assertEqual(objects[2]['id'], 1)
        
    def test_deal_category(self):
        '''
        reported bug: saving the category in deal creation is not saved
        curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"username": "yariv1", "api_key": "12345678", "original_price": 5, "description": "a", "discounted_price": 2, "num_available_places": 5, "category": "/api/v1/category/1/", "valid_from": "Wed, 20 Nov 2013 12:53:00 GMT", "title": "aaa", "valid_to": "Wed, 20 Nov 2013 14:53:00 GMT", "num_total_places": 5, "status": 0, "business_profile": "/api/v1/businessprofile/1/"}' "http://localhost:8000/api/v1/deal/"
        '''
        resp = self.api_client.post(uri='/api/v1/deal/', format='json', data={
                                                                              'username': 'yariv1', 
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
                                                                              "business_profile":"/api/v1/businessprofile/1/",
                                                                              "category":"/api/v1/category/1/"
        })
        self.assertHttpCreated(resp)
#         num_deals = Deal.objects.all().count()
#         deals = Deal.objects.all()
#         new_deal = deals[num_deals - 1]
        deal_id = self.deserialize(resp)['id']
        new_deal = Deal.objects.get(id=deal_id)
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
        
#     def test_transaction(self):
#         '''
#         will check the payment transactions
#         for this test i put a user profile with a client id and payment id
#         we need to pass deal and amount
#         '''
#         resp = self.api_client.post(uri='/api/v1/transaction/?username=yariv3&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/', 'amount': 3})
#         self.assertHttpCreated(resp)
#         transaction_id = self.deserialize(resp)['id']
#         resp = self.api_client.put(uri='/api/v1/transaction/%d/?username=yariv3&api_key=12345678' % transaction_id, format='json', data={'email': 'aaa@vvv.ccc', 'first_name': 'aaa', 'last_name': 'ccc', 'phone': '+972522441431'})
#         print resp.status_code
#         self.assertHttpAccepted(resp)
#         self.assertEquals(UserProfile.objects.get(id=3).phone, '+972522441431')
#         self.assertNotEquals(UserProfile.objects.get(id=3).phone_profile.all()[0].paymill_client_id, None)
        
#     def test_unpaid_transaction(self):
#         '''
#         will check the api for the unpaid transaction
#         '''
#         resp = self.api_client.post(uri='/api/v1/unpaidtransaction/?username=yariv4&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/','phone': '+972522441432'})
#         self.assertHttpCreated(resp)
#         self.assertEquals(UserProfile.objects.get(id=4).phone, '+972522441432')
        
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
        resp = self.api_client.get(uri='/api/v1/deal/?business_profile__id=2&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
        
    def test_deal_category_filter(self):
        '''
        test the filter deal by business
        '''
        resp = self.api_client.get(uri='/api/v1/deal/?category__id=1&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        
    def test_search(self):
        '''
        test the api for the search deals
        '''
        resp = self.api_client.get(uri='/api/v1/deal/?search=promotion&username=yariv1&api_key=12345678', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        
    def test_delete_deal(self):
        '''
        should allow settings the status to zero in the deal
        '''
        resp = self.api_client.put(uri='/api/v1/deal/1/', format='json', data={'username': 'yariv1', 'api_key': '12345678', 'status': 0})
        self.assertHttpAccepted(resp)
        deal = Deal.objects.get(id=1)
        self.assertEqual(deal.status, 0)
        
    def test_confirm_deals(self):
        '''
        test the confirm deals api
        - first test will try to activate a transaction from a cradentials of another business
        - second test will try to successfully change
        '''
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv2', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12345'})
        self.assertHttpUnauthorized(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv1', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12345'})
        self.assertHttpOK(resp)
        self.assertEqual(Transaction.objects.get(id=1).status, 3)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv2', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12344'})
        self.assertHttpUnauthorized(resp)
        
        resp = self.api_client.post(uri='/api/v1/utilities/confirm-transaction/', format='json', data={'username': 'yariv1', 'api_key': '12345678', 'phone': '+972522441431', 'hash': '12344'})
        self.assertHttpOK(resp)
        self.assertEqual(UnpaidTransaction.objects.get(id=1).status, 2)
        
    def test_new_business_cant_modify_deals(self):
        '''
        test that a new registered business cant modify old deals
        reported auth bug
        '''
         
        #register a new business and set it as active
        old_num_users = User.objects.all().count()
        resp = self.api_client.post(uri='/api/v1/utilities/register/', format='json', data={'email': 'yariv3@nerdeez.com', 'business_number': '12345', 'phone': '12345', 'address': 'sdf', 'title': 'asdf'})
        self.assertHttpCreated(resp)
        self.assertEqual(User.objects.all().count(), old_num_users + 1)
        users = User.objects.all()
        for single_user in users:
            if single_user.id == 5:
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
        resp = self.api_client.get(uri='/api/v1/phoneprofile/1/?username=yariv1&api_key=12345678', format='json')
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.put(uri='/api/v1/phoneprofile/1/?username=yariv1&api_key=12345678', format='json', data={'paymill_payment_id': '12345678'})
        self.assertHttpUnauthorized(resp)
        self.assertNotEqual(PhoneProfile.objects.get(id=1).paymill_payment_id, '12345678')
        
    def test_deal_contain_business(self):
        '''
        test that the deal api returns a business object
        '''
        resp = self.api_client.get(uri='/api/v1/deal/', format='json', data={'username': 'yariv1', 'api_key': '12345678'})
        business = self.deserialize(resp)['objects'][0]['business_profile']
        self.assertTrue('id' in business)
        
    def test_transaction_filtering(self):
        resp = self.api_client.get(uri='/api/v1/transaction/?deal__business_profile__id=1&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        resp = self.api_client.get(uri='/api/v1/transaction/?status=1&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        resp = self.api_client.get(uri='/api/v1/transaction/?creation_date__gte=1988-12-4T00:00:00&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        resp = self.api_client.get(uri='/api/v1/transaction/?order_by=creation_date&username=yariv1&api_key=12345678', format='json', data={})
        self.assertHttpOK(resp)
        
    def test_user_details_in_phoneprofile(self):
        '''
        test that the phone profile and business profile returns the first name last name and email
        '''
        
        resp = self.api_client.get(uri='/api/v1/phoneprofile/1/?username=yariv3&api_key=12345678', format='json')
        phone_profile = self.deserialize(resp)
        resp = self.api_client.get(uri='/api/v1/businessprofile/1/?username=yariv1&api_key=12345678', format='json')
        business_profile = self.deserialize(resp)
        self.assertTrue('first_name' in phone_profile['user_profile'])
        self.assertTrue('first_name' in business_profile['user_profile'])
        self.assertTrue('last_name' in phone_profile['user_profile'])
        self.assertTrue('last_name' in business_profile['user_profile'])
        self.assertTrue('email' in phone_profile['user_profile'])
        self.assertTrue('email' in business_profile['user_profile'])
        
    def test_seat_reservation(self):
        '''
        test that if 10 minutes passed after reservation our async process will delete that transaction
        '''
        #create a transaction
        resp = self.api_client.post(uri='/api/v1/transaction/?username=yariv3&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/', 'amount': 3})
        self.assertHttpCreated(resp)
        transaction_id = self.deserialize(resp)['id']
        self.assertEqual(Transaction.objects.get(id=transaction_id).status, 1)
        
        #make sure that deal1 availabel seats are lowered
        resp = self.api_client.get(uri='/api/v1/deal/1/?username=yariv4&api_key=12345678', format='json')
        self.assertEqual(self.deserialize(resp)['num_places_left'], 6)
        
        #modify the creation date to be 10 minutes before
        now = datetime.datetime.now()
        ten_before = now + relativedelta(minutes=-11)
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.creation_date = ten_before
        transaction.save()
        
        #make sure the async process closes the transaction
        close_unactive_reservation()
        resp = self.api_client.get(uri='/api/v1/deal/1/?username=yariv4&api_key=12345678', format='json')
        self.assertEqual(self.deserialize(resp)['num_places_left'], 9)
        self.assertEqual(Transaction.objects.get(id=transaction_id).status, 0)
        
    
#     def test_report(self):
#         '''
#         test 3 scenarios :
#         1. test that we get back mime of type pdf when requesting a report
#         2. test we get unAuthorized if request a report and we're not authorized (phone profile)
#         2. test we get unAuthorized if request a report and we're not authenticated 
#         '''
#         #request report when wer'e authorized and authenticated (business profile)
#         resp = self.api_client.get(uri='/report/transaction/?username=yariv1&api_key=12345678', format='json')
#         self.assertHttpOK(resp)
#         self.assertEqual(resp['content-type'], 'application/pdf')
#         
#         #request report when wer'e authenticated but not authorized (phone profile)
#         resp = self.api_client.get(uri='/report/transaction/?username=yariv3&api_key=12345678', format='json')
#         self.assertHttpUnauthorized(resp)
#         
#         #request report when wer'e not authorized and not authenticated
#         resp = self.api_client.get(uri='/report/transaction/?username=Fake&api_key=Fake', format='json')
#         self.assertHttpUnauthorized(resp)
        
        
        
        
#     def test_update_push_tokens(self):
#         '''
#         - test that we can put the user token
#         - test that we cant change others token 
#         '''
#         resp = self.api_client.put(uri='/api/v1/phoneprofile/1/', format='json', data={'username': 'yariv3', 'api_key': '12345678', 'apn_token': 'yariv'})
#         self.assertHttpAccepted(resp)
#         self.assertEqual(PhoneProfile.objects.get(id=1).apn_token, 'yariv')
#         resp = self.api_client.put(uri='/api/v1/phoneprofile/2/', format='json', data={'username': 'yariv3', 'api_key': '12345678', 'apn_token': 'yariv'})
#         self.assertHttpUnauthorized(resp)
#         self.assertNotEquals(PhoneProfile.objects.get(id=2).apn_token, 'yariv')
        
#     def test_push_notification_task(self):
#         '''
#         test the push notification async task
#         '''
#         send_push_notification()
        
    def test_phoneprofile_ispayed(self):
        '''
        will test that the phone profile returns an is_payed and also that the paymill cradentials are hidden
        '''
        
        resp = self.api_client.get(uri='/api/v1/phoneprofile/1/?username=yariv3&api_key=12345678', format='json')
        print resp.content
        phone_profile = self.deserialize(resp)
        self.assertFalse('paymill_client_id' in phone_profile or 'paymill_payment_id' in phone_profile)
        self.assertTrue(phone_profile['is_payed'])
        
        
        
    def test_transaction_create_search_index_updated(self):
        '''
        test that the transaction search_index field gets updated
        when transaction is created
        '''
        #create a transaction
        resp = self.api_client.post(uri='/api/v1/transaction/?username=yariv3&api_key=12345678', format='json', data={'deal': '/api/v1/deal/1/', 'amount': 1})
        self.assertHttpCreated(resp)  
              
        
        def searchTransactionInResults(queryArg,transactionId):
            '''
            will test if a transaction is in the results
            of the query.
            @param {string} queryArg - a query argument
            @param {int} transactionId - the transaction id
            @return {boolean} - true if transaction found, false if not
            '''
            
            query = connection.ops.quote_name(queryArg)
            searchResults = Transaction.objects.search(query)
            isTransactionFound = False
            for result in searchResults:
                if (result.id == transactionId):
                    isTransactionFound = True
                    break
            
            return isTransactionFound
            
        #get the transaction id we want to check
        transaction_id = self.deserialize(resp)['id']
            
        #check if transaction is found by deal title
        isTransactionFound = searchTransactionInResults(Deal.objects.get(id=1).title,transaction_id)
        self.assertTrue(isTransactionFound)
        
        #check if transaction is found by deal description
        isTransactionFound = searchTransactionInResults(Deal.objects.get(id=1).description,transaction_id)
        self.assertTrue(isTransactionFound)
        
        #check if transaction is found by user email
        isTransactionFound = searchTransactionInResults(User.objects.get(id=3).email,transaction_id)
        self.assertTrue(isTransactionFound)
        
        #check if transaction is found by user last name
        isTransactionFound = searchTransactionInResults(User.objects.get(id=3).last_name,transaction_id)
        self.assertTrue(isTransactionFound)
        
        #check if transaction is found by user first name
        isTransactionFound = searchTransactionInResults(User.objects.get(id=3).first_name,transaction_id)
        self.assertTrue(isTransactionFound)
        
    def test_deal_update_search_index_updated(self):
        '''
        will check the transaction search_index is updated
        after a deal is updated
        '''
        
        #get number of transactions associated to this deal
        transactionsRelatedToDeal = Transaction.objects.filter(deal__id=1).count()

        #assert no transactions can be found by the deal title, since the search_index is null
        query = connection.ops.quote_name(Deal.objects.get(id=1).title)
        searchResults = Transaction.objects.search(query)
        self.assertFalse(searchResults.exists())
        
        #update the deal
        resp = self.api_client.put(uri='/api/v1/deal/1/?username=yariv1&api_key=12345678', format='json', data={'title': 'Great'})
        self.assertHttpAccepted(resp)
        
        #assert number of transactions can be found by query, and is equal to the transactionsRelatedToDeal
        query = connection.ops.quote_name(Deal.objects.get(id=1).title)
        searchResults = Transaction.objects.search(query)
        self.assertTrue(searchResults.count() == transactionsRelatedToDeal)
        
    def test_user_update_search_index_updated(self):
        '''
        will check the transaction search_index is updated
        after a user email is updated
        '''
        #get number of transactions associated to this user
        userProfile = UserProfile.objects.get(user__id = 3)
        phoneProfile = PhoneProfile.objects.get(user_profile__id = userProfile.id)      
        transactionsRelatedToUser = Transaction.objects.filter(phone_profile__id=phoneProfile.id).count()

        #assert no transactions can be found by the user email
        query = connection.ops.quote_name(User.objects.get(id=3).email)
        searchResults = Transaction.objects.search(query)
        self.assertFalse(searchResults.exists())
        
        #update the user email
        userToUpdate = User.objects.get(id=3)
        userToUpdate.email = "test@test.test"
        userToUpdate.save()
        
        #assert number of transactions can be found by query, and is equal to the transactionsRelatedToUser
        query = connection.ops.quote_name(User.objects.get(id=3).email)
        searchResults = Transaction.objects.search(query)
        self.assertTrue(searchResults.count() == transactionsRelatedToUser)
        
    def test_category_auth(self):
        '''
        test unauth user can view the categories
        '''
        
        resp = self.api_client.get(uri='/api/v1/category/', format='json')
        self.assertHttpOK(resp)
        
    def test_registration(self):
        '''
        test that the api for registration works
        test success
        test email duplication erro
        test uuid duplication error
        test registration with token created a push notification object
        test if i register with a token that exists it will create a connection with the new object
        '''
        
        num_users = User.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@gmail.com', 'password': '12345678'})
        self.assertHttpCreated(resp)
        self.assertEqual(num_users + 1, User.objects.count())
        self.assertTrue('api_key' in self.deserialize(resp))
        self.assertTrue('username' in self.deserialize(resp))
        self.assertTrue('phone_profile' in self.deserialize(resp))
        
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@gmail.com', 'password': '12345678'})
        self.assertHttpConflict(resp)
        self.assertEqual(num_users + 1, User.objects.count())
        
    def test_deal_dates_timezone(self):
        '''
        test that the dates returned from the post response when a deal is created
        has the same timezone as dates returned from a get request to the same deal
        '''

        #post a new deal
        resp = self.api_client.post(uri='/api/v1/deal/', format='json', data={
                                                                              'username': 'yariv1', 
                                                                              'api_key': '12345678', 
                                                                              "title":"M&M",
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
                                                                              "business_profile":"/api/v1/businessprofile/1/",
                                                                              "category":"/api/v1/category/1/"
        })
        
        #get the valid_from from the post response
        post_resp_valid_from = self.deserialize(resp)['valid_from']
        post_resp_id = self.deserialize(resp)['id']
        
        #get the deal we've just posted
        resp = self.api_client.get(uri='/api/v1/deal/?username=yariv4&api_key=12345678&id=' + str(post_resp_id) ,format='json')
    
        #get valid_from from the get response
        objects = self.deserialize(resp)['objects'][0]
        get_resp_valid_from =  objects['valid_from']
        
        #check the post valid_From and get valid_from are equal
        print post_resp_valid_from
        print get_resp_valid_from
        print Deal.objects.get(id=post_resp_id).valid_from;
        self.assertEqual(post_resp_valid_from,get_resp_valid_from)

        
    def test_icon_name(self):
        '''
        test that i have icon_name in category
        '''
        resp = self.api_client.get(uri='/api/v1/category/1/', format='json')
        self.assertTrue('icon_name' in self.deserialize(resp))
        
    def test_register_and_login(self):
        '''
        test the registration and login of a phone profile
        '''
        
        #register a user
        data = {
                'first_name': 'yariv',
                'last_name': 'katz',
                'email': 'test@nerdeez.com',
                'password': '12345',
                'phone': '12345'
                }
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data=data)
        self.assertHttpCreated(resp)
        
        #login the user
        data = {
                'email': 'test@nerdeez.com',
                'password': '12345'
                }
        resp = self.api_client.post(uri='/api/v1/utilities/login-user/', format='json', data=data)
        print resp.status_code
        print resp.content
        self.assertHttpAccepted(resp)
        self.assertTrue('phone_profile' in self.deserialize(resp))
        
        data = {
                'email': 'testsfasdf@nerdeez.com',
                'password': '12345'
                }
        resp = self.api_client.post(uri='/api/v1/utilities/login-user/', format='json', data=data)
        self.assertHttpUnauthorized(resp)
        
    def test_register_bug_save_phone(self):
        '''
        there was a bug in the registration with saving the users phone
        '''
        
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@test.test', 'phone': '111111'})
        self.assertHttpCreated(resp)
        phone_profile = PhoneProfile.objects.get(id=self.deserialize(resp)['phone_profile']['id'])
        self.assertEqual(phone_profile.user_profile.phone, '111111')
        
    def test_no_multiple_anonymous(self):
        '''
        bug fix: 2 anonymous users with same details are saved multiple times
        '''
        
        old_phone_count = PhoneProfile.objects.count()
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@test.test', 'phone': '111111'})
        self.assertHttpCreated(resp)
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@test.test', 'phone': '111111'})
        self.assertHttpCreated(resp)
        self.assertEqual(UserProfile.objects.filter(phone='111111').count(), 1)
        self.assertEqual(PhoneProfile.objects.count(), old_phone_count + 1)
        resp = self.api_client.post(uri='/api/v1/utilities/register-user/', format='json', data={'first_name': 'yariv', 'last_name': 'katz', 'email': 'test@test.test', 'phone': '111111', 'password': '12345'})
        self.assertHttpCreated(resp)
        self.assertEqual(UserProfile.objects.filter(phone='111111').count(), 2)
        self.assertEqual(PhoneProfile.objects.count(), old_phone_count + 2)
        
#     def test_register_facebook(self):
#         '''
#         test the facebook registration api
#         - test creation of new user
#         - test taking old user cradentils
#         '''
#         
#         data = {
#                 'uuid': '12345', 
#                 'first_name': 'yariv', 
#                 'last_name': 'katz', 
#                 'email': 'test@nerdeez.com', 
#                 'facebook_user_id': '12345', 
#                 'facebook_access_token': '12345', 
#                 'password': '12345'
#                 }
#         resp = self.api_client.post(uri='/api/v1/utilities/register-facebook/', format='json', data=data)
#         self.assertHttpCreated(resp)
#         self.assertTrue('api_key' in self.deserialize(resp))
#         
#         data = {
#                 'facebook_user_id': '12345', 
#                 'facebook_access_token': '12345', 
#                 }
#         resp = self.api_client.post(uri='/api/v1/utilities/register-facebook/', format='json', data=data)
#         self.assertHttpAccepted(resp)
#         self.assertTrue('api_key' in self.deserialize(resp))
        
        
        
        
        
        
    
        
#     def test_refund(self):
#         '''
#         will check the the api for the refund is working
#         '''
#         #test refund is working
#         resp = self.api_client.post(uri='/api/v1/refund/?username=yariv1&api_key=12345678', format='json', data={'transaction': '/api/v1/transaction/1/', 'description': 'Trying to work my way on a refund'})
#         self.assertHttpCreated(resp)
#         self.assertEqual(Refund.objects.all().count(), 1)
#         self.assertNotEqual(Refund.objects.all()[0].paymill_refund_id, None)
        
        
# 
# {
#         "pk": 2, 
#         "model": "ticketz_backend_app.business", 
#         "fields": {
#             "city": null, 
#             "web_service_url": "", 
#             "modified_data": "2013-11-12T17:04:34.478Z", 
#             "title": "Nerdeez", 
#             "adapter_object": "gAJVAC4=", 
#             "business_number": "0368565401", 
#             "creation_date": "2013-11-10T13:35:09Z", 
#             "phone": "0522441431", 
#             "address": "52 no life lane", 
#             "adapter_class": ""
#         }
#     },   
        
    
#===============================================================================
# end testing
#===============================================================================
