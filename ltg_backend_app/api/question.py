'''
will hold our question resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import Question
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from ltg_backend_app.api.concept import ConceptResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin question resource
#===============================================================================

class QuestionResource(LtgResource):
    '''
    resource for the question model
    '''
    concepts = fields.ManyToManyField(ConceptResource,attribute='concepts')
    sections = fields.ManyToManyField(ConceptResource,attribute='concepts')
    
    class Meta(LtgResource.Meta):
        queryset = Question.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'concepts' : ALL_WITH_RELATIONS,
               'sections' : ALL_WITH_RELATIONS,
               'index' : ALL,
           }
        ordering = ['index',]
        
    def dehydrate_answer(self, bundle):
        return bundle.obj.get_answer_display()
    
#===============================================================================
# end question resource
#===============================================================================