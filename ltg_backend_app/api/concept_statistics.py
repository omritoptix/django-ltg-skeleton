'''
will hold our concept statistics resource
Created on May 13, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import SectionStatistics, ConceptStatistics
from tastypie.authorization import Authorization
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from ltg_backend_app.api.section import SectionResource
from ltg_backend_app.api.concept import ConceptResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin concept statistics resource
#===============================================================================

class ConceptStatisticsResource(LtgResource):
    '''
    resource for the concept model
    '''
    concept = fields.ToOneField(ConceptResource, attribute = 'concept', full=True)
    
    class Meta(LtgResource.Meta):
        queryset = ConceptStatistics.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'concept' : ALL_WITH_RELATIONS,
           }
    
#===============================================================================
# end concept statistics resource
#===============================================================================