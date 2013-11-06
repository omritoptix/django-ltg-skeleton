'''
For my TDD, bitch
Created on Jun 29, 2013

@author: ywarezk
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from nerdeez_server_app.models import Enroll

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
    fixtures = ['nerdeez_server_app']
    
    def test_school_group_search(self):
        '''
        run a search query in the school group
        1 - make sure search query technion in uni yields one result
        1.1 - make sure bullshit search returns null
        2 - make sure search query technion in faculty yields 2 result
        3 - make sure search query technion in course yields 2 result
        '''
        
        resp = self.api_client.get('/api/v1/schoolgroup/', format='json', data={'search': 'technion'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 4)
        
        resp = self.api_client.get('/api/v1/schoolgroup/', format='json', data={'search': 'sdghskod'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 0)
        
        resp = self.api_client.get('/api/v1/schoolgroup/', format='json', data={'search': 'matam'})
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], 1)
        
    def test_flatpage(self):
        '''
        make sure get command works on flatpage url
        '''
        resp = self.api_client.get('/api/v1/flatpage/', format='json', data={})
        self.assertHttpOK(resp)
        
    def test_contactus(self):
        '''
        test send mail
        '''
        resp = self.api_client.post('/api/v1/utilities/contact/', format='json', data={'mail': 'mail', 'message': 'testmessage'})
        self.assertHttpAccepted(resp)
        
    def test_register(self):
        '''
        test the registration
        '''
        resp = self.api_client.post('/api/v1/utilities/register/', format='json', data={'email': 'yariv@nerdeez2.com', 'password': '12345'})
        self.assertHttpCreated(resp)
        
        resp = self.api_client.post('/api/v1/utilities/login/', format='json', data={'email': 'yariv@nerdeez2.com', 'password': '12345'})
        self.assertHttpAccepted(resp)
        
    def test_userprofile_schoolgroups(self):
        '''
        check the user returns school groups as array
        '''
        resp = self.api_client.get('/api/v1/userprofile/1/?username=1234&api_key=12345678', format='json', data={})
        obj = self.deserialize(resp)
        self.assertEqual(len(obj['enrolls']), 2)
        
    def test_enroll(self):
        '''
        check the enroll api
        '''
        
        #test auth
        resp = self.api_client.post(uri='/api/v1/enroll/', format='json', data={'user': '/api/v1/userprofile/3/', 'school_group': '/api/v1/schoolgroup/1/'})
        self.assertHttpUnauthorized(resp)
        
        #
        resp = self.api_client.post(uri='/api/v1/enroll/?username=1234&api_key=12345678', format='json', data={'user': '/api/v1/userprofile/3/', 'school_group': '/api/v1/schoolgroup/1/'})
        self.assertHttpCreated(resp)
        self.assertEqual(Enroll.objects.count(), 2)
        resp = self.api_client.post(uri='/api/v1/enroll/?username=1234&api_key=12345678', format='json', data={'user': '/api/v1/userprofile/3/', 'school_group': '/api/v1/schoolgroup/1/'})
        self.assertHttpCreated(resp)
        self.assertEqual(Enroll.objects.count(), 2)
        
    def test_auth(self):
        '''
        test my auth
        '''
        
        #check that i can get the school group but i cant post
        resp = self.api_client.get(uri='/api/v1/schoolgroup/', format='json', data={})
        self.assertHttpOK(resp)
        resp = self.api_client.post(uri='/api/v1/schoolgroup/', format='json', data={'title': '1', 'description': '2'})
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.post(uri='/api/v1/schoolgroup/?username=1234&api_key=12345678', format='json', data={'title': '1', 'description': '2'})
        self.assertHttpCreated(resp)
        
        #i can only read my own profile
        resp = self.api_client.get(uri='/api/v1/userprofile/', format='json', data={})
        self.assertHttpUnauthorized(resp)
        resp = self.api_client.get(uri='/api/v1/userprofile/?username=1234&api_key=12345678', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.get(uri='/api/v1/userprofile/1/?username=1234&api_key=12345678', format='json')
        self.assertHttpOK(resp)
        resp = self.api_client.get(uri='/api/v1/userprofile/2/?username=1234&api_key=12345678', format='json')
        self.assertHttpUnauthorized(resp)
        
    def test_like_dislike(self):
        '''
        test that the like and dislike works
        '''
        resp = self.api_client.put(uri='/api/v1/schoolgroup/1/?username=1234&api_key=12345678', format='json', data={'like': 3000})
        self.assertHttpAccepted(resp)
        self.assertEqual(self.deserialize(resp)['like'], 1)

            
        
        
        

#===============================================================================
# end testing
#===============================================================================