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
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation

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
    statistics = fields.DictField(attribute='statistics')
    
    class Meta(LtgResource.Meta):
        queryset = Section.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ['get']
    
#===============================================================================
# end section resource
#===============================================================================