'''
will hold our question set resource
Created on April 24, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import QuestionSetAttempt, SectionScore,\
    ConceptScore
from tastypie.authentication import Authentication
from ltg_backend_app.ltg_api.section import SectionResource
from tastypie.authorization import Authorization
from ltg_backend_app.ltg_api.concept import ConceptResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question resource
#===============================================================================

class QuestionSetAttemptResource(LtgResource):
    '''
    resource for the question model
    '''
    sections = fields.ManyToManyField(SectionResource,attribute='sections',null=True)
    concepts = fields.ManyToManyField(ConceptResource,attribute='concepts',null=True)
    
    class Meta(LtgResource.Meta):
        queryset = QuestionSetAttempt.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ['get','post']
        
    def save_m2m(self,bundle):
        '''
        since we're using 'through' relationship, need to override m2m, since 
        our model can't 'add' objects via it's related manager (only the 'through' model)
        '''
        # save sections score
        try:
            sections = bundle.data['sections']
            for section in sections:
                # create the section score object
                try:
                    if (section.data['id'] and section.data['score']):
                        SectionScore.objects.create(question_set_attempt_id = bundle.obj.id, section_id = section.data['id'], score = section.data['score'])
                except:
                    # TODO - log the exception
                    pass
        except:
            pass
        # save concepts score
        try:
            concepts = bundle.data['concepts']
            for concept in concepts:
                # create the concept score object     
                try:
                    if (concept.data['id'] and concept.data['score']):
                        ConceptScore.objects.create(question_set_attempt_id = bundle.obj.id, concept_id = concept.data['id'], score = concept.data['score'])
                except:
                    # TODO - log the exception
                    pass
        except:
            pass
    
#===============================================================================
# end question resource
#===============================================================================