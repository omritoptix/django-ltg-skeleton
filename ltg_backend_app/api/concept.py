'''
will hold our section resource
Created on April 27, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from tastypie import fields
from ltg_backend_app.models import Concept
from tastypie.authorization import Authorization
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin concept resource
#===============================================================================

class ConceptResource(LtgResource):
    '''
    resource for the concept model
    '''
    statistics = fields.DictField(attribute='statistics')
    
    class Meta(LtgResource.Meta):
        queryset = Concept.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
    
#===============================================================================
# end concept resource
#===============================================================================