'''
will hold our section statistics resource
Created on May 13, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import SectionStatistics
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from ltg_backend_app.api.section import SectionResource
from tastypie.authentication import ApiKeyAuthentication

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin section statistics resource
#===============================================================================

class SectionStatisticsResource(LtgResource):
    '''
    resource for the section model
    '''
    section = fields.ToOneField(SectionResource, attribute = 'section', full=True)
    
    class Meta(LtgResource.Meta):
        queryset = SectionStatistics.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'section' : ALL_WITH_RELATIONS,
           }
    
#===============================================================================
# end section statistics resource
#===============================================================================