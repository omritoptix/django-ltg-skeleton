'''
will hold our section resource
Created on April 24, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import Section
from tastypie.authorization import Authorization
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.constants import ALL

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin section resource
#===============================================================================

class SectionResource(LtgResource):
    '''
    resource for the Section model
    '''
    
    class Meta(LtgResource.Meta):
        queryset = Section.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'title' : ALL,
           }
    
#===============================================================================
# end section resource
#===============================================================================