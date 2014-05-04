'''
will hold our question set attempt tests
Created on April 28, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.test import ResourceTestCase
from ltg_backend_app.models import QuestionSetAttempt, SectionScore,\
    ConceptScore, Concept, Section, UserProfile


#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question set attempt test
#===============================================================================

class QuestionSetAttemptTest(ResourceTestCase):
    
    fixtures = ['users_auth']
    
    def setUp(self):
        '''
        create concept, section
        '''
        Concept.objects.bulk_create([Concept(title="Concept1"),Concept(title="Concept2")])
        Section.objects.bulk_create([Section(title="Section1"),Section(title="Section2")])
        return super(QuestionSetAttemptTest,self).setUp()
    
    def test_post_question_set_attempt(self):
        '''
        will test a POST to question set attempt with section and concepts score data
        '''
        # get the concept and section id
        concept_id_1 = Concept.objects.get(title='Concept1').id
        concept_id_2 = Concept.objects.get(title='Concept2').id
        section_id_1 = Section.objects.get(title='Section1').id
        section_id_2 = Section.objects.get(title='Section2').id
        # get the user profile for the QSA
        user_profile = UserProfile.objects.first()
        user_profile_uri= '/api/v1/userprofile/' + str(user_profile.id) + '/'
        # make the post request
        resp = self.api_client.post(uri='/api/v1/questionsetattempt/', format='json',data = {'user_profile':user_profile_uri, 'concepts':[{'id':concept_id_1,'score':550},{'id':concept_id_2,'score':560}], 'sections':[{'id':section_id_1,'score':450},{'id':section_id_2,'score':470}]})
        self.assertHttpCreated(resp)
        # assert score for each concept and section was created
        self.assertTrue(ConceptScore.objects.filter(concept_id = concept_id_1, score = 550).exists())
        self.assertTrue(ConceptScore.objects.filter(concept_id = concept_id_2, score = 560).exists())
        self.assertTrue(SectionScore.objects.filter(section_id = section_id_1, score = 450).exists())
        self.assertTrue(SectionScore.objects.filter(section_id = section_id_2, score = 470).exists())
        
        
#===============================================================================
# end question set attempt test
#===============================================================================