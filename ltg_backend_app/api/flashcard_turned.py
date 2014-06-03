'''
will hold our flashcard turned resource
Created on June 3, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import FlashcardTurned
from tastypie.authentication import ApiKeyAuthentication
from django.conf.urls import url
from tastypie.bundle import Bundle
from ltg_backend_app.api.authorization import UserObjectsOnlyAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from ltg_backend_app.api.flashcard import FlashcardResource
from ltg_backend_app.api.user import UserResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin flashcard turned resource
#===============================================================================

class FlashcardTurnedResource(LtgResource):
    """
    resource for the flashcard turned model
    """
    flashcard = fields.ToOneField(FlashcardResource,attribute='flashcard')
    user = fields.ToOneField(UserResource,attribute='user')
    
    class Meta(LtgResource.Meta):
        queryset = FlashcardTurned.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        allowed_methods = ['post','get','patch']
        detail_allowed_methods = ['get','put','patch']
        filtering = {
            'user' : ALL_WITH_RELATIONS,
            'flashcard' : ALL_WITH_RELATIONS,
        }
    
#===============================================================================
# end flashcard turned resource
#===============================================================================