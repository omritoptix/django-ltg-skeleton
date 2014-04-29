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
from ltg_backend_app.models import Section, QuestionSetAttempt, SectionScore

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin section test
#===============================================================================

class SectionTest(ResourceTestCase):
    
    def setUp(self):
        '''
        create section and section score
        '''
        section = Section.objects.create(title="Section1")
        question_set_attempt = QuestionSetAttempt.objects.create()
        SectionScore.objects.create(section=section , score=400, question_set_attempt=question_set_attempt)                             
        return super(SectionTest,self).setUp()
    
    def test_get_sections(self):
        '''
        will test the section api resource.
        1. get a single section and make sure statistics for this section are returned
        2. get a list of sections and make sure statistics for a section is returned 
        '''
        # get a single section
        resp = self.api_client.get(uri='/api/v1/section/2/', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['statistics']['mean'],400)
        self.assertEqual(self.deserialize(resp)['statistics']['std'],0)
        
        # get sections list
        resp = self.api_client.get(uri='/api/v1/section/', format='json')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['objects'][0]['statistics']['mean'],400)
        
    def test_post_section(self):
        '''
        test that a POST request to a section is not allowed
        '''
        resp = self.api_client.post(uri='/api/v1/section/',data={'title':'hey'})
        self.assertHttpMethodNotAllowed(resp)
        
#===============================================================================
# end section test
#===============================================================================