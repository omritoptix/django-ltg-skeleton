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
from ltg_backend_app.models import Section
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.authentication import ApiKeyAuthentication

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
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'title' : ALL,
           }
    
#===============================================================================
# end section resource
#===============================================================================