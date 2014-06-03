'''
will hold our "flashcard turned" tests
Created on June 3, 2014
 
@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''
 
#===============================================================================
# begin imports
#===============================================================================
 
from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Question, Attempt, Flashcard, FlashcardTurned
from django.contrib.auth.models import User
from tastypie.models import ApiKey
from django.contrib.auth import get_user_model
 
#===============================================================================
# end imports
#===============================================================================
 
#===============================================================================
# begin flashcard turned test
#===============================================================================
 
class FlashcardTurnedTest(ResourceTestCase):
     
    fixtures = ['users_auth','initial_data','flashcards']
     
    def test_create_flashcard_turned(self):
        '''
        will test various flashcard_turned resource scenarios
        1. post for "user" resource matching authorization header, and "flashcard" uri referenced by index - success
        2. bulk create (using 'patch') success
        3. bulk create (using 'patch') for user not matching authorization header - unauthorized  
        4. post without credentails failes
        5. post for other user fails with unauthorized 
        '''
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email='yariv@nerdeez.com')
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
         
        # post for "user" resource matching authorization header, and "flashcard" uri referenced by index 
        flashcard = Flashcard.objects.first()
        flashcard_index = flashcard.index
        flashcard_uri = '/api/v1/flashcard/%d/' % flashcard_index
        user_uri = '/api/v1/user/%d/' % user.id
        # post a new attempt
        resp = self.api_client.post(uri='/api/v1/flashcardturned/', format='json', data={'user':user_uri,'flashcard':flashcard_uri},authentication = authentication_header)
        self.assertHttpCreated(resp)
        # check new attempt was created with correct values
        flashcard_turned = FlashcardTurned.objects.latest('creation_date')
        self.assertEqual(flashcard_turned.flashcard_id,flashcard.id)
        self.assertEqual(flashcard_turned.user_id,user.id)
        # delete the record that was just created in order to avoid 'unique' constraint in the next scripts
        FlashcardTurned.objects.latest('creation_date').delete()
         
        # bulk create (using 'patch')
        num_flashcard_turned =  FlashcardTurned.objects.all().count()
        flashcard2 = Flashcard.objects.last()
        flashcard2_index = flashcard2.index
        flashcard2_uri = '/api/v1/flashcard/%d/' % flashcard2_index
        resp = self.api_client.patch(uri='/api/v1/flashcardturned/', format='json', data={'objects':[{'flashcard':flashcard_uri,'user':user_uri},{'flashcard':flashcard2_uri,'user':user_uri}]},authentication = authentication_header)
        self.assertHttpAccepted(resp)
        # make sure the objects were really created since patch return accepted (not created) on bulk operations
        self.assertEqual(num_flashcard_turned + 2, FlashcardTurned.objects.all().count())
         
        # bulk create (using 'patch') for user not matching authorization header - unauthorized
        user2 = User.objects.get(email='omri@ltgexam.com')
        authentication_header2 = 'ApiKey '+user2.email+':'+user2.api_key.key
        resp = self.api_client.patch(uri='/api/v1/flashcardturned/', format='json', data={'objects':[{'flashcard':flashcard_uri,'user':user_uri},{'flashcard':flashcard2_uri,'user':user_uri}]},authentication = authentication_header2)
        self.assertHttpUnauthorized(resp)
         
        # post without credentails failes
        resp = self.api_client.post(uri='/api/v1/flashcardturned/', format='json', data={'user':user_uri,'flashcard':flashcard_uri})
        self.assertHttpUnauthorized(resp)
        
        # post for other user fails with unauthorized
        resp = self.api_client.post(uri='/api/v1/flashcardturned/', format='json', data={'user':user_uri,'flashcard':flashcard_uri},authentication = authentication_header2)
        self.assertHttpUnauthorized(resp)
        
    def test_get_flashcard_turned(self):
        """
        will test different scenarios of flashcard_turned api get method
        1. GET filtered by 'user' matching authorization header - success 
        2. GET filtered by 'user' not matching authorization header return empty list
        3. GET for flashcard_returned detail endpoint with none matching authorization header - unauthorized
        """
        # set authentication header
        User = get_user_model()
        user = User.objects.get(email='yariv@nerdeez.com')
        authentication_header = 'ApiKey '+user.email+':'+user.api_key.key
        
        # create flashcard_turned record for the user
        flashcard_turned = FlashcardTurned.objects.create(user=user,flashcard=Flashcard.objects.first())
        
        # GET filtered by 'user' matching authorization header
        resp = self.api_client.get(uri='/api/v1/flashcardturned/?user=%d' % user.id, format='json',authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertNotEqual(self.deserialize(resp)['objects'], [])
        
        # GET filtered by 'user' not matching authorization header return empty list
        user2 = User.objects.get(email='omri@ltgexam.com')
        resp = self.api_client.get(uri='/api/v1/flashcardturned/?user=%d' % user2.id, format='json',authentication = authentication_header)
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'], [])
        
        # GET for flashcard_returned detail endpoint with none matching authorization header
        authentication_header2 = 'ApiKey '+user2.email+':'+user2.api_key.key
        resp = self.api_client.get(uri='/api/v1/flashcardturned/%d/' % flashcard_turned.id, format='json',authentication = authentication_header2)
        self.assertHttpUnauthorized(resp)
        
        
        
        

         
#===============================================================================
# end flashcard turned test
#===============================================================================