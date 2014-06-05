'''
will hold our flashcard resource
Created on June 2, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.api.base import LtgResource
from ltg_backend_app.models import Flashcard
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.conf.urls import url
from tastypie.bundle import Bundle
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie import fields
from ltg_backend_app.api.section import SectionResource

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin flashcard resource
#===============================================================================

class FlashcardResource(LtgResource):
    '''
    resource for the flashcard model
    '''
    section = fields.ToOneField(SectionResource,attribute='section')
    
    class Meta(LtgResource.Meta):
        queryset = Flashcard.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = []
        filtering = {
            'section' : ALL_WITH_RELATIONS,
            'lesson' : ALL,
        }
        
    def override_urls(self):
        # will get object by index and not by id
        # i.e /api/v1/flashcard/<index>/ 
        return [
            url(r"^(?P<resource_name>%s)/(?P<index>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.

        By default, it uses the model's ``pk`` in order to create the URI - 
        here it's changed to use the 'index' field to generate the uri.
        """
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['index'] = getattr(bundle_or_obj.obj, 'index')
        else:
            kwargs['index'] = getattr(bundle_or_obj, 'index')

        return kwargs

    
    
#===============================================================================
# end flashcard resource
#===============================================================================