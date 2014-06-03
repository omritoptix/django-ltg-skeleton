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
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from ltg_backend_app.api.concept import ConceptResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.bundle import Bundle
from django.conf.urls import url

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
    sections = fields.ManyToManyField(ConceptResource,attribute='sections')
    
    class Meta(LtgResource.Meta):
        queryset = Question.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
               'concepts' : ALL_WITH_RELATIONS,
               'sections' : ALL_WITH_RELATIONS,
               'index' : ALL,
           }
        ordering = ['index',]
        
    def override_urls(self):
        # will get object by index and not by id
        # i.e /api/v1/question/<index>/ 
        return [
            url(r"^(?P<resource_name>%s)/(?P<index>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
    def dehydrate_answer(self, bundle):
        return bundle.obj.get_answer_display()
    
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
# end question resource
#===============================================================================