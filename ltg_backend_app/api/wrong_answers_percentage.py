'''
will hold our wrong answers percentage resource
Created on May 13, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import WrongAnswersPercentage
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from tastypie.authorization import Authorization

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin wrong answers percentage resource
#===============================================================================

class WrongAnswersPercentageResource(LtgResource):
    '''
    resource for the wrong answers percentage  model
    '''
    class Meta(LtgResource.Meta):
        queryset = WrongAnswersPercentage.objects.all()
        authentication = LtgApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = []
        
    
#===============================================================================
# end wrong answers percentage resource
#===============================================================================