'''
will hold our section tests
Created on April 28, 2014
 
@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''
 
#===============================================================================
# begin imports
#===============================================================================
 
from tastypie.test import ResourceTestCase
from ltg_backend_app.models import Section, UserSectionScore
from django.contrib.auth.models import User
from tastypie.models import ApiKey
import datetime
from django.contrib.auth import get_user_model
 
#===============================================================================
# end imports
#===============================================================================
 
#===============================================================================
# begin section test
#===============================================================================
 
class SectionTest(ResourceTestCase):
     
    fixtures = ['users_auth']
     
    def setUp(self):
        '''
        create section and section score and user
        '''
        # create section and section score
        User = get_user_model()
        section = Section.objects.create(title="Section1")
        UserSectionScore.objects.create(user = User.objects.first(), section = section, score = 400, date = datetime.datetime.now())                         
        return super(SectionTest,self).setUp()
     
    def test_get_sections(self):
        '''
        will test the section api resource.
        1. get a single section and make sure statistics for this section are returned
        2. get a list of sections and make sure statistics for a section is returned 
        '''
        # get a user to authenticate with
        User = get_user_model()
        user = User.objects.first()
        auth_data = {'username':user.email, 'api_key':user.api_key.key}
        # get a single section
        section_id = Section.objects.last().id
        resp = self.api_client.get(uri='/api/v1/section/%d/' % section_id, format='json', data = auth_data)
        self.assertHttpOK(resp)
         
        # get sections list
        resp = self.api_client.get(uri='/api/v1/section/', format='json', data = auth_data)
        self.assertHttpOK(resp)
         
    def test_post_section(self):
        '''
        test that a POST request to a section is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/section/',data={'title':'hey'})
        self.assertHttpMethodNotAllowed(resp)
         
#===============================================================================
# end section test
#===============================================================================